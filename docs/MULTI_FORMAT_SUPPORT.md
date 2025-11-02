# 📁 Multi-Format File Support

> Enhanced UpdateAgent now supports 7 different file formats for knowledge base ingestion!

---

## ✨ What's New?

The `UpdateAgent` has been upgraded to support multiple file formats beyond plain text. You can now add knowledge content in various formats and the agent will automatically extract and process them.

## 🎯 Supported Formats

| Format | Extension | Use Case | Requires |
|--------|-----------|----------|----------|
| **Plain Text** | `.txt` | Simple text files | ✅ Built-in |
| **Markdown** | `.md` | Formatted documentation | ✅ Built-in |
| **PDF** | `.pdf` | Clinical guidelines, research papers | PyPDF2 |
| **Word** | `.docx` | Treatment protocols, reports | python-docx |
| **HTML** | `.html`, `.htm` | Web content, scraped pages | beautifulsoup4* |
| **JSON** | `.json` | Structured FAQs, Q&A databases | ✅ Built-in |
| **CSV** | `.csv` | Resource directories, contact lists | pandas |

\* beautifulsoup4 is already installed for web scraping

---

## 🚀 Quick Start

### 1. Install Optional Dependencies

```bash
# Install all format support (recommended)
pip install PyPDF2 python-docx pandas openpyxl markdown

# Or install selectively
pip install PyPDF2          # For PDFs only
pip install python-docx     # For Word documents only
pip install pandas openpyxl # For CSV/Excel only
```

### 2. Add Files to Knowledge Base

```bash
# PDF documents
cp clinical_guidelines.pdf data/knowledge/clinical_guidelines/

# Word documents
cp treatment_protocol.docx data/knowledge/crisis_protocols/

# CSV data
cp singapore_resources.csv data/knowledge/singapore_resources/

# JSON FAQs
cp mental_health_faqs.json data/knowledge/faqs/

# Markdown documentation
cp coping_strategies.md data/knowledge/coping_strategies/
```

### 3. Update ChromaDB

```bash
# Automatic update (detects changes)
python agent/update_agent.py auto

# Or force full rebuild
python agent/update_agent.py force
```

### 4. Verify

The UpdateAgent will show format support status:

```
📁 Multi-Format Support Status:
  ✅ Plain Text (.txt, .md)
  ✅ PDF Documents (.pdf)
  ✅ Word Documents (.docx)
  ✅ HTML Files (.html, .htm)
  ✅ CSV Data (.csv)
  ✅ JSON Data (.json)
```

---

## 📝 Format-Specific Guidelines

### PDF Files (.pdf)

**Best For:**
- Clinical practice guidelines
- Research papers
- Policy documents
- Medical literature

**How It Works:**
- Extracts text from all pages
- Preserves paragraph structure
- Joins pages with double newlines

**Example:**
```bash
# Add WHO mental health guidelines
cp WHO_Mental_Health_Guidelines_2023.pdf data/knowledge/clinical_guidelines/
python agent/update_agent.py auto
```

---

### Word Documents (.docx)

**Best For:**
- Treatment protocols
- Assessment forms
- Clinical reports
- Structured procedures

**How It Works:**
- Extracts text from paragraphs
- Preserves document structure
- Skips empty paragraphs

**Example:**
```bash
# Add crisis intervention protocol
cp Crisis_Intervention_Protocol.docx data/knowledge/crisis_protocols/
python agent/update_agent.py auto
```

---

### CSV Files (.csv)

**Best For:**
- Resource directories
- Contact lists
- Service providers
- Comparison tables

**How It Works:**
- Converts to readable text table
- Preserves column structure
- Easy to search

**Example CSV Structure:**
```csv
Service Name,Contact,Address,Operating Hours
IMH 24hr Helpline,6389 2222,10 Buangkok View,24/7
SOS Hotline,1767,N/A,24/7
CHAT,6493 6500,Various locations,Mon-Fri 9am-6pm
```

**Add to Knowledge:**
```bash
cp singapore_mental_health_services.csv data/knowledge/singapore_resources/
python agent/update_agent.py auto
```

---

### JSON Files (.json)

**Best For:**
- FAQ databases
- Structured Q&A
- Categorized information
- Configuration data

**How It Works:**
- Converts to readable key-value format
- Handles nested structures
- Preserves organization

**Example JSON Structure:**
```json
{
  "anxiety_faqs": [
    {
      "question": "What is anxiety?",
      "answer": "Anxiety is a natural response to stress..."
    },
    {
      "question": "When should I seek help?",
      "answer": "You should seek help when anxiety interferes..."
    }
  ]
}
```

**Add to Knowledge:**
```bash
cp mental_health_faqs.json data/knowledge/faqs/
python agent/update_agent.py auto
```

---

### HTML Files (.html, .htm)

**Best For:**
- Scraped web content
- Formatted articles
- Online resources
- Blog posts

**How It Works:**
- Removes scripts and styles
- Extracts clean text
- Preserves paragraph structure

**Example:**
```bash
# Add scraped content from trusted sources
cp healthhub_article.html data/knowledge/mental_health_info/
python agent/update_agent.py auto
```

---

### Markdown Files (.md)

**Best For:**
- Formatted documentation
- Structured guides
- README-style content
- Educational materials

**How It Works:**
- Reads as plain text
- Markdown syntax is preserved
- Easy to maintain

**Example:**
```bash
# Add formatted guide
cp mindfulness_guide.md data/knowledge/coping_strategies/
python agent/update_agent.py auto
```

---

## 🔄 How It Works

### Automatic Format Detection

The `UpdateAgent` automatically detects file formats by extension:

```python
# When scanning knowledge folder
for file in files:
    if file.endswith('.pdf'):
        text = extract_text_from_pdf(file)
    elif file.endswith('.docx'):
        text = extract_text_from_docx(file)
    elif file.endswith('.csv'):
        text = extract_text_from_csv(file)
    # ... etc
```

### Graceful Degradation

If a format library is not installed:

```
⚠️  PDF support not available. Install: pip install PyPDF2
```

The agent will:
- Continue processing other files
- Show clear warning messages
- Still work with supported formats

### Format-Specific Metadata

Each chunk stores its original format:

```python
{
    'content': 'extracted text...',
    'source': 'filename.pdf',
    'format': 'PDF Document',
    'category': 'clinical_guidelines'
}
```

---

## 🎯 Best Practices

### Organize by Content Type

```
data/knowledge/
├── clinical_guidelines/      # PDFs, DOCX
│   ├── WHO_Guidelines.pdf
│   └── Treatment_Protocol.docx
├── faqs/                      # JSON
│   ├── anxiety_faqs.json
│   └── depression_faqs.json
├── singapore_resources/       # CSV, TXT
│   ├── services.csv
│   └── hotlines.txt
└── mental_health_info/        # MD, HTML, TXT
    ├── anxiety_info.md
    ├── depression_article.html
    └── stress_info.txt
```

### Choose the Right Format

- **Need structure?** → CSV or JSON
- **Have official docs?** → PDF or DOCX
- **Writing content?** → Markdown or TXT
- **Scraped web?** → HTML
- **Simple text?** → TXT (always works!)

### File Size Considerations

- PDFs: Can be large, will extract all pages
- Word: Usually moderate size
- CSV: Very efficient for tabular data
- JSON: Compact for structured data
- Text/Markdown: Most efficient

### Update Workflow

1. **Add new files** to appropriate category folder
2. **Run auto update** to detect changes
3. **Verify** chunks were added
4. **Test queries** to ensure content is retrievable

---

## 🧪 Testing Multi-Format Support

### Check Installation Status

```bash
# Run test script
python test_multiformat.py
```

**Expected Output:**
```
============================================================
🔍 Testing Multi-Format Support
============================================================

✅ UpdateAgent imported successfully

📁 Supported File Formats:
   .txt     → Plain Text
   .md      → Markdown
   .pdf     → PDF Document
   .docx    → Word Document
   .html    → HTML
   .htm     → HTML
   .json    → JSON Data
   .csv     → CSV Data

============================================================
🚀 Initializing UpdateAgent...
============================================================

📁 Multi-Format Support Status:
  ✅ Plain Text (.txt, .md)
  ✅ PDF Documents (.pdf)
  ✅ Word Documents (.docx)
  ✅ HTML Files (.html, .htm)
  ✅ CSV Data (.csv)
  ✅ JSON Data (.json)

✅ SUCCESS! Multi-format support is ready to use!
```

### Test Individual Formats

Create sample files to test:

```bash
# Test PDF
echo "Sample content" | enscript -p - | ps2pdf - test.pdf
cp test.pdf data/knowledge/test/

# Test Markdown
echo "# Test\nThis is a test." > data/knowledge/test/test.md

# Test JSON
echo '{"test": "value"}' > data/knowledge/test/test.json

# Update and verify
python agent/update_agent.py auto
```

---

## 📊 Migration Guide

### Converting Existing Content

If you have existing content in various formats:

1. **Inventory your content:**
   ```bash
   find ~/Documents -name "*.pdf" -o -name "*.docx" | grep mental
   ```

2. **Organize by category:**
   ```bash
   mkdir -p data/knowledge/{clinical_guidelines,faqs,resources}
   ```

3. **Copy relevant files:**
   ```bash
   cp ~/Documents/clinical/*.pdf data/knowledge/clinical_guidelines/
   cp ~/Documents/protocols/*.docx data/knowledge/crisis_protocols/
   ```

4. **Update ChromaDB:**
   ```bash
   python agent/update_agent.py force
   ```

### Maintaining Mixed Formats

It's perfectly fine to have multiple formats in the same category:

```
data/knowledge/singapore_resources/
├── imh_services.txt          # Plain text
├── chat_services.txt          # Plain text
├── service_directory.csv      # CSV table
├── hotlines.json              # JSON data
└── mental_health_act.pdf      # PDF document
```

All will be processed and indexed together!

---

## 🚨 Troubleshooting

### "PDF support not available"

**Solution:**
```bash
pip install PyPDF2
```

### "DOCX support not available"

**Solution:**
```bash
pip install python-docx
```

### "CSV support not available"

**Solution:**
```bash
pip install pandas openpyxl
```

### File Not Being Processed

**Check:**
1. File extension is correct (`.pdf` not `.PDF`)
2. File is in `data/knowledge/` or subdirectory
3. File is not corrupted
4. Required library is installed

**Debug:**
```bash
python agent/update_agent.py auto --verbose
```

### Chunks Not Appearing

**Verify:**
```bash
# Check ChromaDB state
python agent/update_agent.py status

# Look for your file in output
# Should show: "✏️ MOD filename.pdf [PDF Document] (X chunks)"
```

---

## 🎓 Advanced Usage

### Custom Format Support

To add support for new formats, edit `agent/update_agent.py`:

1. Add format to `SUPPORTED_FORMATS` dictionary
2. Create a `_read_formatname()` method
3. Add case to `extract_text_from_file()`

### Bulk Import Script

```python
#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

# Source folder with various files
SOURCE = "/path/to/mental_health_resources"
DEST = "data/knowledge"

# Map file types to categories
CATEGORY_MAP = {
    '.pdf': 'clinical_guidelines',
    '.docx': 'crisis_protocols',
    '.csv': 'singapore_resources',
    '.json': 'faqs',
}

for file in Path(SOURCE).rglob('*'):
    if file.suffix in CATEGORY_MAP:
        category = CATEGORY_MAP[file.suffix]
        dest_dir = Path(DEST) / category
        dest_dir.mkdir(exist_ok=True)
        shutil.copy(file, dest_dir / file.name)
        print(f"Copied {file.name} → {category}/")

print("\n✅ Import complete! Run: python agent/update_agent.py auto")
```

---

## 📚 Related Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Getting started with multi-format support
- **[TODO.md](TODO.md)** - Knowledge base enhancement roadmap
- **[GUIDE.md](GUIDE.md)** - Complete technical guide
- **[requirements.txt](requirements.txt)** - All dependencies including optional format libraries

---

## ✅ Summary

**What You Get:**
- ✅ Support for 7 file formats
- ✅ Automatic format detection
- ✅ Graceful degradation if libraries missing
- ✅ Format metadata in ChromaDB
- ✅ Easy migration path

**Installation:**
```bash
pip install PyPDF2 python-docx pandas openpyxl markdown
```

**Usage:**
```bash
# Add files in any supported format
cp yourfile.{pdf,docx,csv,json,md} data/knowledge/category/

# Update ChromaDB
python agent/update_agent.py auto

# That's it!
```

---

**Questions?** Check [GUIDE.md](GUIDE.md) or create an issue!
