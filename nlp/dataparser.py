import sqlalchemy as sql
from extract_key_points import *
from sqlalchemy import Table, Column, desc, func, or_, DDLElement
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import sessionmaker

import os


# create sqlalchemy engine to interact with db



db_engine=sql.create_engine('sqlite:///./sqlite.db')
metadata = sql.MetaData()
metadata.reflect(bind=db_engine)

licenses = Table(
    'licenses',
    metadata,
    *(
        Column('key', sql.Text, primary_key=True),
        Column('name', sql.Text),
        Column('short_name', sql.Text),
        Column('category',sql.Text),
        Column('url', sql.Text),
        Column('raw', sql.Text),
        Column('key_parameters', sql.Text),

    ),
    extend_existing=True
)


CREATE = True
DROP = True


if DROP:
    metadata.drop_all(bind=db_engine)
    if not CREATE: exit()
if CREATE:
    metadata.create_all(bind=db_engine)


directory = "/Users/timruppert/Downloads/scancode-licensedb-main/docs"

with db_engine.connect() as connection:
    for filename in os.listdir(directory):
        if filename.startswith("."): continue
        with open(directory + "/" + filename, "r") as file:

            f = file.read().split("---\n")
            d = {i.split(":")[0]: ":".join(i.split(":")[1:]) for i in f[1].split("\n") if i}
            print(d)

            raw = "\n".join(f[2:])
            url_key = None
            for key in d.keys():
                if "url" in key:
                    url_key = key
                    break


            key_parameters = ", ".join(extract_key_points(raw))

            print(key_parameters)

            connection.execute(sql.insert(licenses).values(key=d["key"], name=d["name"], short_name=d["short_name"], category=(d["category"] if "category" in d else None), url=d[url_key] if url_key else None, raw=raw, key_parameters=key_parameters))
        connection.commit()
