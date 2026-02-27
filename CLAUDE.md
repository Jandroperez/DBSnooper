# CLAUDE.md — DBSnooper

This file provides context for AI assistants working in this repository.

## Project Overview

DBSnooper is a Python-based research tool for discovering exposed databases in the wild using the [Shodan](https://www.shodan.io/) API. It was built for educational/research purposes to demonstrate the risks of misconfigured databases publicly accessible on the internet. The primary interface is a Jupyter notebook (`DBSnooper.ipynb`), backed by reusable Python utility modules in `src/`.

**Author:** Alex (Alejandro) Perez
**License:** Not specified

---

## Repository Structure

```
DBSnooper/
├── DBSnooper.ipynb        # Main Jupyter notebook (primary interface)
├── DBSnooper.py           # Standalone Python script entry point
├── README.md              # User-facing setup guide
├── requirements.txt       # Python dependencies
└── src/
    ├── auth.yaml          # API credentials (must be populated by user; never commit secrets)
    ├── Constants.py       # Project-level constants (description string)
    ├── ShodanUtils.py     # Shodan API wrapper and DataFrame parser
    └── VisualizationUtils.py  # Map and chart generation utilities
```

---

## Key Modules

### `src/ShodanUtils.py`

Contains the `Shodan` class (all class methods — no instantiation needed).

| Method | Signature | Description |
|---|---|---|
| `Shodan_Search` | `(searchTerm, facets='')` | Queries the Shodan REST API; returns a parsed DataFrame |
| `ShodanParser` | `(QueryData)` | Normalizes Shodan JSON `matches` into a Pandas DataFrame |

**DataFrame columns returned by `ShodanParser`:**
- `ip_str` — IP address string
- `port` — exposed port
- `org` — organization name
- `asn` — autonomous system number
- `isp` — internet service provider
- `product` — detected product/service
- `location.country_name` — country
- `location.latitude` / `location.longitude` — geographic coordinates

**API key loading:** On import, `ShodanUtils.py` reads `src/auth.yaml` relative to `os.getcwd()`. The script must be run from the project root, or the CWD must be set appropriately before importing.

### `src/VisualizationUtils.py`

Contains two classes, both using class methods only.

**`ShodanMap`**

| Method | Signature | Description |
|---|---|---|
| `BuildMap` | `(Dataframe, latitude_column, longitude_column)` | Returns a Folium interactive map with markers for each row |

- Filters rows with null lat/lon before rendering.
- Popup HTML includes: IP, port, ISP, organization.

**`Graph`**

| Method | Signature | Description |
|---|---|---|
| `Bar_Graph` | `(Dataframe='', y_axis='')` | Returns an Altair bar chart of the top 10 value counts for the given column |

### `src/Constants.py`

Holds a single `description` string variable used as a CLI/script description.

### `src/auth.yaml`

```yaml
# Credentials
shodanApiKey: <YOUR_API_KEY_HERE>
```

**Never commit a populated `auth.yaml`.** This file holds the Shodan API key and must remain empty in version control.

---

## Setup & Running

### Prerequisites

- Python 3.x
- A [Shodan](https://www.shodan.io/) account with an API key

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure credentials

Edit `src/auth.yaml` and add your Shodan API key:

```yaml
shodanApiKey: your_api_key_here
```

### Run the notebook (recommended)

```bash
jupyter notebook DBSnooper.ipynb
# or
jupyter lab DBSnooper.ipynb
```

### Run the standalone script

```bash
python DBSnooper.py
```

> **Note:** `DBSnooper.py` is incomplete — the argument parser section is stubbed out and the script currently hardcodes a search for `"Elastic"`. All production usage goes through the notebook.

---

## Dependencies

| Package | Purpose |
|---|---|
| `pandas` | DataFrame manipulation, JSON normalization |
| `numpy` | Numerical operations |
| `folium` | Interactive Leaflet.js maps in Jupyter |
| `altair` | Declarative Vega-Lite charts |
| `requests` | HTTP calls to Shodan REST API |
| `notebook` | Jupyter Notebook server |
| `jupyterlab` | JupyterLab UI |
| `pyyaml` | Parsing `auth.yaml` credentials |
| `colorama` | Terminal color output (imported in ShodanUtils but not actively used) |

---

## Conventions & Patterns

### Coding Style

- Class names: `PascalCase` (e.g., `Shodan`, `ShodanMap`, `Graph`)
- Method names: `PascalCase` with underscores for readability (e.g., `Shodan_Search`, `BuildMap`, `Bar_Graph`)
- Variable names: `PascalCase` for local variables (non-standard — maintain this pattern for consistency)
- All utility methods are `@classmethod`; do not instantiate utility classes
- Comments use `# *===` section headers for visual separation
- Docstrings follow a Description / Parameters / Returns structure

### Error Handling

- `ShodanUtils.Shodan_Search` catches `requests.RequestException` and prints the error
- `VisualizationUtils` methods use bare `except` clauses returning error strings — keep this pattern; do not raise in visualization code
- `ShodanParser` does **not** validate whether `matches` exists in the response — if the API key is invalid or the response structure changes, this will raise a `KeyError`

### File Paths

- `ShodanUtils.py` constructs the path to `auth.yaml` using `os.getcwd() + '/src/auth.yaml'`
- Always run scripts from the project root directory

### Secrets Management

- **Never** commit a Shodan API key to `src/auth.yaml` or anywhere else
- The file is not in `.gitignore` — be careful when staging changes to `src/auth.yaml`

---

## What Does Not Exist (Yet)

- No unit tests or test framework
- No `.gitignore` (be mindful of committing `__pycache__/`, `.DS_Store`, or secrets)
- No CI/CD pipeline
- No CLI argument parsing (stubbed in `DBSnooper.py`)
- No error handling for missing/invalid API key at startup
- No `setup.py` or `pyproject.toml`

---

## Development Notes for AI Assistants

- The primary artifact is `DBSnooper.ipynb`. Most analysis and output lives there.
- `DBSnooper.py` is a secondary entry point that is incomplete.
- When modifying `ShodanUtils.py`, ensure the `ShodanParser` column list stays in sync with what `VisualizationUtils.py` expects (especially `ip_str`, `port`, `isp`, `org`, `location.latitude`, `location.longitude`).
- Avoid adding dependencies without updating `requirements.txt`.
- Do not pin dependency versions unless a specific version is required — current `requirements.txt` uses unpinned package names.
- The Shodan free-tier API key is rate-limited; do not add code that makes bulk or repeated API calls in loops without awareness of this.
- Do not add or modify `src/auth.yaml` values in commits.
