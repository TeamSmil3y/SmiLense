from importlib import metadata as importlib_metadata
from importlib.metadata import Distribution
from smilense import Config


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

	def compare_license(self, other: License) -> int:
		"""
		Compares this license with the provided other license

		:param other: the license to compare this license to
		:return: 0,1,2 or 3 depending on compatability rating (0 highest, 4 lowest)
		"""
		return 4

	def compare(self, other: License | Config) -> int:
		"""
		Compares this license with another license or with a config file

		:param other: the other license/ the config file to compare this license to
		:return: 0,1,2 or 3 depending on compatability rating (0 highest, 4 lowest)
		"""
		if isinstance(other, License):
			return self.compare_license(other)
		elif isinstance(other, Config):
			return self.compare_config(other)
		else:
			raise TypeError('other should be of type: License | Config')

def get_package(name):
	pkg_data = metadata.metadata(name)
	return pkg_data

def get_package_license(name):
	pkg_data = get_package(name)
	license = License()

	# if licensetext or licensefile attributes are set
	if licensetext:=pkg_data.get('licensetext'):
		license.licensetext = licensetext
	elif licensefile:=pkg_data.get('licensefile'):
		license.licensfile = licensefile
	elif license:=pkg_data.get('license'):
		license.license = license
