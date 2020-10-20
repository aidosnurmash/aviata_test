# aviata_test
aviata
нужен redis-server для celery и кэша
brew service start redis
каждый день в 00:00 запускается periodic task update all flights
добавил в url init и update чтобы запустить инициализацию городов и авиалинии, update для локального тестирования
all_flights показывает все авиалинии с кэша


