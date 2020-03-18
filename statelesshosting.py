from bottle import Bottle, run, route, template, request, response, abort, static_file, default_app, redirect

import config
import util
import json

from simple import *
from sig import *
from ddns import *
from sync import *
from async import *
from client import *

app = application = default_app()

@route('/')
def index():

    protocol = request.urlparts.scheme

    # If the host is my hosting website, render the home page
    if request.headers['Host'] == config.hosting_website:
        
        if protocol == config.protocol:
            return template('index.tpl', {})
        elif config.protocol == 'https':
            return redirect('https://' + config.hosting_website, code=302)
        else:
            return abort(404)

    else:
        # See if the text string was put into DNS
        messagetext = util.get_messagetext(request.headers['Host'])

        # If we haven't found a message, see if this is "whd" variant
        if messagetext is None and request.headers['Host'].startswith('whd.'):
            messagetext = util.get_messagetext(request.header['Host'][4:])

        # If we have no message, we must be done
        if messagetext is None:
            return abort(404)

        # Render the site 
        return template('site.tpl', {'host': request.headers['Host'], 'messagetext': messagetext})

@route('/static/<filename>')
def send_static(filename):
    return static_file(filename, root='static')

# Runs the application for all hosts
if __name__ == "__main__":
    run(host='0.0.0.0', port=81, debug=True)

