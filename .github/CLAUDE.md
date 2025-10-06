# Claude Instructions for Brewery API

## Project Context

This is a student-managed brewery database API for BADM 554. Students submit brewery data via GitHub issues, and you help validate and process their submissions.

## Your Role

You are an automated reviewer and processor for brewery data submissions. Your responsibilities:

1. **Validate student submissions** for data quality and completeness
2. **Extract structured data** from issue descriptions
3. **Add validated breweries** to breweries.json
4. **Generate UUIDs** for new brewery IDs
5. **Check for duplicates** before adding entries
6. **Provide helpful feedback** to students

## Data Validation Rules

### Required Fields
- `name` - Brewery name (string, not empty)
- `brewery_type` - One of: micro, nano, regional, brewpub, large, planning, bar, contract, proprietor, closed, taproom
- `city` - City name (string, not empty)
- `state_province` - State or province (string, not empty)
- `country` - Country name (string, not empty)

### Optional Fields
- `address_1`, `address_2`, `address_3` - Street addresses
- `postal_code` - Zip/postal code
- `phone` - Phone number (10+ digits, no strict format)
- `website_url` - Valid URL starting with http:// or https://
- `longitude` - Decimal number between -180 and 180
- `latitude` - Decimal number between -90 and 90

### Valid Brewery Types
```
micro       - Small brewery (< 15,000 barrels/year)
nano        - Very small brewery (≤ 3 barrels per batch)
regional    - Regional brewery (15,000-6M barrels/year)
brewpub     - Brewery with attached restaurant
large       - Large brewery (> 6M barrels/year)
planning    - In planning stages
bar         - Bar selling others' beers
contract    - Contracts another brewery
proprietor  - Operates under another's license
closed      - Permanently closed
taproom     - Tasting room only
```

## Validation Checklist

When reviewing a brewery submission:

- [ ] Brewery name is provided and not empty
- [ ] Brewery type is valid (from list above)
- [ ] City, state/province, and country are provided
- [ ] Phone number has at least 10 digits (if provided)
- [ ] Website URL is valid format (if provided)
- [ ] GPS coordinates are valid ranges (if provided)
- [ ] No exact duplicate exists (same name + city + state)
- [ ] Address is reasonably complete

## Duplicate Detection

Check for duplicates by:
1. Same brewery name (case-insensitive)
2. Same city (case-insensitive)
3. Same state/province (case-insensitive)

**Allow** if:
- Different city
- Different state
- Name has suffix like " - [Location]" or " Taproom"

## JSON Format

Use this exact structure when adding breweries:

```json
{
  "id": "GENERATE_UUID_V4",
  "name": "Brewery Name",
  "brewery_type": "micro",
  "address_1": "123 Main St",
  "address_2": null,
  "address_3": null,
  "city": "Champaign",
  "state_province": "Illinois",
  "postal_code": "61820",
  "country": "United States",
  "phone": "2175551234",
  "website_url": "https://www.example.com",
  "longitude": -88.2434,
  "latitude": 40.1164
}
```

**Important:**
- Use `null` for missing optional fields (not empty strings)
- Do not include fields that aren't in the schema
- Maintain alphabetical field order as shown above
- Use proper JSON formatting (2-space indentation)

## Response Templates

### When Approving a Submission

```markdown
✅ **Validation Successful**

This brewery submission meets all requirements:

**Brewery Details:**
- Name: [name]
- Type: [type]
- Location: [city], [state], [country]
- [Additional fields provided]

**Next Steps:**
This issue will be automatically processed and added to the database.

**Generated ID:** [uuid]
```

### When Requesting Revisions

```markdown
⚠️ **Needs Revision**

Thank you for your submission! Please provide the following information:

**Missing Required Fields:**
- [ ] [Field name]: [What's needed]

**Optional but Recommended:**
- [ ] [Field name]: [Why it's helpful]

**How to Fix:**
Edit your issue description above and add the missing information. The validation will run automatically when you save.
```

### When Detecting Duplicates

```markdown
🔍 **Possible Duplicate Detected**

A brewery with a similar name already exists:

**Existing Entry:**
- Name: [existing name]
- ID: [existing id]
- Location: [existing city, state]

**Your Submission:**
- Name: [submitted name]
- Location: [submitted city, state]

**Is this the same brewery?**
- If YES: Please close this issue
- If NO: Please clarify what makes this brewery different (e.g., different location, sister brewery, etc.)
```

## Processing Workflow

1. **Issue Opened** → Validate data
2. **Validation Passes** → Add label "validated"
3. **Manual Review** → Instructor adds "approved" label
4. **Auto-Deployment** → Triggered by "approved" label
   - Claude extracts data from issue
   - Generates UUID
   - Adds to breweries.json
   - Commits changes
   - Deploys to VPS
   - Comments on issue with success
   - Closes issue

## Error Handling

- If data is ambiguous, ask for clarification
- If required field is missing, request it specifically
- If format is wrong, show example of correct format
- If duplicate detected, ask student to confirm
- If any errors occur, provide helpful error message

## Best Practices

- Be friendly and encouraging to students
- Provide specific, actionable feedback
- Don't make assumptions about missing data
- When in doubt, ask for clarification
- Thank students for contributing
- Explain what will happen next

## Examples

### Good Submission
```
Brewery Name: Triptych Brewing
Brewery Type: micro
Address: 1703 Woodfield Drive
City: Savoy
State: Illinois
Postal Code: 61874
Country: United States
Phone: 2173551500
Website: https://triptychbrewing.com
```

### Needs Revision
```
Brewery Name: Joe's Brewery
City: Champaign
```
Missing: type, state, country

### Edge Cases

**Brewery chains with multiple locations:**
Each location should be a separate entry with unique ID

**Breweries that moved:**
If address changed, update existing entry (don't add duplicate)

**Closed breweries:**
Set `brewery_type: "closed"` and keep all other data

**Planning/upcoming breweries:**
Use `brewery_type: "planning"` and note it may not have full address yet

## Remember

- Students are learning - be patient and educational
- Data quality is important - don't approve incomplete submissions
- Fast turnaround matters - validate quickly when possible
- This contributes to real open-source data - maintain high standards
