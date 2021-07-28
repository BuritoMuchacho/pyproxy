# PyProxy
### Description
**PyProxy** allows you to get one proxy, a list of proxies, create a csv file with proxies and even connect/disconnect to/from them (only macOS). It is light-weight, written on pure Python module, that gives basic functionality you might need when, for example, web scraping. It uses [proxyscan.io API](https://www.proxyscan.io/api) to get proxies.

### Installation
The easiest yet way to use it is to download `pyproxy` repo and place it to your project's directory. 
To do that, run `git clone https://github.com/BuritoMuchacho/pyproxy.git` in your project's directory.

### Examples
Some basic usage with requests:
```
import requests
from pyproxy.proxy import Proxy

requests.get('https://httpbin.org/ip', proxy=Proxy().proxy(type='https'))
```
Get 100 working http proxies to csv file:
```
from pyproxy.proxy import Proxy

Proxy().to_csv(num=100, type='http')
```
Get 10 elite proxies as a list of strings:
```
from pyproxy.proxy import Proxy

Proxy().list_proxies(num=10, level='elite')
```
Get a list of 10 dictionaries containing connection type and proxy adresses from USA:
```
from pyproxy.proxy import Proxy

Proxy().dict_proxies(num=10, country_code='us')
```
Connect your Mac to proxy:
```
from pyproxy.proxy import Proxy

Proxy().connect(type='http')
```
And disconnect:
```
from pyproxy.proxy import Proxy

Proxy.disconnect(type='http')
```
Basicaly, all functions have the same set of arguments:
* num: *int*, a number of proxies you want to get (only for `to_csv()`, `dict_proxies()` and `list_proxies()`)
`Proxy().list_proxies(num=5)` = list of 5 proxies
* check: *boolean*, whether you want the proxies to be checked or not (True by default).
`Proxy().proxy(check=False)` = get a proxy without checking it
* type: *str*, Proxy Protocol (http, https, socks4, socks5)
`Proxy().dict_proxies(num=5, type='https')` = get a list of 5 https proxies as dictionaries
* country_code: *str*, ISO 3166-1 codes to search a proxy in particular country.
`Proxy().proxy(country_code='ru')` = get proxy located in Russia
* level: *str*, Anonymity Level (transparent, anonymous, elite)
`Proxy().to_csv(num=10, level='anonymous')` = write 10 anonymous proxies to csv file.

Feel free to make pull requests improving the code and report any issues. Happy Coding! 🐍