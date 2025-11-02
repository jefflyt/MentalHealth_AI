#!/usr/bin/env python3
"""
Code verification script for update_agent.py
Checks syntax, logic, and structure without requiring dependencies
"""

import ast
import sys
from pathlib import Path

def check_syntax(filepath):
    """Check Python syntax by parsing AST"""
    print("=" * 70)
    print("🔍 SYNTAX CHECK")
    print("=" * 70)
    
    try:
        with open(filepath, 'r') as f:
            code = f.read()
        ast.parse(code)
        print("✅ Python syntax is valid")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax Error at line {e.lineno}: {e.msg}")
        return False

def check_class_structure(filepath):
    """Verify UpdateAgent class has all required methods"""
    print("\n" + "=" * 70)
    print("🔍 CLASS STRUCTURE CHECK")
    print("=" * 70)
    
    required_methods = [
        '__init__',
        '_print_format_support',
        'extract_text_from_file',
        '_read_text_file',
        '_read_pdf',
        '_read_docx',
        '_read_html',
        '_read_json',
        '_read_csv',
        'load_state',
        'save_state',
        'get_file_hash',
        'split_into_chunks',
        'scan_data_folder',
        'detect_changes',
        'check_for_updates',
        'perform_smart_update',
        'list_current_state',
    ]
    
    with open(filepath, 'r') as f:
        tree = ast.parse(f.read())
    
    # Find UpdateAgent class
    update_agent_class = None
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == 'UpdateAgent':
            update_agent_class = node
            break
    
    if not update_agent_class:
        print("❌ UpdateAgent class not found")
        return False
    
    # Get all methods in the class
    methods = [m.name for m in update_agent_class.body if isinstance(m, ast.FunctionDef)]
    
    print(f"Found UpdateAgent class with {len(methods)} methods:")
    missing = []
    for method in required_methods:
        if method in methods:
            print(f"  ✅ {method}")
        else:
            print(f"  ❌ {method} - MISSING")
            missing.append(method)
    
    if missing:
        print(f"\n❌ Missing {len(missing)} required methods")
        return False
    else:
        print(f"\n✅ All {len(required_methods)} required methods present")
        return True

def check_constants(filepath):
    """Check required constants and imports"""
    print("\n" + "=" * 70)
    print("🔍 CONSTANTS & IMPORTS CHECK")
    print("=" * 70)
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    checks = {
        'SUPPORTED_FORMATS': 'SUPPORTED_FORMATS' in content,
        'PDF_SUPPORT flag': 'PDF_SUPPORT' in content,
        'DOCX_SUPPORT flag': 'DOCX_SUPPORT' in content,
        'CSV_SUPPORT flag': 'CSV_SUPPORT' in content,
        'HTML_SUPPORT flag': 'HTML_SUPPORT' in content,
        'STATE_FILE constant': 'STATE_FILE' in content,
        'chromadb import': 'import chromadb' in content,
        'PyPDF2 import (conditional)': 'import PyPDF2' in content,
        'python-docx import (conditional)': 'from docx import Document' in content,
        'pandas import (conditional)': 'import pandas' in content,
        'BeautifulSoup import (conditional)': 'from bs4 import BeautifulSoup' in content,
    }
    
    all_good = True
    for name, present in checks.items():
        if present:
            print(f"  ✅ {name}")
        else:
            print(f"  ❌ {name} - MISSING")
            all_good = False
    
    if all_good:
        print(f"\n✅ All constants and imports present")
    return all_good

def check_supported_formats(filepath):
    """Verify SUPPORTED_FORMATS dictionary"""
    print("\n" + "=" * 70)
    print("🔍 SUPPORTED FORMATS CHECK")
    print("=" * 70)
    
    with open(filepath, 'r') as f:
        tree = ast.parse(f.read())
    
    # Find SUPPORTED_FORMATS in UpdateAgent class
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == 'UpdateAgent':
            for item in node.body:
                if isinstance(item, ast.Assign):
                    for target in item.targets:
                        if isinstance(target, ast.Name) and target.id == 'SUPPORTED_FORMATS':
                            if isinstance(item.value, ast.Dict):
                                formats = {}
                                for k, v in zip(item.value.keys, item.value.values):
                                    if isinstance(k, ast.Constant) and isinstance(v, ast.Constant):
                                        formats[k.value] = v.value
                                
                                expected_formats = ['.txt', '.md', '.pdf', '.docx', '.html', '.htm', '.json', '.csv']
                                
                                print("Supported formats found:")
                                for ext, desc in formats.items():
                                    print(f"  ✅ {ext:8} → {desc}")
                                
                                missing = [f for f in expected_formats if f not in formats]
                                if missing:
                                    print(f"\n❌ Missing formats: {missing}")
                                    return False
                                else:
                                    print(f"\n✅ All {len(expected_formats)} expected formats present")
                                    return True
    
    print("❌ SUPPORTED_FORMATS not found")
    return False

def check_error_handling(filepath):
    """Check for proper error handling"""
    print("\n" + "=" * 70)
    print("🔍 ERROR HANDLING CHECK")
    print("=" * 70)
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Count try-except blocks
    try_count = content.count('try:')
    except_count = content.count('except')
    
    print(f"  Try-except blocks: {try_count}")
    
    # Check each format reader has error handling
    readers = ['_read_text_file', '_read_pdf', '_read_docx', '_read_html', '_read_json', '_read_csv']
    
    all_have_errors = True
    for reader in readers:
        # Find the method
        start = content.find(f'def {reader}(')
        if start == -1:
            print(f"  ❌ {reader} - NOT FOUND")
            all_have_errors = False
            continue
        
        # Find next method
        next_def = content.find('\n    def ', start + 1)
        method_code = content[start:next_def] if next_def != -1 else content[start:]
        
        has_try = 'try:' in method_code
        has_except = 'except' in method_code
        
        if has_try and has_except:
            print(f"  ✅ {reader} - has error handling")
        else:
            print(f"  ❌ {reader} - MISSING error handling")
            all_have_errors = False
    
    if all_have_errors:
        print(f"\n✅ All format readers have error handling")
    return all_have_errors

def main():
    filepath = Path(__file__).parent / 'agent' / 'update_agent.py'
    
    if not filepath.exists():
        print(f"❌ File not found: {filepath}")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("🧪 VERIFYING update_agent.py CODE")
    print("=" * 70)
    print(f"File: {filepath}")
    print(f"Size: {filepath.stat().st_size:,} bytes")
    print()
    
    results = []
    
    # Run all checks
    results.append(("Syntax", check_syntax(filepath)))
    results.append(("Class Structure", check_class_structure(filepath)))
    results.append(("Constants & Imports", check_constants(filepath)))
    results.append(("Supported Formats", check_supported_formats(filepath)))
    results.append(("Error Handling", check_error_handling(filepath)))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 70)
    
    for check_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status:10} - {check_name}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 70)
    if all_passed:
        print("🎉 ALL CHECKS PASSED!")
        print("=" * 70)
        print("\n✅ The code is structurally sound and ready to use.")
        print("\n📝 Next steps:")
        print("   1. Install optional dependencies:")
        print("      pip install PyPDF2 python-docx pandas openpyxl")
        print("   2. Test with sample files in different formats")
        print("   3. Run: python agent/update_agent.py status")
        sys.exit(0)
    else:
        print("❌ SOME CHECKS FAILED")
        print("=" * 70)
        failed = [name for name, passed in results if not passed]
        print(f"\nFailed checks: {', '.join(failed)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
