---
name: Update Brewery Information
about: Report incorrect or outdated brewery information
title: '[UPDATE] '
labels: 'brewery-update, student-submission'
assignees: ''
---

<!--
📝 HOW TO FILL THIS OUT:

1. Find the brewery: http://178.156.206.171:8000/breweries/search?query=[BREWERY_NAME]
2. Replace all [placeholder text] below with actual information
3. Click "Preview" tab to check before submitting

EXAMPLE:
❌ BEFORE: **Brewery Name:** [Brewery Name]
✅ AFTER:  **Brewery Name:** Blind Pig Brewery
-->

## Brewery to Update

**Brewery Name:** [Exact Brewery Name]

**Brewery ID (if known):** [UUID from API, e.g., 67836207-49ed-4d67-8dca-8f66acdcbb00]
<!-- Find at: http://178.156.206.171:8000/breweries/search?query=[BREWERY_NAME] -->
<!-- Look for "id": "..." in the JSON response -->

**Current Location:**
- City: [City Name]
- State: [State Name]

---

## What Needs to Be Updated?

**Field to Update:** [Select: phone, website, address, brewery_type, postal_code, coordinates, or other]

**Current (Incorrect) Value:** [What the API currently shows - copy exactly from API]

**Correct Value:** [What it SHOULD be]

**How I Verified This:** [Explain your source]
<!-- Examples:
- Called brewery on [date], confirmed with staff
- Checked official website: [URL]
- Visited in person on [date]
- Found in news article: [URL]
-->

---

## Submission Checklist
- [ ] Verified new information is correct (with source)
- [ ] Found brewery in API and confirmed what needs changing
- [ ] Included brewery ID (if possible)
- [ ] Checked current value in API
- [ ] Replaced all `[placeholder text]`

## Student Information (optional)
**Your Name:** [Your Name]

**Course Section:** BADM 554

**Date:** [Today's Date]

---

## ⏱️ What Happens Next?

1. **Automated Validation** (instant) - Checks submission format
2. **Instructor Review** (24-48 hours) - Verifies the correction
3. **Auto-Update** (30 seconds) - Applied to live API
4. **Confirmation** (instant) - You'll get a comment confirming the update

**Timeline:** Updates typically processed within 1-2 business days

---

## 📝 How to Find Brewery Information

**Step 1: Search for brewery**
```
http://178.156.206.171:8000/breweries/search?query=[BREWERY_NAME]
```

**Step 2: Find the brewery ID**
Look for the `"id"` field in the JSON response:
```json
{
  "id": "67836207-49ed-4d67-8dca-8f66acdcbb00",  ← Copy this
  "name": "Blind Pig Brewery",
  "phone": "2173985133",  ← Current value
  ...
}
```

**Step 3: Copy the incorrect value exactly**
This helps us find and fix the right field!

**Need help?** See [SUPPORT.md](../blob/main/.github/SUPPORT.md) for troubleshooting

---

*After approval, your update will be live on the API. This correction may also be submitted to the official [Open Brewery DB](https://www.openbrewerydb.org/).*
