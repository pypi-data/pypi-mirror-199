## ProxyManager()

При активном использовании прокси во время парсинга возникает проблема постоянного перекидывания прокси из проекта в проект.  

Для использования данного модуля: необходимо развернуть АПИ на сервере. [использованное api](https://github.com/mangustik228/api_proxy)

Установка:
```bash
pip install mangust228
```
---


### Пример получения актуальных прокси:
```python
from mangust228 import ProxyManager

proxies = ProxyManager('your_token', 'your_url')
proxies.get('string') 
# [{http://user:pass@127.0.0.1:8000},...]
proxies.get('dict[str,str]')
# [{'server':'http://127.0.0.1:8000','username':'user','password':'pass'}, ...]
proxies.get('playwright')
# [{'proxy':{'server':'http://127.0.0.1:8000','username':'user','password':'pass'}},...]
```

---

### Пример получения списка всех прокси (включая просроченные)
```python
proxies = ProxyManager('your_token', 'your_url')
proxies.get_full()
```
Можно указать путь (только csv!), тогда результат будет сохранен в `csv` файл
```python
proxies.get_full('all_proxies.csv')
```
---

### Пример добавления прокси
```python
data = [{
    'server':'127.0.0.1',
    'port':8000,
    'username':'user',
    'password':'pass',
    'expire':'2023-12-31',
    'service':'example.service.com'
},...]
proxies = ProxyManager(token, url)
proxies.post(data=data)
```

Можно добавлять из файлов excel или csv
```python
proxies.post(path='example.csv')
```
---
### Пример удаления прокси
```python
proxies.delete(id)
```
---
### Пример изменения прокси
```python
data = {
    'id':1,
    'username':'John'
}
proxies.put(data)
```
