# импортируем библиотеку sqlalchemy и ее функции 
import sqlalchemy as sa 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///albums.sqlite3"

# создаем базовый класс моделей таблиц
Base = declarative_base()

# класс, описывающий структуру таблицы album для хранения записей музыкальной библиотеки
class Album(Base):

	# задаем название таблицы
	__tablename__ = "album"

	# описываем столбцы таблицы
	id = sa.Column(sa.INTEGER, primary_key=True)
	year = sa.Column(sa.INTEGER)
	artist = sa.Column(sa.TEXT)
	genre = sa.Column(sa.TEXT)
	album = sa.Column(sa.TEXT)

# Функция, которая устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
def connect_db():

	#создаем соединение с БД:
	engine = sa.create_engine(DB_PATH)
	# создаем описанные таблицы
	Base.metadata.create_all(engine)
	# создаем фабрику сессий
	session = sessionmaker(engine)
	return session()

# задаем функцию для поиска и формирования списка названий альбомов artist (передается в GET-запросе)
def find(artist):
	session = connect_db()
	albums = session.query(Album).filter(Album.artist == artist).all()
	return albums

# данная функция принимает параметры нового альбома, передаваемые в POST-запросе, и записывает их в таблицу sqlite
def save_new_album(year, artist, genre, album):
	# валидация передаваемых данных по их типу:
	assert isinstance(year, int), "Некорректный формат данных года. Введите число"
	assert isinstance(artist, str), "Некорретный формат данных. Введите текст"
	assert isinstance(genre, str), "Некорретный формат данных. Введите текст"
	assert isinstance(album, str), "Некорретный формат данных. Введите текст"

	session = connect_db()
	saved_album = session.query(Album).filter(Album.album == album, Album.artist == artist).first()
	if saved_album is not None:
		raise AlreadyExists("Альбом уже существует и имеет номер {}".format(saved_album.id))

	album = Album(
		year=year,
		artist=artist,
		genre=genre,
		album=album
		)

	session.add(album)
	session.commit()
	return album
