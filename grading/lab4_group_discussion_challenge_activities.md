# Group Discussion & Challenge Activity Ideas

## Group Discussion Topics

### 1. **API Design Patterns & Best Practices**
**Guiding Questions:**
- Why does the Brewery API not require authentication? What are the trade-offs between open vs authenticated APIs?
- Compare the different endpoints (`/search` vs `/breweries` with filters). When would you use each approach?
- The `/autocomplete` endpoint returns simplified data (just `id` and `name`). Why might this design choice improve performance?
- How does pagination (`per_page` parameter) help manage large datasets? What happens without it?

### 2. **JSON vs DataFrames: When to Convert?**
**Guiding Questions:**
- What advantages does pandas DataFrame provide over raw JSON dictionaries?
- Are there scenarios where you'd want to keep data as JSON instead of converting?
- How does the tabular structure of DataFrames limit or enable certain types of analysis?
- When combining data from multiple API calls (Task 6), what challenges arise?

### 3. **Real-World API Integration Scenarios**
**Guiding Questions:**
- How could a business use this brewery data? (e.g., market analysis, logistics, competitor research)
- What additional data would you need to combine with brewery data for meaningful insights?
- If you were building a brewery recommendation app, which endpoints would be most critical?
- How would you handle API downtime or errors in a production application?

### 4. **Data Quality & Validation**
**Guiding Questions:**
- Looking at the dataset (8,925+ breweries), what data quality issues might exist?
- Some breweries have `null` values for optional fields. How should your analysis handle missing data?
- The `brewery_type` field has specific allowed values (micro, nano, brewpub, etc.). Why enforce this constraint?
- If you found duplicate entries (same name + city + state), how would you decide which to keep?

### 5. **RESTful API Principles**
**Guiding Questions:**
- What makes this API "RESTful"?
- Why use `/breweries/{id}` instead of `/get_brewery?id={id}`?
- How do HTTP status codes (200, 404, 500) help communicate API state?
- What's the difference between query parameters (`?query=dog`) and path parameters (`/breweries/{id}`)?

---

## Challenge Activities

### Challenge 1: **The Brewery Geography Game** (15-20 min)
**Setup:** Groups of 3-4 students

**Rules:**
1. Each group gets a U.S. state at random
2. Using the API, teams compete to find:
   - **Most unique brewery type** in their state
   - **Longest brewery name** (character count)
   - **City with most breweries** in their state
   - **Weirdest brewery name** (subjective, voted on by class)
3. First team to complete all queries and present findings wins

**Learning Objective:** Practice filtering, aggregation, and exploratory data analysis under time pressure

**Bonus Round:** Find a brewery that exists in multiple states (franchise/chain) using creative search queries.

---

### Challenge 2: **API Response Time Race** (10-15 min)
**Setup:** Individual or pairs

**Task:**
Write the most efficient code to answer: **"Which state has the most breweries?"**

**Constraints:**
- Minimize number of API calls
- Minimize data transfer (use `per_page` wisely)
- Must verify answer programmatically (not by manual counting)

**Discussion After:**
- Compare approaches (e.g., `/meta` endpoint vs fetching all data)
- Discuss time complexity vs space complexity trade-offs
- Why does API efficiency matter in production?

---

### Challenge 3: **The Missing Data Detective** (15-20 min)
**Setup:** Groups of 2-3 students

**Scenario:**
You're building a brewery map application. Users need complete location data (latitude, longitude, address).

**Task:**
1. Query the API to find breweries with **missing location data** (`null` coordinates)
2. Count how many breweries are "unmappable"
3. Identify which states/cities have the most missing data
4. Propose a solution: How would you handle these breweries in your app?

**Deliverable:**
- Pandas DataFrame showing breweries with incomplete location data
- Summary statistics by state
- 2-minute presentation of findings

---

### Challenge 4: **Build Your Own Endpoint** (20-25 min)
**Setup:** Individual or pairs

**Scenario:**
You're pitching a new endpoint to add to the Brewery API.

**Task:**
1. Design a new endpoint (e.g., `/breweries/nearby`, `/breweries/stats`, `/breweries/compare`)
2. Define what parameters it accepts
3. Mock the expected JSON response format
4. Write Python code that would **consume** your endpoint (even though it doesn't exist yet)
5. Present your design to the class

**Learning Objective:** Think like an API designer, not just a consumer

---

### Challenge 5: **Data Validation Showdown** (15 min)
**Setup:** Groups compete head-to-head

**Task:**
Using the API, find and document **data quality issues**:
- Breweries with invalid phone numbers (too short/long)
- Breweries with missing required fields
- Breweries with mismatched state/postal code combinations
- Duplicate entries (same name + city)

**Scoring:**
- 1 point per unique data quality issue found
- 2 bonus points for writing validation code to detect it automatically
- 3 bonus points for proposing how to fix it programmatically

**Winner:** Group with most points after 15 minutes

---

### Challenge 6: **API Mashup** (Advanced - 25-30 min)
**Setup:** Groups of 3-4 students

**Task:**
Combine the Brewery API with **another public API** to create something interesting.

**Example Ideas:**
- Weather API: "Find breweries in cities with best weather this weekend"
- Google Maps API: "Calculate driving time between breweries for a brewery tour"
- Census API: "Correlate brewery density with population demographics"
- Twitter API: "Find most-mentioned breweries on social media"

**Deliverable:**
- Working code that calls both APIs
- Jupyter notebook showing results
- 3-minute demo to class

**Learning Objective:** Real-world applications combine multiple data sources

---

## Quick 5-Minute Activities (Class Warmups)

### Activity A: **Fastest Query**
Who can write a one-line query to get breweries in their hometown?

### Activity B: **Brewery Bingo**
Create bingo cards with brewery types, cities, or name patterns. Call out search results, students mark their cards.

### Activity C: **Error Code Theater**
Intentionally break API calls (wrong URL, bad parameters, timeout). Students diagnose the error from the output.

### Activity D: **JSON Prettify Contest**
Give students ugly JSON. Who can format it most readably in 2 minutes? (Practice for debugging)

---

## Discussion Debrief Questions (Post-Activity)

1. What was the hardest part of working with this API?
2. What did you learn about JSON structure that surprised you?
3. How would you explain APIs to someone non-technical?
4. What's one thing you'd change about this API's design?
5. Where else in your life do you interact with APIs without realizing it?
