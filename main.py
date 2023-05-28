import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
# from sqlalchemy.types import Date

Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=100), unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)
    publisher = relationship(Publisher, backref="publishers")

class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=100), unique=True)

class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer)

    book = relationship(Book, backref='books')
    shop = relationship(Shop, backref='shops')

class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Numeric(precision=8, scale=2))
    date_sale =  sq.Column(sq.Date())
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer)
    stock = relationship(Stock, backref='stocks')

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

password = input('Пароль: ')
DSN = "postgresql://postgres:"+password+"@localhost:5432/SQL4_hw"
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)
#
Session = sessionmaker(bind=engine)
session = Session()

publisher1 = Publisher(name = 'Пушкин')
publisher2 = Publisher(name = 'Радищев')

book1 = Book(title = 'Онегин', publisher = publisher1)
book2 = Book(title = 'Капитанская дочка', publisher = publisher1)
book3 = Book(title = 'Путешествие из Петербурга в Москву', publisher = publisher2)

shop1 = Shop(name = 'Буквоед')
shop2 = Shop(name = 'Лабиринт')
shop3 = Shop(name = 'Книжный дом')

stock1 = Stock(book = book1, shop = shop1, count = 2)
stock2 = Stock(book = book2, shop = shop1, count = 3)
stock3 = Stock(book = book3, shop = shop1, count = 4)
stock4 = Stock(book = book1, shop = shop2, count = 5)
stock5 = Stock(book = book1, shop = shop3, count = 6)



sale1 = Sale(price = 500, date_sale = '01.01.2023', stock = stock1, count = 1)
sale2 = Sale(price = 400, date_sale = '02.01.2023', stock = stock2, count = 2)
sale3 = Sale(price = 450, date_sale = '03.01.2023', stock = stock3, count = 1)
sale4 = Sale(price = 200, date_sale = '04.01.2023', stock = stock5, count = 1)

session.add_all([publisher1, publisher2, book1, book2, book3, shop1, shop2, shop3, stock1, stock2, stock3, stock4, stock5, sale1, sale2, sale3, sale4])
session.commit()
inp_publisher = input('Введите автора\n').strip()
# inp_publisher = 'Пушкин'
subq = session.query(Publisher).filter(Publisher.name == inp_publisher).subquery()

result2 = session.query(Sale, Book, Shop).join(Stock, Sale.id_stock == Stock.id).join(Shop, Stock.id_shop == Shop.id).join(Book, Book.id == Stock.id_book).join(subq, Book.id_publisher == subq.c.id)
# print(result2)
for sale_, book_, shop_ in result2:
    print(f'{book_.title} | {shop_.name} | {sale_.price * sale_.count} | {sale_.date_sale}')




session.close()

