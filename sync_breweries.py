#!/usr/bin/env python3
"""
Brewery Database Sync Script

Syncs the local brewery database with the official Open Brewery DB API.
This script will:
1. Fetch the latest data from the official API
2. Compare with the local database
3. Add new breweries
4. Update existing breweries with new information
5. Generate a detailed sync report

Usage:
    python3 sync_breweries.py [--dry-run] [--backup] [--verbose]

Options:
    --dry-run    Show what would be changed without making changes
    --backup     Create a backup before syncing (default: True)
    --verbose    Show detailed output
    --no-backup  Skip backup creation
"""

import json
import requests
import time
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Set
import shutil


class BrewerySync:
    """Handles syncing brewery data with official Open Brewery DB API."""

    API_BASE_URL = "https://api.openbrewerydb.org/v1"
    LOCAL_DB_FILE = "breweries.json"
    BACKUP_DIR = "backups"

    def __init__(self, dry_run: bool = False, backup: bool = True, verbose: bool = False):
        self.dry_run = dry_run
        self.backup = backup
        self.verbose = verbose
        self.stats = {
            'new_breweries': 0,
            'updated_breweries': 0,
            'unchanged_breweries': 0,
            'local_only_breweries': 0,
            'errors': []
        }

    def log(self, message: str, level: str = 'INFO'):
        """Print log message."""
        if level == 'VERBOSE' and not self.verbose:
            return
        prefix = {
            'INFO': 'ℹ️ ',
            'SUCCESS': '✅',
            'WARNING': '⚠️ ',
            'ERROR': '❌',
            'VERBOSE': '  '
        }.get(level, '')
        print(f"{prefix} {message}")

    def fetch_official_data(self) -> List[Dict]:
        """Fetch all brewery data from official API."""
        self.log("Fetching data from Open Brewery DB API...")

        all_breweries = []
        per_page = 200
        page = 1
        max_retries = 5

        while True:
            url = f"{self.API_BASE_URL}/breweries?per_page={per_page}&page={page}"

            # Retry logic with exponential backoff
            for attempt in range(max_retries):
                try:
                    self.log(f"Fetching page {page} (attempt {attempt + 1}/{max_retries})...", 'VERBOSE')
                    response = requests.get(url, timeout=15)
                    response.raise_for_status()
                    breweries = response.json()

                    if not breweries:
                        self.log("Reached end of data", 'VERBOSE')
                        return all_breweries

                    all_breweries.extend(breweries)
                    self.log(f"Page {page}: Got {len(breweries)} breweries (total: {len(all_breweries)})", 'VERBOSE')

                    if len(breweries) < per_page:
                        self.log(f"Received partial page - all data fetched", 'VERBOSE')
                        return all_breweries

                    page += 1
                    time.sleep(1)  # Be nice to the API
                    break  # Success, move to next page

                except requests.exceptions.HTTPError as e:
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt
                        self.log(f"HTTP Error {e.response.status_code}, retrying in {wait_time}s...", 'WARNING')
                        time.sleep(wait_time)
                    else:
                        self.log(f"Failed to fetch page {page} after {max_retries} attempts", 'ERROR')
                        self.stats['errors'].append(f"Failed to fetch page {page}")
                        return all_breweries

                except Exception as e:
                    self.log(f"Error fetching data: {e}", 'ERROR')
                    self.stats['errors'].append(f"Error on page {page}: {str(e)}")
                    if attempt == max_retries - 1:
                        return all_breweries

        return all_breweries

    def load_local_data(self) -> List[Dict]:
        """Load local brewery database."""
        self.log(f"Loading local database: {self.LOCAL_DB_FILE}")
        try:
            with open(self.LOCAL_DB_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.log(f"Local database not found: {self.LOCAL_DB_FILE}", 'ERROR')
            return []
        except json.JSONDecodeError as e:
            self.log(f"Invalid JSON in local database: {e}", 'ERROR')
            return []

    def create_backup(self):
        """Create backup of current database."""
        if not self.backup:
            return

        self.log("Creating backup...")
        backup_dir = Path(self.BACKUP_DIR)
        backup_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = backup_dir / f"breweries_backup_{timestamp}.json"

        try:
            shutil.copy2(self.LOCAL_DB_FILE, backup_file)
            self.log(f"Backup created: {backup_file}", 'SUCCESS')
        except Exception as e:
            self.log(f"Failed to create backup: {e}", 'ERROR')
            raise

    def normalize_brewery(self, brewery: Dict) -> Dict:
        """
        Normalize brewery data to our schema.
        Removes 'state' and 'street' fields from official API data.
        """
        normalized = brewery.copy()
        # Remove extra fields from official API
        normalized.pop('state', None)
        normalized.pop('street', None)
        return normalized

    def compare_breweries(self, current: List[Dict], official: List[Dict]) -> Tuple[List[Dict], List[Dict], Set[str]]:
        """
        Compare current and official brewery lists.
        Returns: (new_breweries, updated_breweries, local_only_ids)
        """
        self.log("Comparing databases...")

        current_dict = {b['id']: b for b in current}
        official_dict = {b['id']: self.normalize_brewery(b) for b in official}

        current_ids = set(current_dict.keys())
        official_ids = set(official_dict.keys())

        # Find new breweries
        new_ids = official_ids - current_ids
        new_breweries = [official_dict[bid] for bid in new_ids]

        # Find updated breweries
        updated_breweries = []
        common_ids = current_ids & official_ids

        for brew_id in common_ids:
            if current_dict[brew_id] != official_dict[brew_id]:
                updated_breweries.append(official_dict[brew_id])

        # Find local-only breweries (not in official API)
        local_only_ids = current_ids - official_ids

        return new_breweries, updated_breweries, local_only_ids

    def merge_data(self, current: List[Dict], new_breweries: List[Dict], updated_breweries: List[Dict]) -> List[Dict]:
        """Merge new and updated breweries into current database."""
        self.log("Merging data...")

        # Create dict for faster lookup
        merged_dict = {b['id']: b for b in current}

        # Add new breweries
        for brewery in new_breweries:
            merged_dict[brewery['id']] = brewery
            self.stats['new_breweries'] += 1
            self.log(f"NEW: {brewery['name']} ({brewery['city']}, {brewery['state_province']})", 'VERBOSE')

        # Update existing breweries
        for brewery in updated_breweries:
            if merged_dict[brewery['id']] != brewery:
                merged_dict[brewery['id']] = brewery
                self.stats['updated_breweries'] += 1
                self.log(f"UPDATE: {brewery['name']} ({brewery['city']}, {brewery['state_province']})", 'VERBOSE')
            else:
                self.stats['unchanged_breweries'] += 1

        # Convert back to list and sort by name
        merged_list = list(merged_dict.values())
        merged_list.sort(key=lambda x: (x['name'].lower(), x['city'].lower()))

        return merged_list

    def save_data(self, data: List[Dict]):
        """Save merged data to local database."""
        if self.dry_run:
            self.log("DRY RUN - Not saving changes", 'WARNING')
            return

        self.log(f"Saving {len(data)} breweries to {self.LOCAL_DB_FILE}...")
        try:
            with open(self.LOCAL_DB_FILE, 'w') as f:
                json.dump(data, f, indent=2)
            self.log("Database saved successfully", 'SUCCESS')
        except Exception as e:
            self.log(f"Failed to save database: {e}", 'ERROR')
            raise

    def generate_report(self, local_only_ids: Set[str], current: List[Dict]) -> str:
        """Generate sync report."""
        report = []
        report.append("\n" + "=" * 60)
        report.append("BREWERY DATABASE SYNC REPORT")
        report.append("=" * 60)
        report.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE SYNC'}")
        report.append("")
        report.append("STATISTICS:")
        report.append(f"  🆕 New breweries added:     {self.stats['new_breweries']}")
        report.append(f"  📝 Existing breweries updated: {self.stats['updated_breweries']}")
        report.append(f"  ✓  Breweries unchanged:    {self.stats['unchanged_breweries']}")
        report.append(f"  🔍 Local-only breweries:   {len(local_only_ids)}")

        if self.stats['errors']:
            report.append(f"  ❌ Errors encountered:     {len(self.stats['errors'])}")

        # Show local-only breweries (student submissions not yet in official API)
        if local_only_ids:
            report.append("\nLOCAL-ONLY BREWERIES (Student Submissions):")
            current_dict = {b['id']: b for b in current}
            for brew_id in sorted(local_only_ids)[:10]:
                brewery = current_dict[brew_id]
                report.append(f"  - {brewery['name']} ({brewery['city']}, {brewery['state_province']})")
            if len(local_only_ids) > 10:
                report.append(f"  ... and {len(local_only_ids) - 10} more")

        if self.stats['errors']:
            report.append("\nERRORS:")
            for error in self.stats['errors']:
                report.append(f"  - {error}")

        report.append("=" * 60)
        return "\n".join(report)

    def sync(self):
        """Main sync process."""
        self.log("Starting brewery database sync...")
        self.log("")

        # Load local data
        current_data = self.load_local_data()
        if not current_data:
            self.log("No local data to sync", 'ERROR')
            return False

        self.log(f"Current database: {len(current_data)} breweries")

        # Fetch official data
        official_data = self.fetch_official_data()
        if not official_data:
            self.log("Failed to fetch official data", 'ERROR')
            return False

        self.log(f"Official API: {len(official_data)} breweries")
        self.log("")

        # Compare data
        new_breweries, updated_breweries, local_only_ids = self.compare_breweries(current_data, official_data)
        self.stats['local_only_breweries'] = len(local_only_ids)

        self.log(f"Found {len(new_breweries)} new breweries")
        self.log(f"Found {len(updated_breweries)} breweries with updates")
        self.log(f"Found {len(local_only_ids)} local-only breweries (student submissions)")
        self.log("")

        # Create backup before making changes
        if not self.dry_run and (new_breweries or updated_breweries):
            self.create_backup()

        # Merge data
        merged_data = self.merge_data(current_data, new_breweries, updated_breweries)

        # Save data
        self.save_data(merged_data)

        # Generate and print report
        report = self.generate_report(local_only_ids, current_data)
        print(report)

        # Save report to file
        report_file = f"sync_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w') as f:
            f.write(report)
        self.log(f"\nReport saved to: {report_file}")

        return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Sync local brewery database with Open Brewery DB API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would change without making changes')
    parser.add_argument('--no-backup', action='store_true',
                        help='Skip backup creation')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show detailed output')

    args = parser.parse_args()

    syncer = BrewerySync(
        dry_run=args.dry_run,
        backup=not args.no_backup,
        verbose=args.verbose
    )

    try:
        success = syncer.sync()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Sync interrupted by user")
        exit(130)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        exit(1)


if __name__ == '__main__':
    main()
