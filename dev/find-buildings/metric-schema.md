# Residential Plan Metric Schema

Version: `1.0.0`

This schema defines implementation-ready inputs and outputs for comparative
analysis of anonymized residential plans. It supports geometry, room-access,
route, privacy and visibility metrics. It does not define a universal security
score, rank buildings by vulnerability or model site-specific attack paths.

## Conventions

- `plan_id` is a random, non-reversible identifier. Do not retain addresses,
  coordinates, listing IDs or source URLs that identify a home.
- Coordinates use a plan-local Cartesian system. Metric calculations requiring
  distance or area are null when `scale_status != "metric"`.
- Polygons use GeoJSON winding rules and must be closed.
- Distances are metres, areas square metres and angles decimal degrees.
- Missing numeric values are JSON `null` and empty CSV fields, never zero.
- Ratios are in `[0,1]`. Centralities are reported both raw and normalized where
  specified.
- Graphs are undirected unless a traversable opening is explicitly directional.
- Exterior is represented by one synthetic node, `space_type = "exterior"`.
- Enumerations are lowercase snake case.

## Required Input Records

### `plans.csv`

One row per plan or independently analyzed level.

| Field | Type | Required | Definition |
| --- | --- | --- | --- |
| `schema_version` | string | yes | Schema semantic version, currently `1.0.0`. |
| `plan_id` | string | yes | Random unique identifier. |
| `source_dataset` | string | yes | Non-identifying dataset and release name. |
| `level_id` | string | yes | Anonymized level identifier. |
| `split` | enum | yes | `train`, `validation`, `test` or `analysis`. |
| `coordinate_unit` | enum | yes | `m`, `cm`, `mm`, `px` or `unknown`. |
| `scale_to_m` | number | conditional | Coordinate units multiplied by this value to obtain metres. |
| `scale_status` | enum | yes | `metric`, `estimated` or `unknown`. |
| `plan_boundary_json` | JSON string | yes | GeoJSON Polygon or MultiPolygon in local coordinates. |
| `input_revision` | string | yes | Immutable source-normalization revision or checksum. |

`scale_to_m` is required when `scale_status` is `metric` or `estimated`.
Estimated scale may be used only when outputs also carry
`estimated_scale_used`.

### `spaces.csv`

One row per room, circulation space or synthetic exterior node.

| Field | Type | Required | Definition |
| --- | --- | --- | --- |
| `plan_id` | string | yes | Parent plan. |
| `space_id` | string | yes | Unique within the plan. |
| `space_type` | enum | yes | `exterior`, `entrance_zone`, `circulation`, `living`, `dining`, `kitchen`, `bedroom`, `bathroom`, `toilet`, `utility`, `storage`, `balcony`, `other` or `unknown`. |
| `privacy_class` | integer | yes | Ordinal class: `0` exterior, `1` public, `2` transitional, `3` private, `4` intimate/service-private. |
| `polygon_json` | JSON string | conditional | GeoJSON Polygon; null only for the exterior node. |
| `label_confidence` | number | yes | Confidence in normalized type, `[0,1]`. |
| `is_occupiable` | boolean | yes | Whether normal residential activity occurs in the space. |
| `is_circulation` | boolean | yes | Whether circulation is the primary function. |

Privacy classes must be assigned by a documented mapping configured before
analysis. They describe design transitions, not resident behavior.

### `openings.csv`

One row per traversable opening used to construct the room-access graph.

| Field | Type | Required | Definition |
| --- | --- | --- | --- |
| `plan_id` | string | yes | Parent plan. |
| `opening_id` | string | yes | Unique within the plan. |
| `space_a_id` | string | yes | First incident node. |
| `space_b_id` | string | yes | Second incident node. |
| `opening_type` | enum | yes | `door`, `open_passage`, `stair`, `lift` or `other`. |
| `segment_json` | JSON string | yes | GeoJSON LineString representing the opening. |
| `width_m` | number | no | Clear width; null without metric scale. |
| `traversable` | boolean | yes | Include edge only when true. |
| `direction` | enum | yes | `both`, `a_to_b` or `b_to_a`. Normally `both`. |
| `is_primary_entrance` | boolean | yes | True only for a legitimate exterior-to-interior entrance. |

Exactly one exterior node is required. At least one traversable exterior edge
must be marked as a primary entrance. Analyses with multiple primary entrances
must report entrance aggregation as described below.

## Geometry Validation

Emit `geometry_validation.csv`, one row per plan:

| Field | Type | Definition |
| --- | --- | --- |
| `plan_id` | string | Plan identifier. |
| `boundary_valid` | boolean | Boundary passes OGC validity checks. |
| `all_space_polygons_valid` | boolean | Every non-exterior polygon is closed, simple and valid. |
| `spaces_with_self_intersection` | integer | Count of invalid self-intersecting spaces. |
| `spaces_outside_boundary` | integer | Count whose area outside the boundary exceeds tolerance. |
| `overlap_area_m2` | number/null | Pairwise room overlap excluding shared boundaries. |
| `unassigned_area_m2` | number/null | Boundary area not assigned to a space. |
| `openings_with_bad_incidence` | integer | Openings not touching both referenced spaces within tolerance. |
| `duplicate_openings` | integer | Geometrically and topologically duplicate openings. |
| `min_space_area_m2` | number/null | Minimum non-exterior polygon area. |
| `max_space_area_m2` | number/null | Maximum non-exterior polygon area. |
| `geometry_pass` | boolean | True when no fatal geometry flag is present. |

Recommended tolerances after conversion to metres:

```text
snap_tolerance = 0.05
outside_area_tolerance = max(0.01 m2, 0.001 * polygon_area)
overlap_area_tolerance = max(0.01 m2, 0.001 * min(area_i, area_j))
```

Validation pseudocode:

```text
for each non-exterior space:
    require polygon.is_valid and polygon.is_simple
    outside = area(polygon - plan_boundary)
    flag if outside > outside_area_tolerance

for each pair of spaces:
    overlap = area(intersection(space_i, space_j))
    flag if overlap > overlap_area_tolerance

for each traversable opening:
    require distance(opening, boundary(space_a)) <= snap_tolerance
    require distance(opening, boundary(space_b)) <= snap_tolerance
```

## Room-Access Graph

Construct `G = (V, E)` from `spaces.csv` and traversable openings. Parallel
openings between the same spaces produce one graph edge for topological metrics,
with `opening_count` retained. The edge length is:

```text
topological_weight = 1
metric_weight = distance(centroid_a, midpoint_opening)
              + distance(midpoint_opening, centroid_b)
```

For the exterior node, use only the interior centroid-to-opening term.

Emit `graph_nodes.csv`:

| Field | Type | Definition |
| --- | --- | --- |
| `plan_id`, `space_id` | string | Composite key. |
| `degree` | integer | Number of distinct adjacent nodes. |
| `weighted_degree` | number/null | Sum of opening widths; null without widths. |
| `component_id` | integer | Connected-component index, largest first. |
| `reachable_from_entrance` | boolean | Reachable from any primary entrance. |
| `is_dead_end` | boolean | Non-exterior node with degree one. |

Emit `graph_edges.csv`:

| Field | Type | Definition |
| --- | --- | --- |
| `plan_id`, `space_a_id`, `space_b_id` | string | Canonically ordered edge key. |
| `opening_count` | integer | Number of traversable openings collapsed into this edge. |
| `topological_weight` | integer | Always `1`. |
| `metric_weight_m` | number/null | Centroid-to-opening route approximation. |
| `min_width_m` | number/null | Narrowest represented opening. |

## Depth and Centrality

Emit one row per non-exterior space in `space_metrics.csv`.

### Entrance depth

For primary entrance interior nodes `R`, report the minimum distance from any
entrance:

```text
entrance_depth_steps(v) = min(shortest_path_length(G, r, v)) for r in R
entrance_depth_m(v) = min(weighted_shortest_path(G, r, v)) for r in R
```

Fields:

| Field | Type | Definition |
| --- | --- | --- |
| `entrance_depth_steps` | integer/null | Minimum topological transitions from an entrance interior node; that node has depth `0`. |
| `entrance_depth_m` | number/null | Minimum metric-weighted depth. |
| `nearest_entrance_space_id` | string/null | Entrance root producing minimum depth; ties resolve lexically. |

### Integration / closeness

For reachable nodes in the interior graph `G_i` with `n > 1`:

```text
closeness_raw(v) = (n - 1) / sum(distance(v, u))
closeness_wf(v) = reachable_count/(n - 1)
                * reachable_count/sum(distance(v, u))
```

Use topological distance for `_steps` and metric-weighted distance for `_m`.
Wasserman-Faust correction (`closeness_wf`) is required for disconnected graphs.

Fields: `closeness_steps_raw`, `closeness_steps_wf`,
`closeness_m_raw`, `closeness_m_wf`. Metric variants are null without metric
scale. In this schema, `integration` is an alias for corrected closeness and is
exported as `integration_steps = closeness_steps_wf` and
`integration_m = closeness_m_wf`; do not mix it with other space-syntax
normalizations without adding a separately named field.

### Choice / betweenness

For unordered pairs `s,t` in the interior graph:

```text
betweenness(v) = sum((sigma_st(v) / sigma_st) for s != v != t)
betweenness_norm(v) = 2 * betweenness(v) / ((n - 1) * (n - 2))
```

`sigma_st` is the number of shortest paths and `sigma_st(v)` the number passing
through `v`. Export `betweenness_steps_raw`, `betweenness_steps_norm`,
`betweenness_m_raw` and `betweenness_m_norm`. Metric variants are null without
metric scale. For `n < 3`, normalized betweenness is `0`.

## Route Overlap

Route classes are analytical, non-site-specific design categories:

- `resident`: primary entrance to all occupiable spaces;
- `guest`: primary entrance to configured public destination types;
- `service`: primary entrance to configured kitchen, utility and storage types.

Destination mappings must be stored in analysis configuration. Do not infer
occupant routines. For equal shortest paths, split one unit of route flow evenly
across all equal paths.

Emit `route_metrics.csv`, one row per plan and pair of route classes:

| Field | Type | Definition |
| --- | --- | --- |
| `plan_id` | string | Plan identifier. |
| `class_a`, `class_b` | enum | Two distinct route classes. |
| `edge_set_a_count`, `edge_set_b_count` | integer | Edges receiving nonzero route flow. |
| `shared_edge_count` | integer | Intersection size of nonzero-flow edge sets. |
| `edge_jaccard` | number/null | `|E_a intersect E_b| / |E_a union E_b|`. |
| `flow_overlap` | number/null | `sum_e min(f_a(e),f_b(e)) / sum_e max(f_a(e),f_b(e))`. |
| `shared_distance_m` | number/null | Sum of lengths of shared edges. |
| `destination_count_a`, `destination_count_b` | integer | Number of valid destinations. |

Ratios are null if either route class has no valid destination.

## Privacy Gradient

For every entrance-to-destination shortest path with privacy classes
`p_0 ... p_k`:

```text
positive_gain = sum(max(0, p_i - p_(i-1)))
regression = sum(max(0, p_(i-1) - p_i))
net_gradient = p_k - p_0
monotonic = regression == 0
transition_count = count(p_i != p_(i-1))
```

Aggregate equal shortest paths by their mean; aggregate destinations by their
unweighted mean. Emit `privacy_metrics.csv`:

| Field | Type | Definition |
| --- | --- | --- |
| `plan_id` | string | Plan identifier. |
| `destination_group` | enum | `all_occupiable`, `private`, `bedroom`, `bathroom` or configured group. |
| `destination_count` | integer | Reachable destinations in the group. |
| `mean_net_gradient` | number/null | Mean endpoint class difference. |
| `mean_positive_gain` | number/null | Mean accumulated increase. |
| `mean_regression` | number/null | Mean accumulated decrease. |
| `monotonic_path_fraction` | number/null | Fraction of routes with no privacy regression. |
| `mean_transition_count` | number/null | Mean number of class changes. |
| `direct_private_access_fraction` | number/null | Fraction of destinations with no transitional-class node before a class `>=3` destination. |

These values measure label progression only. They are not claims about safety,
social acceptability or actual use.

## Visibility Fields

Visibility graph analysis (VGA) uses walkable interior polygons with fixed
obstacles removed. Record the method before comparing plans:

| Configuration field | Type | Definition |
| --- | --- | --- |
| `grid_spacing_m` | number | Default `0.25`; required for VGA. |
| `observer_height_m` | number | Default `1.60`; relevant when 3D occluders exist. |
| `max_view_distance_m` | number/null | Null means unbounded within the plan. |
| `door_state` | enum | `open`, `closed` or `as_modelled`. |
| `visibility_engine` | string | Engine name and version. |

Emit `visibility_cells.csv`, one row per valid grid cell:

| Field | Type | Definition |
| --- | --- | --- |
| `plan_id`, `cell_id`, `space_id` | string | Cell identity and containing space. |
| `x_m`, `y_m` | number | Cell centre. |
| `visible_cell_count` | integer | Number of mutually visible valid cells. |
| `visual_connectivity` | integer | Same as visible cell count, excluding self. |
| `visual_closeness_norm` | number/null | Corrected closeness in the visibility graph. |
| `visual_betweenness_norm` | number/null | Normalized betweenness in the visibility graph. |
| `isovist_area_m2` | number | Area visible from the cell. |
| `isovist_perimeter_m` | number | Perimeter of the isovist polygon. |
| `isovist_occlusivity_m` | number | Total length of radial occluding boundaries. |
| `entrance_visible` | boolean | Any primary entrance opening is directly visible. |
| `private_space_visible` | boolean | Any polygon with privacy class `>=3` is directly visible. |

Aggregate cells to `space_visibility_metrics.csv` using area weighting:
`cell_count`, `mean_visual_connectivity`, `mean_visual_closeness_norm`,
`mean_visual_betweenness_norm`, `mean_isovist_area_m2`,
`p10_isovist_area_m2`, `p90_isovist_area_m2`,
`entrance_visible_area_fraction` and `private_visible_area_fraction`.

Visibility fields are null when metric geometry, opening state or obstacle
geometry is insufficient. Never silently substitute room adjacency for direct
line of sight.

## Quality Flags

Emit `quality_flags.csv`, one row per observed issue:

| Field | Type | Definition |
| --- | --- | --- |
| `plan_id` | string | Plan identifier. |
| `entity_type` | enum | `plan`, `space`, `opening`, `graph`, `route` or `visibility`. |
| `entity_id` | string/null | Affected record identifier. |
| `flag_code` | enum | Code below or a versioned extension. |
| `severity` | enum | `info`, `warning`, `fatal`. |
| `metric_family` | enum | `geometry`, `graph`, `depth`, `centrality`, `route`, `privacy`, `visibility` or `all`. |
| `message` | string | Human-readable non-identifying explanation. |

Core flag codes:

```text
unknown_scale
estimated_scale_used
invalid_plan_boundary
invalid_space_polygon
self_intersection
space_outside_boundary
space_overlap
unassigned_plan_area
opening_bad_incidence
duplicate_opening
missing_primary_entrance
multiple_primary_entrances
disconnected_graph
unreachable_space
unknown_space_type
low_label_confidence
empty_route_class
visibility_geometry_incomplete
visibility_engine_failure
```

A fatal flag invalidates only its `metric_family` unless the family is `all`.
Every output table must include `metric_valid` and `quality_flag_count`; invalid
metrics remain null rather than being imputed.

## Aggregate Outputs

Emit `plan_metrics.csv`, one row per plan:

| Field | Type | Definition |
| --- | --- | --- |
| `schema_version`, `plan_id`, `input_revision` | string | Lineage fields. |
| `space_count`, `occupiable_space_count`, `circulation_space_count` | integer | Node counts excluding exterior. |
| `traversable_edge_count` | integer | Distinct graph edges. |
| `connected_component_count` | integer | Interior graph component count. |
| `reachable_space_fraction` | number | Spaces reachable from a primary entrance. |
| `mean_entrance_depth_steps`, `max_entrance_depth_steps` | number/null | Depth summaries over reachable occupiable spaces. |
| `mean_entrance_depth_m`, `max_entrance_depth_m` | number/null | Metric depth summaries. |
| `mean_integration_steps`, `max_integration_steps` | number/null | Corrected topological closeness summaries. |
| `mean_betweenness_steps_norm`, `max_betweenness_steps_norm` | number/null | Topological choice summaries. |
| `dead_end_space_fraction` | number/null | Degree-one interior spaces divided by interior spaces. |
| `circulation_dead_end_fraction` | number/null | Degree-one circulation spaces divided by circulation spaces. |
| `mean_route_edge_jaccard` | number/null | Mean across valid route-class pairs. |
| `mean_route_flow_overlap` | number/null | Mean across valid route-class pairs. |
| `private_monotonic_path_fraction` | number/null | Privacy result for private destinations. |
| `private_mean_regression` | number/null | Privacy regression for private destinations. |
| `mean_visual_closeness_norm` | number/null | Area-weighted mean over valid VGA cells. |
| `entrance_visible_area_fraction` | number/null | Walkable area from which an entrance is visible. |
| `private_visible_area_fraction` | number/null | Walkable area with direct visibility into private spaces. |
| `geometry_valid`, `graph_valid`, `visibility_valid` | boolean | Metric-family validity. |
| `warning_count`, `fatal_count` | integer | Quality summary. |

Dataset-level `aggregate_metrics.csv` contains no plan identifiers and groups by
pre-registered, non-identifying dimensions such as dataset release, split,
plan-area band and room-count band:

| Field | Type | Definition |
| --- | --- | --- |
| `group_key_json` | JSON string | Sorted grouping dimensions and values. |
| `metric_name` | string | Exact `plan_metrics.csv` field name. |
| `valid_n`, `missing_n` | integer | Valid and null observation counts. |
| `mean`, `std`, `median`, `p10`, `p25`, `p75`, `p90` | number/null | Distribution summaries. |
| `ci95_low`, `ci95_high` | number/null | Pre-registered bootstrap or analytic confidence interval. |
| `method` | string | Aggregation and CI method with version. |

Do not combine heterogeneous metrics into a single score. Publish distributions,
uncertainty and metric validity separately.

## JSON Exchange Format

The canonical JSON form contains the same records as the CSV tables:

```json
{
  "schema_version": "1.0.0",
  "plan": {
    "plan_id": "p_7f31c2",
    "source_dataset": "dataset_release",
    "level_id": "level_0",
    "split": "analysis",
    "coordinate_unit": "m",
    "scale_to_m": 1.0,
    "scale_status": "metric",
    "input_revision": "sha256:..."
  },
  "spaces": [],
  "openings": [],
  "geometry_validation": {},
  "graph": {"nodes": [], "edges": []},
  "space_metrics": [],
  "route_metrics": [],
  "privacy_metrics": [],
  "visibility": {
    "configuration": {},
    "cells": [],
    "space_metrics": []
  },
  "quality_flags": [],
  "plan_metrics": {}
}
```

CSV uses UTF-8, a header row, RFC 4180 quoting, lowercase booleans
(`true`/`false`) and ISO decimal notation without thousands separators. JSON
must validate finite numbers: `NaN` and infinities are prohibited.
