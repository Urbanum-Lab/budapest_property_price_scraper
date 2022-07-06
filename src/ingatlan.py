import random
import time
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

with open("src/utils/proxies.txt") as infile:
    proxies = infile.read().strip().split("\n")

proxies = list(set(proxies))
print(f"we have {len(proxies)} proxies")
# hardcoded & as ugly as hell
property_feats = {"lakas": 1368,
                  "haz": 372}


def get_page(url):
    proxy = random.choice(proxies)

    options = Options()
    # options.add_argument("--headless")
    options.add_argument(f"--proxy-server={proxy}")
    options.add_argument("--disable-notifications")
    options.add_argument("disable-infobars")
    driver = webdriver.Chrome(chrome_options=options)

    driver.get(url)
    time.sleep(random.randint(3, 7))
    html = driver.page_source
    driver.close()
    return html


def get_page_p(url):
    while True:
        try:
            return get_page(url)
        except Exception as e:
            continue


def get_page_data(page_url):
    try:
        if "lakas" in page_url:
            pt = "lakas"
        else:
            pt = "haz"
        page_at_i = get_page_p(page_url)
        soup = BeautifulSoup(page_at_i, "lxml")
        addresses = soup.find_all("div", {"class": "listing__address"})
        m2prices = soup.find_all("div", {"class": "price--sqm"})
        if addresses:
            addresses = [e.text.strip() for e in addresses]
        if m2prices:
            res = []
            m2prices = [e.text.strip() for e in m2prices]
            for e in zip(addresses, m2prices):
                o = e[0] + "\t" + e[1] + "\t" + pt + "\n"
                res.append(o)
            # print("\n".join(res))
            print("ok")
            return res
    except Exception as e:
        print("bad")
        pass


urls = []
for property_type, page_num in property_feats.items():
    print(property_type)
    for i in range(1, page_num+1):
        page_url = f"https://ingatlan.com/szukites/elado+{property_type}+budapest?page={i}"
        urls.append(page_url)

print(len(urls))

futures = []
with ThreadPoolExecutor(max_workers=55) as ex:
    for url in urls:
        futures.append(ex.submit(get_page_data, url))


with open("data/ingatlan_sqrm_price.tsv", "a") as outfile:
    for future in futures:
        res = future.result()
        if res:
            for e in res:
                outfile.write(e)
        else:
            print("none")
