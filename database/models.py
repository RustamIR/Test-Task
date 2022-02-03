from sqlalchemy import Table, Integer, Column, DateTime
from sqlalchemy import Column, DateTime, Integer, Text
from db_settings import metadata


Post = Table('posts', metadata,
              Column('id', Integer, primary_key=True),
              Column('rubrics', Text, nullable=False),
              Column('text', Text, nullable=False,),
              Column('created_date', DateTime, nullable=False)
)

def get_data(self):
    return {
        'id': self.id,
        'rubrics': self.rubrics,
        'text': self.text,
    }

