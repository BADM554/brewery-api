# Support & Troubleshooting Guide

Need help with your brewery submission? This guide covers common issues, how to check your submission status, and where to get help.

---

## 📊 Check Your Submission Status

### Understanding Labels

Your issue will have one or more labels that show its current status:

| Label | Meaning | What's Next |
|-------|---------|-------------|
| `brewery-addition` | New brewery submission | Automated validation will run |
| `brewery-update` | Update existing brewery | Automated validation will run |
| `brewery-closed` | Report closed brewery | Automated validation will run |
| `student-submission` | Submitted by student | All student issues get this |
| `validated` ✅ | Passed automated checks | Waiting for instructor review |
| `needs-revision` ❌ | Failed validation | Edit your issue to fix problems |
| `approved` 🎉 | Instructor approved | Deploying now! |
| Closed issue | Successfully deployed | Your brewery is live! |

### Timeline Expectations

**Typical processing time:**
1. **Validation:** Instant (within 30 seconds)
2. **Instructor review:** 24-48 hours (business days only)
3. **Deployment:** 30-60 seconds after approval
4. **Total time:** 1-2 business days from submission to live

**Note:** Submissions during weekends/holidays may take longer.

### How to Check API Status

Once deployed, verify your brewery is live:

**Search by name:**
```
http://178.156.206.171:8000/breweries/search?query=YOUR_BREWERY_NAME
```

**Check all endpoints:**
- Interactive docs: http://178.156.206.171:8000/docs
- Health check: http://178.156.206.171:8000/health

---

## 🐛 Common Issues & Solutions

### Issue: "Validation Failed" - Missing Required Fields

**Problem:** Your submission is missing name, type, city, state, or country.

**Solution:**
1. Click "Edit" on your issue description
2. Fill in all required fields:
   - Brewery Name: [Must not be blank]
   - Brewery Type: [Must be: micro, nano, regional, brewpub, large, planning, bar, contract, or proprietor]
   - City: [Must not be blank]
   - State/Province: [Full name, not abbreviation]
   - Country: [Usually "United States"]
3. Save changes - validation will run automatically

**Example:**
```
❌ BAD:
**Brewery Name:** [Your Brewery Name]
**State/Province:** IL

✅ GOOD:
**Brewery Name:** Triptych Brewing
**State/Province:** Illinois
```

---

### Issue: "Validation Failed" - Invalid Brewery Type

**Problem:** The brewery type you entered isn't recognized.

**Valid types:**
- `micro` - Small craft brewery (most common)
- `nano` - Very small brewery
- `regional` - Regional brewery
- `brewpub` - Brewery with restaurant
- `large` - Major commercial brewery
- `planning` - Not yet open
- `bar` - Bar (doesn't brew)
- `contract` - Contracts brewing to another brewery
- `proprietor` - Operates under another's license
- `closed` - Permanently closed

**Solution:** Edit your issue and use one of the exact types above (lowercase).

---

### Issue: Multiple Validation Comments

**Problem:** You see 2+ identical validation comments on your issue.

**Cause:** This was a bug that has been fixed. Old issues may still show duplicates.

**What to do:** Ignore the duplicates - look at the most recent validation comment and the labels on your issue.

---

### Issue: Phone Number Format Error

**Problem:** Phone number rejected as invalid.

**Requirements:**
- At least 10 digits
- Numbers only (no spaces, dashes, parentheses, or +)
- International format OK if 10+ digits

**Examples:**
```
❌ BAD:
(217) 355-1500
217-355-1500
+1-217-355-1500

✅ GOOD:
2173551500
12173551500
```

---

### Issue: Website URL Format Error

**Problem:** Website URL rejected as invalid.

**Requirements:**
- Must start with `http://` or `https://`
- Must be a complete URL

**Examples:**
```
❌ BAD:
triptychbrewing.com
www.triptychbrewing.com

✅ GOOD:
https://triptychbrewing.com
http://www.triptychbrewing.com
```

---

### Issue: "Possible Duplicate Detected"

**Problem:** A brewery with similar name/location already exists.

**What to check:**
1. Search the API: `http://178.156.206.171:8000/breweries/search?query=BREWERY_NAME`
2. Compare locations - same city and state?
3. Check if it's actually the same brewery

**If it's the same brewery:**
- Close your issue (no action needed)
- If information is wrong, open an "Update Brewery" issue instead

**If it's different:**
- Reply to the issue explaining the difference
- Examples: "Different location - this one is in Savoy, not Champaign" or "This is their second taproom location"

---

### Issue: I Made a Mistake - How Do I Fix It?

**Before approval:**
1. Click "Edit" on your issue description
2. Make corrections
3. Save - validation will run again automatically

**After approval (issue closed):**
1. Open a **new** issue using the "Update Brewery Information" template
2. Reference your original issue number
3. Explain what needs to be corrected

**Don't reopen closed issues** - create new ones for corrections.

---

### Issue: My Brewery Isn't Showing in API

**Check these steps:**

1. **Is your issue closed?** If not, it hasn't been deployed yet.
2. **Check labels:** Look for `approved` label = deployed
3. **Wait 1-2 minutes** after deployment comment
4. **Try searching:** `http://178.156.206.171:8000/breweries/search?query=EXACT_NAME`
5. **Check spelling:** API search is case-insensitive but spelling must match

**Still not working?**
- Clear your browser cache (Ctrl+F5 or Cmd+Shift+R)
- Try the direct API docs: http://178.156.206.171:8000/docs
- Check the deployment comment for the direct brewery link

---

### Issue: Validation Passed but Nothing Happened

**This is normal!** Here's what happens:

1. ✅ **Validation passed** = Automated checks complete
2. ⏳ **Waiting...** = Instructor needs to manually review
3. 🎯 **Approved label added** = Instructor approved (you might not see this happen)
4. 🚀 **Deployment** = Automatic within 30 seconds
5. ✅ **Closed + Comment** = Your brewery is live!

**Timeline:** Steps 2-5 typically take 24-48 business hours.

**What you can do:**
- Nothing! Just wait for instructor review
- Check back in 1-2 days
- Look for the `approved` label

---

## 💡 Tips for Successful Submissions

### Before Submitting

- [ ] **Check for duplicates first:** Search API before submitting
- [ ] **Verify brewery exists:** Check website, Google Maps, or visit
- [ ] **Get accurate info:** Use official website for contact details
- [ ] **Test phone/website:** Make sure they're current and working
- [ ] **Replace ALL placeholders:** No `[text in brackets]` should remain
- [ ] **Preview your submission:** Click Preview tab before submitting

### Writing Good Submissions

**Be specific:**
```
❌ "Local brewery downtown"
✅ "Triptych Brewing - 1703 Woodfield Drive, Savoy, Illinois"
```

**Use official names:**
```
❌ "Tony's beer place"
✅ "Tony's Pizza & Pub" (if that's the official name)
```

**Include optional fields when possible:**
- GPS coordinates (helps with mapping)
- Phone number (helps students contact)
- Website (provides additional info)
- Notes (unique features, hours, specialties)

---

## 🔍 How to Find Information

### Finding Brewery Details

**Official website:**
- Google: `"brewery name" + city + official site`
- Look for "Contact" or "About" pages
- Social media (Facebook, Instagram) often has details

**Google Maps:**
- Search brewery name + city
- Check reviews and photos to confirm it exists
- Right-click location → Copy coordinates for GPS

**Phone verification:**
- Call during business hours
- Confirm they're still operating
- Ask about address if uncertain

### Finding GPS Coordinates

**Method 1: Google Maps**
1. Search for brewery
2. Right-click the location marker
3. Click the coordinates at top
4. Copy latitude (first number) and longitude (second number)

**Method 2: Brewery website**
- Some websites include coordinates in their contact page
- Look for embedded Google Maps - URL may contain coordinates

**Format:**
- Latitude: Number between -90 and 90 (e.g., 40.0564)
- Longitude: Number between -180 and 180 (e.g., -88.2825)

### Finding Brewery ID for Updates

**Step 1:** Search the API
```
http://178.156.206.171:8000/breweries/search?query=BREWERY_NAME
```

**Step 2:** Find the brewery in results

**Step 3:** Copy the `id` field
```json
{
  "id": "67836207-49ed-4d67-8dca-8f66acdcbb00",  ← Copy this entire UUID
  "name": "Blind Pig Brewery",
  ...
}
```

**Step 4:** Paste into your update issue

---

## 📞 Additional Help

### Still Stuck?

If this guide doesn't solve your problem:

1. **Check recent issues:** See if others had the same problem
2. **Review validation message:** Read the full comment for specific guidance
3. **Check your labels:** Labels show current status
4. **Wait for timeline:** Most issues resolve within 24-48 hours

### Learning Resources

**Understanding APIs:**
- API Documentation: http://178.156.206.171:8000/docs
- Open Brewery DB (upstream project): https://www.openbrewerydb.org/

**Understanding JSON:**
- JSON.org: https://www.json.org/
- JSON Formatter (validate format): https://jsonformatter.org/

**Understanding GitHub Issues:**
- GitHub Issues Guide: https://guides.github.com/features/issues/

---

## 📋 Quick Reference

### Issue Template Selection

| To Do This | Use This Template |
|------------|-------------------|
| Add new brewery | "Add New Brewery" |
| Fix wrong information | "Update Brewery Information" |
| Report closed brewery | "Report Closed Brewery" |

### API Endpoints Quick Reference

```bash
# Search by name
http://178.156.206.171:8000/breweries/search?query=NAME

# Get by ID
http://178.156.206.171:8000/breweries/UUID

# Filter by city
http://178.156.206.171:8000/breweries?by_city=CITY_NAME

# Filter by state
http://178.156.206.171:8000/breweries?by_state=STATE_NAME

# Filter by type
http://178.156.206.171:8000/breweries?by_type=micro

# Interactive docs
http://178.156.206.171:8000/docs
```

### API Pagination Guide

**Default limit:** All queries return **50 results** by default.

**Working with large result sets:**

```bash
# Default: returns only 50 breweries
http://178.156.206.171:8000/breweries?by_state=California

# Increase to maximum: 200 results per page
http://178.156.206.171:8000/breweries?by_state=California&per_page=200

# Get next page (results 201-400)
http://178.156.206.171:8000/breweries?by_state=California&per_page=200&page=2
```

**Getting total counts without limits:**

```bash
# Returns {"total": 523} - shows count without pagination
http://178.156.206.171:8000/breweries/meta?by_state=California
```

**Example: Getting all breweries from a state with 500+ entries**

```python
import requests

# Step 1: Get total count
meta = requests.get("http://178.156.206.171:8000/breweries/meta?by_state=California")
total = meta.json()["total"]
print(f"Total breweries: {total}")

# Step 2: Calculate pages needed (200 per page)
pages = (total + 199) // 200

# Step 3: Loop through all pages
all_breweries = []
for page in range(1, pages + 1):
    response = requests.get(
        f"http://178.156.206.171:8000/breweries?by_state=California&per_page=200&page={page}"
    )
    all_breweries.extend(response.json())

print(f"Retrieved {len(all_breweries)} breweries")
```

**Limits by endpoint:**

| Endpoint | Default | Maximum |
|----------|---------|---------|
| `/breweries` | 50 | 200 per page |
| `/breweries/search` | 50 | 200 per page |
| `/breweries/random` | 1 | 50 |
| `/breweries/autocomplete` | 15 | 15 (fixed) |
| `/breweries/meta` | No limit | Returns count only |
| `/breweries/{id}` | 1 | 1 (single brewery) |

### Validation Requirements Checklist

**Required fields:**
- [x] Brewery name (not blank)
- [x] Brewery type (valid type from list)
- [x] City (not blank)
- [x] State/Province (full name)
- [x] Country (usually "United States")

**Optional but recommended:**
- [ ] Street address
- [ ] Postal code
- [ ] Phone (10+ digits, numbers only)
- [ ] Website (must start with http:// or https://)
- [ ] GPS coordinates
- [ ] Additional notes

---

**Last Updated:** 2025-10-09

*This guide is maintained by the BADM 554 course staff. If you notice errors or have suggestions for improvement, please mention them in your issue or open a documentation issue.*
