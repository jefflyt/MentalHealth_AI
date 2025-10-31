# Smart Update Agent - Quick Reference

## 🤖 What It Does

The **Update Agent** automatically monitors your `data/knowledge/` folder and intelligently updates ChromaDB when:
- ✅ New `.txt` files are added
- ✅ Existing files are modified
- ✅ Files are deleted

It uses **file hashing** to detect changes and only processes what's new or modified.

**Folder Structure:**
```
MentalHealth_AI/
└── data/
    ├── chroma_db/         # Vector database (auto-generated)
    └── knowledge/         # Your mental health content (source)
        ├── mental_health_info/
        ├── singapore_resources/
        ├── coping_strategies/
        ├── dass21_guidelines/
        └── crisis_protocols/
```

## 📝 Usage Commands

### Check for Changes (No Updates)
```bash
python update_agent.py check
```
- Shows what files have changed
- Doesn't modify ChromaDB
- Good for previewing before updating

### Smart Update (Recommended)
```bash
python update_agent.py auto
```
- Checks for changes
- Only updates if changes detected
- **This is the command you want most of the time!**

### Manual Update
```bash
python update_agent.py update
```
- Forces update even if already checked
- Use after `check` command

### View Current State
```bash
python update_agent.py status
```
- Shows all files currently in ChromaDB
- Displays chunk counts per file
- Shows last update time

### Force Recreate (Nuclear Option)
```bash
python update_agent.py force
```
- Deletes and recreates entire collection
- Re-ingests all files from scratch
- ⚠️ Use only if corruption suspected

## 🔄 Typical Workflows

### Adding New Content
```bash
# 1. Add your new file to knowledge folder
echo "New content..." > data/knowledge/coping_strategies/new_technique.txt

# 2. Run auto-update
python update_agent.py auto

# 3. Verify it was added
python update_agent.py status
```

### Modifying Existing Content
```bash
# 1. Edit your file in knowledge folder
nano data/knowledge/singapore_resources/chat_services.txt

# 2. Run auto-update (detects changes via hash)
python update_agent.py auto

# 3. Old chunks removed, new chunks added automatically!
```

### Before Running App
```bash
# Check for updates before starting your app
python update_agent.py auto && python app.py
```

## 🎯 Integration with App

The update agent is **automatically integrated** into `app.py`!

When you run `python app.py`, it will:
1. Check for data changes
2. Perform smart update if needed
3. Then start the chat agent

## 📊 State Tracking

The agent tracks state in: `data/chroma_db/.update_state.json`

This file contains:
- File hashes for change detection
- Last update timestamp
- Total chunk count

**Don't delete this file** unless you want to force a full re-ingestion.

## 💡 Pro Tips

### Batch Updates
```bash
# Add multiple files to knowledge folder
cp new_files/*.txt data/knowledge/mental_health_info/

# Single update command handles all
python update_agent.py auto
```

### Check Before Committing
```bash
# See what will be updated
python update_agent.py check

# Then decide to update or not
python update_agent.py update
```

### Regular Maintenance
```bash
# Weekly cron job to keep ChromaDB fresh
0 2 * * 0 cd /path/to/project && python update_agent.py auto
```

## 🔍 Understanding Output

### New File Detection
```
🔍 Changes Detected:
   📄 New files: 1
      + coping_strategies/positive_affirmations.txt
```

### Modified File Detection
```
🔍 Changes Detected:
   ✏️  Modified files: 1
      ~ singapore_resources/chat_services.txt
```

### Update Results
```
📊 Update Summary:
   • Total chunks in ChromaDB: 168
   • New/modified chunks added: 4
   • Deleted chunks removed: 0
   • Files processed: 1
```

## ⚠️ Troubleshooting

### "No changes detected" but file was added
- Check if file is `.txt` format
- Verify file is in `data/knowledge/` subdirectories
- Run `python update_agent.py status` to see current files

### Duplicates in ChromaDB
- Run `python update_agent.py force` to rebuild cleanly
- Check for multiple files with same name in different dirs

### Update takes too long
- Normal for first run (all files are "new")
- Subsequent runs only process changes
- Large files create more chunks (normal)

## � How It Works

1. **File Scanning**: Walks `data/knowledge/` directory for `.txt` files
2. **Hash Calculation**: MD5 hash of each file's content
3. **Change Detection**: Compares current hashes to saved state
4. **Smart Processing**: 
   - New files → Add chunks
   - Modified files → Delete old chunks, add new chunks
   - Deleted files → Remove chunks
5. **State Update**: Save new hashes for next run

## 🚀 Quick Start Examples

### Complete Workflow
```bash
# 1. Check current state
python update_agent.py status

# 2. Add new mental health resource
cat > data/knowledge/mental_health_info/burnout.txt << EOF
Understanding Burnout
...your content here...
EOF

# 3. Smart update
python update_agent.py auto

# 4. Test in app
python app.py
# Ask: "Tell me about burnout"
# Agent will now use your new file!
```

### Daily Routine
```bash
# Morning: Check for any manual file edits
python update_agent.py check

# If changes: Update ChromaDB
python update_agent.py update

# Start your agent
python app.py
```

## 📈 Monitoring

Track your knowledge base growth:
```bash
# See total chunks over time
python update_agent.py status | grep "Total chunks"
```

## 🎯 Best Practices

1. ✅ **Always run `auto` before starting app** (or just run app, it's integrated!)
2. ✅ **Use `check` to preview changes** before committing
3. ✅ **Keep backup of `chroma_db/.update_state.json`** for rollback
4. ✅ **Organize files by category** in subdirectories
5. ✅ **Use descriptive filenames** for better tracking
6. ⚠️ **Don't manually edit ChromaDB** - always use update agent

---

**Need help?** Run `python update_agent.py` with no arguments for command list.
