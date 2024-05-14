import yaml
import base64
from pigeon.shortcuts import Log
import sqlalchemy as sql
from sqlalchemy import Table, Column

log = Log('SMILESENSE', 'blue')

# create sqlalchemy engine to interact with db
db_engine=sql.create_engine('sqlite:///./sqlite.db')
metadata = sql.MetaData()
metadata.reflect(bind=db_engine)


class Config:
	def __init__(self, employees: int, software_type: str:, whitelist: list[str], blacklist: list[str]):
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
	)
)

with db_engine.connect() as connection:
	connection.execute(...)
	connection.commit()

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


def check_match_known():
	...
=======
	#config = yaml.safe_load(data)
	#log.info(config)
	return {'status': 1, 'compatability': 3, 'message': '...'
}
