# aviata_test
aviata
<br>
нужен redis-server для celery и кэша
<br>
brew service start redis
<br>
каждый день в 00:00 запускается periodic task update all flights
<br>
добавил в url init и update чтобы запустить инициализацию городов и авиалинии, update для локального тестирования
<br>
all_flights показывает все авиалинии с кэша


