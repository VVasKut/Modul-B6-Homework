from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

# импортируем модуль для поиска альбомов артиста
import album


@route("/albums/<artist>")
def albums(artist):
	# методом find сортируем таблицу album по названию artist, переданному в GET-запросе
	albums_list = album.find(artist)
	# если в GET-запросе передается название артиста, которые отсутствует в таблице (например, Nirvana), выводится сообщение об ошибке
	if not albums_list:
		message = "Альбомов {} не найдено".format(artist)
		result = HTTPError(400, message)
	# если artist найдет в таблице, сортируются строки с альбомами данного исполнителя и выводится сообщение о количестве этих альбомов,
	# а также список с их названиями
	else:
		# метдом спискового включения формируем список названий альбомов исполнителя artist из отсортированной таблицы albums_list
		album_names = [album.album for album in albums_list]
		# в результат вывоводим сообщение с количеством найденных альбомов (len(albums_list)) и списком названий
		result = "У исполнителя {} найдено {} альбомов.<br> Список всех альбомов:<br>".format(artist, len(album_names))
		result += "<br>".join(album_names)
	return result

"""Чтобы протестировать работу сервера с GET-запросами, нужно:
1. Запустить сервер через консоль: python album_server.py
2. Открыть браузер и в адресной строке ввести:
   localhost:8080/albums/Pink Floyd
   потом попробовать:
   localhost:8080/albums/Nirvana"""


@route("/albums", method="POST")
def add_album():
	year = request.forms.get("year")
	artist = request.forms.get("artist")
	genre = request.forms.get("genre")
	album_name = request.forms.get("album")

	try:
		year=int(year)
	except ValueError:
		return HTTPError(409, "Указан некорректный год альбома")

	try:
		new_album = album.save_new_album(year, artist, genre, album_name)
	except AssertionError as err:
		result = HTTPError(400, str(err))
	except album.AlreadyExists as err:
		result = HTTPError(409, str(err))
	else:
		print("New #{} album successfully saved".format(new_album.id))
		result = "Альбом #{} успешно сохранен".format(new_album.id)
	return result

"""Чтобы протестировать работу сервера с POST-запросами, нужно:
1. Запустить сервер через консоль: python album_server.py
2. Открыть консоль и ввести: http -f POST localhost:8080/albums artist="" genre="" year=9999 album="""


if __name__ == "__main__":
	run(host="localhost", port=8080, debug=True)