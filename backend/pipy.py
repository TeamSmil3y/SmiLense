from pigeon.shortcuts import Log
import pip
from importlib import metadata as importlib_metadata
from importlib.metadata import Distribution, requires
from typing import Any
from smilense import Config
import requests
import json
import re


log = Log("PiPy-API", "#03e3fc")


class License:
	def __init__(self, licensetext: str, licensefile: str, license: str):
		self.licensetext = licensetext
		self.licensefile = licensefile
		self.license = license
	
	def compare_config(self, config: Config) -> int:
		"""
		Compares the client configuration with this license for compatability.

		:param config: the config to compare this license to
		:return: 0,1,2 or 3 depending on compatability rating (0 highest, 4 lowest)
		"""
		return 4

	def compare_license(self, other: Any) -> int:
		"""
		Compares this license with the provided other license

		:param other: the license to compare this license to
		:return: 0,1,2 or 3 depending on compatability rating (0 highest, 4 lowest)
		"""
		return 4

	def compare(self, other: Any | Config) -> int:
		"""
		Compares this license with another license or with a config file

		:param other: the other license/ the config file to compare this license to
		:return: 0,1,2 or 3 depending on compatability rating (0 highest, 4 lowest)
		"""
		if isinstance(other, type(self)):
			return self.compare_license(other)
		elif isinstance(other, Config):
			return self.compare_config(other)
		else:
			raise TypeError('other should be of type: License | Config')

	@classmethod
	def from_pipy_package(cls, name):
		"""
		Grabs pipy package form pipy and constructs License object for it.

		:param name: name of pipy package
		:return: the License object corresponding to the package
		"""
		pkg_data = PiPy.get_pkg_metadata(name)

		# if licensetext or licensefile attributes are set
		licensetext=pkg_data.get('licensetext')
		licensefile=pkg_data.get('licensefile')
		license=pkg_data.get('license')
	
		return cls(licensetext=licensetext, licensefile=licensefile, license=license)

class PiPyPackage:
	def __init__(self, metadata):
		self.metadata = metadata
	
	def get_repo(self) -> str | None:
		"""
		Gets the url of the github repository

		:return: the url to the github repository of the package, or None
		"""
		interesting_headers = [header[1].split(',')[1].strip() for header in self.metadata._headers if 'url' in header[0].lower()]
		pattern = re.compile('^https://github\\.com/[^/]*/[^/]*/?$')
		for header in interesting_headers:
			if pattern.match(header):
				return header



class PiPy:
	@staticmethod


	@staticmethod
	def get_license(name: str) -> str:
		"""
		Grabs license of package by PiPy name

		:param name: gets license from PiPy package name
		:return: str for license or None
		"""
		pkg = get_pkg()

	@staticmethod
	def get_pkg_metadata(name: str):
		"""
		Grabs PiPy package by name and returns metadata of pkg

		:param name: Name of PiPy package
		:return: metadata for PiPy package
		"""
		return importlib_metadata.metadata(name)
	
	@staticmethod
	def get_pkg(name: str):
		"""
		Grabs PiPy package by name and returns PiPyPackage object representing the package

		:param name: Name of PiPy package
		:return: PiPyPackage object representing the package
		"""
		pkg_metadata = PiPy.get_pkg_metadata(name)
		return PiPyPackage(metadata=pkg_metadata)

	@staticmethod
	def get_pkg_repo(name: str, import_name=None) -> str | None:
		"""
		Gets the url of the github repository if existent

		:param name: name of the PiPy package
		:param import_name: name of package for import
		:return: the url to the github repository of the package, or None
		"""
		import_name = import_name or name
		
		# if package is installed check metadata
		try:
			__import__(import_name)
			repo = PiPy.get_pkg(name).get_repo()
			if repo: return repo
		except ImportError:
			pass
		
		# check from api
		data = PiPy.api_call(name)
		try:
			repo = data.get('info').get('project_urls').get('Source')
			if repo and re.compile('^https://github\\.com/[^/]*/[^/]*/?$').match(repo):
				return repo
		except AttributeError:
			return

		# install package and check package metadata
		pip.main(['install', '--user', '--break-system-packages', name])
		__import__(import_name)
		return PiPy.get_pkg(name).get_repo()



	@staticmethod
	def api_call(name: str) -> dict:
		"""
		Does an API call to PiPy to get the JSON metadata for a given package.

		:param name: name of the PiPy package
		:return: the data as a dict
		"""
		url = f'https://pypi.org/pypi/{name}/json'
		log.verbose(f'checking {url}')
		response = requests.get(url)
		data = response.json()

		return dict(data)

	@staticmethod
	def isntall(name: str) -> dict:
		"""
		Does an API call to PiPy to get the JSON metadata for a given package.

		:param name: name of the PiPy package
		:return: the data as a dict
		"""
		url = f'https://pypi.org/pypi/{name}/json'
		log.verbose(f'checking {url}')
		response = requests.get(url)
		data = response.json()

		return dict(data)


if __name__ == '__main__':
	print("TEST 1")

	pkg  = PiPy.get_pkg('numpy')
	pkg  = PiPy.get_pkg('sqlalchemy')
	pkg  = PiPy.get_pkg('flask')
	print(PiPy.get_pkg_repo('flask'))
	print(PiPy.get_pkg_repo('django'))
	print(PiPy.get_pkg_repo('sqlalchemy'))
	print(PiPy.get_pkg_repo('beautifulsoup4', 'bs4'))
	print(PiPy.get_pkg_repo('pigeonpost', 'pigeon'))
	print(PiPy.get_pkg_repo('sqlite3', 'sqlite3'))
