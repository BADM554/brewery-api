# Quick Setup - Claude GitHub App Already Installed ✅

Since you've already installed the Claude GitHub App, you just need to add a few secrets.

## Required GitHub Secrets

Go to: https://github.com/BADM554/brewery-api/settings/secrets/actions

Click **"New repository secret"** and add these **4 secrets**:

### 1. VPS_HOST
```
178.156.206.171
```

### 2. VPS_USERNAME
```
root
```

### 3. VPS_SSH_KEY
```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACDunlOQvP9jUo5oCWnteZatZtqh9LrvlfCLzVVddiMe+AAAAJhjlQytY5UM
rQAAAAtzc2gtZWQyNTUxOQAAACDunlOQvP9jUo5oCWnteZatZtqh9LrvlfCLzVVddiMe+A
AAAEAHMa3xApcP/jbgd+Mfw1GouHxzNiXAcrYY1E8n2VGdFO6eU5C8/2NSjmgJae15lq1m
2qH0uu+V8IvNVV12Ix74AAAADnZpc2hhbEBiYWRtNTU0AQIDBAUGBw==
-----END OPENSSH PRIVATE KEY-----
```

### 4. ANTHROPIC_API_KEY
```
sk-ant-api03-... (your Anthropic API key from https://console.anthropic.com/settings/keys)
```

## How It Works

### With Claude GitHub App Installed:

1. **Student submits issue** → Claude app automatically sees it
2. **Claude validates** → Comments with ✅ or asks for more info
3. **You review** → Add `approved` label if good
4. **Auto-deploys** → GitHub Action deploys to VPS
5. **Student notified** → Gets live API link

### Your Workflow:

```bash
# You only need to:
1. Review Claude's validation comment
2. If valid, add label: "approved"
3. Done! It auto-deploys in ~3 minutes
```

## Test It Now

1. Go to: https://github.com/BADM554/brewery-api/issues/new?template=add-brewery.md
2. Fill in test brewery:
   ```
   Brewery Name: Test Automation Brewery
   Brewery Type: micro
   Street: 123 Test St
   City: Springfield
   State/Province: Illinois
   Postal Code: 62701
   Country: United States
   Phone: 2175551234
   Website: https://test.example.com
   ```
3. Submit issue
4. Wait for Claude's validation comment (~1 min)
5. Add label: `approved`
6. Watch Actions tab: https://github.com/BADM554/brewery-api/actions
7. Check API: http://178.156.206.171:8000/breweries/search?query=test

## Secrets Summary

| Secret | Value | Purpose |
|--------|-------|---------|
| `ANTHROPIC_API_KEY` | *(from Anthropic Console)* | Claude API authentication |
| `VPS_HOST` | `178.156.206.171` | Your Hetzner server IP |
| `VPS_USERNAME` | `root` | SSH username |
| `VPS_SSH_KEY` | *(SSH private key above)* | For deployment authentication |

## What Happens After "Approved"

```mermaid
graph LR
    A[You add 'approved' label] --> B[GitHub Action starts]
    B --> C[Claude extracts brewery data]
    C --> D[Adds to breweries.json]
    D --> E[Commits & pushes]
    E --> F[SSH to VPS]
    F --> G[Git pull]
    G --> H[Docker rebuild]
    H --> I[Comments on issue]
    I --> J[Closes issue]
```

**Total time:** ~3-4 minutes

## Troubleshooting

### If deployment fails:

1. Check Actions logs: https://github.com/BADM554/brewery-api/actions
2. Verify secrets are set correctly
3. Test SSH manually: `ssh root@178.156.206.171`

### If Claude doesn't comment:

- Check GitHub App is installed: https://github.com/settings/installations
- Ensure repo has the app enabled
- Check issue has correct label

## Student Instructions

Share this with students:

```markdown
📢 Submit Breweries via GitHub!

1. Go to: https://github.com/BADM554/brewery-api/issues/new/choose
2. Choose "Add New Brewery" template
3. Fill out all fields
4. Submit issue
5. Claude AI will validate your submission
6. After approval, your brewery goes live in ~5 minutes!

Check your brewery: http://178.156.206.171:8000/docs
```

## Cost

- Anthropic API: ~$0.01-0.05 per submission (minimal token usage)
- GitHub Actions: Free tier
- VPS: €4/month (already running)

## What's Next

1. ✅ Add the 4 secrets above
2. ✅ Test with dummy issue
3. ✅ Share repo with students
4. ✅ Let automation handle submissions!

---

**Ready?** Add those 4 secrets and test it out! 🚀
