# Open Brewery DB API - BADM 554

Self-hosted Open Brewery DB API for student use. Contains **8,925 breweries** from around the world.

## 🌐 Live API

**Base URL:** http://178.156.206.171:8000

**Interactive Docs:** http://178.156.206.171:8000/docs

## 🎓 For Students

### Using the API

See the [interactive documentation](http://178.156.206.171:8000/docs) for all endpoints and examples.

**Quick Examples:**

```python
import requests

# Get breweries in your city
response = requests.get("http://178.156.206.171:8000/breweries?by_city=Champaign&per_page=10")
breweries = response.json()

# Search for breweries
response = requests.get("http://178.156.206.171:8000/breweries/search?query=dog")
results = response.json()
```

### Contributing Data

**Found a missing brewery? Incorrect information?**

👉 [Submit a GitHub Issue](../../issues/new/choose)

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed instructions.

**Why contribute?**
- Help improve real-world open data
- Your contributions will be submitted to the official Open Brewery DB
- Learn about open-source collaboration
- Make the data better for everyone!

## 🚀 Quick Start

### Local Development
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Docker Deployment
```bash
docker-compose up -d
```

## 📚 API Endpoints

**Base URL:** `http://178.156.206.171:8000` (or `http://localhost:8000`)

### List Breweries
```
GET /breweries?by_city=Portland&by_state=Oregon&by_type=micro&per_page=50
```

**Parameters:**
- `by_city` - Filter by city (case insensitive)
- `by_country` - Filter by country
- `by_name` - Filter by brewery name
- `by_state` - Filter by state/province
- `by_postal` - Filter by postal code
- `by_type` - Filter by brewery type
- `page` - Page number (default: 1)
- `per_page` - Results per page (max 200, default: 50)

### Search Breweries
```
GET /breweries/search?query=dog&per_page=20
```

Searches across name, city, and state fields.

### Random Brewery
```
GET /breweries/random?size=5
```

Get 1-50 random breweries.

### Autocomplete
```
GET /breweries/autocomplete?query=dog
```

Returns brewery names for autocomplete (max 15 results).

### Get by ID
```
GET /breweries/{brewery_id}
```

### Metadata
```
GET /breweries/meta?by_state=California&by_type=micro
```

Returns count of breweries matching filters.

## 🍺 Brewery Types

- `micro` - Small-scale brewery (< 15,000 barrels/year)
- `nano` - Extremely small brewery (≤ 3 barrels per batch)
- `regional` - Regional brewery (15,000-6M barrels/year)
- `brewpub` - Brewery with attached restaurant
- `large` - Large brewery (> 6M barrels/year)
- `planning` - In planning stages
- `bar` - Bar selling others' beers
- `contract` - Brewery hiring another to produce
- `proprietor` - Brewery operating under another's license
- `closed` - Permanently closed brewery

## 📊 Data Format

Each brewery contains:
```json
{
  "id": "unique-uuid",
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
  "website_url": "https://example.com",
  "longitude": -88.2434,
  "latitude": 40.1164
}
```

## 🔧 Example Usage

### Python
```python
import requests

API_URL = "http://178.156.206.171:8000"

# Get breweries in Illinois
response = requests.get(f"{API_URL}/breweries?by_state=Illinois&per_page=50")
breweries = response.json()

for brewery in breweries:
    print(f"{brewery['name']} - {brewery['city']}, {brewery['state_province']}")
```

### JavaScript
```javascript
const API_URL = "http://178.156.206.171:8000";

// Fetch breweries
fetch(`${API_URL}/breweries?by_city=Portland&per_page=20`)
  .then(res => res.json())
  .then(breweries => {
    breweries.forEach(b => {
      console.log(`${b.name} - ${b.city}`);
    });
  });
```

### R
```r
library(httr)
library(jsonlite)

# Get breweries
url <- "http://178.156.206.171:8000/breweries?by_state=California&per_page=50"
response <- GET(url)
breweries <- fromJSON(content(response, "text"))

# Display results
head(breweries)
```

### cURL
```bash
# List breweries
curl "http://178.156.206.171:8000/breweries?by_city=Champaign"

# Search
curl "http://178.156.206.171:8000/breweries/search?query=dog"

# Random
curl "http://178.156.206.171:8000/breweries/random"
```

## 🚢 Deployment

### Hetzner VPS (Recommended - €4/month)
See [HETZNER_DEPLOYMENT.md](HETZNER_DEPLOYMENT.md) for complete setup guide.

**Quick deploy:**
```bash
./deploy.sh YOUR_SERVER_IP
```

### Other Platforms
- **Railway**: `railway up`
- **Fly.io**: `fly launch`
- **DigitalOcean**: Deploy from GitHub

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Student Contributions:**
1. [Add a new brewery](../../issues/new?template=add-brewery.md)
2. [Update brewery info](../../issues/new?template=update-brewery.md)
3. [Report closed brewery](../../issues/new?template=remove-brewery.md)

**Upstream Sync:**
See [UPSTREAM_SYNC.md](UPSTREAM_SYNC.md) for submitting student contributions to the official Open Brewery DB.

## 📦 Project Structure

```
badm554-api/
├── main.py                 # FastAPI application
├── breweries.json          # Brewery database (8,925 entries)
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose for simple deployment
├── docker-compose-caddy.yml  # Production deployment with Caddy
├── Caddyfile              # Caddy reverse proxy config
├── deploy.sh              # Quick deployment script
├── .github/
│   ├── ISSUE_TEMPLATE/    # Student submission templates
│   │   ├── add-brewery.md
│   │   ├── update-brewery.md
│   │   └── remove-brewery.md
│   └── workflows/
│       └── validate-breweries.yml  # Data validation
├── CONTRIBUTING.md        # Contribution guidelines
├── HETZNER_DEPLOYMENT.md  # Hetzner VPS deployment guide
├── UPSTREAM_SYNC.md       # Sync workflow with Open Brewery DB
└── README.md              # This file
```

## 🎯 Course Learning Objectives

This project teaches:
- **API Usage**: REST API concepts and HTTP methods
- **Data Quality**: Verifying and validating real-world data
- **Open Source**: Contributing to public datasets
- **Git/GitHub**: Version control and collaboration
- **Data Formats**: JSON, CSV, and data transformation
- **Documentation**: Writing clear technical documentation

## 🔗 Resources

- **Live API**: http://178.156.206.171:8000
- **API Docs**: http://178.156.206.171:8000/docs
- **Official Open Brewery DB**: https://www.openbrewerydb.org
- **Upstream Repo**: https://github.com/openbrewerydb/openbrewerydb

## 📊 Performance

- **Dataset Size**: ~3.2 MB JSON
- **Total Breweries**: 8,925
- **No Database Required**: In-memory data
- **Concurrent Users**: 50+ supported
- **CORS**: Enabled for browser access
- **Response Time**: < 100ms for most queries

## 📄 License

- **Code**: MIT License
- **Data**: [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) (Public Domain)

## 🙏 Acknowledgments

- Data from [Open Brewery DB](https://www.openbrewerydb.org/)
- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Hosted on [Hetzner Cloud](https://www.hetzner.com/cloud)

---

**Course:** BADM 554 | **Semester:** Fall 2025 | **Institution:** University of Illinois
