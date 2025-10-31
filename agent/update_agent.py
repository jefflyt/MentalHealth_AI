#!/usr/bin/env python3
"""
Smart Update Agent for AI Mental Health ChromaDB
Monitors data/knowledge/ folder and performs intelligent updates when changes are detected
"""

import os
import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Set
import hashlib
import json
from datetime import datetime
from pathlib import Path

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./data/chroma_db")
embedding_function = embedding_functions.DefaultEmbeddingFunction()

# State tracking file
STATE_FILE = "data/chroma_db/.update_state.json"

class UpdateAgent:
    """Smart agent for monitoring and updating ChromaDB with new data."""
    
    def __init__(self, knowledge_dir: str = "data/knowledge", collection_name: str = "mental_health_kb"):
        self.knowledge_dir = knowledge_dir
        self.collection_name = collection_name
        self.state = self.load_state()
        
    def load_state(self) -> Dict:
        """Load previous state to track changes."""
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"file_hashes": {}, "last_update": None, "total_chunks": 0}
    
    def save_state(self):
        """Save current state for next comparison."""
        self.state["last_update"] = datetime.now().isoformat()
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        with open(STATE_FILE, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def get_file_hash(self, filepath: str) -> str:
        """Get MD5 hash of file content to detect changes."""
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def split_into_chunks(self, text: str, max_length: int = 1000) -> List[str]:
        """Split text into chunks for better retrieval."""
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            if len(current_chunk + paragraph) < max_length:
                current_chunk += paragraph + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + "\n\n"
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def scan_data_folder(self) -> Dict[str, Dict]:
        """
        Scan knowledge folder and return file information.
        
        Returns:
            Dict mapping file paths to their metadata (hash, category, etc.)
        """
        files_info = {}
        
        if not os.path.exists(self.knowledge_dir):
            print(f"⚠️  Knowledge directory not found: {self.knowledge_dir}")
            return files_info
        
        for root, dirs, files in os.walk(self.knowledge_dir):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.knowledge_dir)
                    
                    try:
                        file_hash = self.get_file_hash(file_path)
                        category = os.path.basename(root)
                        
                        files_info[rel_path] = {
                            'full_path': file_path,
                            'hash': file_hash,
                            'category': category,
                            'filename': file
                        }
                    except Exception as e:
                        print(f"   ✗ Error reading {file_path}: {e}")
        
        return files_info
    
    def detect_changes(self) -> tuple[Set[str], Set[str], Set[str]]:
        """
        Detect new, modified, and deleted files.
        
        Returns:
            (new_files, modified_files, deleted_files)
        """
        current_files = self.scan_data_folder()
        previous_hashes = self.state.get("file_hashes", {})
        
        current_paths = set(current_files.keys())
        previous_paths = set(previous_hashes.keys())
        
        # Detect changes
        new_files = current_paths - previous_paths
        deleted_files = previous_paths - current_paths
        
        # Detect modifications
        modified_files = set()
        for path in current_paths & previous_paths:
            if current_files[path]['hash'] != previous_hashes[path]['hash']:
                modified_files.add(path)
        
        return new_files, modified_files, deleted_files
    
    def check_for_updates(self) -> bool:
        """
        Check if there are any new or modified files.
        
        Returns:
            True if updates are needed, False otherwise
        """
        new_files, modified_files, deleted_files = self.detect_changes()
        
        has_changes = bool(new_files or modified_files or deleted_files)
        
        if has_changes:
            print("\n🔍 Changes Detected:")
            if new_files:
                print(f"   📄 New files: {len(new_files)}")
                for f in sorted(new_files):
                    print(f"      + {f}")
            if modified_files:
                print(f"   ✏️  Modified files: {len(modified_files)}")
                for f in sorted(modified_files):
                    print(f"      ~ {f}")
            if deleted_files:
                print(f"   🗑️  Deleted files: {len(deleted_files)}")
                for f in sorted(deleted_files):
                    print(f"      - {f}")
        else:
            print("\n✓ No changes detected - ChromaDB is up to date")
        
        return has_changes
    
    def perform_smart_update(self):
        """Perform smart update: only process new/modified files."""
        print("\n🔄 Starting Smart Update...")
        
        # Get or create collection
        try:
            collection = chroma_client.get_collection(
                name=self.collection_name,
                embedding_function=embedding_function
            )
            print(f"✅ Using existing collection: {self.collection_name}")
        except:
            collection = chroma_client.create_collection(
                name=self.collection_name,
                embedding_function=embedding_function
            )
            print(f"📚 Created new collection: {self.collection_name}")
        
        # Detect changes
        new_files, modified_files, deleted_files = self.detect_changes()
        current_files = self.scan_data_folder()
        
        # Get existing document IDs for cleanup
        existing_ids = set(collection.get()['ids'])
        
        # Process deletions
        deleted_chunks = 0
        for deleted_file in deleted_files:
            # Find and delete chunks from this file
            file_prefix = current_files.get(deleted_file, {}).get('filename', deleted_file)
            ids_to_delete = [id for id in existing_ids if id.startswith(file_prefix)]
            
            if ids_to_delete:
                collection.delete(ids=ids_to_delete)
                deleted_chunks += len(ids_to_delete)
                print(f"   🗑️  Deleted {len(ids_to_delete)} chunks from {deleted_file}")
        
        # Process new and modified files
        files_to_process = new_files | modified_files
        new_documents = []
        updated_count = 0
        
        for rel_path in files_to_process:
            file_info = current_files[rel_path]
            file_path = file_info['full_path']
            filename = file_info['filename']
            category = file_info['category']
            file_hash = file_info['hash']
            
            try:
                # Read file content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # If modified, delete old chunks first
                if rel_path in modified_files:
                    old_ids = [id for id in existing_ids if id.startswith(filename)]
                    if old_ids:
                        collection.delete(ids=old_ids)
                        print(f"   ♻️  Removed {len(old_ids)} old chunks from {filename}")
                
                # Split into chunks
                chunks = self.split_into_chunks(content, max_length=1000)
                
                # Create new chunks
                for i, chunk in enumerate(chunks):
                    chunk_id = f"{filename}_{i}_{file_hash[:8]}"
                    
                    new_documents.append({
                        'content': chunk,
                        'source': filename,
                        'chunk_id': chunk_id,
                        'category': category,
                        'file_hash': file_hash,
                        'file_path': rel_path
                    })
                    updated_count += 1
                
                status = "📄 NEW" if rel_path in new_files else "✏️  MOD"
                print(f"   {status} {filename} ({len(chunks)} chunks)")
                
            except Exception as e:
                print(f"   ✗ Error processing {file_path}: {e}")
        
        # Add new documents to ChromaDB
        if new_documents:
            print(f"\n📝 Adding {len(new_documents)} chunks to ChromaDB...")
            
            collection.add(
                documents=[doc['content'] for doc in new_documents],
                metadatas=[{
                    'source': doc['source'], 
                    'category': doc['category'],
                    'chunk_id': doc['chunk_id'],
                    'file_hash': doc['file_hash'],
                    'file_path': doc['file_path']
                } for doc in new_documents],
                ids=[doc['chunk_id'] for doc in new_documents]
            )
            print(f"✅ Successfully added {len(new_documents)} chunks")
        
        # Update state
        self.state["file_hashes"] = {
            path: {'hash': info['hash'], 'category': info['category']}
            for path, info in current_files.items()
        }
        self.state["total_chunks"] = len(collection.get()['ids'])
        self.save_state()
        
        # Print summary
        total_docs = len(collection.get()['ids'])
        print(f"\n📊 Update Summary:")
        print(f"   • Total chunks in ChromaDB: {total_docs}")
        print(f"   • New/modified chunks added: {updated_count}")
        print(f"   • Deleted chunks removed: {deleted_chunks}")
        print(f"   • Files processed: {len(files_to_process)}")
        print(f"   • Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return updated_count > 0 or deleted_chunks > 0
    
    def list_current_state(self):
        """Display current ChromaDB state."""
        try:
            collection = chroma_client.get_collection(self.collection_name)
            results = collection.get()
            
            print(f"\n📚 Current ChromaDB State:")
            print(f"   Collection: {self.collection_name}")
            print(f"   Total chunks: {len(results['ids'])}")
            
            # Group by source file
            sources = {}
            for metadata in results['metadatas']:
                category = metadata.get('category', 'unknown')
                source = metadata.get('source', 'unknown')
                key = f"{category}/{source}"
                sources[key] = sources.get(key, 0) + 1
            
            print(f"\n   Files by category:")
            for source, count in sorted(sources.items()):
                print(f"      • {source}: {count} chunks")
            
            # Show last update info
            if self.state.get("last_update"):
                print(f"\n   Last update: {self.state['last_update']}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            print("   ChromaDB collection may not exist yet.")

def main():
    """Main CLI for update agent."""
    import sys
    
    agent = UpdateAgent()
    
    if len(sys.argv) < 2:
        print("""
🤖 AI Mental Health Agent - Smart Update Agent

This agent monitors the data/knowledge/ folder and intelligently updates ChromaDB
when new or modified files are detected.

Usage:
    python update_agent.py [command]

Commands:
    check           Check for new/modified data (no updates)
    update          Perform smart update if changes detected
    force           Force update all files (recreate)
    status          Show current ChromaDB state
    auto            Auto-update if changes detected (recommended)

Examples:
    python update_agent.py check     # Just check for changes
    python update_agent.py auto      # Update if needed (smart)
    python update_agent.py status    # View current state
        """)
        return
    
    command = sys.argv[1].lower()
    
    if command == "check":
        print("🔍 Checking for changes in data/knowledge/ folder...")
        has_changes = agent.check_for_updates()
        if has_changes:
            print("\n💡 Tip: Run 'python update_agent.py update' to apply changes")
        
    elif command == "update":
        agent.perform_smart_update()
        
    elif command == "auto":
        print("🤖 Auto-Update Agent Running...")
        has_changes = agent.check_for_updates()
        if has_changes:
            agent.perform_smart_update()
        else:
            print("✓ No updates needed")
        
    elif command == "force":
        print("🔄 Force Update: Recreating collection...")
        confirm = input("⚠️  This will recreate the entire collection. Continue? (yes/no): ")
        if confirm.lower() == 'yes':
            try:
                chroma_client.delete_collection(name=agent.collection_name)
                print("🗑️  Deleted existing collection")
            except:
                pass
            agent.state = {"file_hashes": {}, "last_update": None, "total_chunks": 0}
            agent.perform_smart_update()
        else:
            print("❌ Cancelled")
            
    elif command == "status":
        agent.list_current_state()
        
    else:
        print(f"❌ Unknown command: {command}")
        print("Use: check, update, auto, force, or status")

if __name__ == "__main__":
    main()
