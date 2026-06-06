#!/usr/bin/env python3
"""
Script Iterator — Analyze assessment feedback and improve access scripts.

Reads feedback files from assessments/results/, extracts patterns,
ranks scripts by success, and generates an updated access-scripts.md
"""

import os
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import json


class ScriptIterator:
    def __init__(self, assessments_dir="assessments"):
        self.assessments_dir = Path(assessments_dir)
        self.results_dir = self.assessments_dir / "results"
        self.scripts_file = self.assessments_dir / "access-scripts.md"

        self.results_dir.mkdir(parents=True, exist_ok=True)

        self.feedback = defaultdict(list)
        self.script_stats = defaultdict(lambda: {
            "attempts": 0,
            "successes": 0,
            "success_rate": 0,
            "key_phrases": [],
            "barriers": [],
            "recommendations": []
        })

    def parse_feedback_file(self, filepath):
        """Extract structured data from feedback markdown."""
        with open(filepath, 'r') as f:
            content = f.read()

        data = {}

        # Extract basic fields
        patterns = {
            "date": r"^\*\*Date:\*\*\s+(.+)$",
            "building": r"^\*\*Building:\*\*\s+(.+)$",
            "script_used": r"^\*\*Script used:\*\*\s+(.+)$",
            "result": r"^\*\*Result:\*\*\s+(.+)$",
            "entry_point": r"^\*\*Entry point:\*\*\s+(.+)$",
            "time_of_day": r"^\*\*Time of day:\*\*\s+(.+)$",
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, content, re.MULTILINE)
            if match:
                data[key] = match.group(1).strip()

        # Extract what worked (list items under "## What Worked")
        worked_section = re.search(
            r"## What Worked.*?(?=##|$)",
            content,
            re.DOTALL | re.IGNORECASE
        )
        if worked_section:
            items = re.findall(r"^\d+\.\s+(.+)$", worked_section.group(), re.MULTILINE)
            data["what_worked"] = items

            # Extract key phrase
            key_phrase_match = re.search(
                r"^\s*>\s*(.+)$",
                worked_section.group(),
                re.MULTILINE
            )
            if key_phrase_match:
                data["key_phrase"] = key_phrase_match.group(1)

        # Extract what didn't work
        barriers_section = re.search(
            r"## What Didn't Work.*?(?=##|$)",
            content,
            re.DOTALL | re.IGNORECASE
        )
        if barriers_section:
            items = re.findall(r"^\d+\.\s+(.+)$", barriers_section.group(), re.MULTILINE)
            data["barriers"] = items

        # Extract recommendations
        rec_section = re.search(
            r"## Recommendations for Next Time.*?(?=##|$)",
            content,
            re.DOTALL | re.IGNORECASE
        )
        if rec_section:
            data["recommendations"] = re.findall(
                r"^-\s+(.+)$",
                rec_section.group(),
                re.MULTILINE
            )

        return data

    def load_feedback(self):
        """Load all feedback files."""
        if not self.results_dir.exists():
            print(f"No results directory at {self.results_dir}")
            return

        for filepath in self.results_dir.glob("*.md"):
            print(f"Loading {filepath.name}...")
            data = self.parse_feedback_file(filepath)
            script = data.get("script_used", "Unknown")
            self.feedback[script].append(data)

    def analyze_scripts(self):
        """Calculate success rates and aggregate feedback."""
        for script, attempts in self.feedback.items():
            stats = self.script_stats[script]
            stats["attempts"] = len(attempts)

            # Count successes
            successes = sum(1 for a in attempts if "✅" in a.get("result", ""))
            stats["successes"] = successes
            stats["success_rate"] = (successes / stats["attempts"] * 100) if stats["attempts"] > 0 else 0

            # Aggregate key phrases
            phrases = []
            for attempt in attempts:
                if "key_phrase" in attempt:
                    phrases.append(attempt["key_phrase"])
                for item in attempt.get("what_worked", []):
                    phrases.append(item)
            stats["key_phrases"] = list(set(phrases))

            # Aggregate barriers
            barriers = []
            for attempt in attempts:
                barriers.extend(attempt.get("barriers", []))
            stats["barriers"] = list(set(barriers))

            # Aggregate recommendations
            recs = []
            for attempt in attempts:
                recs.extend(attempt.get("recommendations", []))
            stats["recommendations"] = list(set(recs))

    def generate_report(self, output_file="assessments/script-effectiveness-report.md"):
        """Generate a markdown report of script performance."""
        self.load_feedback()
        self.analyze_scripts()

        if not self.script_stats:
            print("No feedback data found.")
            return

        # Sort by success rate
        sorted_scripts = sorted(
            self.script_stats.items(),
            key=lambda x: x[1]["success_rate"],
            reverse=True
        )

        report = f"""# Script Effectiveness Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Summary

**Total scripts tested:** {len(sorted_scripts)}
**Total assessment attempts:** {sum(s[1]["attempts"] for s in sorted_scripts)}
**Overall success rate:** {sum(s[1]["successes"] for s in sorted_scripts) / sum(s[1]["attempts"] for s in sorted_scripts) * 100:.1f}%

---

## Scripts by Effectiveness

"""

        for script, stats in sorted_scripts:
            report += f"""
### {script}

**Performance:** {stats["success_rate"]:.0f}% ({stats["successes"]}/{stats["attempts"]} successes)

**What worked:**
"""
            for phrase in stats["key_phrases"][:3]:  # Top 3
                report += f"- {phrase}\n"

            if stats["barriers"]:
                report += "\n**Common barriers encountered:**\n"
                for barrier in stats["barriers"][:3]:
                    report += f"- {barrier}\n"

            if stats["recommendations"]:
                report += "\n**Suggested improvements:**\n"
                for rec in stats["recommendations"][:3]:
                    report += f"- {rec}\n"

        report += "\n---\n\n## Raw Data\n\n```json\n"
        report += json.dumps(self.script_stats, indent=2)
        report += "\n```\n"

        # Write report
        Path(output_file).write_text(report)
        print(f"Report written to {output_file}")

        return report

    def suggest_improvements(self):
        """Print suggestions for script improvement."""
        self.load_feedback()
        self.analyze_scripts()

        print("\n=== SCRIPT IMPROVEMENT SUGGESTIONS ===\n")

        for script, stats in sorted(
            self.script_stats.items(),
            key=lambda x: x[1]["success_rate"]
        ):
            print(f"\n{script}")
            print(f"Current success rate: {stats['success_rate']:.0f}%")

            if stats["success_rate"] < 50:
                print("⚠️  LOW SUCCESS RATE — Consider:")
                for rec in stats["recommendations"][:2]:
                    print(f"  - {rec}")
            else:
                print("✅ Performing well — Consider:")
                for phrase in stats["key_phrases"][:1]:
                    print(f"  - Double down on: '{phrase}'")


if __name__ == "__main__":
    iterator = ScriptIterator()

    # Generate report
    iterator.generate_report()

    # Print suggestions
    iterator.suggest_improvements()
