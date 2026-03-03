#!/usr/bin/env python3
"""
Quality control script for technical articles.
Analyzes literary techniques and readability scores.
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict
from collections import Counter
from datetime import datetime


@dataclass
class LiteraryTechnique:
    """Literary technique found in the article."""
    name: str
    count: int
    examples: List[str]


@dataclass
class ReadabilityMetrics:
    """Readability metrics for the article."""
    avg_sentence_length: float
    avg_word_length: float
    vocabulary_richness: float
    readability_score: float
    grade_level: str


@dataclass
class QualityReport:
    """Quality control report for an article."""
    file_path: str
    timestamp: str
    word_count: int
    sentence_count: int
    paragraph_count: int
    literary_techniques: List[Dict[str, Any]]
    readability_metrics: Dict[str, Any]
    suggestions: List[str]


class LiteraryAnalyzer:
    """Analyzer for literary techniques in technical articles."""

    TECHNIQUE_PATTERNS = {
        '列锦': [
            r'（[^）]+、[^）]+、[^）]+）',
            r'（[^，]+，[^，]+，[^，]+）',
            r'「[^」]+、[^」]+、[^」]+」',
            r'「[^，]+，[^，]+，[^，]+」'
        ],
        '物化': [
            r'数据[像如]（[^）]+）',
            r'查询[像如]（[^）]+）',
            r'索引[像如]（[^）]+）',
            r'表[像如]（[^）]+）',
            r'视图[像如]（[^）]+）',
            r'锁[像如]（[^）]+）',
            r'事务[像如]（[^）]+）'
        ],
        '金庸式笔触': [
            r'（[^）]{1,4}）[一-龥]{1,3}（[^）]{1,4}）',
            r'（[^）]{1,4}）[一-龥]{1,3}（[^）]{1,4}）[一-龥]{1,3}（[^）]{1,4}）',
            r'（[^）]{1,4}）[一-龥]{1,3}（[^）]{1,4}）[一-龥]{1,3}（[^）]{1,4}）[一-龥]{1,3}（[^）]{1,4}）'
        ],
        '比喻': [
            r'（[^）]+）[像如]（[^）]+）',
            r'（[^）]+）[是成为]（[^）]+）',
            r'（[^）]+）[仿佛宛如]（[^）]+）'
        ],
        '拟人': [
            r'（[^）]+）[说告诉告诉]（[^）]+）',
            r'（[^）]+）[知道明白懂得]（[^）]+）',
            r'（[^）]+）[想要希望]（[^）]+）',
            r'（[^）]+）[拒绝接受]（[^）]+）'
        ],
        '排比': [
            r'（[^）]+），（[^）]+），（[^）]+）',
            r'（[^）]+）；（[^）]+）；（[^）]+）'
        ],
        '设问': [
            r'（[^？]+？）（[^。]+。）',
            r'（[^？]+？）（[^！]+！）'
        ],
        '反问': [
            r'（[^？]+？）[吗呢吧]',
            r'（[^？]+？）[难道岂能]'
        ]
    }

    def __init__(self, content: str):
        self.content = content
        self.techniques: List[LiteraryTechnique] = []

    def analyze(self) -> List[LiteraryTechnique]:
        """Analyze literary techniques in the content."""
        self.techniques = []

        for technique_name, patterns in self.TECHNIQUE_PATTERNS.items():
            total_count = 0
            all_examples = []

            for pattern in patterns:
                matches = re.finditer(pattern, self.content)
                for match in matches:
                    total_count += 1
                    example = match.group(0)
                    if len(example) > 50:
                        example = example[:50] + '...'
                    if example not in all_examples:
                        all_examples.append(example)

            if total_count > 0:
                self.techniques.append(LiteraryTechnique(
                    name=technique_name,
                    count=total_count,
                    examples=all_examples[:5]
                ))

        return self.techniques


class ReadabilityAnalyzer:
    """Analyzer for readability metrics."""

    def __init__(self, content: str):
        self.content = content
        self.remove_code_blocks()

    def remove_code_blocks(self):
        """Remove code blocks from content for analysis."""
        self.content = re.sub(r'```.*?```', '', self.content, flags=re.DOTALL)

    def analyze(self) -> ReadabilityMetrics:
        """Analyze readability metrics."""
        sentences = re.split(r'[。！？\n]+', self.content)
        sentences = [s.strip() for s in sentences if s.strip()]

        words = re.findall(r'[\u4e00-\u9fa5]+', self.content)
        word_lengths = [len(w) for w in words]

        paragraphs = re.split(r'\n\s*\n', self.content)
        paragraphs = [p.strip() for p in paragraphs if p.strip()]

        avg_sentence_length = sum(len(s) for s in sentences) / len(sentences) if sentences else 0
        avg_word_length = sum(word_lengths) / len(word_lengths) if word_lengths else 0

        unique_words = set(words)
        vocabulary_richness = len(unique_words) / len(words) if words else 0

        readability_score = self.calculate_readability_score(
            avg_sentence_length,
            avg_word_length,
            vocabulary_richness
        )

        grade_level = self.get_grade_level(readability_score)

        return ReadabilityMetrics(
            avg_sentence_length=round(avg_sentence_length, 2),
            avg_word_length=round(avg_word_length, 2),
            vocabulary_richness=round(vocabulary_richness, 4),
            readability_score=round(readability_score, 2),
            grade_level=grade_level
        )

    def calculate_readability_score(self, avg_sentence_length: float,
                                    avg_word_length: float,
                                    vocabulary_richness: float) -> float:
        """Calculate readability score (0-100)."""
        score = 100

        if avg_sentence_length > 50:
            score -= (avg_sentence_length - 50) * 0.5
        elif avg_sentence_length < 10:
            score -= (10 - avg_sentence_length) * 1

        if avg_word_length > 3:
            score -= (avg_word_length - 3) * 5

        if vocabulary_richness < 0.3:
            score -= (0.3 - vocabulary_richness) * 100

        return max(0, min(100, score))

    def get_grade_level(self, score: float) -> str:
        """Get grade level based on readability score."""
        if score >= 90:
            return "优秀"
        elif score >= 80:
            return "良好"
        elif score >= 70:
            return "中等"
        elif score >= 60:
            return "及格"
        else:
            return "需改进"


class QualityController:
    """Main quality controller for articles."""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.content = ""
        self.report: Optional[QualityReport] = None

    def read_file(self) -> bool:
        """Read the markdown file."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
            return True
        except FileNotFoundError:
            print(f"❌ Error: File not found: {self.file_path}")
            return False
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return False

    def analyze(self) -> Optional[QualityReport]:
        """Perform quality analysis."""
        if not self.read_file():
            return None

        literary_analyzer = LiteraryAnalyzer(self.content)
        literary_techniques = literary_analyzer.analyze()

        readability_analyzer = ReadabilityAnalyzer(self.content)
        readability_metrics = readability_analyzer.analyze()

        word_count = len(re.findall(r'[\u4e00-\u9fa5]+', self.content))
        sentence_count = len(re.split(r'[。！？\n]+', self.content))
        paragraph_count = len(re.split(r'\n\s*\n', self.content))

        suggestions = self.generate_suggestions(
            literary_techniques,
            readability_metrics
        )

        self.report = QualityReport(
            file_path=str(self.file_path),
            timestamp=datetime.now().isoformat(),
            word_count=word_count,
            sentence_count=sentence_count,
            paragraph_count=paragraph_count,
            literary_techniques=[asdict(t) for t in literary_techniques],
            readability_metrics=asdict(readability_metrics),
            suggestions=suggestions
        )

        return self.report

    def generate_suggestions(self, literary_techniques: List[LiteraryTechnique],
                            readability_metrics: ReadabilityMetrics) -> List[str]:
        """Generate improvement suggestions."""
        suggestions = []

        technique_names = [t.name for t in literary_techniques]

        if '列锦' not in technique_names:
            suggestions.append("建议添加「列锦」手法，用三个或更多并列元素增强表现力")

        if '物化' not in technique_names:
            suggestions.append("建议添加「物化」手法，将技术概念具象化")

        if '金庸式笔触' not in technique_names:
            suggestions.append("建议添加「金庸式笔触」，用武侠风格描述技术场景")

        if readability_metrics.readability_score < 70:
            suggestions.append(f"可读性评分较低（{readability_metrics.readability_score}），建议简化句子结构")

        if readability_metrics.avg_sentence_length > 40:
            suggestions.append(f"平均句子长度过长（{readability_metrics.avg_sentence_length}字），建议拆分长句")

        if readability_metrics.vocabulary_richness < 0.3:
            suggestions.append(f"词汇丰富度较低（{readability_metrics.vocabulary_richness:.2%}），建议增加词汇多样性")

        if not suggestions:
            suggestions.append("文章质量优秀，无需改进")

        return suggestions

    def print_report(self):
        """Print the quality report."""
        if not self.report:
            print("❌ No report available")
            return

        print("\n" + "="*80)
        print("📊 QUALITY CONTROL REPORT")
        print("="*80)

        print(f"\n📁 File: {self.report.file_path}")
        print(f"🕐 Timestamp: {self.report.timestamp}")

        print(f"\n📈 Basic Statistics:")
        print(f"   Word Count: {self.report.word_count}")
        print(f"   Sentence Count: {self.report.sentence_count}")
        print(f"   Paragraph Count: {self.report.paragraph_count}")

        print(f"\n🎨 Literary Techniques:")
        if self.report.literary_techniques:
            for technique in self.report.literary_techniques:
                print(f"\n   {technique['name']}: {technique['count']} occurrences")
                if technique['examples']:
                    print(f"   Examples:")
                    for example in technique['examples'][:3]:
                        print(f"      - {example}")
        else:
            print("   No literary techniques detected")

        print(f"\n📖 Readability Metrics:")
        metrics = self.report.readability_metrics
        print(f"   Average Sentence Length: {metrics['avg_sentence_length']} characters")
        print(f"   Average Word Length: {metrics['avg_word_length']} characters")
        print(f"   Vocabulary Richness: {metrics['vocabulary_richness']:.2%}")
        print(f"   Readability Score: {metrics['readability_score']}/100")
        print(f"   Grade Level: {metrics['grade_level']}")

        print(f"\n💡 Suggestions:")
        for suggestion in self.report.suggestions:
            print(f"   • {suggestion}")

        print("\n" + "="*80)

    def save_report(self, output_file: str):
        """Save the report to a JSON file."""
        if not self.report:
            print("❌ No report available")
            return

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(self.report), f, indent=2, ensure_ascii=False)

        print(f"\n📄 Report saved to: {output_file}")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Quality control script for technical articles.")
    parser.add_argument("files", nargs='+', help="Files or directories to analyze")
    parser.add_argument("--output", help="Save report to JSON file", default=None)
    
    args = parser.parse_args()
    
    file_paths = []
    for target in args.files:
        path = Path(target)
        if path.is_file():
            file_paths.append(str(path))
        elif path.is_dir():
            file_paths.extend([str(f) for f in path.rglob("*.md")])
    
    if not file_paths:
        print("❌ No markdown files found.")
        sys.exit(1)

    print(f"📊 Starting quality analysis of {len(file_paths)} files...")
    
    reports = []
    for file_path in file_paths:
        controller = QualityController(file_path)
        report = controller.analyze()
        if report:
            reports.append(report)
            controller.print_report()
    
    # Summary
    print("\n" + "="*80)
    print("📈 BATCH SUMMARY")
    print("="*80)
    print(f"Total Files: {len(reports)}")
    avg_score = sum(r.readability_metrics['readability_score'] for r in reports) / len(reports) if reports else 0
    print(f"Average Readability Score: {avg_score:.2f}")
    
    # Save combined output if requested
    if args.output:
        data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_files": len(reports),
                "average_readability": avg_score
            },
            "reports": [asdict(r) for r in reports]
        }
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n📄 Combined report saved to: {args.output}")


if __name__ == "__main__":
    main()
