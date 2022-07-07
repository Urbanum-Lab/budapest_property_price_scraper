# Scrape square meter prices [Kludgery]
This project tries to scrape square meter
prices in Budapest. Its source is the
biggest real estate site in Hungary.

The scraper collects only the address and
the square meter prices for each listing.

## How to use the scraper
- you need python 3.9+ on your system
- use `pipenv` to install the requirements
- run `src/utils/get_proxies.py` to get a list
of free proxies
- run `src/ingatlan.py` to collect data for flats
and houses in Budapest
- run the script several times, so you get most of the ads
- use `run-one-constantly` to automate the process
- check the number of unique lines `sort ingatlan_sqrm_price_more.tsv | uniq -c | wc -l`
- save a deduplicated version `sort ingatlan_sqrm_price_more.tsv | uniq -c > unique.tsv`
- run `src/geocoding.py` on the deduped tsv to get
lat long data and clean up the tsv
- `geocoding.py` aggregates square meter prices
on various h3 resolutions

## Warning
- This code comes with absolutely no warranty!
- This is a quick and dirty solution
- You should configure selenium on your machine
on your own
- Maybe you should adjust the number of workers
according to the capabilities of your hardware