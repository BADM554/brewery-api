---
name: Add New Brewery
about: Submit a new brewery to add to the database
title: '[ADD] '
labels: 'brewery-addition, student-submission'
assignees: ''
---

<!--
📝 HOW TO FILL THIS OUT:

Replace the placeholder text [LIKE THIS] with your brewery's actual information.

EXAMPLE:
❌ BEFORE: **Brewery Name:** [Your Brewery Name]
✅ AFTER:  **Brewery Name:** Triptych Brewing

💡 TIP: Click the "Preview" tab to see how your submission looks before submitting!
-->

## Brewery Information

**Brewery Name:** [Your Brewery Name]

**Brewery Type:** [Select: micro, nano, regional, brewpub, large, planning, bar, contract, or proprietor]
<!-- Common types: micro (small craft brewery), brewpub (brewery + restaurant), nano (very small) -->

**Address:**
- Street: [Street Address]
- City: [City]
- State/Province: [Full State Name, e.g., Illinois]
- Postal Code: [ZIP Code]
- Country: [Country Name, e.g., United States]

**Contact Information:**
- Phone: [10-digit phone number, no spaces or dashes - e.g., 2173551500]
- Website: [Full URL including https:// - e.g., https://example.com]

**GPS Coordinates (optional but recommended):**
<!-- Find on Google Maps: Right-click location → Copy coordinates -->
- Latitude: [e.g., 40.0564 or leave blank]
- Longitude: [e.g., -88.2825 or leave blank]

**Additional Notes (optional):**
[Any interesting details - specialties, outdoor seating, pet-friendly, etc. Or leave blank]

---

## Submission Checklist
Check these before submitting:
- [ ] Brewery exists (verified via website, Google Maps, or in-person visit)
- [ ] Not already in database - checked: http://178.156.206.171:8000/breweries/search?query=[BREWERY_NAME]
- [ ] All required fields filled: Name, Type, City, State, Country
- [ ] Phone and website are accurate (if provided)
- [ ] Replaced all `[placeholder text]` with actual information

## Student Information (optional)
**Your Name:** [Your Name]

**Course Section:** BADM 554

**Date:** [Today's Date]

---

## ⏱️ What Happens Next?

1. **Automated Validation** (instant) - System checks your submission format
2. **Instructor Review** (24-48 hours) - Manual approval during business days
3. **Auto-Deployment** (30 seconds) - Added to live API automatically
4. **Confirmation** (instant) - You'll get a comment with links to test your brewery

**Track your submission:**
- `validated` label = Passed automated checks
- `approved` label = Instructor approved, deployment in progress
- Closed issue = Successfully deployed! 🎉

---

## 📚 Helpful Resources

**Find GPS coordinates:**
1. Open Google Maps
2. Right-click the brewery location
3. Click the coordinates at top
4. Paste into Latitude/Longitude fields

**Brewery type guide:**
- `micro` - Small craft brewery (most common, <15k barrels/year)
- `brewpub` - Brewery with attached restaurant/food service
- `nano` - Very small brewery (≤3 barrels per batch)
- `regional` - Larger regional brewery (15k-6M barrels/year)
- `bar` - Bar that doesn't brew (sells others' beers)

**Need help?** See [SUPPORT.md](../blob/main/.github/SUPPORT.md) for troubleshooting

---

*After approval, your brewery will be live on the API and available to all students. This data may also be contributed to the official [Open Brewery DB](https://www.openbrewerydb.org/).*
