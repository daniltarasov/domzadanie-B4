
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import date

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class User(Base):

    __tablename__ = 'user'

    id = sa.Column(sa.INTEGER, primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.REAL)


class Athelete(Base):

    __tablename__ = 'athelete'

    id = sa.Column(sa.INTEGER, primary_key=True)
    name = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.REAL)
    age = sa.Column(sa.Integer)
    gender = sa.Column(sa.Text)
    weight = sa.Column(sa.Integer)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)


def connect_db():

    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(user_id, session):

    user_found = session.query(User).filter(User.id == user_id).first()
    if not user_found:
        return None, None, None

    athelete_bd_query = session.query(Athelete).all()

    atl_dict_height = {atl.id: atl.height for atl in athelete_bd_query if atl.height}   #словарь для сравнения по росту, проверяем на наличие поля
    atl_dict_bdate = {atl.id: date.fromisoformat(atl.birthdate) for atl in athelete_bd_query if atl.birthdate}  #словарь для сравнения по д.р., сразу переволим в datetime

    compared = user_found.height    #аргумент для сравнивающей функции
    id_height_found = find_atl(atl_dict_height, compared)   #искомый id по весу
    compared = date.fromisoformat(user_found.birthdate)     #то же самое по дате, в datetime
    id_bdate_found = find_atl(atl_dict_bdate, compared)

    atl_height = session.query(Athelete).filter(Athelete.id == id_height_found).first()     #получаем нужные объекты
    atl_bdate = session.query(Athelete).filter(Athelete.id == id_bdate_found).first()

    return user_found, atl_height, atl_bdate


def find_atl(atl_dict, compared):
    min_differ = None
    atl_id = None

    for key, value in atl_dict.items():
        differ = abs(value-compared)
        if min_differ == None or min_differ > differ:
            min_differ = differ
            atl_id = key
        if min_differ == 0:
            break

    return atl_id


def main():

    session = connect_db()
    user_id = int(input("Введите id пользователя для поиска: "))

    user_found, atl_height, atl_bdate = find(user_id, session)
    if not user_found:
        print("Такого пользователя нет")
    else:
        print("Для пользователя с именем {}. ростом {} м и датой рождения {}:" .format(user_found.first_name, user_found.height, user_found.birthdate))
        print("Атлет {} с ростом {} м" .format(atl_height.name, atl_height.height))
        print("Атлет {} c датой рождения {}" .format(atl_bdate.name, atl_bdate.birthdate))


if __name__ == "__main__":
    main()