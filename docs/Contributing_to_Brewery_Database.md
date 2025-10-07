# Contributing to the Brewery Database

## Overview

As part of this course, you'll contribute to a real, live API by adding, updating, or reporting closed breweries. Your contributions will be reviewed and deployed to the production API at http://178.156.206.171:8000.

This exercise teaches you:
- How to contribute to open-source projects
- GitHub Issues workflow
- Data validation and quality
- API data structures
- Collaborative development

---

## Getting Started

### Prerequisites

1. **GitHub Account** - You'll need a GitHub account to submit issues
2. **Find a Brewery** - Research a brewery to add/update (see resources below)
3. **Gather Data** - Collect all required information about the brewery

### Resources for Finding Breweries

- **Brewery Finder:** https://www.brewerydb.com/
- **RateBeer:** https://www.ratebeer.com/
- **Untappd:** https://untappd.com/
- **Google Maps** - Search "breweries near me"
- **Local brewery websites** - Most have contact/location info

---

## How to Contribute

### Step 1: Check for Duplicates

Before submitting, **search the existing database** to avoid duplicates:

```bash
# Search by name
http://178.156.206.171:8000/breweries/search?query=brewery_name

# Search by city
http://178.156.206.171:8000/breweries?by_city=CityName

# Search by state
http://178.156.206.171:8000/breweries?by_state=StateName
```

Or use the interactive API docs: http://178.156.206.171:8000/docs

### Step 2: Choose Your Contribution Type

You can submit three types of contributions:

1. **Add a New Brewery** - A brewery not currently in the database
2. **Update Existing Brewery** - Correct/update information for an existing brewery
3. **Report Closed Brewery** - Mark a brewery that has closed

### Step 3: Submit a GitHub Issue

Go to the repository: **https://github.com/BADM554/brewery-api/issues**

Click **"New Issue"** and select the appropriate template:

---

## Template 1: Add a New Brewery

Use this template when adding a brewery that doesn't exist in the database.

### Required Information

| Field | Description | Example |
|-------|-------------|---------|
| **Name** | Official brewery name | Stone Brewing |
| **Brewery Type** | Type of brewery (see options below) | micro |
| **Street Address** | Street address | 1999 Citracado Parkway |
| **City** | City name | Escondido |
| **State/Province** | Full state name | California |
| **Postal Code** | ZIP/postal code | 92029 |
| **Country** | Country name | United States |
| **Phone** | Phone number (10+ digits) | 7609520444 |
| **Website** | Full URL (must include http:// or https://) | https://www.stonebrewing.com |
| **Longitude** | Longitude coordinate | -117.0841 |
| **Latitude** | Latitude coordinate | 33.1331 |

### Brewery Types

Choose one of the following:
- `micro` - Small brewery, typically sells 75% or more on-site
- `nano` - Extremely small brewery (less than 3-barrel system)
- `regional` - Regional brewery with wider distribution
- `brewpub` - Restaurant brewery that sells 25%+ on-site
- `large` - Large brewery (6+ million barrels annually)
- `planning` - Brewery in planning stages
- `bar` - Bar that brews beer
- `contract` - Hires another brewery to make their beer
- `proprietor` - Brewery owned by another brewery

### Finding Coordinates

Use one of these tools to find latitude/longitude:
- **Google Maps:** Right-click on location → Click coordinates to copy
- **LatLong.net:** https://www.latlong.net/
- **GPS Coordinates:** https://gps-coordinates.org/

### Example Issue

```markdown
**Brewery Name:** Stone Brewing

**Type:** micro

**Address:**
- Street: 1999 Citracado Parkway
- City: Escondido
- State: California
- Postal Code: 92029
- Country: United States

**Contact:**
- Phone: 7609520444
- Website: https://www.stonebrewing.com

**Coordinates:**
- Latitude: 33.1331
- Longitude: -117.0841

**Additional Notes:**
Famous craft brewery known for Stone IPA. Opened in 1996.
```

---

## Template 2: Update Existing Brewery

Use this template to correct or update information for a brewery already in the database.

### Required Information

1. **Brewery ID** - Get this from the API (search for the brewery first)
2. **Field to Update** - Which field needs correction
3. **Current Value** - What's currently in the database
4. **Correct Value** - What it should be
5. **Source** - Where you verified the correct information

### How to Find Brewery ID

```bash
# Search for the brewery
http://178.156.206.171:8000/breweries/search?query=brewery_name

# Look for the "id" field in the response
# Example: "id": "b54b16e1-ac3b-4bff-a11f-f7ae9ddc27e0"
```

### Example Issue

```markdown
**Brewery ID:** b54b16e1-ac3b-4bff-a11f-f7ae9ddc27e0

**Brewery Name:** Stone Brewing

**Field to Update:** website_url

**Current Value:** http://www.stonebrewing.com

**Correct Value:** https://www.stonebrewing.com

**Source:** Official website (verified 2024-10-06)

**Reason for Update:**
Website has migrated to HTTPS. HTTP redirects to HTTPS.
```

---

## Template 3: Report Closed Brewery

Use this template to report a brewery that has permanently closed.

### Required Information

1. **Brewery ID** - Get this from the API
2. **Brewery Name** - Name of the closed brewery
3. **Closure Date** - When it closed (if known)
4. **Source** - Where you confirmed the closure

### Example Issue

```markdown
**Brewery ID:** b54b16e1-ac3b-4bff-a11f-f7ae9ddc27e0

**Brewery Name:** Stone Brewing Escondido

**Closure Date:** March 2020 (approximate)

**Source:**
- https://www.sandiegouniontribune.com/business/story/2020-03-15/stone-brewing-closes
- Google Maps shows "Permanently Closed"

**Additional Notes:**
Location closed due to COVID-19 pandemic. Other Stone locations still open.
```

---

## What Happens After You Submit?

### 1. Automated Validation (Instant)

Claude AI will automatically validate your submission and post a comment within seconds:

- ✅ **Valid** - Your submission meets all requirements
- ❌ **Needs Revision** - Issues found, please address the feedback

### 2. Instructor Review (1-2 days)

Your instructor will review the submission and either:
- **Approve** - Adds the `approved` label
- **Request Changes** - Posts comments with requested changes

### 3. Automatic Deployment (Instant)

Once approved, the system automatically:
1. Extracts the data from your issue
2. Adds it to the database
3. Commits the change to GitHub
4. Deploys to the production API
5. Posts a success comment with a link to search for your brewery
6. Closes the issue

**You'll receive a comment like:**

> ✅ Successfully added brewery **Stone Brewing**!
>
> View it in the API: http://178.156.206.171:8000/breweries/search?query=Stone%20Brewing

### 4. Verify Your Contribution

After deployment, test your contribution:

```bash
# Search for your brewery
http://178.156.206.171:8000/breweries/search?query=YOUR_BREWERY_NAME

# View by ID (from the success comment)
http://178.156.206.171:8000/breweries/YOUR_BREWERY_ID
```

---

## Data Quality Guidelines

### Required Fields

These fields **must** be provided:
- Name
- Brewery Type
- City
- State/Province
- Country

### Optional Fields

These fields can be `null` if unknown:
- address_1, address_2, address_3
- postal_code
- phone
- website_url
- longitude
- latitude

### Validation Rules

1. **Phone Numbers:**
   - Minimum 10 digits
   - Remove spaces, dashes, parentheses
   - Example: `(555) 123-4567` → `5551234567`

2. **Website URLs:**
   - Must start with `http://` or `https://`
   - Include full URL: `https://example.com` ✅
   - Don't use: `example.com` ❌

3. **Brewery Type:**
   - Must be one of: micro, nano, regional, brewpub, large, planning, bar, contract, proprietor, closed
   - Use lowercase
   - Use `closed` for permanently closed breweries

4. **Coordinates:**
   - Latitude: -90 to 90
   - Longitude: -180 to 180
   - Use decimal format: `33.1331` ✅
   - Don't use DMS format: `33°7'59"N` ❌

5. **State Names:**
   - Use full state name: `California` ✅
   - Don't use abbreviations: `CA` ❌

---

## Common Mistakes to Avoid

### ❌ Duplicate Submissions

**Problem:** Brewery already exists in database

**Solution:** Always search first before submitting

```bash
http://178.156.206.171:8000/breweries/search?query=brewery_name
```

### ❌ Incomplete Data

**Problem:** Missing required fields

**Solution:** Ensure name, type, city, state, and country are provided

### ❌ Invalid Brewery Type

**Problem:** Using incorrect type like "taproom" or "craft"

**Solution:** Use only the approved types listed above

### ❌ Wrong URL Format

**Problem:** Website URL missing protocol

**Solution:** Always include `https://` or `http://`

### ❌ Incorrect Coordinates

**Problem:** Swapping latitude and longitude

**Solution:** Remember - Latitude is North/South (-90 to 90), Longitude is East/West (-180 to 180)

---

## Grading Rubric

Your contribution will be graded on:

| Criteria | Points | Description |
|----------|--------|-------------|
| **Completeness** | 30% | All required fields provided |
| **Accuracy** | 30% | Information is correct and verified |
| **Formatting** | 20% | Data follows the correct format |
| **Duplicate Check** | 10% | Verified brewery doesn't already exist |
| **Source Citation** | 10% | Provided credible source for information |

### Grade Scale

- **A (90-100%):** Complete, accurate data with all fields properly formatted
- **B (80-89%):** Minor formatting issues or missing optional fields
- **C (70-79%):** Missing some required data or accuracy concerns
- **D (60-69%):** Significant issues with data quality
- **F (<60%):** Incomplete submission or duplicate entry

---

## Tips for Success

1. **Start Early** - Don't wait until the deadline
2. **Choose a Local Brewery** - Easier to verify information
3. **Double-Check Everything** - Review your submission before posting
4. **Use Official Sources** - Brewery websites, not third-party reviews
5. **Test the API** - Search for your brewery after it's deployed
6. **Keep It Simple** - Start with a straightforward addition

---

## Frequently Asked Questions

### Q: Can I submit multiple breweries?

**A:** Yes! You can submit as many as you like, but each must be a separate GitHub issue.

### Q: What if I don't know the coordinates?

**A:** You can leave them as `null` or use Google Maps to find them (right-click on the location).

### Q: Can I update a brewery I didn't add?

**A:** Yes! Anyone can submit updates to improve data quality.

### Q: What if the brewery doesn't have a website?

**A:** Enter `null` for the website_url field.

### Q: How long does approval take?

**A:** Typically 1-2 business days. Validation is instant, but instructor approval may take longer.

### Q: Can I delete a brewery?

**A:** Use the "Report Closed Brewery" template instead. We mark them as closed rather than deleting.

### Q: What if my submission is rejected?

**A:** Read the feedback, make the requested changes, and update your issue. Don't create a new issue.

### Q: Can I submit breweries from other countries?

**A:** Yes! The database includes international breweries.

---

## Example: Complete Workflow

Here's a complete example from start to finish:

### 1. Find a Brewery

You visit a local brewery: **Riggs Beer Company** in Urbana, IL

### 2. Search for Duplicates

```
http://178.156.206.171:8000/breweries/search?query=Riggs
```

Result: No matches found ✅

### 3. Gather Information

Visit their website: https://www.riggsbeer.com/

Collect data:
- Name: Riggs Beer Company
- Type: micro
- Address: 613 E Green St, Urbana, IL 61801
- Phone: (217) 344-2337
- Website: https://www.riggsbeer.com/
- Coordinates: 40.1104, -88.2073 (from Google Maps)

### 4. Submit GitHub Issue

Go to: https://github.com/BADM554/brewery-api/issues/new

Select: "Add New Brewery" template

Fill out the form with your data

### 5. Wait for Validation

Claude posts a comment within seconds:

> ✅ Validation successful! Your submission will be reviewed by the instructor.

### 6. Wait for Approval

Instructor reviews and adds `approved` label

### 7. Automatic Deployment

System posts:

> ✅ Successfully added brewery **Riggs Beer Company**!
>
> View it in the API: http://178.156.206.171:8000/breweries/search?query=Riggs

### 8. Verify

Visit the API link and confirm your brewery appears correctly!

---

## Getting Help

If you run into issues:

1. **Check the validation comment** - It will tell you what's wrong
2. **Review this guide** - Most questions are answered here
3. **Ask in class** - Your instructor can help troubleshoot
4. **Check the API docs** - http://178.156.206.171:8000/docs
5. **Post on discussion board** - Help each other out

---

## Learning Outcomes

By completing this assignment, you will:

- ✅ Understand REST API data structures
- ✅ Practice JSON data formatting
- ✅ Learn GitHub collaboration workflows
- ✅ Contribute to a real, live API
- ✅ Understand data validation and quality
- ✅ Experience automated CI/CD pipelines

Good luck, and happy brewing! 🍺

---

**Last Updated:** October 6, 2025
**API Version:** v1
**Course:** BADM 554 - Data Analytics Programming
