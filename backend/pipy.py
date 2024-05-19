from pigeon.shortcuts import Log
from rich import print
import pip
import subprocess
import importlib
from importlib import metadata as importlib_metadata
from importlib.metadata import Distribution, requires
from typing import Any
import nlp.data_services as db
import requests
import json
import re
from random import choice


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
	def execute_safe(name, func):
		"""
		Installes a PyPI package and calls func(name) before uninstalling the package again

		:param name: name of PyPI package
		:param func: func to call on name
		:return: return value of func
		"""
		# check if package is installed
		exists = True if importlib.util.find_spec(name) else False

		# install package
		if not exists:
			print(f'[bold red]INSTALLING {name} SINCE IT DOES NOT EXIST[/]')
			pip.main(['install', '--user', '--break-system-packages', name])
			print(f'[bold green]INSTALL SUCCESS[/]')	
		
		return_val = func(name)

		# don't you wanna keep these? ;)
		return return_val

		# uninstall package
		if not exists:
			print(f'[bold red]UNINSTALLING {name}[/]')
			pip.main(['uninstall', '-y', '--break-system-packages', name])

		return return_val

	@staticmethod
	def get_dependencies(name: str) -> set[str]:
		"""
		Grabs the dependencies of a PiPy package

		:param name: PiPy package name
		:return: list of dependencies
		"""
		dependency_info = PiPy.get_dependency_info(name)
		
		if not isinstance(dependency_info, list):
			return None
		else:
			if not dependency_info: return dependency_info
			#print(dependency_info)
			return set(PiPy.flatten_dependencies(dependency_info[0]))

	@staticmethod
	def flatten_dependencies(dependency_info: dict) -> list[str]:
		"""
		Flattens the json dependency_info to a list of dependencies

		:param dependency_info: the json data for dependencies
		:returns: flat list of strings (name of PiPy dependencies)
		"""
		dependencies = [dependency_info.get('key')]
		if further_dependencies:=dependency_info.get('dependencies'):
			for further_dependency in further_dependencies:
				dependencies += PiPy.flatten_dependencies(further_dependency)
		return dependencies


	@staticmethod
	def get_dependency_info(name: str) -> list:
		"""
		Grabs the dependency info of a PiPy package

		:param name: PiPy package name
		:return: list of dependencies
		"""
		cmd = f'pipdeptree --packages {name} --json-tree'
		print(f'RUNNING [bold yellow]{cmd}[/]')
		data = subprocess.getoutput(cmd)
		if isinstance(data, str):
			if not data: 
				return []
			dependencies = json.loads(data)
			return(dependencies)
		else:
			print(f'DEPENDENCIES INVALID: {type(data)}, {data}')

	@staticmethod
	def get_license(name: str) -> str:
		"""
		Grabs license of package by PiPy name

		:param name: PiPy package name
		:return: str for license or None
		"""
		license_info = PiPy.get_licenses(name)
		if not license_info:
			return None
		else:
			return license_info[0].get('LicenseText')

	@staticmethod
	def get_all_licenses_safe(name: str) -> list[tuple[str,str]]:
		"""
		Grabs all licenses from all dependencies of any PyPI package (even if not installed)

		:param name: the name of the PyPI package
		:return: list of licenses as list[tuple[str,str]]
		"""
		return PiPy.execute_safe(name, PiPy.get_all_licenses)

	@staticmethod
	def get_all_licenses(name: str) -> list[tuple[str,str]]:
		"""
		Grabs all licenses from all dependencies of a PyPI package

		:param name: the name of the PyPI package
		:return: list of licenses as list[tuple[str,str]]
		"""
		# get all dependencies
		dependencies = [*PiPy.get_dependencies(name)]
		print(f'[bold green]FOUND DEPENDENCIES FOR {name}:[/] {dependencies}')

		licenses = []
		for dependency in dependencies:
			dependency_version = 'unknown'
			if dependency:
				if db.check_dependency_cache(dependency, dependency_version):
					license = db.get_cached_properties(dependency, dependency_version)
					print(f'[bold green]FOUND CACHE FOR[/] {dependency}: {license}')
				else:
					license = PiPy.get_license(dependency)
					print(f'[bold green]LICENSE FOR[/] {dependency}: {None if not license else license[0:30]}...')
				licenses.append(((dependency, dependency_version), license))
		return licenses

	@staticmethod
	def get_licenses(name: str) -> list:
		"""
		Grabs license info of package by PiPy name

		:param name: PiPy package name
		:return: str for license or None
		"""
		cmd = f'pip-licenses --with-license-file --format=json --packages {name}'
		print(f'RUNNING [bold yellow]{cmd}[/]')
		data = subprocess.getoutput(cmd)
		if isinstance(data, str):
			licenses = json.loads(data)
			return(licenses)
		else:
			print(f'LICENSE INVALID: {type(data)}, {data}')

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
	examples = [
		'numpy',
		'sqlalchemy',
		'flask',
		'django',
		'beautifulsoup4',
		'pigeonpost',
		'sqlite3',
		'rapid-sdk',
	]

	test_case = choice(examples)
	
	#print(f'[bold green]TESTCASE:[/] [bold yellow](LICENSES)[/] {test_case}')
	#print(PiPy.get_license(test_case))

	#print(f'[bold green]TESTCASE:[/] [bold yellow](DEPENDENCIES)[/] {test_case}')
	#print(PiPy.get_dependencies(test_case))

	print(f'[bold green]TESTCASE:[/] [bold yellow](ALL LICENSES)[/] {test_case}')
	print(PiPy.get_all_licenses(test_case))

	print(f'[bold green]TESTCASE:[/] [bold yellow]([/][bold blue]SAFE[/][bold yellow] - ALL LICENSES)[/] {test_case}')
	print(PiPy.get_all_licenses_safe(test_case))