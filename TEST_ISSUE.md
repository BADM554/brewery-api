# Test Issue for Triptych Brewing

Copy and paste the text below into a new GitHub issue to test the automation.

---

## GO TO:
https://github.com/BADM554/brewery-api/issues/new?template=add-brewery.md

## PASTE THIS (after deleting the template instructions):

**Brewery Name:** Triptych Brewing

**Brewery Type:** micro

**Address:**
- Street: 1703 Woodfield Drive
- City: Savoy
- State/Province: Illinois
- Postal Code: 61874
- Country: United States

**Contact Information:**
- Phone: 7792323376
- Website: https://triptychbrewing.com

**Location (if known):**
- Latitude: 40.0564
- Longitude: -88.2825

**Additional Notes:** Known for IPAs and experimental beers. Has a taproom with tasting options and carry-out.

---

## Submission Checklist
- [x] I have verified this brewery exists (website, Google Maps, or visited in person)
- [x] I checked it's not already in the database: http://178.156.206.171:8000/breweries/search?query=triptych
- [x] All required fields are filled out (Name, Type, City, State, Country)
- [x] Contact information is accurate
- [x] I removed the example comments before submitting

## Student Information (Optional)
**Your Name:** Test User

**Course Section:** BADM 554

**Date:** 2025-10-06

---

## WHAT SHOULD HAPPEN:

1. ✅ Claude validates the issue (~1 min)
2. ✅ Claude comments with validation results
3. ⏳ You add "approved" label manually
4. ✅ GitHub Action deploys to VPS (~3 min)
5. ✅ Issue gets closed with success message
6. ✅ Brewery appears in API: http://178.156.206.171:8000/breweries/search?query=triptych

## TO TEST:

1. Go to: https://github.com/BADM554/brewery-api/issues/new?template=add-brewery.md
2. Delete all the template placeholder text (the parts with parentheses)
3. Paste the brewery information from above
4. Click "Submit new issue"
5. Wait for Claude to validate
6. Add label: "approved"
7. Watch the magic happen!
