---
name: Update Brewery Information
about: Report incorrect or outdated brewery information
title: '[UPDATE] '
labels: 'brewery-update, student-submission'
assignees: ''
---

## Brewery to Update

**Brewery Name:**
<!-- Example: Blind Pig Brewery -->

**Brewery ID (if known):**
<!-- Find this in the API response at http://178.156.206.171:8000/breweries/search?query=BREWERY_NAME -->
<!-- Example: 67836207-49ed-4d67-8dca-8f66acdcbb00 -->

**Current Location:**
- City: <!-- Example: Champaign -->
- State: <!-- Example: Illinois -->

---

## What needs to be updated?

**Field to Update:**
<!-- Select one: phone, website, address, status, type, postal_code, coordinates -->
<!-- Example: phone -->

**Current Value:**
<!-- What the database currently shows -->
<!-- Example: 2173985133 -->

**Correct Value:**
<!-- What it should be -->
<!-- Example: 2173985134 -->

**Source/Verification:**
<!-- How did you verify this information? -->
<!-- Example: Called the brewery directly on 2025-10-06 -->
<!-- Example: Checked their website at https://blindpigbrewery.com/contact -->
<!-- Example: Visited in person and confirmed with staff -->

---

## Submission Checklist
- [ ] I have verified the new information is correct
- [ ] I have identified the specific brewery that needs updating
- [ ] I have provided a source for the updated information
- [ ] I checked the current value in the API first

## Student Information (Optional)
**Your Name:**
<!-- Example: Jane Doe -->

**Course Section:** BADM 554

**Date:**
<!-- Example: 2025-10-06 -->

---

## 📝 How to Find Brewery ID

1. Go to: http://178.156.206.171:8000/breweries/search?query=BREWERY_NAME
2. Look for the brewery in the results
3. Copy the `"id"` field value

**Example:**
```json
{
  "id": "67836207-49ed-4d67-8dca-8f66acdcbb00",  ← Copy this
  "name": "Blind Pig Brewery",
  ...
}
```

---
*After approval, this update will be applied to our database within minutes and may be submitted to the official Open Brewery DB.*
