# Ouedkniss Car Parts Scraper

A small, standalone Scrapy-based scraper that extracts car parts ("pieces_detachees") announcements from Ouedkniss via their GraphQL API and saves the results to a JSON file (`ouedkniss_cars.json`).

## Key points

- The project is a single-file Scrapy spider (`ouedkniss_scraper.py`) that uses `CrawlerProcess` to run a spider programmatically.
- It queries Ouedkniss' GraphQL endpoints to fetch listing pages, announcement details, phone numbers, comments and reaction/view counts.
- Output: `ouedkniss_cars.json` (JSON lines / pretty-printed JSON as configured in the script).

## Requirements

- Python 3.8+ (3.7 may work but 3.8+ is recommended)
- pip
- The Python packages listed in `requirements.txt` (at minimum `scrapy`).

If you see import errors for `itemloaders`, install it as well:

```cmd
pip install itemloaders
```

## Installation

1. Clone or download this repository.
2. (Recommended) Create and activate a virtual environment.
3. Install dependencies:

```cmd
pip install -r requirements.txt
```

## Usage (Windows cmd)

Run the script directly with Python. The script prompts for three inputs: the listing URL, the first page number and the last page number.

Example (in Command Prompt):

```cmd
cd "c:\Users\benso\Desktop\portfolio projects info & testing\ouedkniss scraper"
python ouedkniss_scraper.py

# When prompted, enter values such as:
# Paste your URL : https://www.ouedkniss.com/pieces_detachees/1
# Enter the first page id : 1
# Enter the last page id : 3
```

After the spider finishes, the output file `ouedkniss_cars.json` will be created/overwritten in the same folder.

Notes:

- The script currently uses interactive prompts to receive inputs. If you prefer automating runs, consider converting the script to accept CLI arguments or running it as a proper Scrapy project/spider.
- The script enables HTTPCACHE in its `CrawlerProcess` settings and allows HTTP 404 responses (see settings inside `ouedkniss_scraper.py`).

## Project structure

```
ouedkniss_scraper.py    # Main Scrapy spider + runnable __main__ harness
requirements.txt        # Python dependencies (contains `scrapy`)
ouedkniss_cars.json     # Output file produced by the scraper (after running)
README.md               # This file
```

## Troubleshooting

- If you get an import error for `scrapy` or other packages, double-check your virtual environment and re-run `pip install -r requirements.txt`.
- If GraphQL responses or endpoints change on the site, the spider may need updates to the payloads and parsing logic.

## Contributing

Small patches or fixes are welcome. Suggested low-risk improvements:

- Add CLI argument support (argparse) instead of interactive prompts.
- Add a small unit or integration test that validates the payload builders.
- Add logging configuration and a --limit flag for quick tests.

## License

This repository is provided for educational purposes. See the project `LICENSE` (if added) for details.
