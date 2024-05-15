from pigeon import Pigeon
from pigeon.shortcuts import HTTPRequest, HTTPResponse, error, Log
import smilense

log = Log('VIEWS', 'green')


@Pigeon.view('/', 'application/json')
def api_hello_world(request: HTTPRequest):
	return ""


@Pigeon.view('/api', 'application/json')
def api_hello_world(request: HTTPRequest):
	return "Hello World!"


@Pigeon.view('/api/compare', 'application/json')
def api_compare(request: HTTPRequest):
	if request.method != 'POST':
		return error(405)
	if not request.data:
		return error(405)
	return smilense.compare(request.data)

