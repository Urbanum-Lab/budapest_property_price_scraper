# Scrape square meter prices
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

## Warning
- This code comes with absolutely no warranty!
- This is a quick and dirty solution
- You should configure selenium on your machine
on your own
- Maybe you should adjust the number of workers
according to the capabilities of your hardware