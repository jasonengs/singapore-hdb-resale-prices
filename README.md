# HDB Resale Price Dashboard

An interactive analytics dashboard for exploring Singapore HDB resale flat transactions. Fetches data from public APIs, geocodes addresses, enriches records with nearby MRT stations, and presents the results through a browser-based dashboard with maps, charts, and filterable tables.

---

## Overview

- Fetches resale transaction records from [data.gov.sg](https://data.gov.sg)
- Geocodes flat addresses via the Google Maps Geocoding API
- Enriches records with nearby MRT stations via the Google Maps Places API
- Cleans and transforms raw data into analysis-ready datasets
- Serves an interactive Dash dashboard with views for trends, distributions, rankings, correlations, comparisons, choropleth maps, and scatter maps

> **Pre-fetched data is included under `data/`.** You can skip ingestion entirely and go straight to running the dashboard unless you need fresh data.

> Clean data is also available on [HuggingFace](https://huggingface.co/datasets/jasonengs/singapore_hdb_resale_prices).
---

## Preview

<!-- ![Dashboard](assets/preview.png) -->
![Trend](assets/preview_trend.png)
![Distribution and Correlation](assets/preview_distribution_correlation.png)
![Ranking and Comparison](assets/preview_ranking_comparison.png)
![Map](assets/preview_map.png)
![Table](assets/preview_table.png)



---

## Prerequisites

| Requirement | Version |
|---|---|
| Python | >=3.11 |
| [uv](https://docs.astral.sh/uv/) | Latest |
| Node.js + npm | For TailwindCSS CLI |

**Optional — only needed to refresh data:**

| Service | Used for | Cost |
|---|---|---|
| [data.gov.sg API](https://data.gov.sg/developer) | HDB resale, price index, geo, and MRT records | Free |
| [Google Maps Geocoding API](https://developers.google.com/maps/documentation/geocoding) | Geocoding flat addresses | Free up to 10,000 requests/month |
| [Google Maps Places API](https://developers.google.com/maps/documentation/places) | MRT station lookup | **Paid** — charges apply per request |

---

## Installation

### 1. Clone the repo

```bash
git clone https://github.com/jasonengs/singapore-hdb-resale-prices.git
cd hdb-resale
```

### 2. Install Python dependencies

```bash
uv sync
uv run pip install -e .
```

### 3. Install Node dependencies (TailwindCSS)

```bash
npm install
```

---

## Environment Variables

Create a `.env` file in the project root. API keys are only required if you intend to re-ingest data.

```env
# Required only for data ingestion / refresh
DATA_GOV_API_KEY="YOUR_DATA_GOV_SG_API_KEY"
GOOGLE_MAPS_API_KEY="YOUR_GOOGLE_MAPS_API_KEY"

# Required for Font Awesome icons in the dashboard
FONT_AWESOME_KIT="YOUR_FONTAWESOME_KIT_ID"
```

---

## Running Locally

### 1. Build TailwindCSS

The dashboard requires a compiled `styles.css`. Run the watcher during development.

```bash
npm run dev
```

Reads from `src/dashboard/assets/input.css` → writes to `src/dashboard/assets/styles.css`.

> See the [TailwindCSS CLI docs](https://tailwindcss.com/docs/installation/tailwind-cli) for further reference.

### 2. Start the app

```bash
uv run python src/main.py
```

Open `http://localhost:8050` in your browser.

---

## Data Ingestion (Optional)

Skip this section if you are using the pre-fetched data in `data/`.


| Script | Command | Source | Output |
|---|---|---|---|
| `ingestion/flat.py` | `uv run src/ingestion/flat.py` | data.gov.sg HDB resale API | `data/latest_data.csv` |
| `ingestion/address.py` | `uv run src/ingestion/address.py` | Google Maps Geocoding API | `data/address.csv` |
| `ingestion/mrt.py` | `uv run src/ingestion/mrt.py` | Google Maps Places API | `data/mrt.csv` |
| `ingestion/price_index.py` | `uv run src/ingestion/price_index.py` | data.gov.sg | `data/resale_price_index.csv` |
| `ingestion/geo.py` | `uv run src/ingestion/geo.py` | data.gov.sg | `data/pln_area.geojson`, `data/region.geojson` |

---

## Project Structure

```
root/
├── data/                        # Raw and processed data files
│   ├── address.csv
│   ├── latest_data.csv
│   ├── train.csv
│   ├── pln_area.geojson
│   ├── region.geojson
│   └── resale_price_index.csv
├── notebook/
│   ├── data_cleaning.ipynb
│   └── data_visualization.ipynb
└── src/
    ├── core/                    # Shared utilities (config, paths, transforms)
    ├── dashboard/
    │   ├── assets/              # input.css (Tailwind source) → styles.css (compiled)
    │   ├── callbacks/           # Dash callbacks per chart type
    │   ├── components/          # Reusable UI components (cards, dropdowns, tables)
    │   ├── datasets/            # Data loading and geo helpers
    │   ├── metrics/             # Metric formatters and lookups
    │   ├── models/              # Pydantic types for KPI data
    │   ├── transforms/          # Aggregations, enrichment, filters
    │   ├── viz/                 # Plotly figure builders per chart type
    │   ├── app.py
    │   └── layout.py
    ├── ingestion/               # API fetchers
    ├── schemas/                 # Pydantic validation models
    └── main.py
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | [Python](https://www.python.org/) |
| Package manager | [uv](https://docs.astral.sh/uv/) |
| Dashboard framework | [Dash](https://dash.plotly.com/) + [Dash AG Grid](https://dash.plotly.com/dash-ag-grid) |
| Charts | [Plotly](https://plotly.com/python/) |
| Geospatial | [GeoPandas](https://geopandas.org/), [GeoPy](https://geopy.readthedocs.io/) |
| Styling | [TailwindCSS](https://tailwindcss.com/) (CLI), [Font Awesome](https://fontawesome.com/) |
| Data | [pandas](https://pandas.pydata.org/docs/), [NumPy](https://numpy.org/doc/stable/) |
| Validation | [Pydantic](https://pydantic.dev/docs/) |
| HTTP | [AIOHTTP](https://docs.aiohttp.org/en/stable/), [aiolimiter](https://aiolimiter.readthedocs.io/en/stable/) |
| Config | [python-dotenv](https://github.com/theskumar/python-dotenv) |

---

## Dashboard Views

| View | Description |
|---|---|
| **KPIs** | Four summary cards — median price, transaction count, median price per sqm, and median lease — each showing the current value alongside year-on-year change. |
| **Trends** | Two line charts: monthly median resale price for recent movements, and a long-run historical median price for broader context. |
| **Distribution** | a dropdown between a box plot (resale price spread by flat type) and a bar chart (median resale price by flat type), giving both a distributional and a point-estimate view. |
| **Correlation** | Scatter plot of resale price against a selected metrics — floor area (sqm), remaining lease, or distance to MRT — color-coded by flat type to surface segment-level patterns. |
| **Ranking** | Top-5 and bottom-5 planning areas ranked by a selected metric — median price, transaction count, median remaining lease. |
| **Comparison** | Tornado/butterfly chart comparing the previous year against a selected year for a chosen metric — median price, transaction count, median remaining lease. |
| **Maps** | Two map types: a choropleth map aggregated by planning area or region, and a scatter map plotting individual addresses alongside MRT stations — both colored by a selected metric (median price, transaction count, median remaining lease). |
| **Table** | Full transaction-level data in an AG Grid table — sortable, filterable, and paginated. |

---

## Notebooks
 
The `notebook/` directory contains Jupyter notebooks for ad-hoc exploration:

| Notebook | Purpose |
|---|---|
| `data_cleaning.ipynb` | Inspect and clean raw data |
| `data_visualization.ipynb` | Exploratory plots outside the dashboard |

---

## Known Limitations

- **Google Maps Places API is not free.** Each MRT lookup incurs a charge. Review your usage and billing limits before running a full re-ingestion.
- **Google Maps Geocoding API** is free up to 10,000 requests per month. Exceeding this threshold will incur charges.
- **Google Maps API restrictions** (referrer, IP, or key scope) may block requests during ingestion if your API key is not configured for server-side use.
- **Rate limiting:** API calls are throttled via `aiolimiter`; a full re-ingestion takes time.
- **Geocoding accuracy** depends on the address formatting in the source data.
- **Local use only:** The dashboard has no authentication or multi-user support.
