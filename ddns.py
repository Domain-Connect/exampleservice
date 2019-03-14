#-----------------------------------------------------------------------------
# /ddnscode
#
# OK.  We are being lazy here.  We are leveraging this web site as a landing page for
# displaying the code for the Dynamic DNS Demonstration application
#

from bottle import Bottle, run, route, template, request, response, abort, static_file, default_app, redirect

import config

@route('/ddnscode', method='GET')
def ddnscode():
    # This only works for the ddns wesbsite over the supported protocol
    if request.headers['Host'] != config.dynamicdns_website or request.urlparts.scheme != config.protocol:
        return abort(404)

    # Get the data from the URL
    code = request.query.get('code')
    error = request.query.get('error')

    if error != None and error != '':
        return template('ddns_error',
                {
                    'error': error
                })

    # Return template
    return template('ddns_oauth_code.tpl',
                    {
                        "oauth_code" : code
                    })
