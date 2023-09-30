# Web-scraper
PubMed API website scraper 

# Requirements
```
pip install requests
pip install pandas
```
# Usage

```
usage: main.py "string" [options]

PubMed API scraper that collects paper information and stores them in a database

positional arguments:

  string               the string you would like to search (ideally keywords)

options:

  -h, --help           show this help message and exit
  
  --quantity           the number of papers you would like to retrieve, default 1000
  
  --all                retrieve all the papers
  
  --format {csv,json}  define the database format, default csv
  
  --score              compute relevance score for each paper

```
## example:
python main.py "cnn lung cancer" --quantity 200 --score

# license
This project is licensed under the MIT License.
