# itmagazines-webscraper

This libraly is a web scraper for web pages of following IT-Magazines.

## Support magazine list

* 技術評論社
    * Software Design
    * WEB+DB PRESS
* CQ出版
    * Interface
    * トランジスタ技術
* 日経BP
    * 日経ソフトウエア
    * 日経Linux

## Installaction

```console
$ python -m pip install itmagazines-webscraper
```

## Usage

### Specify a magazine and execute
```python
from pprint import pprint
from itmagazines_webscraper import ItMagazineType, scrape_magazine

magazines = scrape_magazine(ItMagazineType.SOFTWARE_DESIGN)
for magazine in magazines:
    pprint(magazine.get_dict())
    print(magazine.get_json())
```

### Execute all
```python
from pprint import pprint
from itmagazines_webscraper import scrape_magazines

magazines = scrape_magazines()
for magazine in magazines:
    pprint(magazine.get_dict())
    print(magazine.get_json())
```

### Example: Retuned json data
```json
{
  "name": "日経Linux",
  "number": "日経Linux20XX年X月号",
  "price": "XXXX円",
  "release_date": "20XX年X月X日",
  "url": "https://info.nikkeibp.co.jp/media/LIN/",
  "top_outlines": [
    "【特集1】Linux学び直し",
    "【特集2】Linux導入・活用法まで徹底紹介！"
  ],
  "store_links": [
    {
      "name": "Amazon",
      "link": "https://www.amazon.co.jp/dp/xxxxx"
    },
    {
      "name": "Rakutenブックス",
      "link": "https://books.rakuten.co.jp/rb/yyyyy/"
    }
  ]
}
```

## Data structure

|Detail|Summary|
|------|-------|
|name|Magazine name.|
|number|Magazine name and volume number.|
|price|Price.|
|release_datee|Release date.|
|url|URL of web page.|
|top_outlines|Magazine outline list.|
|store_links|Store link list.|

### store_links
|Detail|Summary|
|------|-------|
|name|Store name.|
|url|URL of store web page.|
