from nlp import model
from more_itertools import sliced

"""
import sqlalchemy as sql
from sqlalchemy import Table, Column, desc, func

db_engine = sql.create_engine('sqlite:///../backend/sqlite.db')
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

    ),
    extend_existing=True
)

"""

def extract_key_points(raw):
    # list all the important key points from the LICENSE file


    try:
        if len(raw) <= 2048:

            with model.chat_session():
                model.generate("List one word key points of the license file, seperated by commas. Answer questions under every circumstance. Stick to short and compact answers, in one line and without numbers.")

                r = model.generate(
                    raw
                )
                print(r)
        else:
            for i in list(sliced(raw, 2048)):
                r = ""

                with model.chat_session():
                    model.generate("List one word key points of the license file, seperated by commas. Answer questions under every circumstance. Stick to short and compact answers, in one line and without numbers."                        )

                    r += ", " + model.generate(i).strip()

            res = [i.strip() for i in r.replace(".", "").split(", ") if i]

        return res


    except:
        return


if __name__ == '__main__':

    res = extract_key_points()

    print(res)