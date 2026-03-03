#!/usr/bin/env python3
"""
Tech Article Polisher - Multi-Technology Technical Accuracy Validation Script

This script validates the technical accuracy of technical articles across multiple
technologies: Oracle, MySQL, PostgreSQL, Kubernetes, Docker, LLM, Mermaid, etc.
"""

import re
import sys
import json
import argparse
from typing import List, Dict, Tuple, Optional, Any
from pathlib import Path
from enum import Enum


class Technology(Enum):
    """Supported technologies."""
    ORACLE = "Oracle"
    MYSQL = "MySQL"
    POSTGRESQL = "PostgreSQL"
    KUBERNETES = "Kubernetes"
    DOCKER = "Docker"
    LLM = "LLM"
    MERMAID = "Mermaid"
    PYTHON = "Python"
    JAVA = "Java"
    GO = "Go"
    UNKNOWN = "Unknown"


class TechnologyDetector:
    """Detect the technology domain from article content."""

    KEYWORDS = {
        Technology.ORACLE: [
            ('V\\$', 3), ('DBA_', 3), ('GV\\$', 3), ('CDB_', 3), ('PL/SQL', 2),
            ('RMAN', 2), ('Data Guard', 2), ('RAC', 2), ('SGA', 2), ('PGA', 2),
            ('Buffer Cache', 2), ('Redo Log', 2), ('Undo Segment', 2),
            ('Oracle', 1), ('SQL*Plus', 1), ('SQL Developer', 1)
        ],
        Technology.MYSQL: [
            ('information_schema', 3), ('performance_schema', 3), ('InnoDB', 2),
            ('MyISAM', 2), ('slow_query_log', 2), ('binary_log', 2),
            ('relay_log', 2), ('SHOW VARIABLES', 2), ('SHOW STATUS', 2),
            ('EXPLAIN', 1), ('MySQL', 1), ('mysqldump', 1)
        ],
        Technology.POSTGRESQL: [
            ('pg_stat_', 3), ('pg_catalog', 2), ('WAL', 2), ('MVCC', 2),
            ('TOAST', 2), ('Vacuum', 2), ('Autovacuum', 2), ('pg_dump', 2),
            ('psql', 1), ('PostgreSQL', 1), ('Postgres', 1)
        ],
        Technology.KUBERNETES: [
            ('kubectl', 2), ('Pod', 2), ('Service', 2), ('Deployment', 2),
            ('StatefulSet', 2), ('DaemonSet', 2), ('ConfigMap', 2),
            ('Secret', 2), ('Ingress', 2), ('HPA', 2),
            ('apiVersion: apps/v1', 3), ('kind: Deployment', 3),
            ('Kubernetes', 1), ('K8s', 1)
        ],
        Technology.DOCKER: [
            ('docker', 2), ('Dockerfile', 3), ('docker-compose', 3),
            ('Container', 1), ('Image', 1), ('Volume', 1), ('Network', 1),
            ('FROM', 2), ('RUN', 2), ('CMD', 2)
        ],
        Technology.LLM: [
            ('OpenAI', 3), ('GPT', 2), ('Claude', 2), ('Prompt', 2),
            ('Temperature', 2), ('Token', 2), ('Embedding', 2),
            ('RAG', 3), ('Fine-tuning', 2), ('Chain of Thought', 2),
            ('chat.completions.create', 3), ('LLM', 1)
        ],
        Technology.MERMAID: [
            ('graph TD', 3), ('graph LR', 3), ('sequenceDiagram', 3),
            ('classDiagram', 3), ('stateDiagram', 3), ('stateDiagram-v2', 3),
            ('gantt', 2), ('pie', 2), ('mermaid', 3)
        ],
        Technology.PYTHON: [
            ('import ', 1), ('def ', 1), ('class ', 1), ('async def', 2),
            ('from ', 1), ('pip install', 2), ('python', 1),
            ('Django', 2), ('Flask', 2), ('FastAPI', 2), ('pandas', 2),
            ('numpy', 2)
        ],
        Technology.JAVA: [
            ('public class', 2), ('import java', 2), ('Spring Boot', 3),
            ('Maven', 2), ('Gradle', 2), ('@SpringBootApplication', 3),
            ('System.out.println', 1)
        ],
        Technology.GO: [
            ('package main', 3), ('func main', 3), ('import "', 1),
            ('go run', 2), ('go build', 2), ('Goroutine', 2),
            ('Channel', 2), ('interface{', 2), ('struct {', 2)
        ]
    }

    FILENAME_PATTERNS = {
        Technology.ORACLE: [r'oracle', r'rman', r'dataguard', r'rac'],
        Technology.MYSQL: [r'mysql'],
        Technology.POSTGRESQL: [r'postgres', r'postgresql'],
        Technology.KUBERNETES: [r'k8s', r'kubernetes', r'kubectl'],
        Technology.DOCKER: [r'docker'],
        Technology.LLM: [r'llm', r'prompt', r'embedding', r'rag'],
        Technology.MERMAID: [r'mermaid'],
        Technology.PYTHON: [r'python', r'django', r'flask'],
        Technology.JAVA: [r'java', r'spring'],
        Technology.GO: [r'golang', r'\.go$']
    }

    @classmethod
    def detect(cls, content: str, filename: str = "") -> Technology:
        """Detect technology from content and filename."""
        scores = {}

        for tech, keywords in cls.KEYWORDS.items():
            score = 0
            for keyword, weight in keywords:
                matches = len(re.findall(keyword, content, re.IGNORECASE))
                score += matches * weight
            scores[tech] = score

        if filename:
            for tech, patterns in cls.FILENAME_PATTERNS.items():
                for pattern in patterns:
                    if re.search(pattern, filename, re.IGNORECASE):
                        scores[tech] += 5

        max_score = max(scores.values())
        if max_score == 0:
            return Technology.UNKNOWN

        return max(scores, key=lambda k: scores[k])

    @classmethod
    def detect_with_details(cls, content: str, filename: str = "") -> Tuple[Technology, Dict[str, int]]:
        """Detect technology from content and return detailed scores."""
        scores = {}

        for tech, keywords in cls.KEYWORDS.items():
            score = 0
            for keyword, weight in keywords:
                matches = len(re.findall(keyword, content, re.IGNORECASE))
                score += matches * weight
            scores[tech.value] = score

        if filename:
            for tech, patterns in cls.FILENAME_PATTERNS.items():
                for pattern in patterns:
                    if re.search(pattern, filename, re.IGNORECASE):
                        scores[tech.value] += 5

        max_score = max(scores.values())
        if max_score == 0:
            return Technology.UNKNOWN, scores

        detected_tech = max(scores, key=lambda k: scores[k])
        for tech in Technology:
            if tech.value == detected_tech:
                return tech, scores

        return Technology.UNKNOWN, scores


class BaseValidator:
    """Base validator for all technologies."""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.content = ""
        self.code_blocks = []
        self.issues = []

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

    def extract_code_blocks(self, language: str) -> List[Tuple[str, int]]:
        """Extract code blocks of a specific language from markdown."""
        code_blocks = []
        lines = self.content.split('\n')

        in_code_block = False
        current_code = []
        start_line = 0
        block_language = ""

        for i, line in enumerate(lines, 1):
            if line.strip().startswith('```'):
                if not in_code_block:
                    in_code_block = True
                    current_code = []
                    start_line = i
                    block_language = line.strip()[3:].strip().lower()
                else:
                    in_code_block = False
                    if block_language == language.lower():
                        code_content = '\n'.join(current_code)
                        code_blocks.append((code_content, start_line))
                    current_code = []
            elif in_code_block:
                current_code.append(line)

        self.code_blocks = code_blocks
        return code_blocks

    def validate_all(self) -> Dict[str, Any]:
        """Validate all code blocks. To be implemented by subclasses."""
        raise NotImplementedError


class OracleValidator(BaseValidator):
    """Validator for Oracle technical content."""

    VIEWS = {
        'V$INSTANCE', 'V$SESSION', 'V$PROCESS', 'V$SQL', 'V$SQLAREA',
        'V$SQL_PLAN', 'V$LOCK', 'V$TRANSACTION', 'V$SESSION_LONGOPS',
        'V$ACTIVE_SESSION_HISTORY', 'V$OSSTAT', 'V$SYSMETRIC',
        'V$SQL_MONITOR', 'V$PGASTAT', 'V$SGASTAT', 'V$ARCHIVED_LOG',
        'V$DATAGUARD_STATS', 'V$MANAGED_STANDBY', 'V$RMAN_STATUS',
        'V$CONTAINERS', 'V$PDBS', 'V$VECTOR_MEMORY_POOL',
        'GV$SESSION', 'GV$SYSTEM_EVENT', 'GV$SEGMENT_STATISTICS',
        'GV$INSTANCE', 'DBA_TABLES', 'DBA_INDEXES', 'DBA_TAB_COLUMNS',
        'DBA_DEPENDENCIES', 'DBA_VECTOR_INDEXES', 'DBA_HIST_SNAPSHOT',
        'DBA_HIST_SQLSTAT', 'DBA_HIST_SEG_STAT', 'DBA_HIST_SQL_PLAN',
        'DBA_HIST_ACTIVE_SESS_HISTORY'
    }

    def __init__(self, file_path: str):
        super().__init__(file_path)

    def validate_sql_syntax(self, sql: str, line_num: int) -> List[str]:
        """Validate basic SQL syntax."""
        issues = []

        if 'SELECT' in sql.upper() and 'FROM' not in sql.upper():
            issues.append(f"Line {line_num}: SELECT statement without FROM clause")

        open_parens = sql.count('(')
        close_parens = sql.count(')')
        if open_parens != close_parens:
            issues.append(f"Line {line_num}: Unmatched parentheses ({open_parens} open, {close_parens} close)")

        return issues

    def validate_view_names(self, sql: str, line_num: int) -> List[str]:
        """Validate Oracle view names."""
        issues = []
        view_pattern = r'\b(V\$|DBA_|GV\$|CDB_)[A-Z_]+\b'
        views = re.findall(view_pattern, sql, re.IGNORECASE)

        for view in views:
            view_upper = view.upper()
            known = any(view_upper.startswith(v.split('$')[0].split('_')[0]) for v in self.VIEWS)

            if not known and not view_upper.startswith('DBA_HIST_'):
                issues.append(f"Line {line_num}: Unknown view name '{view}'")

        return issues

    def validate_version_annotation(self, sql: str, line_num: int) -> List[str]:
        """Validate version compatibility annotations."""
        issues = []
        version_pattern = r'--\s*适用版本：(.+)'
        version_match = re.search(version_pattern, sql)

        if not version_match:
            issues.append(f"Line {line_num}: Missing version compatibility annotation")
            return issues

        version_info = version_match.group(1)
        valid_versions = ['11g', '12c', '19c', '21c', '23ai', '26ai']
        versions_in_annotation = re.findall(r'(11g|12c|19c|21c|23ai|26ai)', version_info)

        if not versions_in_annotation:
            issues.append(f"Line {line_num}: Invalid version format in annotation: '{version_info}'")

        if 'CON_ID' in sql.upper() or 'CDB_' in sql.upper():
            if not any(v in version_info for v in ['12c', '19c', '21c', '23ai', '26ai']):
                issues.append(f"Line {line_num}: Uses multitenant features but annotation doesn't include 12c+")

        if 'VECTOR' in sql.upper() or 'HNSW' in sql.upper():
            if '23ai' not in version_info and '26ai' not in version_info:
                issues.append(f"Line {line_num}: Uses vector features but annotation doesn't include 23ai/26ai")

        return issues

    def validate_sql_block(self, sql: str, line_num: int) -> List[str]:
        """Validate a single SQL block."""
        issues = []

        if not sql.strip():
            return issues

        issues.extend(self.validate_sql_syntax(sql, line_num))
        issues.extend(self.validate_view_names(sql, line_num))
        issues.extend(self.validate_version_annotation(sql, line_num))

        return issues

    def validate_all(self) -> Dict[str, Any]:
        """Validate all SQL blocks."""
        results = {
            'total_blocks': len(self.code_blocks),
            'valid_blocks': 0,
            'issues': []
        }

        for sql, line_num in self.code_blocks:
            issues = self.validate_sql_block(sql, line_num)
            if issues:
                results['issues'].extend(issues)
            else:
                results['valid_blocks'] += 1

        return results


class MySQLValidator(BaseValidator):
    """Validator for MySQL technical content."""

    TABLES = {
        'information_schema', 'performance_schema', 'mysql', 'sys'
    }

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.extract_code_blocks('sql')

    def validate_sql_syntax(self, sql: str, line_num: int) -> List[str]:
        """Validate basic MySQL SQL syntax."""
        issues = []

        if 'SELECT' in sql.upper() and 'FROM' not in sql.upper():
            issues.append(f"Line {line_num}: SELECT statement without FROM clause")

        open_parens = sql.count('(')
        close_parens = sql.count(')')
        if open_parens != close_parens:
            issues.append(f"Line {line_num}: Unmatched parentheses ({open_parens} open, {close_parens} close)")

        return issues

    def validate_version_annotation(self, sql: str, line_num: int) -> List[str]:
        """Validate version compatibility annotations."""
        issues = []
        version_pattern = r'--\s*适用版本：(.+)'
        version_match = re.search(version_pattern, sql)

        if not version_match:
            issues.append(f"Line {line_num}: Missing version compatibility annotation")
            return issues

        version_info = version_match.group(1)
        valid_versions = ['5.7', '8.0', '8.4']
        versions_in_annotation = re.findall(r'(5\.7|8\.0|8\.4)', version_info)

        if not versions_in_annotation:
            issues.append(f"Line {line_num}: Invalid version format in annotation: '{version_info}'")

        return issues

    def validate_sql_block(self, sql: str, line_num: int) -> List[str]:
        """Validate a single SQL block."""
        issues = []

        if not sql.strip():
            return issues

        issues.extend(self.validate_sql_syntax(sql, line_num))
        issues.extend(self.validate_version_annotation(sql, line_num))

        return issues

    def validate_all(self) -> Dict[str, Any]:
        """Validate all SQL blocks."""
        results = {
            'total_blocks': len(self.code_blocks),
            'valid_blocks': 0,
            'issues': []
        }

        for sql, line_num in self.code_blocks:
            issues = self.validate_sql_block(sql, line_num)
            if issues:
                results['issues'].extend(issues)
            else:
                results['valid_blocks'] += 1

        return results


class PostgreSQLValidator(BaseValidator):
    """Validator for PostgreSQL technical content."""

    VIEWS = {
        'pg_stat_activity', 'pg_stat_database', 'pg_stat_user_tables',
        'pg_stat_user_indexes', 'pg_locks', 'pg_stat_statements'
    }

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.extract_code_blocks('sql')

    def validate_sql_syntax(self, sql: str, line_num: int) -> List[str]:
        """Validate basic PostgreSQL SQL syntax."""
        issues = []

        if 'SELECT' in sql.upper() and 'FROM' not in sql.upper():
            issues.append(f"Line {line_num}: SELECT statement without FROM clause")

        open_parens = sql.count('(')
        close_parens = sql.count(')')
        if open_parens != close_parens:
            issues.append(f"Line {line_num}: Unmatched parentheses ({open_parens} open, {close_parens} close)")

        return issues

    def validate_version_annotation(self, sql: str, line_num: int) -> List[str]:
        """Validate version compatibility annotations."""
        issues = []
        version_pattern = r'--\s*适用版本：(.+)'
        version_match = re.search(version_pattern, sql)

        if not version_match:
            issues.append(f"Line {line_num}: Missing version compatibility annotation")
            return issues

        version_info = version_match.group(1)
        valid_versions = ['12', '13', '14', '15', '16']
        versions_in_annotation = re.findall(r'(12|13|14|15|16)', version_info)

        if not versions_in_annotation:
            issues.append(f"Line {line_num}: Invalid version format in annotation: '{version_info}'")

        return issues

    def validate_sql_block(self, sql: str, line_num: int) -> List[str]:
        """Validate a single SQL block."""
        issues = []

        if not sql.strip():
            return issues

        issues.extend(self.validate_sql_syntax(sql, line_num))
        issues.extend(self.validate_version_annotation(sql, line_num))

        return issues

    def validate_all(self) -> Dict[str, Any]:
        """Validate all SQL blocks."""
        results = {
            'total_blocks': len(self.code_blocks),
            'valid_blocks': 0,
            'issues': []
        }

        for sql, line_num in self.code_blocks:
            issues = self.validate_sql_block(sql, line_num)
            if issues:
                results['issues'].extend(issues)
            else:
                results['valid_blocks'] += 1

        return results


class KubernetesValidator(BaseValidator):
    """Validator for Kubernetes technical content."""

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.extract_code_blocks('yaml')

    def validate_yaml_syntax(self, yaml: str, line_num: int) -> List[str]:
        """Validate basic YAML syntax."""
        issues = []

        if 'apiVersion:' not in yaml and 'kind:' not in yaml:
            issues.append(f"Line {line_num}: Missing apiVersion or kind field")

        if 'kind:' in yaml:
            valid_kinds = ['Pod', 'Service', 'Deployment', 'StatefulSet', 'DaemonSet',
                          'ConfigMap', 'Secret', 'Ingress', 'Namespace', 'Node']
            kind_match = re.search(r'kind:\s*(\w+)', yaml)
            if kind_match:
                kind = kind_match.group(1)
                if kind not in valid_kinds:
                    issues.append(f"Line {line_num}: Unknown kind '{kind}'")

        return issues

    def validate_version_annotation(self, yaml: str, line_num: int) -> List[str]:
        """Validate version compatibility annotations."""
        issues = []
        version_pattern = r'#\s*适用版本：(.+)'
        version_match = re.search(version_pattern, yaml)

        if not version_match:
            issues.append(f"Line {line_num}: Missing version compatibility annotation")
            return issues

        version_info = version_match.group(1)
        valid_versions = ['1.20+', '1.24+', '1.28+']
        versions_in_annotation = re.findall(r'(1\.20\+|1\.24\+|1\.28\+)', version_info)

        if not versions_in_annotation:
            issues.append(f"Line {line_num}: Invalid version format in annotation: '{version_info}'")

        return issues

    def validate_yaml_block(self, yaml: str, line_num: int) -> List[str]:
        """Validate a single YAML block."""
        issues = []

        if not yaml.strip():
            return issues

        issues.extend(self.validate_yaml_syntax(yaml, line_num))
        issues.extend(self.validate_version_annotation(yaml, line_num))

        return issues

    def validate_all(self) -> Dict[str, Any]:
        """Validate all YAML blocks."""
        results = {
            'total_blocks': len(self.code_blocks),
            'valid_blocks': 0,
            'issues': []
        }

        for yaml, line_num in self.code_blocks:
            issues = self.validate_yaml_block(yaml, line_num)
            if issues:
                results['issues'].extend(issues)
            else:
                results['valid_blocks'] += 1

        return results


class LLMValidator(BaseValidator):
    """Validator for LLM/Prompt Engineering technical content."""

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.extract_code_blocks('python')

    def validate_python_syntax(self, python: str, line_num: int) -> List[str]:
        """Validate basic Python syntax."""
        issues = []

        if 'client.chat.completions.create' in python:
            if 'model=' not in python:
                issues.append(f"Line {line_num}: Missing 'model' parameter in API call")

            if 'messages=' not in python:
                issues.append(f"Line {line_num}: Missing 'messages' parameter in API call")

        open_parens = python.count('(')
        close_parens = python.count(')')
        if open_parens != close_parens:
            issues.append(f"Line {line_num}: Unmatched parentheses ({open_parens} open, {close_parens} close)")

        return issues

    def validate_version_annotation(self, python: str, line_num: int) -> List[str]:
        """Validate version compatibility annotations."""
        issues = []
        version_pattern = r'#\s*适用版本：(.+)'
        version_match = re.search(version_pattern, python)

        if not version_match:
            issues.append(f"Line {line_num}: Missing version compatibility annotation")
            return issues

        version_info = version_match.group(1)
        valid_versions = ['3.8+', 'v1.0+', 'v1.5+']
        versions_in_annotation = re.findall(r'(3\.8\+|v1\.0\+|v1\.5\+)', version_info)

        if not versions_in_annotation:
            issues.append(f"Line {line_num}: Invalid version format in annotation: '{version_info}'")

        return issues

    def validate_python_block(self, python: str, line_num: int) -> List[str]:
        """Validate a single Python block."""
        issues = []

        if not python.strip():
            return issues

        issues.extend(self.validate_python_syntax(python, line_num))
        issues.extend(self.validate_version_annotation(python, line_num))

        return issues

    def validate_all(self) -> Dict[str, Any]:
        """Validate all Python blocks."""
        results = {
            'total_blocks': len(self.code_blocks),
            'valid_blocks': 0,
            'issues': []
        }

        for python, line_num in self.code_blocks:
            issues = self.validate_python_block(python, line_num)
            if issues:
                results['issues'].extend(issues)
            else:
                results['valid_blocks'] += 1

        return results


class MermaidValidator(BaseValidator):
    """Validator for Mermaid diagram technical content."""

    VALID_TYPES = ['graph', 'flowchart', 'sequenceDiagram', 'classDiagram', 'stateDiagram', 'stateDiagram-v2', 'gantt', 'pie', 'erDiagram', 'gitGraph']

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.extract_code_blocks('mermaid')

    def validate_mermaid_syntax(self, mermaid: str, line_num: int) -> List[str]:
        """Validate basic Mermaid syntax."""
        issues = []

        first_line = mermaid.strip().split('\n')[0] if mermaid.strip() else ''
        if not any(first_line.startswith(t) for t in self.VALID_TYPES):
            issues.append(f"Line {line_num}: Unknown Mermaid diagram type")

        return issues

    def validate_mermaid_block(self, mermaid: str, line_num: int) -> List[str]:
        """Validate a single Mermaid block."""
        issues = []

        if not mermaid.strip():
            return issues

        issues.extend(self.validate_mermaid_syntax(mermaid, line_num))

        return issues

    def validate_all(self) -> Dict[str, Any]:
        """Validate all Mermaid blocks."""
        results = {
            'total_blocks': len(self.code_blocks),
            'valid_blocks': 0,
            'issues': []
        }

        for mermaid, line_num in self.code_blocks:
            issues = self.validate_mermaid_block(mermaid, line_num)
            if issues:
                results['issues'].extend(issues)
            else:
                results['valid_blocks'] += 1

        return results


def get_validator(technology: Technology, file_path: str) -> Optional[BaseValidator]:
    """Get the appropriate validator for the technology."""
    validators = {
        Technology.ORACLE: OracleValidator,
        Technology.MYSQL: MySQLValidator,
        Technology.POSTGRESQL: PostgreSQLValidator,
        Technology.KUBERNETES: KubernetesValidator,
        Technology.LLM: LLMValidator,
        Technology.MERMAID: MermaidValidator,
    }

    validator_class = validators.get(technology)
    if validator_class:
        return validator_class(file_path)
    return None


def print_report(results: Dict[str, Any], technology: Technology, file_path: str):
    """Print validation report."""
    print("\n" + "="*60)
    print("📊 Technical Accuracy Validation Report")
    print("="*60)
    print(f"\n📁 File: {file_path}")
    print(f"🔧 Technology: {technology.value}")
    print(f"📦 Total Code Blocks: {results['total_blocks']}")
    print(f"✅ Valid Blocks: {results['valid_blocks']}")
    print(f"❌ Issues Found: {len(results['issues'])}")

    if results['issues']:
        print("\n" + "-"*60)
        print("⚠️  Issues:")
        print("-"*60)
        for issue in results['issues']:
            print(f"  {issue}")
    else:
        print("\n✅ All code blocks are technically accurate!")

    print("="*60 + "\n")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Validate technical accuracy of articles.")
    parser.add_argument("file_path", help="Path to the file to validate")
    parser.add_argument("--tech", help="Specific technology to validate against (e.g., Oracle, MySQL)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()

    file_path = args.file_path
    technology = None
    verbose = args.verbose

    if args.tech:
        for tech in Technology:
            if tech.value.lower() == args.tech.lower():
                technology = tech
                break
        if not technology:
            print(f"❌ Error: Unknown technology '{args.tech}'")
            print("Supported technologies:")
            for tech in Technology:
                if tech != Technology.UNKNOWN:
                    print(f"  - {tech.value}")
            sys.exit(1)

    if not technology:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            technology, scores = TechnologyDetector.detect_with_details(content)

            if verbose:
                print("\n🔍 Technology Detection Results:")
                print("-" * 60)
                for tech_name, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
                    if score > 0:
                        print(f"  {tech_name}: {score} matches")
                print("-" * 60 + "\n")
        except FileNotFoundError:
             print(f"❌ Error: File not found: {file_path}")
             sys.exit(1)

    if technology == Technology.UNKNOWN:
        print("⚠️  Could not detect technology. Please specify using --tech option.")
        sys.exit(1)

    validator = get_validator(technology, file_path)
    if not validator:
        print(f"❌ No validator available for technology: {technology.value}")
        sys.exit(1)

    if not validator.read_file():
        sys.exit(1)

    if technology == Technology.ORACLE:
        validator.extract_code_blocks('sql')
    elif technology == Technology.MYSQL:
        validator.extract_code_blocks('sql')
    elif technology == Technology.POSTGRESQL:
        validator.extract_code_blocks('sql')
    elif technology == Technology.KUBERNETES:
        validator.extract_code_blocks('yaml')
    elif technology == Technology.LLM:
        validator.extract_code_blocks('python')
    elif technology == Technology.MERMAID:
        validator.extract_code_blocks('mermaid')

    if not validator.code_blocks:
        print(f"⚠️  No code blocks found for {technology.value}.")
        sys.exit(0)

    results = validator.validate_all()
    print_report(results, technology, file_path)

    if results['issues']:
        sys.exit(1)


if __name__ == '__main__':
    main()
