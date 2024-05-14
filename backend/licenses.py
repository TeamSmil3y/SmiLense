from importlib import metadata as importlib_metadata
from importlib.metadata import Distribution

class License:
	def __init__(self, licensetext, licensefile, license):
		self.licensetext = licensetext
		self.licensefile = licensefile
		self.license = license

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