import yaml
import base64
from pigeon.shortcuts import Log
import sqlalchemy as sql
from sqlalchemy import Table, Column, desc, func

log = Log('SMILESENSE', 'blue')

# create sqlalchemy engine to interact with db
db_engine = sql.create_engine('sqlite:///./sqlite.db')
metadata = sql.MetaData()
metadata.reflect(bind=db_engine)


class Config:
	def __init__(self, employees: int, software_type: str, whitelist: list[str], blacklist: list[str]):
		self.employees = employees
		self.software_type = software_type
		self.whitelist = whitelist
		self.blacklist = blacklist

    
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

#with db_engine.connect() as connection:
	#connection.execute(...)
#	connection.commit()

def compare(data):
	"""
	Compares the license in the data to the configuration in the data.

	:param data: pigeon HTTPRequest data
	:return:
	"""
	log.info(data)
	config = yaml.safe_load(base64.b64decode(data.config))
	license = base64.b64decode(data.config)
	dependencies = base64.b64decode(data.dependencies)

	#log.info(config)

	return {'status': 1, 'compatability': 3, 'message': '...'}


def compare(data, files):
	log.info(files)
	log.info(data)
	config = yaml.load_sage(base64.b64decode(data.config))
	license = base64.b64decode(data.config)
	dependencies = base64.b64decode(data.dependencies)
	#config = yaml.safe_load(data)
	#log.info(config)
	return {'status': 1, 'compatability': 3, 'message': '...'}



def check_match_known(license_txt) -> tuple[str | None, str | None]:
	lst = license_txt.split('\n')

	keys = []

	for l in lst:
		with db_engine.connect() as connection:
			s = connection.execute(
				sql.select(licenses).where(licenses.columns.raw.icontains(license_txt))
			).first()

	if s:
		return s[0], "original"

	with db_engine.connect() as connection:
		s = connection.execute(
			sql.select(licenses).where(licenses.columns.raw.icontains(license_txt))
		).first()

	if s:
		return s[0], f"This license is based on {s[1]} and extended with: {license_txt.replace(s[5], str())}"

	return None, None



if __name__ == '__main__':
	LICENSE = """
	MIT License
	
	Copyright (c) 2023 lstuma
	
	Permission is hereby granted, free of charge, to any person obtaining a copy
	of this software and associated documentation files (the "Software"), to deal
	in the Software without restriction, including without limitation the rights
	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
	copies of the Software, and to permit persons to whom the Software is
	furnished to do so, subject to the following conditions:
	
	The above copyright notice and this permission notice shall be included in all
	copies or substantial portions of the Software.
	
	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
	SOFTWARE.
	"""

	r = check_match_known(LICENSE)

	print(r)