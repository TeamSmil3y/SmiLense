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



def check_match_known():
	...