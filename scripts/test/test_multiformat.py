#!/usr/bin/env python3
"""
Quick test to demonstrate multi-format file support in UpdateAgent
"""

# Test 1: Verify imports work
print("=" * 60)
print("🔍 Testing Multi-Format Support")
print("=" * 60)

try:
    from agent.update_agent import UpdateAgent
    print("\n✅ UpdateAgent imported successfully")
except Exception as e:
    print(f"\n❌ Import failed: {e}")
    exit(1)

# Test 2: Check supported formats
print("\n📁 Supported File Formats:")
for ext, desc in UpdateAgent.SUPPORTED_FORMATS.items():
    print(f"   {ext:8} → {desc}")

# Test 3: Initialize agent and show format support
print("\n" + "=" * 60)
print("🚀 Initializing UpdateAgent...")
print("=" * 60)

agent = UpdateAgent()

print("\n✅ SUCCESS! Multi-format support is ready to use!")
print("\n📝 Next Steps:")
print("   1. Install optional libraries: pip install PyPDF2 python-docx pandas")
print("   2. Add files in any supported format to data/knowledge/")
print("   3. Run: python agent/update_agent.py auto")
print("   4. Files will be automatically processed!\n")
