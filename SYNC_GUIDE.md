# Brewery Database Sync Guide

This guide explains how to sync the local brewery database with the official Open Brewery DB API.

## Quick Start

### Dry Run (Recommended First)
```bash
python3 sync_breweries.py --dry-run
```

This shows what would change without making any actual changes.

### Live Sync
```bash
python3 sync_breweries.py
```

This will:
1. Create a backup of your current database
2. Fetch latest data from Open Brewery DB API
3. Add new breweries
4. Update existing breweries
5. Generate a sync report

## Options

```bash
python3 sync_breweries.py [OPTIONS]

Options:
  --dry-run       Show what would change without making changes
  --no-backup     Skip backup creation (not recommended)
  --verbose, -v   Show detailed output during sync
  --help, -h      Show help message
```

## Examples

### Preview Changes
```bash
# See what would change
python3 sync_breweries.py --dry-run

# See detailed changes
python3 sync_breweries.py --dry-run --verbose
```

### Sync with Backup (Recommended)
```bash
# Normal sync with automatic backup
python3 sync_breweries.py

# Sync with verbose output
python3 sync_breweries.py --verbose
```

### Sync Without Backup (Not Recommended)
```bash
python3 sync_breweries.py --no-backup
```

## What Gets Synced

The sync script will:

### ✅ Add New Breweries
- New breweries from the official API are added
- Each gets a unique ID assigned by the official API

### ✅ Update Existing Breweries
- Existing breweries are updated if data changed
- Updates include: address, phone, website, coordinates, etc.

### ✅ Preserve Local-Only Breweries
- Student submissions not yet in official API are kept
- These are breweries unique to your database

### ❌ Does NOT Delete
- The script never deletes breweries
- Local-only entries are preserved

## Output Files

### Backups
```
backups/
├── breweries_backup_20251122_073000.json
├── breweries_backup_20251122_074500.json
└── ...
```

### Sync Reports
```
sync_report_20251122_073000.txt
sync_report_20251122_074500.txt
...
```

## Sync Report Explanation

```
BREWERY DATABASE SYNC REPORT
============================================================
Date: 2025-11-22 07:30:00
Mode: LIVE SYNC

STATISTICS:
  🆕 New breweries added:     116    ← Breweries added from official API
  📝 Existing breweries updated: 211 ← Breweries with data changes
  ✓  Breweries unchanged:    8614   ← Breweries with no changes
  🔍 Local-only breweries:   3      ← Student submissions

LOCAL-ONLY BREWERIES (Student Submissions):
  - Example Brewery (Champaign, Illinois)
  - Another Brewery (Urbana, Illinois)
  ...
```

## When to Sync

### Regular Schedule
- **Weekly**: During active semesters when students submit breweries
- **Monthly**: During breaks to catch official API updates
- **Before Major Events**: Before showcasing the API

### After Student Submissions
After approving student brewery submissions:
1. Add to local database (via GitHub Actions)
2. Wait a few weeks
3. Sync with official API to get other updates

### After Official API Updates
When the Open Brewery DB announces major updates:
1. Run `--dry-run` first
2. Review the report
3. Run live sync

## Troubleshooting

### API Rate Limiting
If you see 429 errors (Too Many Requests):
```bash
# The script has built-in retry logic
# Just wait a few minutes and try again
```

### Network Errors
If you see connection errors:
```bash
# The script retries with exponential backoff
# Check your internet connection
# Try again in a few minutes
```

### Sync Interrupted
If sync is interrupted (Ctrl+C):
- Your original database is safe (backup created first)
- Run the sync again - it will start fresh
- Review the backup files if needed

### Restore from Backup
```bash
# If something goes wrong, restore from backup:
cp backups/breweries_backup_20251122_073000.json breweries.json
```

## Advanced Usage

### Check What Changed
```bash
# Run dry-run and save output
python3 sync_breweries.py --dry-run > preview.txt

# Review changes
less preview.txt
```

### Automated Sync (Cron Job)
```bash
# Add to crontab for weekly sync every Sunday at 2 AM
0 2 * * 0 cd /opt/badm554-api && python3 sync_breweries.py >> sync.log 2>&1
```

### Compare with Official API
```bash
# Get current count
cat breweries.json | python3 -c "import json, sys; print(len(json.load(sys.stdin)))"

# Get official count
curl -s "https://api.openbrewerydb.org/v1/breweries/meta" | python3 -c "import json, sys; print(json.load(sys.stdin)['total'])"
```

## Data Quality

### What Gets Updated
- ✅ Name corrections
- ✅ Address updates
- ✅ Phone number changes
- ✅ Website URL updates
- ✅ GPS coordinates corrections
- ✅ Brewery type changes
- ✅ Status changes (closed, planning, etc.)

### What Doesn't Change
- ❌ Brewery IDs (UUIDs)
- ❌ Local-only submissions

## Integration with GitHub Actions

The sync script works alongside your GitHub Actions workflows:

1. **Student submits** brewery via GitHub issue
2. **Auto-validate** workflow checks submission
3. **Instructor approves** (adds "approved" label)
4. **Auto-deploy** workflow adds to local database
5. **Periodic sync** updates from official API

## Best Practices

### Before Syncing
1. ✅ Always run `--dry-run` first
2. ✅ Review the sync report
3. ✅ Ensure backups are enabled
4. ✅ Test API endpoint after sync

### After Syncing
1. ✅ Review sync report
2. ✅ Check brewery count
3. ✅ Test API queries
4. ✅ Deploy to production (if needed)

### For Production
```bash
# Recommended production sync workflow:

# 1. Dry run first
python3 sync_breweries.py --dry-run > /tmp/sync_preview.txt

# 2. Review changes
less /tmp/sync_preview.txt

# 3. If looks good, run live sync
python3 sync_breweries.py

# 4. Test API
curl http://localhost:8000/breweries/meta

# 5. Deploy to production
./deploy.sh 178.156.206.171
```

## Monitoring

### Check Sync History
```bash
# View all sync reports
ls -lt sync_report_*.txt | head -10

# View latest report
cat $(ls -t sync_report_*.txt | head -1)
```

### Check Backups
```bash
# List all backups
ls -lh backups/

# Check backup size
du -sh backups/
```

## Schema Notes

The official Open Brewery DB API returns data with extra fields (`state` and `street`). The sync script automatically normalizes these to match our schema:

**Official API Schema:**
- `state` (duplicate of `state_province`)
- `street` (duplicate of `address_1`)

**Our Schema:**
- `state_province`
- `address_1`, `address_2`, `address_3`

The sync script removes `state` and `street` during sync to maintain consistency.

## Resources

- **Official API**: https://www.openbrewerydb.org/
- **API Docs**: https://www.openbrewerydb.org/documentation
- **GitHub Repo**: https://github.com/openbrewerydb/openbrewerydb

---

**Questions?** Check the main [CLAUDE.md](CLAUDE.md) or [UPSTREAM_SYNC.md](UPSTREAM_SYNC.md) documentation.
