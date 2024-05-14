from pigeon.shortcuts import Log
import pip
from importlib import metadata as importlib_metadata
from importlib.metadata import Distribution, requires
from typing import Any
import requests
import json
import re


log = Log("PiPy-API", "#03e3fc")


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
