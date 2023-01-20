from sqlalchemy import String, Column, Integer, Float
from scrpy.base.db import Base

class Nout(Base):
    __tablename__='nouts'
    id = Column("id",Integer, primary_key=True, autoincrement=True, unique=True, comment='ID')
    url = Column("url",String, unique=True, comment='Ссылка на товар')
    date = Column("date",String, comment='Время получения данных')
    name = Column("name",String, unique=False, comment='Название товара')
    processor = Column("processor",String, unique=False, comment='Тип процессора')
    core = Column("core",Integer, unique=False, comment='Количество ядер')
    mhz = Column("mhz",Float, unique=False, comment='Суммарная частота процессора')
    ram = Column("ram",Integer, unique=False, comment='RAM')
    screen = Column("screen",Float, unique=False, comment='Диагональ экрана')
    price = Column("price",Integer, comment='Цена')
    rank = Column("rank",Float, comment='Вычисляемый ранг')

    def __init__(self, id=None, url=None, date=None,  name=None, processor=None, core=None, mhz=None, ram=None, screen=None, price=None, rank=None) -> None:
        self.id=id
        self.url=url
        self.date=date
        self.name=name
        self.processor=processor
        self.core=core
        self.mhz=mhz
        self.ram=ram
        self.screen=screen
        self.price=price
        self.rank=rank