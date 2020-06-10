## Getting Started
- You must have been installed the python (>3.6) and also it's pip3 in your machine.
- You must download the chrome-webdriver at https://chromedriver.chromium.org/downloads.
*How am I choosing the webdriver version?* It depends on chrome version that installed in your machine (open this URL in from your chrome: [chrome://settings/help](chrome://settings/help "chrome://settings/help")).
- Download this project.
- Install the dependencies by executing:
```
pip3 install -r requirements.txt
```
- Extract the chrome-webdriver that you have been downloaded into the root project directory.
- That's all.

## Usage & Example
- Usage
```bash
usage: scraping-tools-v2.py [-m MODE] [-u URL] [-t TOTAL_PAGE] [-o OUTPUT]
```
- This tool divided by 2 modes, by search, and by a specific shop
- An example to run by search mode:
```bash
python3 scraper-tool.py \
	--mode=search \
	--url="https://www.tokopedia.com/search?st=product&q=kopi" \
	--output=kopi \
	--total_page=2
```
- And by specific shop you can execute:
```bash
python3 scraper-tool.py \
	--mode=shop \
	--url="https://www.tokopedia.com/growbuysurabaya" \
	--output=growbuysurabaya \
```
- All output will be exported as a CSV file on your root project directory.

## Limitation
- On the shop mode, this tool will be crawling all products, you cannot specify how many pages will be downloaded.
- Scope of data that will be gathered is:
> title, rating, price, total_reviewer, total_sold, seen_counter, weight, weight_unit, shop_name, shop_region, is_power_merchant


