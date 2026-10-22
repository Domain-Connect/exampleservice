#!/bin/sh
# Dev server at http://exampleservice.internal:8081/
cd "$(dirname "$0")"
APP_DOMAIN=exampleservice.internal:8081 APP_PROTOCOL=http APP_IP=172.25.0.2 \
  exec .venv/bin/python -c "import bottle, statelesshosting; bottle.run(statelesshosting.app, host='exampleservice.internal', port=8081)"
