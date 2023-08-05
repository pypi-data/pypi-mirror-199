### proxy_manager

Модуль для получения актуальных прокси по своей апи. 

Использование: 
Сохраняем в папке `/home/user/dev/packages/proxy_manager`


## Вариант установки 1
Создаем дистрибутив с помощью команды:
```bash 
cd proxy_manager
python3 setup.py sdist
```

Можно установить глобально
```bash
pip install dist/proxy_manager-0.1.tar.gz
```

Установка из venv: 
```bash 
pip install /home/user/dev/packages/proxy_manager
```

## Вариант установки 2 
Собираем: 
```bash 
python3 setup.py bdist_wheel 
```

Устанавливаем
```bash
pip install /home/user/dev/packages/proxy_manager/dist/proxy_manager-0.1.tar.gz
```


Подключаем 
```python
from proxy_manager import ProxyManager
```

Пример использования: 
```python
proxies = ProxyManager(token)
proxies.get() # Возвращает список актульных прокси
```            