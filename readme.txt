Приложение тестировалось с gunicorn 19.7.1., ubuntu 16.04, virtualenv 15.0.3, python 3.5.2 (CPython)
Пример запуска в каталоге с app.py: gunicorn -b 0.0.0.0:8090 app:app
