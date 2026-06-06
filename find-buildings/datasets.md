# Floor-Plan Datasets for Architecture Research

Last checked: 2026-06-06

This catalogue favors datasets released for research over address-targeted planning
records. Before downloading or publishing results, re-check each dataset's current
license and terms at the linked source. A code license does not necessarily grant
the same rights over the data.

## Recommended starting set

| Dataset | Scale and content | Best use | Access and caveats |
| --- | --- | --- | --- |
| [CubiCasa5K](https://github.com/CubiCasa/CubiCasa5k) | 5,000 raster floor plans with dense polygon annotations and more than 80 object categories | Raster parsing, room segmentation, door/window detection | Public repository and download. Inspect the repository license and dataset terms before redistribution. The original pipeline is old, so isolate its dependencies or write a modern loader. |
| [Swiss Dwellings](https://archilyse.standfest.science/swiss-dwellings) | Large, structured collection of apartment models with geometry and calculated spatial features | Apartment topology, accessibility, daylight and centrality research | Downloaded as CSV data. Check the current release documentation and license. Geography and housing conventions are Swiss, so do not assume direct transfer to London. |
| [Zillow Indoor Dataset (ZInD)](https://github.com/zillow/zind) | Real homes represented by panoramas, room geometry, doors, windows and 2D/3D floor plans | Layout reconstruction and whole-home connectivity | Research dataset with a required download process and its own terms. Zillow describes privacy filtering of people, photographs and significant exterior views. Do not attempt to re-identify homes. |
| [Structured3D](https://github.com/bertjiazheng/Structured3D) | 3,500 synthetic, professionally designed houses with rendered images and structural annotations | Synthetic pretraining, geometry extraction and controlled experiments | Requires accepting dataset terms. Synthetic scenes avoid resident privacy issues but have a simulation-to-reality gap. |

## Secondary datasets

### RPLAN

RPLAN is widely used for residential layout generation. Later papers report
different prepared subsets, commonly around 60,000 layouts, while House-GAN
reports experiments over 117,000 floor-plan images. Treat those as paper-specific
corpora rather than assuming one canonical public download.

Start with:

- [House-GAN paper](https://arxiv.org/abs/2003.06988)
- [House-GAN++ paper](https://openaccess.thecvf.com/content/CVPR2021/html/Nauata_House-GAN_Relational_Generative_Adversarial_Networks_for_Graph-Constrained_House_Layout_Generation_CVPR_2021_paper.html)

Confirm provenance, permission, split construction and redistribution rights
before using any third-party mirror.

### ResPlan

[ResPlan](https://arxiv.org/abs/2508.14006) describes 17,000 vector-graph
residential plans. It is newer and structurally useful, but access and licensing
should be verified from the authors' official release before including it in a
reproducible pipeline.

### LIFULL HOME'S

The LIFULL HOME'S academic dataset is distributed through Japan's National
Institute of Informatics Informatics Research Data Repository. It can be valuable
for Japanese housing-plan research, but access is application-based and usage is
controlled by dataset-specific terms. Do not source it from unofficial mirrors.

## Selection matrix

| Research question | Primary dataset | Validation dataset |
| --- | --- | --- |
| Parse plan images into rooms/openings | CubiCasa5K | ZInD |
| Learn room adjacency or generate layouts | Swiss Dwellings | RPLAN, if lawfully obtained |
| Reconstruct plans from indoor imagery | ZInD | Structured3D |
| Test spatial-analysis metrics | Swiss Dwellings | Structured3D |
| Pretrain without occupant privacy exposure | Structured3D | CubiCasa5K |

## Dataset acceptance checklist

Record the following in a machine-readable dataset card before ingestion:

1. Official source URL, release/version and retrieval date.
2. Data license, code license and any separate terms of use.
3. Permitted research, training, publication and redistribution uses.
4. Provenance and whether plans represent real, synthetic or transformed homes.
5. Presence of addresses, coordinates, names, photographs or other identifiers.
6. Required deletion, access-control or attribution conditions.
7. Geographic, cultural, typological and annotation biases.
8. Train/validation/test split method and duplicate detection.

Reject data obtained from scraped listings, unofficial mirrors, leaked drawing
sets or records that can be tied to a specific occupied home. Keep raw datasets
access-controlled and publish only aggregate statistics or non-identifying
derived representations.

## Minimal normalized schema

Store geometry in a consistent coordinate system and preserve provenance:

```text
building_id       random internal identifier
source_dataset    dataset and version
level_id          floor within the sample
space_id          room or circulation-space identifier
space_type        normalized semantic label
polygon           room boundary in metric coordinates where available
openings          doors/windows with geometry and type
adjacency         space-to-space connection edges
entrance          dataset-provided or explicitly derived entrance flag
quality_flags     parsing, geometry and label warnings
split             train, validation or test
```

Do not retain source addresses or create a lookup from `building_id` to a real
property.

