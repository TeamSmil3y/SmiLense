from nlp.nlp import model
from more_itertools import sliced
from timeit import default_timer as timer

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


prompt = (
    "Give me an analysis of the following license file matching exactly this format, do under no circumstances answer in a different format and add nothing, seperate by comma:"
    "commercial_use: allowed / notallowed / notmentioned; "
    "open_source: yes / no / notmentioned; "
    "attribution: required / notrequired / notmentioned; "
    "redistribution: allowed / notallowed/ notmentioned; "
    "profit: allowed / notallowed / notmentioned; "
    "aditional: add additional infos here"
)


def extract_key_points_2(raw):
    # list all the important key points from the LICENSE file

    try:
        if len(raw) <= 2048:

            with model.chat_session():
                model.generate(
                    prompt
                )

                r = model.generate(
                    raw.strip()
                )
                print(r)
        else:
            for i in list(sliced(raw, 2048)):
                r = ""

                with model.chat_session():
                    model.generate(
                        prompt
                    )

                    r += ", " + model.generate(i.strip()).strip()
                    print(r)

        res = [i.strip() for i in r.replace(".", "").split("\n")[-1].split(", ") if i]

        return res


    except:
        return

if __name__ == '__main__':

    LICENSE = """
    This software was developed by the Unidata Program Center of the
University Corporation for Atmospheric Research (UCAR)
<http://www.unidata.ucar.edu>.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

   1) Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
   2) Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.
   3) Neither the names of the development group, the copyright holders, nor the
      names of contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.
   4) This license shall terminate automatically and you may no longer exercise
      any of the rights granted to you by this license as of the date you
      commence an action, including a cross-claim or counterclaim, against
      the copyright holders or any contributor alleging that this software
      infringes a patent. This termination provision shall not apply for an
      action alleging patent infringement by combinations of this software with
      other software or hardware.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE CONTRIBUTORS
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS WITH THE SOFTWARE.
    """

    start = timer()
    print(extract_key_points_2(LICENSE))
    end = timer()
    print(end - start)