from sqlalchemy import Table, Column, desc, func, or_, and_, DDLElement
import sqlalchemy as sql


db_engine = sql.create_engine('sqlite:///./sqlite.db')
metadata = sql.MetaData()
metadata.reflect(bind=db_engine)

licenses = Table(
    'licenses',
    metadata,
    *(
        Column('hash', sql.Text, primary_key=True),
        Column('commercial_use', sql.Text, nullable=True),
        Column('open_source', sql.Text, nullable=True),
        Column('attribution',sql.Text, nullable=True),
        Column('redistribution', sql.Text, nullable=True),
        Column('profit', sql.Text, nullable=True),
        Column('free', sql.Text, nullable=True),
        Column('additional', sql.Text, nullable=True),
    ),
    extend_existing=True
)

packages = Table(
    'packages',
    metadata,
    *(
        Column('id', sql.Integer, primary_key=True),
        Column('name', sql.Text),
        Column('version', sql.Text),
        Column('hash', sql.Text)
    ),
    extend_existing=True
)

CREATE = False
DROP = False


if DROP:
    metadata.drop_all(bind=db_engine)
    if not CREATE: exit()
if CREATE:
    metadata.create_all(bind=db_engine)

