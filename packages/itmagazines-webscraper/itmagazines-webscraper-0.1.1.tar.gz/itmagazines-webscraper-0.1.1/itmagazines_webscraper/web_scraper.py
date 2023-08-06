'''
IT-Magazines web scraping
'''

import json
import re
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List
import requests
from bs4 import BeautifulSoup, Tag

class ItMagazineType(Enum):
    '''
    IT-Magazine type
    '''
    # 技術評論社
    SOFTWARE_DESIGN = 1
    WEB_DB_PRESS = 2
    # CQ出版
    INTERFACE = 11
    TRANGISTOR_GIJUTSU = 12
    # 日経BP
    NIKKEI_SOFTWARE = 21
    NIKKEI_LINUX = 22

@dataclass
class ItMagazineStoreLink:
    '''
    IT-Magazine store-link data class
    '''
    name: str = ''
    url: str = ''

@dataclass
class ItMagazineData:
    '''
    IT-Magazine data class
    '''
    name: str
    number: str = ''
    price: str = ''
    release_date: str = ''
    url: str = ''
    top_outlines: List[str] = field(default_factory=list)
    store_links: List[ItMagazineStoreLink] = field(default_factory=list)

    def get_dict(self):
        '''
        get dict data
        '''
        return asdict(self)

    def get_json(self):
        '''
        get json data
        '''
        return json.dumps(self.get_dict(), indent=2, ensure_ascii=False)

def __get_soup(url: str) -> BeautifulSoup:
    '''
    get soup data from url
    '''
    html = requests.get(url, timeout=(3.0, 10.0))
    return BeautifulSoup(html.content, 'html.parser')

def __extract_magazine_number(_number: Tag) -> str:
    if _number is None:
        return ''
    _num_str = _number.get_text(strip=True)
    res = re.findall(r'\d{4}年\d{1,2}月号', _num_str)
    if len(res) > 0:
        return res[0]
    res = re.findall(r'Vol.\d{3}', _num_str)
    if len(res) > 0:
        return res[0]
    return ''

def __extract_year(_date: Tag) -> str:
    if _date is None:
        return ''
    _date_str = _date.get_text(strip=True)
    res = re.findall(r'\d{4}年', _date_str)
    if len(res) > 0:
        return res[0]
    return ''

def __extract_date(_date: Tag) -> str:
    if _date is None:
        return ''
    _date_str = _date.get_text(strip=True)
    res = re.findall(r'\d{4}年\d{1,2}月\d{1,2}日', _date_str)
    if len(res) > 0:
        return res[0]
    res = re.findall(r'\d{1,2}月\d{1,2}日', _date_str)
    if len(res) > 0:
        return res[0]
    res = re.findall(r'\d{4}/\d{1,2}/\d{1,2}', _date_str)
    if len(res) > 0:
        return res[0]
    return ''

def __extract_price(_price: Tag) -> str:
    if _price is None:
        return ''
    _price_str = _price.get_text(strip=True)
    res = re.findall(r'\d{1,3},?\d{1,3}円', _price_str)
    if len(res) > 0:
        return res[0]
    res = re.findall(r'[￥¥]\d{1,3},?\d{1,3}', _price_str)
    if len(res) > 0:
        return res[0]
    return ''

def __scrape_software_design() -> List[ItMagazineData]:
    _url = 'http://gihyo.jp/magazine/SD'
    magazine_datas: List[ItMagazineData] = []

    soup = __get_soup(_url)
    tag_links = soup.find('ul', class_='magazineNavigation')
    if tag_links is not None:
        tag_links = tag_links.find_all('a', string=re.compile('詳細|次号'))
    if tag_links is None:
        return magazine_datas
    for tag_link in tag_links:
        if tag_link is not None:
            _url = 'http://gihyo.jp' + tag_link.get('href')
        if _url is None:
            continue

        magazine_data = ItMagazineData(name='Software Design', url=_url)
        magazine_datas.append(magazine_data)
        soup2 = __get_soup(_url)
        _number = soup2.find('h1', string=re.compile('月号'))
        magazine_data.number = __extract_magazine_number(_number=_number)
        tag_salesinfo2 = soup2.find('div', id='publishedDetail')
        if tag_salesinfo2 is not None:
            tag_salesinfo2 = tag_salesinfo2.find('div', class_='information')
        if tag_salesinfo2 is not None:
            _price = tag_salesinfo2.find(string=re.compile('定価'))
            magazine_data.price = __extract_price(_price=_price)
            _release_date = tag_salesinfo2.find('span', itemprop='datePublished')
            magazine_data.release_date = __extract_date(_date=_release_date)

        tag_topoutline = soup2.find('div', id='summary')
        if tag_topoutline is not None:
            tag_topoutline = soup2.find('div', class_='readingContent01')
        if tag_topoutline is not None:
            for tag_li in tag_topoutline.find_all('h3'):
                _category = tag_li.find('span', class_='category')
                _title = tag_li.find('span', class_='title')
                magazine_data.top_outlines.append(
                    (_category.get_text(strip=True) + ' ' if _category is not None else '')\
                        + (_title.get_text(strip=True) if _title is not None else '')
                )

        tag_storelink = soup.find('dl', class_='storeLink01')
        if tag_storelink is not None:
            for tag_li in tag_storelink.find_all('li'):
                _store_link = tag_li.find('a')
                magazine_data.store_links.append(
                    ItMagazineStoreLink(
                        name=_store_link.get_text(strip=True) if _store_link is not None else '',
                        url=_store_link.get('href') if _store_link is not None else ''
                    )
                )
    return magazine_datas

def __scrape_web_db_press() -> List[ItMagazineData]:
    _url = 'https://gihyo.jp/magazine/wdpress'
    magazine_datas: List[ItMagazineData] = []

    soup = __get_soup(_url)
    tag_links = soup.find('ul', class_='magazineNavigation')
    if tag_links is not None:
        tag_links = tag_links.find_all('a', string=re.compile('詳細|次号'))
    if tag_links is None:
        return magazine_datas
    for tag_link in tag_links:
        if tag_link is not None:
            _url = 'http://gihyo.jp' + tag_link.get('href')
        if _url is None:
            continue

        magazine_data = ItMagazineData(name='WEB+DB PRESS', url=_url)
        magazine_datas.append(magazine_data)
        soup2 = __get_soup(_url)
        _number = soup2.find('h1', string=re.compile('Vol.'))
        magazine_data.number = __extract_magazine_number(_number=_number)
        tag_salesinfo2 = soup2.find('div', id='publishedDetail')
        if tag_salesinfo2 is not None:
            tag_salesinfo2 = tag_salesinfo2.find('div', class_='information')
        if tag_salesinfo2 is not None:
            _price = tag_salesinfo2.find(string=re.compile('定価'))
            magazine_data.price = __extract_price(_price=_price)
            _release_date = tag_salesinfo2.find('span', itemprop='datePublished')
            magazine_data.release_date = __extract_date(_date=_release_date)

        tag_topoutline = soup2.find('div', id='summary')
        if tag_topoutline is not None:
            tag_topoutline = soup2.find('div', class_='readingContent01')
        if tag_topoutline is not None:
            for tag_li in tag_topoutline.find_all('h3'):
                _category = tag_li.find('span', class_='category')
                _title = tag_li.find('span', class_='title')
                magazine_data.top_outlines.append(
                    (_category.get_text(strip=True) + ' ' if _category is not None else '')\
                        + (_title.get_text(strip=True) if _title is not None else '')
                )

        tag_storelink = soup.find('dl', class_='storeLink01')
        if tag_storelink is not None:
            for tag_li in tag_storelink.find_all('li'):
                _store_link = tag_li.find('a')
                magazine_data.store_links.append(
                    ItMagazineStoreLink(
                        name=_store_link.get_text(strip=True) if _store_link is not None else '',
                        url=_store_link.get('href') if _store_link is not None else ''
                    )
                )
    return magazine_datas

def __scrape_interface() -> List[ItMagazineData]:
    _url = 'https://interface.cqpub.co.jp/'
    magazine_datas: List[ItMagazineData] = []
    urls: List[str] = []

    # search book page link
    soup = __get_soup(_url)
    tag_link = soup.find('div', class_='latest-info')
    if tag_link is not None:
        tag_link = tag_link.find('a')
    if tag_link is not None:
        _url = tag_link.get('href')
        if _url is not None:
            urls.append(_url)
    tag_link = soup.find('div', class_='next-book')
    if tag_link is not None:
        tag_link = tag_link.find('a')
    if tag_link is not None:
        _url = tag_link.get('href')
        if _url is not None:
            urls.append(_url)
    # scrape page
    for _url in urls:
        magazine_data = ItMagazineData(name='Interface', url=_url)
        magazine_datas.append(magazine_data)
        soup2 = __get_soup(_url)
        tag_salesinfo1 = soup2.find('div', class_='latest-info')
        if tag_salesinfo1 is not None:
            _number = tag_salesinfo1.find('h2')
            magazine_data.number = __extract_magazine_number(_number=_number)
            _price = tag_salesinfo1.find(class_='price')
            magazine_data.release_date\
                = __extract_year(_date=_number) + __extract_date(_date=_price)
            magazine_data.price = __extract_price(_price=_price)
            _copy = tag_salesinfo1.find(class_='copy')
            _tokushu = tag_salesinfo1.find(class_='tokushu')
            magazine_data.top_outlines.append(
                (_copy.get_text(strip=True) if _copy is not None else '') + \
                (_tokushu.get_text(strip=True) if _tokushu is not None else '')
            )

        for tag_h3 in soup2.find_all('h3', class_='title01'):
            magazine_data.top_outlines.append(
                tag_h3.get_text(strip=True) if tag_h3 is not None else ''
            )

        _store_link = tag_salesinfo1.find('img', title='書籍の購入')
        if _store_link is not None:
            magazine_data.store_links.append(
                ItMagazineStoreLink(
                    name='CQ出版WebShop',
                    url=_store_link.parent.get('href') if _store_link is not None else ''
                )
            )
    return magazine_datas

def __scrape_trangistor_gijutsu() -> List[ItMagazineData]:
    magazine_datas: List[ItMagazineData] = []
    magazine_data = ItMagazineData(name='トランジスタ技術')
    magazine_datas.append(magazine_data)

    # search book page link
    soup = __get_soup('https://toragi.cqpub.co.jp/')
    tag_link = soup.find('section', id='sec01')
    if tag_link is not None:
        tag_link = tag_link.find('div', class_='book')
    if tag_link is not None:
        tag_link = tag_link.find('a')
    if tag_link is not None:
        _url = tag_link.get('href')
    if _url is None:
        return magazine_datas
    # scrape page
    magazine_data.url = _url
    soup2 = __get_soup(_url)
    tag_salesinfo1 = soup2.find('div', class_='latest-info')
    if tag_salesinfo1 is not None:
        _number = tag_salesinfo1.find('h2', class_='book-title')
        magazine_data.number = __extract_magazine_number(_number=_number)
        _price = tag_salesinfo1.find('div', class_='issue-date')
        magazine_data.release_date = __extract_date(_date=_price)
        magazine_data.price = __extract_price(_price=_price)

    for tag_li in tag_salesinfo1.find_all('dl', class_=['tokushu', 'furoku']):
        _category = tag_li.find('dt')
        _title = tag_li.find('dd')
        magazine_data.top_outlines.append(
            (_category.get_text(strip=True) + ' ' if _category is not None else '')\
                + (_title.get_text(strip=True) if _title is not None else '')
        )

    _store_link = tag_salesinfo1.find('a', string='書籍の購入')
    if _store_link is not None:
        magazine_data.store_links.append(
            ItMagazineStoreLink(
                name='CQ出版WebShop',
                url=_store_link.get('href') if _store_link is not None else ''
            )
        )
    return magazine_datas

def __scrape_nikkei_software() -> List[ItMagazineData]:
    _url = 'https://info.nikkeibp.co.jp/media/NSW/'
    magazine_datas: List[ItMagazineData] = []
    magazine_data = ItMagazineData(name='日経ソフトウエア', url=_url)
    magazine_datas.append(magazine_data)

    soup = __get_soup(_url)
    tag_salesinfo1 = soup.find('div', class_='articleBody')
    if tag_salesinfo1 is not None:
        tag_salesinfo1 = tag_salesinfo1.find('div', class_='cover-txt')
    if tag_salesinfo1 is not None:
        _number = tag_salesinfo1.find('p', class_='Title')
        magazine_data.number = __extract_magazine_number(_number=_number)
        _release_date = tag_salesinfo1.find(string=re.compile('発売日'))
        _price = tag_salesinfo1.find(string=re.compile('価格'))
        magazine_data.release_date = __extract_date(_date=_release_date)
        magazine_data.price = __extract_price(_price=_price)

        for tag_b in tag_salesinfo1.find_all('b', string='【特集】'):
            magazine_data.top_outlines.append(
                tag_b.parent.get_text(strip=True)
            )

        _store_link = tag_salesinfo1.find('a', href=re.compile('amazon'))
        if _store_link is not None:
            magazine_data.store_links.append(
                ItMagazineStoreLink(
                    name='Amazon',
                    url=_store_link.get('href')
                )
            )
        _store_link = tag_salesinfo1.find('a', href=re.compile('books.rakuten'))
        if _store_link is not None:
            magazine_data.store_links.append(
                ItMagazineStoreLink(
                    name='Rakutenブックス',
                    url=_store_link.get('href')
                )
            )
    return magazine_datas

def __scrape_nikkei_linux() -> List[ItMagazineData]:
    _url = 'https://info.nikkeibp.co.jp/media/LIN/'
    magazine_datas: List[ItMagazineData] = []
    magazine_data = ItMagazineData(name='日経Linux', url=_url)
    magazine_datas.append(magazine_data)

    soup = __get_soup(_url)
    tag_salesinfo1 = soup.find('div', class_='articleBody')
    if tag_salesinfo1 is not None:
        tag_salesinfo1 = tag_salesinfo1.find('div', class_='cover-txt')
    if tag_salesinfo1 is not None:
        _number = tag_salesinfo1.find('p', class_='Title')
        magazine_data.number = __extract_magazine_number(_number=_number)
        _release_date = tag_salesinfo1.find(string=re.compile('発売日'))
        _price = tag_salesinfo1.find(string=re.compile('価格'))
        magazine_data.release_date = __extract_date(_date=_release_date)
        magazine_data.price = __extract_price(_price=_price)

        for tag_b in tag_salesinfo1.find_all('b', string=re.compile('【特集')):
            magazine_data.top_outlines.append(
                tag_b.parent.get_text(strip=True)
            )

        _store_link = tag_salesinfo1.find('a', href=re.compile('amazon'))
        if _store_link is not None:
            magazine_data.store_links.append(
                ItMagazineStoreLink(
                    name='Amazon',
                    url=_store_link.get('href')
                )
            )
        _store_link = tag_salesinfo1.find('a', href=re.compile('books.rakuten'))
        if _store_link is not None:
            magazine_data.store_links.append(
                ItMagazineStoreLink(
                    name='Rakutenブックス',
                    url=_store_link.get('href')
                )
            )
    return magazine_datas

def scrape_magazine(magazine_type: ItMagazineType) -> List[ItMagazineData]:
    '''
    scrape magazine
    '''
    print(f'{magazine_type.name} scraping ...', end='')
    _magazines: List[ItMagazineData] = []
    if magazine_type == ItMagazineType.SOFTWARE_DESIGN:
        _magazines = __scrape_software_design()
    elif magazine_type == ItMagazineType.WEB_DB_PRESS:
        _magazines = __scrape_web_db_press()
    elif magazine_type == ItMagazineType.INTERFACE:
        _magazines = __scrape_interface()
    elif magazine_type == ItMagazineType.TRANGISTOR_GIJUTSU:
        _magazines = __scrape_trangistor_gijutsu()
    elif magazine_type == ItMagazineType.NIKKEI_SOFTWARE:
        _magazines = __scrape_nikkei_software()
    elif magazine_type == ItMagazineType.NIKKEI_LINUX:
        _magazines = __scrape_nikkei_linux()
    # check magazine number duplication
    _rmv_list = []
    for _magazine1 in _magazines:
        for _magazine2 in _magazines:
            if _magazine1 == _magazine2 or _magazine1 in _rmv_list:
                continue
            if _magazine1.name != _magazine2.name or _magazine1.number != _magazine2.number:
                continue
            _rmv_list.append(_magazine2)
    for _rmv_item in _rmv_list:
        _magazines.remove(_rmv_item)
    print('done')
    return _magazines

def scrape_magazines() -> List[ItMagazineData]:
    '''
    scrape magazines
    '''
    _magazines: List[ItMagazineData] = []
    for magazine_type in ItMagazineType:
        _magazines.extend(scrape_magazine(magazine_type=magazine_type))
    return _magazines

if __name__ == '__main__':
    for magazine in scrape_magazines():
        print(magazine.get_json())
