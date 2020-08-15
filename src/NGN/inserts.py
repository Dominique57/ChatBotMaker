from db_manager import Session, engine, Base
from models import User, Channel, Server

Base.metadata.create_all(engine)
session = Session()
# yolo begin


u1 = User(fb_id='dominique', state='home')
u2 = User(fb_id='lea', state='home')
s1 = Server(name='epita.news')
c1 = Channel(name='epita.news.assistants', server=s1)
c2 = Channel(name='epita.news.announcement', server=s1)

objects = [
    u1, u2, s1, c1, c2
]

for obj in objects:
    session.add(obj)

# yolo ends
session.commit()
session.close()
