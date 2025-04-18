### Описани:
Сервис предоставляет API для учёта данных, поступающих с устройства. Релизовано:
- Создание устройства
- Создание данных устройства
- Создание владельца устройства
- Получение минимального, максимального, медианного значений и количества по трём характеристиками устройства ('x', 'y', 'z')
- Получение этой же статистики, агрегированной для пользователя по всем его утсройствам
- Статистику можно получать за определённый период и за всё время

Результаты нагрузочного тестирования приложены в виде файла "нагрузочное тестирование (100 users)". При необходимости можно проверить командой locust и перейдя в веб-интерфейс


### Стек:
- Python 3.10
- FastAPI 0.115
- SQLAlchemy 2.0
- PostgreSQL 15
- Docker


### Запуск:
Клонировать репозиторий:
```
git clone https://github.com/Randy-Colt/device_analyzer.git
```

Перейти в директорию проекта:
```
cd device_analyzer
```

Запустить приложение:
```
docker compose up
```

Приложение доступно по адресу:
```
http://127.0.0.1:8000/api/devices
```

Документация доступна по адресу:
```
http://127.0.0.1:8000/docs
```
