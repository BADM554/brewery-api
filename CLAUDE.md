# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**BADM 554 Brewery API** - Student-managed brewery database with automated GitHub Actions workflows for validation and deployment. Students submit breweries via GitHub issues, Claude validates submissions, instructor approves, and changes auto-deploy to production VPS.

**Live API:** http://178.156.206.171:8000 (Hetzner VPS)
**Dataset:** 8,925+ breweries in JSON format (~3.2 MB)

## Architecture

### Two-Stage Automation Pipeline

```
Student Submission (GitHub Issue)
    ↓
Auto-Validate Workflow (Claude 3.5 Haiku validates)
    ↓
Manual Review (Instructor adds "approved" label)
    ↓
Auto-Deploy Workflow (Claude extracts → commits → deploys to VPS)
    ↓
Production API Updated
```

### Critical Design Pattern: Claude GitHub Actions Permissions Workaround

**Problem:** Claude Code Action cannot directly post comments or add labels to GitHub issues due to permission restrictions (even with `additional_permissions` configured).

**Solution:** Two-step approach:
1. **Claude validates** and returns structured JSON (no permissions needed)
2. **GitHub Actions script** posts comments and adds labels (native permissions)

This pattern is implemented in `.github/workflows/auto-validate-brewery.yml`:
- Step 1: Claude validates submission → returns `{"valid": true/false, "message": "..."}`
- Step 2: `actions/github-script` reads Claude's response → posts comment → adds label

**Do NOT attempt to have Claude directly use `gh` commands or GitHub API calls.** This will fail with permission errors.

## Local Development

### Run API Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload --port 8000

# Access at http://localhost:8000/docs
```

### Docker Development
```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Test API Endpoints
```bash
# Health check
curl http://localhost:8000/health

# Search breweries
curl "http://localhost:8000/breweries/search?query=dog"

# Get by city
curl "http://localhost:8000/breweries?by_city=Champaign&per_page=10"
```

## GitHub Actions Workflows

### Auto-Validate Workflow (`.github/workflows/auto-validate-brewery.yml`)

**Triggers:** Issue opened/edited with labels `brewery-addition`, `brewery-update`, or `brewery-closed`

**Process:**
1. Claude (Haiku model) validates submission data
2. Returns JSON: `{"valid": true/false, "message": "..."}`
3. GitHub Actions script posts validation comment
4. Adds label: `validated` (if valid) or `needs-revision` (if invalid)

**Cost:** ~$0.03 per validation (using Haiku vs $0.30 with Sonnet)

**Important:** Validation always defaults to valid due to hardcoded logic in lines 58-59. This is intentional for student experience.

### Auto-Deploy Workflow (`.github/workflows/auto-deploy-brewery.yml`)

**Triggers:** Issue labeled with `approved`

**Process:**
1. Claude extracts brewery data from issue body
2. Generates UUID v4 for new brewery ID
3. Checks for duplicates in `breweries.json`
4. Adds new brewery to JSON array
5. Commits changes with message: `"Add brewery from issue #N: [name]"`
6. Pushes to GitHub
7. SSH to VPS → `git pull` → `docker-compose up -d --build`
8. Posts success comment with API search link
9. Closes issue

**VPS Deployment Path:** `/opt/badm554-api`

**Required Secrets:**
- `ANTHROPIC_API_KEY` - Claude API authentication
- `VPS_HOST` - VPS IP address (178.156.206.171)
- `VPS_USERNAME` - SSH user (root)
- `VPS_SSH_KEY` - SSH private key for deployment

## Data Structure

### breweries.json Format
```json
{
  "id": "uuid-v4",
  "name": "Brewery Name",
  "brewery_type": "micro|nano|regional|brewpub|large|planning|bar|contract|proprietor|closed",
  "address_1": "123 Main St",
  "address_2": null,
  "address_3": null,
  "city": "City Name",
  "state_province": "State",
  "postal_code": "12345",
  "country": "United States",
  "phone": "1234567890",
  "website_url": "https://example.com",
  "longitude": -88.2434,
  "latitude": 40.1164
}
```

**Key Constraints:**
- Use `null` for missing optional fields (not empty strings or omitted fields)
- All fields must be present in the schema
- Maintain 2-space JSON indentation
- Brewery type must be from predefined list

## FastAPI Application (`main.py`)

**Framework:** FastAPI with Uvicorn
**Data Loading:** In-memory (loaded from `breweries.json` at startup)
**CORS:** Enabled for all origins (student browser access)

**Endpoints:**
- `GET /breweries` - List with filters (city, state, type, etc.)
- `GET /breweries/search` - Full-text search
- `GET /breweries/random` - Random brewery(ies)
- `GET /breweries/autocomplete` - Name autocomplete
- `GET /breweries/{id}` - Get by UUID
- `GET /breweries/meta` - Count metadata
- `GET /health` - Health check

**URL Compatibility:** Both `/breweries` and `/v1/breweries` (Open Brewery DB v1 spec)

## Deployment

### VPS Deployment
- **Host:** Hetzner CX11 (€4/month)
- **IP:** 178.156.206.171
- **Path:** `/opt/badm554-api`
- **Container:** Docker Compose with single service
- **Port:** 8000

### Deployment Trigger
Automatic on `git push` to `main` branch (via GitHub Actions auto-deploy workflow when issue is approved).

### Manual Deployment
```bash
# SSH to VPS
ssh root@178.156.206.171

# Navigate to app directory
cd /opt/badm554-api

# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

## Common Tasks

### Add a New Brewery (Manual)
1. Generate UUID: `python -c "import uuid; print(uuid.uuid4())"`
2. Edit `breweries.json` - add new entry to array
3. Verify JSON syntax: `python -m json.tool breweries.json > /dev/null`
4. Commit and push
5. Deploy to VPS

### Test Validation Workflow
1. Create issue with template: `.github/ISSUE_TEMPLATE/add-brewery.md`
2. Check Actions tab for workflow run
3. Verify validation comment appears
4. Check label applied (`validated` or `needs-revision`)

### Test Deployment Workflow
1. Add `approved` label to validated issue
2. Monitor Actions tab for deployment workflow
3. Check VPS logs: `ssh root@178.156.206.171 "cd /opt/badm554-api && docker-compose logs"`
4. Test API: `curl "http://178.156.206.171:8000/breweries/search?query=[brewery_name]"`

### Update Existing Brewery
1. Find brewery ID in `breweries.json`
2. Edit fields as needed
3. Commit and push
4. Deploy to VPS

## Important Notes

### Claude Workflow Instructions
Separate instructions for Claude when processing issues are in `.github/CLAUDE.md`. This includes validation rules, response templates, and duplicate detection logic.

### Student Issue Templates
Three templates in `.github/ISSUE_TEMPLATE/`:
- `add-brewery.md` - New brewery submissions
- `update-brewery.md` - Corrections to existing data
- `remove-brewery.md` - Report closed breweries

### Data Quality Standards
- All required fields must be present (name, type, city, state, country)
- Phone numbers: minimum 10 digits
- Website URLs: must start with `http://` or `https://`
- Brewery type: must be from valid list
- Duplicates: Check name + city + state combination

### Model Selection
**Validation:** Claude 3.5 Haiku (`--model claude-3-5-haiku-20241022`)
- Cost-effective: $0.03 vs $0.30 with Sonnet
- Sufficient for structured data validation
- Fast response time

**Deployment:** Default Claude model (can use Haiku or Sonnet)
- More complex task (extraction, UUID generation, JSON manipulation)
- Consider cost vs accuracy tradeoff

## Troubleshooting

### Workflow Fails with Permission Error
**Symptom:** Claude tries to run `gh issue comment` or `gh issue edit` and gets denied.

**Solution:** This is the expected behavior. The workaround is already implemented - Claude returns JSON, GitHub Actions script posts comment. Do not try to fix this by adding `additional_permissions`.

### Deployment Doesn't Update API
**Check:**
1. GitHub Actions deployment workflow completed successfully
2. VPS received git pull: `ssh root@178.156.206.171 "cd /opt/badm554-api && git log -1"`
3. Docker container restarted: `ssh root@178.156.206.171 "docker ps"`
4. Data file updated: `curl http://178.156.206.171:8000/health`

### Validation Always Passes
**By Design:** Lines 58-59 in `auto-validate-brewery.yml` hardcode `isValid = true`. This is intentional for student experience - Claude validates, but GitHub Actions always marks as valid to avoid blocking students.

### Duplicate Entries
Check `breweries.json` for existing entry with same name + city + state before approving. Claude checks in deployment workflow, but manual verification recommended.

## Course Context

**Course:** BADM 554 - Data Analytics Programming
**Use Case:** Students learn API usage, data validation, JSON, Git/GitHub, open-source contribution
**Student Workflow:** Submit brewery → Automated validation → Instructor approval → Auto-deploy
**Learning Objectives:**
- REST API interaction
- JSON data formats
- GitHub collaboration
- Data quality verification
- Open-source contribution

## References

- **Live API Docs:** http://178.156.206.171:8000/docs
- **GitHub Repo:** https://github.com/BADM554/brewery-api
- **Open Brewery DB Spec:** https://www.openbrewerydb.org/documentation
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **Claude GitHub Actions:** https://docs.claude.com/en/docs/claude-code/github-actions
