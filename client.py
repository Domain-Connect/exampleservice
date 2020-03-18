#-------------------------------------------------------------
# Client tools

from bottle import Bottle, run, route, template, request, response, abort, static_file, default_app, redirect

import config

@route('/client', method='GET')
def client():

    # This only works for the hosting website over the supported protocol
    if request.headers['Host'] != config.hosting_website or request.urlparts.scheme != config.protocol:
        return abort(404)

    return template('client.tpl')
    
