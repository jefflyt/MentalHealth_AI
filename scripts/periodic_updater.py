"""
Periodic Knowledge Update Script
Automatically updates the knowledge base from web sources on a schedule
"""

import os
import sys
import time
import schedule
from datetime import datetime
from web_scraper import MentalHealthWebScraper
from agent.update_agent import UpdateAgent

class PeriodicUpdater:
    """Manage periodic updates of the knowledge base."""
    
    def __init__(self):
        self.scraper = MentalHealthWebScraper()
        self.update_agent = UpdateAgent()
        self.log_file = "data/update_log.txt"
        
        # Ensure data directory exists for log file
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
    
    def log(self, message):
        """Log update activities."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        
        # Append to log file
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')
    
    def run_web_scraping(self):
        """Run web scraping to fetch latest content."""
        self.log("🌐 Starting web scraping...")
        
        try:
            # Scrape from trusted sources
            files = self.scraper.scrape_all()
            
            if files:
                self.log(f"✅ Scraped {len(files)} files from web sources")
            else:
                self.log("⚠️  No new files scraped (might be blocked or network issue)")
            
            return len(files)
            
        except Exception as e:
            self.log(f"❌ Web scraping error: {e}")
            return 0
    
    def run_knowledge_update(self):
        """Update ChromaDB with new knowledge."""
        self.log("🔄 Checking for knowledge base updates...")
        
        try:
            # Check if there are changes
            has_changes = self.update_agent.check_for_updates()
            
            if has_changes:
                self.log("📝 Changes detected, updating ChromaDB...")
                self.update_agent.perform_smart_update()
                self.log("✅ Knowledge base updated successfully")
                return True
            else:
                self.log("ℹ️  No changes detected, knowledge base is up to date")
                return False
                
        except Exception as e:
            self.log(f"❌ Knowledge update error: {e}")
            return False
    
    def full_update_cycle(self):
        """Run a complete update cycle: scrape + update knowledge base."""
        self.log("\n" + "="*60)
        self.log("🔄 Starting periodic update cycle")
        self.log("="*60)
        
        # Step 1: Web scraping
        scraped_count = self.run_web_scraping()
        
        # Step 2: Update knowledge base
        updated = self.run_knowledge_update()
        
        # Summary
        self.log("="*60)
        if scraped_count > 0 or updated:
            self.log(f"✅ Update cycle complete! Scraped: {scraped_count}, Updated: {updated}")
        else:
            self.log("ℹ️  Update cycle complete (no changes)")
        self.log("="*60 + "\n")
    
    def schedule_updates(self, frequency='weekly'):
        """Schedule automatic updates."""
        self.log(f"⏰ Scheduling {frequency} updates")
        
        if frequency == 'daily':
            # Run every day at 2 AM
            schedule.every().day.at("02:00").do(self.full_update_cycle)
            self.log("   Daily updates scheduled for 2:00 AM")
            
        elif frequency == 'weekly':
            # Run every Sunday at 2 AM
            schedule.every().sunday.at("02:00").do(self.full_update_cycle)
            self.log("   Weekly updates scheduled for Sunday 2:00 AM")
            
        elif frequency == 'monthly':
            # Run on the 1st of each month at 2 AM
            # Note: This is a simplified version, check if it's the 1st each day
            def monthly_check():
                if datetime.now().day == 1:
                    self.full_update_cycle()
            
            schedule.every().day.at("02:00").do(monthly_check)
            self.log("   Monthly updates scheduled for 1st of month at 2:00 AM")
        
        else:
            self.log(f"❌ Unknown frequency: {frequency}")
            return
        
        # Start the scheduler
        self.log("✅ Scheduler started. Press Ctrl+C to stop.")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            self.log("\n⏹️  Scheduler stopped by user")


def run_manual_update():
    """Run a manual update immediately."""
    updater = PeriodicUpdater()
    updater.full_update_cycle()


def run_scheduled_updates(frequency='weekly'):
    """Start scheduled automatic updates."""
    updater = PeriodicUpdater()
    updater.schedule_updates(frequency)


def main():
    """Main entry point with command-line options."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Update mental health knowledge base from web sources'
    )
    parser.add_argument(
        'mode',
        choices=['manual', 'schedule'],
        help='Run mode: manual (one-time) or schedule (periodic)'
    )
    parser.add_argument(
        '--frequency',
        choices=['daily', 'weekly', 'monthly'],
        default='weekly',
        help='Update frequency for scheduled mode (default: weekly)'
    )
    
    args = parser.parse_args()
    
    print("""
╔════════════════════════════════════════════════════════════╗
║     Mental Health AI - Knowledge Base Update Tool         ║
╚════════════════════════════════════════════════════════════╝
""")
    
    if args.mode == 'manual':
        print("🔄 Running manual update...")
        run_manual_update()
    else:
        print(f"⏰ Starting scheduled updates ({args.frequency})...")
        run_scheduled_updates(args.frequency)


if __name__ == "__main__":
    # If no arguments, run manual update
    if len(sys.argv) == 1:
        print("No mode specified. Running manual update...")
        run_manual_update()
    else:
        main()
