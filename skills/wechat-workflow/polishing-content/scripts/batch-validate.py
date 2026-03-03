#!/usr/bin/env python3
"""
Batch validation script for technical articles.
Supports parallel processing, progress tracking, and error recovery.
"""

import sys
import os
import json
import time
import importlib.util
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

scripts_dir = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "validate_technical_accuracy",
    os.path.join(scripts_dir, 'validate-technical-accuracy.py')
)
if spec and spec.loader:
    validate_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validate_module)

    Technology = validate_module.Technology
    TechnologyDetector = validate_module.TechnologyDetector
    get_validator = validate_module.get_validator
    print_report = validate_module.print_report
else:
    raise ImportError("Failed to load validate_technical_accuracy module")


@dataclass
class ValidationResult:
    """Result of validating a single file."""
    file_path: str
    technology: str
    success: bool
    total_blocks: int
    valid_blocks: int
    issues: List[str]
    error: Optional[str] = None
    timestamp: str = ""


class BatchValidator:
    """Batch validator for multiple articles."""

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.results: List[ValidationResult] = []
        self.progress_file = Path(".validation_progress.json")

    def load_progress(self) -> Dict[str, Any]:
        """Load progress from file."""
        if self.progress_file.exists():
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"completed": [], "failed": []}

    def save_progress(self, progress: Dict[str, Any]):
        """Save progress to file."""
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress, f, indent=2, ensure_ascii=False)

    def validate_file(self, file_path: str, technology: Optional[str] = None) -> ValidationResult:
        """Validate a single file."""
        timestamp = datetime.now().isoformat()

        try:
            if not Path(file_path).exists():
                return ValidationResult(
                    file_path=file_path,
                    technology="unknown",
                    success=False,
                    total_blocks=0,
                    valid_blocks=0,
                    issues=[],
                    error=f"File not found: {file_path}",
                    timestamp=timestamp
                )

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            filename = Path(file_path).name

            if technology:
                for tech in Technology:
                    if tech.value.lower() == technology.lower():
                        detected_tech = tech
                        break
                else:
                    detected_tech = Technology.UNKNOWN
            else:
                detected_tech, _ = TechnologyDetector.detect_with_details(content, filename)

            if detected_tech == Technology.UNKNOWN:
                return ValidationResult(
                    file_path=file_path,
                    technology="unknown",
                    success=False,
                    total_blocks=0,
                    valid_blocks=0,
                    issues=[],
                    error="Could not detect technology",
                    timestamp=timestamp
                )

            validator = get_validator(detected_tech, file_path)
            if not validator:
                return ValidationResult(
                    file_path=file_path,
                    technology=detected_tech.value,
                    success=False,
                    total_blocks=0,
                    valid_blocks=0,
                    issues=[],
                    error=f"No validator available for {detected_tech.value}",
                    timestamp=timestamp
                )

            if not validator.read_file():
                return ValidationResult(
                    file_path=file_path,
                    technology=detected_tech.value,
                    success=False,
                    total_blocks=0,
                    valid_blocks=0,
                    issues=[],
                    error="Failed to read file",
                    timestamp=timestamp
                )

            if detected_tech == Technology.ORACLE:
                validator.extract_code_blocks('sql')
            elif detected_tech == Technology.MYSQL:
                validator.extract_code_blocks('sql')
            elif detected_tech == Technology.POSTGRESQL:
                validator.extract_code_blocks('sql')
            elif detected_tech == Technology.KUBERNETES:
                validator.extract_code_blocks('yaml')
            elif detected_tech == Technology.LLM:
                validator.extract_code_blocks('python')
            elif detected_tech == Technology.MERMAID:
                validator.extract_code_blocks('mermaid')

            if not validator.code_blocks:
                return ValidationResult(
                    file_path=file_path,
                    technology=detected_tech.value,
                    success=True,
                    total_blocks=0,
                    valid_blocks=0,
                    issues=[],
                    timestamp=timestamp
                )

            results = validator.validate_all()

            return ValidationResult(
                file_path=file_path,
                technology=detected_tech.value,
                success=len(results['issues']) == 0,
                total_blocks=results['total_blocks'],
                valid_blocks=results['valid_blocks'],
                issues=results['issues'],
                timestamp=timestamp
            )

        except Exception as e:
            return ValidationResult(
                file_path=file_path,
                technology="unknown",
                success=False,
                total_blocks=0,
                valid_blocks=0,
                issues=[],
                error=str(e),
                timestamp=timestamp
            )

    def validate_batch(
        self,
        file_paths: List[str],
        technology: Optional[str] = None,
        resume: bool = False
    ) -> List[ValidationResult]:
        """Validate multiple files in parallel."""
        progress = self.load_progress() if resume else {"completed": [], "failed": []}

        files_to_process = []
        for file_path in file_paths:
            if file_path in progress["completed"] or file_path in progress["failed"]:
                continue
            files_to_process.append(file_path)

        if not files_to_process:
            print("✅ All files have been processed already.")
            return []

        print(f"📊 Starting batch validation of {len(files_to_process)} files...")
        print(f"⚙️  Using {self.max_workers} workers for parallel processing\n")

        completed = 0
        failed = 0

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_file = {
                executor.submit(self.validate_file, file_path, technology): file_path
                for file_path in files_to_process
            }

            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    result = future.result()
                    self.results.append(result)

                    if result.success:
                        completed += 1
                        progress["completed"].append(file_path)
                        print(f"✅ [{completed + failed}/{len(files_to_process)}] {Path(file_path).name}")
                    else:
                        failed += 1
                        progress["failed"].append(file_path)
                        error_msg = result.error or f"{len(result.issues)} issues"
                        print(f"❌ [{completed + failed}/{len(files_to_process)}] {Path(file_path).name} - {error_msg}")

                    self.save_progress(progress)

                except Exception as e:
                    failed += 1
                    progress["failed"].append(file_path)
                    print(f"❌ [{completed + failed}/{len(files_to_process)}] {Path(file_path).name} - Error: {e}")
                    self.save_progress(progress)

        print(f"\n📊 Batch validation complete:")
        print(f"   ✅ Passed: {completed}")
        print(f"   ❌ Failed: {failed}")
        print(f"   📁 Total: {len(files_to_process)}")

        return self.results

    def generate_report(self, output_file: Optional[str] = None):
        """Generate a detailed report of validation results."""
        if not self.results:
            print("No validation results to report.")
            return

        print("\n" + "="*80)
        print("📊 DETAILED VALIDATION REPORT")
        print("="*80)

        passed = [r for r in self.results if r.success]
        failed = [r for r in self.results if not r.success]

        print(f"\n📈 Summary:")
        print(f"   Total Files: {len(self.results)}")
        print(f"   ✅ Passed: {len(passed)}")
        print(f"   ❌ Failed: {len(failed)}")

        if failed:
            print(f"\n❌ Failed Files:")
            for result in failed:
                print(f"\n   📁 {result.file_path}")
                print(f"   🔧 Technology: {result.technology}")
                if result.error:
                    print(f"   ⚠️  Error: {result.error}")
                if result.issues:
                    print(f"   📋 Issues:")
                    for issue in result.issues:
                        print(f"      - {issue}")

        if output_file:
            report_data = {
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total": len(self.results),
                    "passed": len(passed),
                    "failed": len(failed)
                },
                "results": [asdict(r) for r in self.results]
            }

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)

            print(f"\n📄 Report saved to: {output_file}")


def find_markdown_files(directory: str, recursive: bool = True) -> List[str]:
    """Find all markdown files in a directory."""
    path = Path(directory)
    if recursive:
        return [str(f) for f in path.rglob("*.md")]
    else:
        return [str(f) for f in path.glob("*.md")]


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python batch-validate.py <file_or_directory> [options]")
        print("\nOptions:")
        print("  --tech <technology>    Specify technology for all files")
        print("  --workers <n>          Number of parallel workers (default: 4)")
        print("  --resume               Resume from previous progress")
        print("  --output <file>        Save report to JSON file")
        print("  --recursive            Search directory recursively (default: true)")
        print("\nExample:")
        print("  python batch-validate.py ./articles --tech Oracle --workers 8")
        sys.exit(1)

    target = sys.argv[1]
    technology = None
    workers = 4
    resume = False
    output_file = None
    recursive = True

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--tech" and i + 1 < len(sys.argv):
            technology = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--workers" and i + 1 < len(sys.argv):
            workers = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--resume":
            resume = True
            i += 1
        elif sys.argv[i] == "--output" and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--recursive":
            recursive = True
            i += 1
        elif sys.argv[i] == "--no-recursive":
            recursive = False
            i += 1
        else:
            i += 1

    if Path(target).is_file():
        file_paths = [target]
    elif Path(target).is_dir():
        file_paths = find_markdown_files(target, recursive)
        if not file_paths:
            print(f"❌ No markdown files found in {target}")
            sys.exit(1)
    else:
        print(f"❌ Path not found: {target}")
        sys.exit(1)

    validator = BatchValidator(max_workers=workers)
    validator.validate_batch(file_paths, technology, resume)
    validator.generate_report(output_file)


if __name__ == "__main__":
    main()
