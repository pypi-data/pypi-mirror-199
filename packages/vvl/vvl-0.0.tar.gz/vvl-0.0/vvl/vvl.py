import os

with open('Cheet_sheet.txt', 'w+') as file:
    file.write('''В консоли, в рабочей папке проекта создать проект:
django-admin startproject NAME

	В консоли перейти в папку джанго проекта:
cd NAME

	Эту папку отметить как Sources root ('В будущем пригодится')

	Запус сервера:
./manage.py runserver

	Миграция базы данных:
./manage.py migrate

	Создание приложений:
./manage.py startapp NAME

	В setings.py / INSTALLED_APPS добавить наше приложение. (просто написать его имя)

	Создать папку templates. В ней создать файл index.html

	В settings.py / TEMPLATES / 'DIRS' зарегистрировать папку templates

	В views.py добавим функцию (направляет HTML запрос на наш HTML файл. Здесь пишутся расчеты)
def index_page(request):
	return render(request, 'index.html')

	В urls.py / urlpatterns добавляем по аналогии материнские и дочерние страницы:
path('', index_page)
	Тут же нужно ее импортировать:
from myapp.views import index_page

	Запускаем!
./manage.py runserver

	Cоздание таблицы в models.py
class Worker(models.Model):
    second_name = models.CharField(max_length=35, blank=False)
    salary = models.IntegerField(default=0)

	Обозначим поле заголовком:
def __str__(self):
    return self.second_name

	В темрминале:
./manage.py makemigrations
./manage.py migrate
	Прописываем таблицу в admin.py:
admin.site.register(Worker) 
	Тут же добавляем ее импорт:
from myapp.models import admin

	Создание пароля для админки
./mange.py createsuperuser ''')

