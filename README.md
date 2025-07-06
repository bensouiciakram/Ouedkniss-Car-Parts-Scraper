# Ouedkniss Car Parts Scraper

A web scraping tool designed to extract car parts information from Ouedkniss, an Algerian automotive marketplace.

## Features

- **Automated Data Extraction**: Scrapes car parts listings from Ouedkniss
- **Comprehensive Data Collection**: Extracts product details, prices, descriptions, and contact information
- **Error Handling**: Robust error handling and retry mechanisms
- **Data Export**: Exports scraped data in structured formats
- **Type Safety**: Full type annotations for better code maintainability

## Requirements

- Python 3.7+
- Selenium WebDriver
- Chrome browser
- Required Python packages (see requirements.txt)

## Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Download ChromeDriver and ensure it's in your PATH

## Usage

Run the main scraper:
```bash
python ouedkniss_scraper.py
```

## Project Structure

```
Ouedkniss Car Parts Scraper/
├── ouedkniss_scraper.py    # Main scraper script
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── .gitignore            # Git ignore rules
```

## Configuration

The scraper can be configured by modifying the constants at the top of `ouedkniss_scraper.py`:
- Search URLs
- Output file paths
- Scraping delays
- Data extraction patterns

## Output

The scraper generates structured data files containing:
- Product titles
- Prices
- Descriptions
- Contact information
- URLs
- Timestamps

## Error Handling

The scraper includes comprehensive error handling for:
- Network timeouts
- Page loading failures
- Element not found errors
- Data extraction failures

## Contributing

When contributing to this project:
1. Follow the existing code style
2. Add type annotations to new functions
3. Include comprehensive docstrings
4. Test your changes thoroughly

## License

This project is for educational and research purposes only. 