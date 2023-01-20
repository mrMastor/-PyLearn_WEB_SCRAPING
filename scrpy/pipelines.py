from sqlalchemy.orm import sessionmaker
from scrpy.base.model import Nout
from scrpy.base.db import db_connect

class NoutService():

    def __init__(self) -> None:
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        instance = session.query(Nout).filter_by(**item).one_or_none()
        if instance:
            return instance

        new_item = Nout(
            url = item['url'],
            date = item['date'],
            name = item['name'], 
            processor = item['processor'], 
            core = item['core'], 
            mhz= item['mhz'],
            ram = item['ram'],
            screen = item['screen'],
            price = item['price'],
            rank = round(float(float(item['mhz'])*10 + int(item['ram'])*8 + float(item['screen'])*7 + int(item['price'])*-0.004), 2)
            )

        try:
            session.add(new_item)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item