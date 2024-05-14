import json
from nlp.extract_key_points import extract_key_points
import yaml
import base64
from pigeon.shortcuts import Log
import sqlalchemy as sql
from sqlalchemy import Table, Column, desc, func
from pipy import PiPy as PyPI
from nlp.db_init import *

log = Log('SMILESENSE', 'blue')


def compare(data):
	"""
	Compares the license in the data to the configuration in the data.

	:param data: pigeon HTTPRequest data
	:return:
	"""
	log.info(data)
	config = yaml.safe_load(base64.b64decode(data.get('license-manifest.yaml')))  # {"keyparameter": "value"}
	#license = base64.b64decode(data.get('LICENSE'))  # LICENSE.txt as string
	dependency = base64.b64decode(data.get('checkPackage'))  # Name of dependency

	#all_licenses = PyPI.get_all_licenses(dependency)  # list of LICENSE strinfs

	#key_parameters = dict()

	#for DEPENDENCY, LICENSE in all_licenses:
	#	key_parameters.append(extract_key_points(LICENSE))





#	return {'0'}
	return {'1': [['testpkg1', '0.0.1'], ['testpkg2', '2.0.9']]}



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