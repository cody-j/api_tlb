from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import DateTime

engine = create_engine('postgresql+psycopg2://127.0.0.1:5432/the_local_bodega')

Base = declarative_base()

class Prompt(Base):
    __tablename__ = 'prompts'

    id = Column(Integer, primary_key=True)
    recursion = Column(String)
    prompt = Column(String)
    
    def __repr__(self):
        return f"<Prompt(recursion={self.recursion}, prompt={self.prompt})>"


class Post(Base):
    __tablename__ = 'prompts'

    id = Column(Integer, primary_key=True)
    post = Column(String)
    timestamp = Column(DateTime)

def main():
    print(Prompt.__table__)
#     with engine.connect() as con:
#         rs = con.execute(
#             """
#                 select * from prompts
#             """
#         )

#         for row in rs:
#             print(row)

if __name__=="__main__":
    main()
