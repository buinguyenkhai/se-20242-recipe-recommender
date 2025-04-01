### Scraping everything:
```sh
scrapy crawl vaobep -O output_test/vaobep.json
```

### Scraping a category (example: mon-kem):
```sh
scrapy crawl vaobep -O output_test/vaobep.json -a category=mon-kem
```