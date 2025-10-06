---
name: Update Brewery Information
about: Report incorrect or outdated brewery information
title: '[UPDATE] '
labels: 'brewery-update, student-submission'
assignees: ''
---

<!--
📝 HOW TO FILL THIS OUT:

⚠️ FIRST: Click the "Preview" tab above to see what this looks like!
         Gray text disappears in preview - only your answers show.

THEN:
1. Find the brewery in our API: http://178.156.206.171:8000/breweries/search?query=BREWERY_NAME
2. Copy what's currently wrong and what it should be
3. Click back to "Write" tab
4. Delete the gray text and examples
5. Type your information on the same line after each field
6. Click "Preview" to check it looks right before submitting

EXAMPLE:
**Current Value:** 2173985133
**Correct Value:** 2173985134

💡 TIP: Use the Preview tab to make sure you deleted all the instructions!
-->

## Brewery to Update

**Brewery Name:** (delete this and type the brewery name)
<!-- Example: Blind Pig Brewery -->

**Brewery ID (if known):** (delete this and paste the ID from the API, or leave blank)
<!-- Find this in the API response at http://178.156.206.171:8000/breweries/search?query=BREWERY_NAME -->
<!-- Look for "id": "67836207..." and copy that whole code -->
<!-- Example: 67836207-49ed-4d67-8dca-8f66acdcbb00 -->

**Current Location:**
- City: (delete this and type city)
  <!-- Example: Champaign -->
- State: (delete this and type state)
  <!-- Example: Illinois -->

---

## What needs to be updated?

**Field to Update:** (delete this and type which field is wrong: phone, website, address, etc.)
<!-- Select one: phone, website, address, status, type, postal_code, coordinates -->
<!-- Example: phone -->

**Current Value:** (what the API shows RIGHT NOW - copy it exactly)
<!-- What the database currently shows -->
<!-- Example: 2173985133 -->

**Correct Value:** (what it SHOULD be - the correct information)
<!-- What it should be -->
<!-- Example: 2173985134 -->

**Source/Verification:** (how did you confirm this is correct?)
<!-- Delete this and explain how you verified: -->
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
