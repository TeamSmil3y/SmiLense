from pigeon import Pigeon
from pigeon.shortcuts import HTTPRequest, HTTPResponse, error
import smilense


@Pigeon.view('/api', 'application/json')
def api_hello_world(request: HTTPRequest):
	return "Hello World!"

@Pigeon.view('/api/check_github_repo', 'application/json')
def api_check_github_repo(request: HTTPRequest):
	if request.method != 'POST':
		return error(405)

	if not request.post.
	smilense.check_github_repo()
