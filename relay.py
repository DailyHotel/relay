import json
import os
import pprint
import requests
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor

url = os.environ['SLACK_URL']
port = int(os.environ['RELAY_PORT'])
default_channel = os.environ.get('DEFAULT_CHANNEL')
if not default_channel:
    default_channel = "#dev"
default_icon_url = os.environ.get['ICON_URL']    
if not default_icon_url:
    default_icon_url = 'https://dailyhotel.atlassian.net/s/rvt46q/b/20/bb034c42ada37676f34de6633df1f793/_/jira-logo-scaled.png'
headers = {'content-type': 'application/json'}

def channel_of_repo_name(repo_name):
    if not os.path.exists('channel_selector.json'):
        return default_channel
    with open('channel_selector.json', 'r') as json_file:
        channel_selector = json.load(json_file)
    if repo_name in channel_selector:
        return channel_selector[repo_name]
    else:
        return default_channel

def make_slack_post(docker_data):
    repo = docker_data['repository']
    push_data = docker_data['push_data']
    return {
        'channel': channel_of_repo_name(repo['repo_name']),
        'username': 'Docker Hub',
        'text': '<{}|{}> built successfully.'.format(repo['repo_url'], repo['repo_name']),
        'attachments': [{ "color": "good", "fields": [{ "title": "Tag", "value": push_data['tag'], "short": "false"}] }],
        "unfurl_links": 'false',
        'mrkdwn': 'true',
        'icon_url': default_icon_url
    }

class Relay(Resource):
    def render_GET(self, request):
        return '<html><body>Relay is running.</body></html>'

    def render_POST(self, request):
        print request.args
        payload = make_slack_post(json.loads(request.content.read()))
        pprint.pprint(payload)
        return requests.post(url, data=json.dumps(payload), headers=headers)

root = Resource()
root.putChild('relay', Relay())
factory = Site(root)
reactor.listenTCP(port, factory)
reactor.run()
