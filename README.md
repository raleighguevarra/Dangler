# Dangling Domain Finder

Dangling Domain Finder is a Python tool designed to identify and report dangling or inactive subdomains for a given domain. This tool is particularly useful for cybersecurity professionals and enthusiasts for reconnaissance and security assessments.

## Features

- Fetch subdomains from crt.sh.
- Check each subdomain for DNS resolution to determine if it's active or dangling.
- Multithreaded checks for faster processing.
- Summary metrics including total time taken, total subdomains checked, and counts of active vs. dangling subdomains.
- Outputs results in a clean, tabular format for easy reading.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher installed on your system.
- Access to the internet for fetching subdomain data and performing DNS resolutions.

## Installation

Clone the project repository to your local machine:

```bash
git clone https://github.com/yourusername/dangling-domain-finder.git
cd dangling-domain-finder
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage

To use Dangling Domain Finder, run the following command from the terminal, replacing `example.com` with the domain you wish to check:

```bash
python dangler.py example.com
```

### Optional Arguments

- `-s` or `--show`: Display all discovered subdomains in the output.
- `-o <filename>` or `--output <filename>`: Output results to a specified CSV file.

Example with optional arguments:

```bash
python dangler.py example.com -s -o results.csv
```

## Contributing

Contributions to the Dangling Domain Finder are welcome. If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

Don't forget to give the project a star! Thanks again!

## License

Distributed under the MIT License. See `LICENSE` for more information.