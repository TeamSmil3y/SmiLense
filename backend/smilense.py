import yaml
from pigeon.shortcuts import Log
import sqalchemy as sqa

log = Log('SMILESENSE', 'blue')


def compare(data, files):
	log.info(files)
	log.info(data)
	#config = yaml.safe_load(data)
	#log.info(config)
	return {'status': 1, 'compatability': 3, 'message': '...'}


