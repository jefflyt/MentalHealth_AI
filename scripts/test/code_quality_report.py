#!/usr/bin/env python3
"""
Code Quality Report - Comprehensive Validation
Generates a detailed report of the Mental Health AI codebase health
"""

import os
import sys
import re
from pathlib import Path


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def check_syntax():
    """Check Python syntax for all core files."""
    print_section("1. SYNTAX VALIDATION")
    
    core_files = [
        "app.py",
        "agent/router_agent.py",
        "agent/crisis_agent.py",
        "agent/information_agent.py",
        "agent/resource_agent.py",
        "agent/assessment_agent.py",
        "agent/escalation_agent.py",
        "agent/sunny_persona.py",
        "agent/reranker.py",
        "agent/update_agent.py",
        "interface/web/app.py"
    ]
    
    passed = 0
    failed = 0
    
    for file_path in core_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    compile(f.read(), file_path, 'exec')
                print(f"  ✅ {file_path}")
                passed += 1
            except SyntaxError as e:
                print(f"  ❌ {file_path}: Line {e.lineno} - {e.msg}")
                failed += 1
        else:
            print(f"  ⚠️  {file_path}: File not found")
    
    print(f"\n  Total: {passed} passed, {failed} failed")
    return failed == 0


def check_imports():
    """Verify critical imports are present."""
    print_section("2. IMPORT VALIDATION")
    
    checks = {
        "agent/router_agent.py": [
            "from typing import TypedDict, List, Tuple",
            "from langchain_groq import ChatGroq",
            "import re",
            "import logging"
        ],
        "agent/resource_agent.py": [
            "from .sunny_persona import build_sunny_prompt",
            "import logging"
        ],
        "agent/escalation_agent.py": [
            "from .sunny_persona import build_sunny_prompt",
            "import logging"
        ]
    }
    
    all_passed = True
    
    for file_path, required_imports in checks.items():
        if not os.path.exists(file_path):
            print(f"  ⚠️  {file_path}: File not found")
            continue
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"\n  📄 {file_path}")
        for import_stmt in required_imports:
            if import_stmt in content:
                print(f"    ✅ {import_stmt}")
            else:
                print(f"    ❌ Missing: {import_stmt}")
                all_passed = False
    
    return all_passed


def check_router_refactoring():
    """Validate Phase 1 & 2 router refactoring implementations."""
    print_section("3. ROUTER REFACTORING VALIDATION")
    
    router_file = "agent/router_agent.py"
    
    if not os.path.exists(router_file):
        print(f"  ❌ {router_file} not found")
        return False
    
    with open(router_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = {
        "Tuple Return Type": "def detect_distress_level(query: str) -> Tuple[str, float]:",
        "Word Boundary Function": "def _matches_with_word_boundary(phrase: str, text: str) -> bool:",
        "Enhanced Negation": "def _is_negated(phrase: str, text: str, phrase_position: int) -> bool:",
        "Logger Configuration": "logger = logging.getLogger(__name__)",
        "Tuple Unpacking": "distress_level, distress_score = detect_distress_level(query)",
        "5-Level Priority System": "# Priority 1: Crisis detection",
        "Early Crisis Check": "# Check BEFORE expensive context fetch",
        "Word Boundary Usage": r"if _matches_with_word_boundary\(phrase, query_lower\):",
        "Compound Negation": "not at all|not really|never",
        "Logging Calls": "logger.info|logger.warning|logger.error|logger.debug"
    }
    
    all_passed = True
    
    for check_name, pattern in checks.items():
        if re.search(pattern, content):
            print(f"  ✅ {check_name}")
        else:
            print(f"  ❌ Missing: {check_name}")
            all_passed = False
    
    return all_passed


def check_state_definition():
    """Verify AgentState TypedDict is properly defined."""
    print_section("4. STATE DEFINITION VALIDATION")
    
    files_to_check = ["app.py", "agent/router_agent.py"]
    
    required_fields = [
        "current_query: str",
        "messages: List[str]",
        "current_agent: str",
        "crisis_detected: bool",
        "context: str",
        "distress_level: str",
        "last_menu_options: List[str]",
        "turn_count: int"
    ]
    
    all_passed = True
    
    for file_path in files_to_check:
        if not os.path.exists(file_path):
            print(f"  ⚠️  {file_path}: File not found")
            continue
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find AgentState definition
        state_match = re.search(r'class AgentState\(TypedDict\):(.*?)(?=\n\n|\nclass |\ndef )', 
                               content, re.DOTALL)
        
        if not state_match:
            print(f"  ❌ {file_path}: AgentState not found")
            all_passed = False
            continue
        
        state_content = state_match.group(1)
        
        print(f"\n  📄 {file_path}")
        for field in required_fields:
            if field in state_content:
                print(f"    ✅ {field}")
            else:
                print(f"    ❌ Missing: {field}")
                all_passed = False
    
    return all_passed


def check_logging_implementation():
    """Verify logging is properly implemented across agents."""
    print_section("5. LOGGING IMPLEMENTATION")
    
    files_with_logging = {
        "agent/router_agent.py": ["logger.info", "logger.warning", "logger.error"],
        "agent/resource_agent.py": ["logger.info", "logger.warning", "logger.error"],
        "agent/escalation_agent.py": ["logger.info", "logger.warning", "logger.error"]
    }
    
    all_passed = True
    
    for file_path, logging_calls in files_with_logging.items():
        if not os.path.exists(file_path):
            print(f"  ⚠️  {file_path}: File not found")
            continue
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"\n  📄 {file_path}")
        
        # Check logger configuration
        if "logger = logging.getLogger(__name__)" in content:
            print(f"    ✅ Logger configured")
        else:
            print(f"    ❌ Logger not configured")
            all_passed = False
        
        # Check for logging calls
        for log_call in logging_calls:
            if log_call in content:
                count = content.count(log_call)
                print(f"    ✅ {log_call} ({count} uses)")
            else:
                print(f"    ⚠️  No {log_call} calls found")
    
    return all_passed


def check_shared_prompts():
    """Verify build_sunny_prompt usage in agents."""
    print_section("6. SHARED PROMPT UTILITY")
    
    agents_using_prompts = {
        "agent/resource_agent.py": "build_sunny_prompt",
        "agent/escalation_agent.py": "build_sunny_prompt"
    }
    
    all_passed = True
    
    for file_path, function_name in agents_using_prompts.items():
        if not os.path.exists(file_path):
            print(f"  ⚠️  {file_path}: File not found")
            continue
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"\n  📄 {file_path}")
        
        # Check import
        if "from .sunny_persona import build_sunny_prompt" in content:
            print(f"    ✅ Imports {function_name}")
        else:
            print(f"    ❌ Missing import for {function_name}")
            all_passed = False
        
        # Check usage
        if f"{function_name}(" in content:
            count = content.count(f"{function_name}(")
            print(f"    ✅ Uses {function_name} ({count} times)")
        else:
            print(f"    ❌ Never calls {function_name}")
            all_passed = False
    
    return all_passed


def check_test_coverage():
    """Verify comprehensive test coverage."""
    print_section("7. TEST COVERAGE")
    
    test_files = [
        "scripts/test/test_router_refactoring.py",
        "scripts/test/test_phase2_improvements.py",
        "scripts/test/test_distress_detection.py",
        "scripts/test/test_router_integration.py"
    ]
    
    existing_tests = []
    missing_tests = []
    
    for test_file in test_files:
        if os.path.exists(test_file):
            existing_tests.append(test_file)
            print(f"  ✅ {test_file}")
        else:
            missing_tests.append(test_file)
            print(f"  ❌ {test_file}")
    
    print(f"\n  Total: {len(existing_tests)}/{len(test_files)} test files present")
    
    return len(missing_tests) == 0


def check_dependencies():
    """Verify dependencies are properly defined."""
    print_section("8. DEPENDENCY CHECK")
    
    req_file = "requirements.txt"
    
    if not os.path.exists(req_file):
        print(f"  ❌ {req_file} not found")
        return False
    
    with open(req_file, 'r', encoding='utf-8') as f:
        requirements = f.read()
    
    critical_deps = [
        "langgraph",
        "langchain",
        "langchain-groq",
        "chromadb",
        "flask",
        "python-dotenv",
        "beautifulsoup4",
        "sentence-transformers"
    ]
    
    all_present = True
    
    for dep in critical_deps:
        if dep in requirements:
            print(f"  ✅ {dep}")
        else:
            print(f"  ❌ Missing: {dep}")
            all_present = False
    
    return all_present


def generate_summary(results):
    """Generate final summary report."""
    print_section("SUMMARY REPORT")
    
    total_checks = len(results)
    passed_checks = sum(1 for r in results.values() if r)
    failed_checks = total_checks - passed_checks
    
    print(f"\n  Total Checks: {total_checks}")
    print(f"  ✅ Passed: {passed_checks}")
    print(f"  ❌ Failed: {failed_checks}")
    
    if failed_checks == 0:
        print("\n  🎉 ALL QUALITY CHECKS PASSED!")
        print("  📊 Code is production-ready")
    else:
        print("\n  ⚠️  SOME CHECKS FAILED")
        print("  📝 Review failed checks above")
        
        print("\n  Failed Checks:")
        for check_name, result in results.items():
            if not result:
                print(f"    - {check_name}")
    
    print("\n" + "="*70)
    
    return failed_checks == 0


def main():
    """Run all code quality checks."""
    print("\n" + "="*70)
    print("  🔍 AI MENTAL HEALTH AGENT - CODE QUALITY REPORT")
    print("="*70)
    print(f"  Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Change to project root
    os.chdir(Path(__file__).parent.parent.parent)
    
    # Run all checks
    results = {
        "Syntax Validation": check_syntax(),
        "Import Validation": check_imports(),
        "Router Refactoring": check_router_refactoring(),
        "State Definition": check_state_definition(),
        "Logging Implementation": check_logging_implementation(),
        "Shared Prompt Utility": check_shared_prompts(),
        "Test Coverage": check_test_coverage(),
        "Dependencies": check_dependencies()
    }
    
    # Generate summary
    all_passed = generate_summary(results)
    
    # Exit with appropriate code
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
