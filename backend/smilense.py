from pigeon.shortcuts import Log
import sqlalchemy as sqa
import yaml
import base64

log = Log('SMILESENSE', 'blue')


def compare(data, files):
	log.info(files)
	log.info(data)

	config = yaml.load_sage(base64.b64decode(data.config))
	license = base64.b64decode(data.config)
	dependencies = base64.b64decode(data.dependencies)

	#config = yaml.safe_load(data)
	#log.info(config)
	return {'status': 1, 'compatability': 3, 'message': '...'
}