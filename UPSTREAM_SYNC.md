# Upstream Sync Workflow

This document explains how to sync student contributions with the official Open Brewery DB repository.

## Overview

```
Student Submissions → Review & Approve → Update Local DB → Deploy API → Submit to Upstream
```

## Step 1: Collect Approved Student Submissions

### Review Process

1. Students submit issues using templates
2. You review for:
   - Data completeness
   - Verification/sources provided
   - No duplicates
   - Correct formatting

3. Label approved issues: `approved` + `ready-for-upstream`

### Generate Contribution List

Run this to extract all approved submissions:

```bash
# List all approved brewery additions
gh issue list --label "approved,brewery-addition" --json number,title,body

# Or manually review closed issues with "approved" label
```

## Step 2: Update Local Database

### Add New Brewery

```python
import json
import uuid

# Load current data
with open('breweries.json', 'r') as f:
    breweries = json.load(f)

# Add new brewery (from student submission)
new_brewery = {
    "id": str(uuid.uuid4()),
    "name": "Example Brewery",
    "brewery_type": "micro",
    "address_1": "123 Main St",
    "address_2": None,
    "address_3": None,
    "city": "Champaign",
    "state_province": "Illinois",
    "postal_code": "61820",
    "country": "United States",
    "phone": "2175551234",
    "website_url": "https://example.com",
    "longitude": -88.2434,
    "latitude": 40.1164
}

breweries.append(new_brewery)

# Save updated data
with open('breweries.json', 'w') as f:
    json.dump(breweries, f, indent=2)
```

### Update Existing Brewery

```python
import json

with open('breweries.json', 'r') as f:
    breweries = json.load(f)

# Find and update brewery
for brewery in breweries:
    if brewery['id'] == 'BREWERY_ID_HERE':
        brewery['phone'] = '2175555678'  # Example update
        brewery['website_url'] = 'https://newsite.com'
        break

with open('breweries.json', 'w') as f:
    json.dump(breweries, f, indent=2)
```

## Step 3: Deploy to API

```bash
# Test locally first
uvicorn main:app --reload

# Test the changes
curl http://localhost:8000/breweries/search?query=newbrewery

# Deploy to Hetzner
./deploy.sh 178.156.206.171

# Verify deployment
curl http://178.156.206.171:8000/breweries/search?query=newbrewery
```

## Step 4: Submit to Open Brewery DB

### Fork & Clone Official Repo

```bash
# Fork the repo on GitHub first
# https://github.com/openbrewerydb/openbrewerydb

# Clone your fork
git clone https://github.com/YOUR_USERNAME/openbrewerydb.git
cd openbrewerydb
```

### Add Breweries to CSV

The official repo uses CSV format, not JSON. Add to `data/breweries.csv`:

```csv
obdb_id,name,brewery_type,street,city,state,postal_code,country,phone,website_url,longitude,latitude
NEW_UUID,Example Brewery,micro,123 Main St,Champaign,Illinois,61820,United States,2175551234,https://example.com,-88.2434,40.1164
```

**Important:** Follow their CSV format exactly. Fields in order:
- `obdb_id` - Use UUID v4
- `name`
- `brewery_type`
- `street` - Combines address_1, address_2, address_3
- `city`
- `state` - Full state name (not abbreviation)
- `postal_code`
- `country`
- `phone`
- `website_url`
- `longitude`
- `latitude`

### Create Pull Request

```bash
# Create branch for your changes
git checkout -b badm554-contributions-2025

# Add your changes
git add data/breweries.csv

# Commit with descriptive message
git commit -m "Add breweries from BADM 554 student research

- Added: Example Brewery (Champaign, IL)
- Added: Another Brewery (Urbana, IL)
- Updated: Third Brewery (phone number correction)

Verified by students in BADM 554 course at University of Illinois."

# Push to your fork
git push origin badm554-contributions-2025
```

### Submit PR on GitHub

1. Go to official repo: https://github.com/openbrewerydb/openbrewerydb
2. Click "New Pull Request"
3. Select your fork and branch
4. Title: "Add/Update breweries from BADM 554 student research"
5. Description:

```markdown
## Summary
This PR adds [X] new breweries and updates [Y] existing entries based on research conducted by students in BADM 554 at the University of Illinois.

## Breweries Added
- Example Brewery (Champaign, IL) - [verification source]
- Another Brewery (Urbana, IL) - [verification source]

## Breweries Updated
- Third Brewery - Updated phone number - [verification source]

## Verification
All entries were verified by students through:
- Official brewery websites
- Phone calls
- In-person visits
- Google Maps verification

## Additional Notes
These contributions are part of a class project where students learn about open data and API usage. All submissions were reviewed and approved by the course instructor.
```

6. Submit the PR
7. Respond to any feedback from maintainers

## Step 5: Track Contributions

### Create a Contributions Log

Create `STUDENT_CONTRIBUTIONS.md`:

```markdown
# Student Contributions

## Spring 2025

### Approved and Submitted to Upstream
- [ ] Example Brewery (Champaign, IL) - Submitted PR #123 - Student: John Doe
- [ ] Another Brewery (Urbana, IL) - Submitted PR #123 - Student: Jane Smith

### Approved - Pending Upstream Submission
- [ ] Third Brewery (Mahomet, IL) - Student: Bob Johnson

### Under Review
- [ ] Fourth Brewery (Savoy, IL) - Issue #5 - Student: Alice Williams
```

## Batch Submissions

Consider batching student contributions:
- **Weekly batches**: Review and approve issues weekly
- **Semester-end batch**: Submit all approved entries at end of term
- **Monthly updates**: Regular monthly submissions to upstream

## Verification Standards for Upstream

Before submitting to Open Brewery DB, ensure:
- ✅ Brewery exists (verified via website, phone, or visit)
- ✅ Address is complete and accurate
- ✅ GPS coordinates are correct (use Google Maps)
- ✅ Phone number is current
- ✅ Website URL is active
- ✅ Brewery type is appropriate
- ✅ No duplicate entries

## Handling Rejections

If upstream PR is rejected:
1. Review maintainer feedback
2. Make requested corrections
3. Update local database accordingly
4. Notify student (if applicable)
5. Resubmit if appropriate

## Communication Template

When notifying students their contribution was accepted:

```
Hi [Student Name],

Great news! Your brewery submission for [Brewery Name] has been:
✅ Approved and added to our BADM 554 API
✅ Submitted to the official Open Brewery DB (PR #XXX)

Your contribution is now helping thousands of developers and beer enthusiasts worldwide access accurate brewery data!

You can see your brewery live at:
- Our API: http://178.156.206.171:8000/breweries/search?query=[brewery]
- Track upstream PR: https://github.com/openbrewerydb/openbrewerydb/pull/XXX

Thank you for contributing to open data!
```

## Automation Ideas (Future)

Consider automating:
- Issue → JSON conversion
- JSON → CSV conversion for upstream
- Automatic PR generation
- Contribution tracking dashboard

## Resources

- **Official Repo**: https://github.com/openbrewerydb/openbrewerydb
- **Contributing Guide**: https://github.com/openbrewerydb/openbrewerydb/blob/master/CONTRIBUTING.md
- **CSV Format**: Check `data/breweries.csv` for examples
- **Community**: https://discord.gg/SHtpdEN

---

**Remember:** Quality over quantity. Better to submit 5 well-verified entries than 20 questionable ones.
