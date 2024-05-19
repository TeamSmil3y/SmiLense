import json
from nlp.extract_key_points import extract_key_points_2
import yaml
import base64
from pigeon.shortcuts import Log
import sqlalchemy as sql
from sqlalchemy import Table, Column, desc, func
from pipy import PiPy as PyPI
from nlp.db_init import *
import nlp.data_services as db
import compare_key_params

log = Log('SMILESENSE', 'blue')


def compare(data):
	"""
	Compares the license in the data to the configuration in the data.

	:param data: pigeon HTTPRequest data
	:return:
	"""
	log.info(data)
	print(data)
	config = yaml.safe_load(base64.b64decode(data.get('license-manifest.yaml')))  # {"keyparameter": "value"}
	dependency = data.get('checkPackageName')  # Name of dependency
	version = data.get('checkPackageVersion')  # Name of dependency

	all_licenses = PyPI.get_all_licenses_safe(dependency)  # list of LICENSE strinfs

	response = dict()

	for (dependency_name, dependency_version), license_or_props in all_licenses:
		props = dict()
		if isinstance(license_or_props, str):
			lcs = license_or_props
			hashed_lcs = str(hash(lcs))

			props = extract_key_points_2(lcs)

			if props:
				db.write_cache(dependency_name, dependency_version, hashed_lcs, props)
				lvl = str(compare_key_params.calc_score(config, props))
			else:
				lvl = 4

		elif isinstance(license_or_props, dict):
			props = license_or_props

			lvl = str(compare_key_params.calc_score(config, props))

		elif license_or_props is None:

			lvl = 4

		info = dict()
		if props:
			info = compare_key_params.differing_params_dict(config, [props])



		if lvl in response.keys():

			response[lvl].append([dependency_name, dependency_version, info])
		else:
			response[lvl] = [[dependency_name, dependency_version, info]]


	#key_parameters = dict()

	#for DEPENDENCY, LICENSE in all_licenses:
	#	key_parameters.append(extract_key_points(LICENSE))

#	return {'0'}


	if response.keys() == ["0"] or not response.get('1') and not response.get('2') and not response.get('3'):
		return '0'


	for i in range(1,4):
		if str(i) in response.keys():
			continue
		response[str(i)] = []

	return response



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