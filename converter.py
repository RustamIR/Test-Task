import csv
import json
import sqlite3
import psycopg2
import os
import pandas as pd


from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, DateTime, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import ARRAY, Column, DateTime, Integer, Text
from sqlalchemy.orm import sessionmaker
from elasticsearch import Elasticsearch


metadata = MetaData()

posts = Table('Posts', metadata,
              Column('id', Integer, primary_key=True),
              Column('rubrics', Text, nullable=False),
              Column('text', Text, nullable=False,),
              Column('created_date', DateTime, nullable=False)
              )


engine = create_engine('sqlite:///db.sqlite3', echo=True)
metadata.create_all(engine)
Base = declarative_base()


conn = engine.connect()


INDEX = "posts"


def es_converter(df):
    for record in df.to_dict(orient="records"):
        yield '{ "index" : { "_index" : "%s", "_type" : "%s" }}' % (INDEX, "record")
        yield json.dumps(record, default=int)


def elastic_insert_logic(file_name: str):
    df = pd.read_csv(file_name, usecols=[0])
    df["id"] = df.index + 1
    e = Elasticsearch("http://127.0.0.1:9200")

    if e.indices.exists(INDEX):
        e.indices.delete(index=INDEX)
    e.indices.create(index=INDEX)

    r = e.bulk(es_converter(df))
    if not r["errors"]:
        print("Успешно записал данные в elastic")
    else:
        print("Не удалось записать данные в elastic")


def sqlite_insert_logic(file_name: str):
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()

    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            cur.execute('INSERT INTO posts (rubrics, text, created_date) VALUES(?,?,?)', (row[2], row[0], row[1]))
    conn.commit() 


def main():
    file_name = "posts.csv"
    sqlite_insert_logic(file_name)
    elastic_insert_logic(file_name)

if __name__ == "__main__":
    main()
