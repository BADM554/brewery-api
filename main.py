from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import json
import random
from typing import Optional, List, Union

app = FastAPI(
    title="Open Brewery DB API",
    description="""
    ## Open Brewery DB API - Self-Hosted for BADM 554

    Free dataset of breweries, cideries, brewpubs, and bottleshops.

    ### Dataset
    * Total Breweries: 8,925+
    * Coverage: Primarily United States with international breweries
    * Data includes: Name, location, type, contact info, coordinates

    ### Official Documentation
    Compatible with [Open Brewery DB API](https://www.openbrewerydb.org/documentation)

    ### Brewery Types
    * `micro` - Small-scale brewery (less than 15,000 barrels/year)
    * `nano` - Extremely small brewery (3 barrels or less)
    * `regional` - Regional brewery (between 15,000-6,000,000 barrels/year)
    * `brewpub` - Brewery with attached restaurant
    * `large` - Large brewery (over 6,000,000 barrels/year)
    * `planning` - Brewery in planning stages
    * `bar` - Bar selling others' beers
    * `contract` - Brewery hiring another to produce their beer
    * `proprietor` - Brewery operating under another's license
    * `closed` - Permanently closed brewery
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/documentation"
)

# Enable CORS for student access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load brewery data at startup
with open("breweries.json", "r") as f:
    breweries_data = json.load(f)

@app.get("/", include_in_schema=False)
def root():
    """Redirect to API documentation"""
    return RedirectResponse(url="/docs")

@app.get("/v1/breweries", tags=["Breweries"])
@app.get("/breweries", tags=["Breweries"])
def list_breweries(
    by_city: Optional[str] = Query(None, description="Filter by city (case insensitive)"),
    by_country: Optional[str] = Query(None, description="Filter by country (case insensitive)"),
    by_name: Optional[str] = Query(None, description="Filter by brewery name (case insensitive)"),
    by_state: Optional[str] = Query(None, description="Filter by state/province (case insensitive)"),
    by_postal: Optional[str] = Query(None, description="Filter by postal code"),
    by_type: Optional[str] = Query(None, description="Filter by brewery type (micro, nano, regional, brewpub, large, planning, bar, contract, proprietor, closed)"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    per_page: int = Query(50, ge=1, le=200, description="Number of breweries per page (max 200)")
):
    """
    List breweries with optional filters and pagination.

    Compatible with Open Brewery DB API v1 specification.

    **Examples:**
    * All breweries: `/breweries?per_page=50`
    * By city: `/breweries?by_city=Portland`
    * By state: `/breweries?by_state=California`
    * By type: `/breweries?by_type=micro`
    * Combined: `/breweries?by_city=Denver&by_type=brewpub&per_page=20`
    """
    results = breweries_data

    if by_city:
        results = [b for b in results if by_city.lower() in b.get("city", "").lower()]

    if by_country:
        results = [b for b in results if by_country.lower() in b.get("country", "").lower()]

    if by_name:
        results = [b for b in results if by_name.lower() in b.get("name", "").lower()]

    if by_state:
        results = [b for b in results if by_state.lower() in b.get("state_province", "").lower()]

    if by_postal:
        results = [b for b in results if by_postal in b.get("postal_code", "")]

    if by_type:
        results = [b for b in results if by_type.lower() == b.get("brewery_type", "").lower()]

    start = (page - 1) * per_page
    end = start + per_page

    return results[start:end]

@app.get("/v1/breweries/random", tags=["Breweries"])
@app.get("/breweries/random", tags=["Breweries"])
def get_random_breweries(
    size: int = Query(1, ge=1, le=50, description="Number of random breweries to return (max 50)")
):
    """
    Get random brewery(ies).

    Compatible with Open Brewery DB API v1 specification.

    **Examples:**
    * Single random: `/breweries/random`
    * Multiple random: `/breweries/random?size=5`
    """
    if size == 1:
        return random.choice(breweries_data)
    return random.sample(breweries_data, min(size, len(breweries_data)))

@app.get("/v1/breweries/search", tags=["Search"])
@app.get("/breweries/search", tags=["Search"])
def search_breweries(
    query: str = Query(..., description="Search term for brewery name, city, or state"),
    per_page: int = Query(50, ge=1, le=200, description="Number of results per page (max 200)")
):
    """
    Search breweries by name, city, or state.

    Compatible with Open Brewery DB API v1 specification.

    **Examples:**
    * Search by name: `/breweries/search?query=dog`
    * Search any field: `/breweries/search?query=Portland`
    """
    query_lower = query.lower()
    results = [
        b for b in breweries_data
        if query_lower in b.get("name", "").lower()
        or query_lower in b.get("city", "").lower()
        or query_lower in b.get("state_province", "").lower()
    ]
    return results[:per_page]

@app.get("/v1/breweries/autocomplete", tags=["Search"])
@app.get("/breweries/autocomplete", tags=["Search"])
def autocomplete_breweries(
    query: str = Query(..., description="Autocomplete search term")
):
    """
    Autocomplete brewery names (returns max 15 results).

    Compatible with Open Brewery DB API v1 specification.

    **Example:**
    * `/breweries/autocomplete?query=dog`
    """
    query_lower = query.lower()
    results = [
        {"id": b["id"], "name": b["name"]}
        for b in breweries_data
        if query_lower in b.get("name", "").lower()
    ]
    return results[:15]

@app.get("/v1/breweries/meta", tags=["Metadata"])
@app.get("/breweries/meta", tags=["Metadata"])
def get_metadata(
    by_city: Optional[str] = Query(None, description="Filter by city"),
    by_country: Optional[str] = Query(None, description="Filter by country"),
    by_state: Optional[str] = Query(None, description="Filter by state"),
    by_type: Optional[str] = Query(None, description="Filter by type")
):
    """
    Get metadata about breweries (count and filters).

    Compatible with Open Brewery DB API v1 specification.

    **Example:**
    * `/breweries/meta?by_state=California&by_type=micro`
    """
    results = breweries_data

    if by_city:
        results = [b for b in results if by_city.lower() in b.get("city", "").lower()]
    if by_country:
        results = [b for b in results if by_country.lower() in b.get("country", "").lower()]
    if by_state:
        results = [b for b in results if by_state.lower() in b.get("state_province", "").lower()]
    if by_type:
        results = [b for b in results if by_type.lower() == b.get("brewery_type", "").lower()]

    return {"total": len(results)}

@app.get("/v1/breweries/{brewery_id}", tags=["Breweries"])
@app.get("/breweries/{brewery_id}", tags=["Breweries"])
def get_brewery(brewery_id: str):
    """
    Get a single brewery by ID.

    Compatible with Open Brewery DB API v1 specification.

    **Example:**
    * `/breweries/5128df48-79fc-4f0f-8b52-d06be54d0cec`
    """
    for brewery in breweries_data:
        if brewery.get("id") == brewery_id:
            return brewery

    raise HTTPException(status_code=404, detail="Brewery not found")

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "breweries_loaded": len(breweries_data)}
