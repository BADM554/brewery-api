# Automation Setup Guide

This guide explains how to set up the automated brewery submission and deployment system.

## Overview

```
Student submits issue → Claude validates → You approve → Auto-deploy → Student sees update
```

**Timeline:** Student sees their brewery live in ~2-5 minutes after approval!

## Prerequisites

1. **GitHub Repository** - https://github.com/BADM554/brewery-api
2. **Anthropic API Key** - For Claude integration
3. **VPS Access** - SSH key for deployment
4. **GitHub Permissions** - Admin access to repo

## Step 1: Get Anthropic API Key

1. Go to https://console.anthropic.com/
2. Sign in with your account
3. Navigate to **API Keys**
4. Click **Create Key**
5. Copy the key (starts with `sk-ant-`)

**Important:** Keep this key secret!

## Step 2: Add GitHub Repository Secrets

Go to: https://github.com/BADM554/brewery-api/settings/secrets/actions

Add these secrets:

### Required Secrets

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `ANTHROPIC_API_KEY` | `sk-ant-...` | Your Anthropic API key |
| `VPS_HOST` | `178.156.206.171` | Your Hetzner server IP |
| `VPS_USERNAME` | `root` | SSH username |
| `VPS_SSH_KEY` | Private SSH key | Your `~/.ssh/id_ed25519` contents |

### How to Get SSH Private Key

```bash
# Copy your private key
cat ~/.ssh/id_ed25519

# Copy the ENTIRE output including:
# -----BEGIN OPENSSH PRIVATE KEY-----
# ...
# -----END OPENSSH PRIVATE KEY-----
```

Paste this into `VPS_SSH_KEY` secret.

## Step 3: Install Claude GitHub App (Optional)

For advanced features:

1. Visit https://github.com/apps/claude-code
2. Click **Install**
3. Select **BADM554** organization
4. Choose **brewery-api** repository
5. Click **Install**

This enables Claude to:
- Comment on issues
- Create commits
- Suggest code changes

## Step 4: Test the Automation

### Create a Test Issue

1. Go to https://github.com/BADM554/brewery-api/issues/new?template=add-brewery.md
2. Fill out with test data:

```
Brewery Name: Test Automation Brewery
Brewery Type: micro
Street: 123 Test St
City: Testville
State/Province: Illinois
Postal Code: 61820
Country: United States
Phone: 2175551234
Website: https://test.example.com
```

3. Submit the issue
4. Watch for Claude's validation comment (~30 seconds)

### Approve and Deploy

1. If Claude validates ✅, add label: `approved`
2. Watch GitHub Actions run (Actions tab)
3. Wait 2-5 minutes for deployment
4. Check: http://178.156.206.171:8000/breweries/search?query=test
5. Issue should auto-close with success comment

## Step 5: Workflow Details

### Workflow 1: Auto-Validation

**File:** `.github/workflows/auto-validate-brewery.yml`

**Triggers:** When issue is opened/edited with brewery labels

**Actions:**
1. Claude reads issue
2. Validates required fields
3. Checks for duplicates
4. Comments with ✅ or ⚠️
5. Adds label: `validated` or `needs-revision`

**Manual Step:** You review and add `approved` label

### Workflow 2: Auto-Deployment

**File:** `.github/workflows/auto-deploy-brewery.yml`

**Triggers:** When you add `approved` label

**Actions:**
1. Claude extracts brewery data from issue
2. Generates UUID for new brewery
3. Checks for duplicates
4. Adds to `breweries.json`
5. Commits and pushes changes
6. SSHs to VPS
7. Pulls latest code
8. Rebuilds and restarts Docker container
9. Comments on issue with success + live link
10. Closes issue

**No manual steps** - fully automated!

## Troubleshooting

### Claude Not Commenting

**Check:**
- `ANTHROPIC_API_KEY` secret is set correctly
- Issue has correct label (`brewery-addition`, etc.)
- Workflow file syntax is correct

**View logs:**
https://github.com/BADM554/brewery-api/actions

### Deployment Fails

**Check:**
- `VPS_SSH_KEY` secret has full private key
- `VPS_HOST` is correct IP
- SSH key has access to VPS
- Docker is running on VPS

**Debug:**
```bash
# Test SSH connection
ssh root@178.156.206.171

# Check Docker status
docker-compose ps

# View logs
docker-compose logs -f
```

### Duplicate Not Detected

Claude checks: same name + city + state (case-insensitive)

**Manually check:**
```bash
grep -i "brewery name" breweries.json
```

### Deployment Slow

Normal timeline:
- Validation: 30-60 seconds
- Approval: Manual (you add label)
- Deployment: 2-3 minutes
- Total: ~3-5 minutes from approval

## Workflow Customization

### Change Deployment Server

Edit `.github/workflows/auto-deploy-brewery.yml`:

```yaml
host: ${{ secrets.VPS_HOST }}  # Change secret value
```

### Adjust Validation Rules

Edit `.github/CLAUDE.md`:

Add/modify validation rules for Claude to follow.

### Change Auto-Close Behavior

Edit `.github/workflows/auto-deploy-brewery.yml`:

```yaml
# Comment out to prevent auto-close
# github.rest.issues.update({
#   state: 'closed'
# });
```

## Manual Overrides

### Skip Automation

If you need to manually add a brewery:

1. Edit `breweries.json` locally
2. Commit and push
3. Run: `./deploy.sh 178.156.206.171`
4. Manually close issue

### Bulk Approvals

To approve multiple issues at once:

```bash
# Label multiple issues as approved
gh issue edit 1,2,3,4,5 --add-label "approved"
```

All will deploy in parallel!

## Cost Estimation

### Anthropic API Costs

**Per submission:**
- Validation: ~2,000 tokens (~$0.01)
- Deployment: ~3,000 tokens (~$0.015)
- **Total per brewery:** ~$0.025 (2.5 cents)

**For 50 students × 2 submissions each:**
- 100 breweries × $0.025 = **$2.50 total**

Very affordable! 💰

### GitHub Actions

- Free tier: 2,000 minutes/month
- Each workflow: ~2-3 minutes
- **More than enough for class use**

## Monitoring

### View All Workflow Runs

https://github.com/BADM554/brewery-api/actions

### Check API Status

```bash
curl http://178.156.206.171:8000/health
```

### View Recent Deployments

```bash
ssh root@178.156.206.171
cd /opt/badm554-api
git log --oneline -10
```

## Student Communication

### Notify Class About Automation

```
📢 Brewery Submissions Now Automated!

When you submit a brewery:
1. Claude AI validates your submission (~1 min)
2. I review and approve ✅
3. Auto-deploys to live API (~3 min)
4. You get notified with API link

Timeline: Your brewery goes live in ~5 minutes! 🚀

Submit here: https://github.com/BADM554/brewery-api/issues/new/choose
```

### Response Template

When students ask "Is my brewery live?"

```
Check the issue comments - it will show:
✅ Deployed successfully + live API link

Or search here:
http://178.156.206.171:8000/breweries/search?query=[brewery-name]
```

## Advanced Features

### Enable Auto-Approve (Optional)

If you want Claude to auto-approve high-quality submissions:

Edit `.github/workflows/auto-validate-brewery.yml`:

```yaml
- name: Auto-approve high quality
  if: steps.claude.outputs.quality_score > 90
  run: |
    gh issue edit ${{ github.event.issue.number }} --add-label "approved"
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

⚠️ **Not recommended initially** - review first to ensure quality!

### Notification on Approval

Get notified when you need to approve:

Repository → Settings → Notifications → Issues

Enable: "Issues assigned to you"

## Security Notes

- ✅ API keys stored in GitHub Secrets (encrypted)
- ✅ SSH key access limited to deployment user
- ✅ Claude can only read/write to this repo
- ✅ All actions logged in GitHub Actions
- ✅ Students cannot access secrets
- ✅ Workflow requires your manual approval label

## Next Steps

1. ✅ Set up secrets (above)
2. ✅ Test with dummy issue
3. ✅ Announce to students
4. ✅ Review first few submissions manually
5. ✅ Monitor automation performance
6. 📊 Gather student feedback

---

**Questions?** Check GitHub Actions logs or test with a dummy submission first!
