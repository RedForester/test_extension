import os

# base url of the RedForester API
RF_BACKEND_BASE_URL = os.getenv('RF_BACKEND_BASE_URL', 'http://app.test,redforester.com/api')


########################################################
# address and port where you can send a request for extension
EXT_ADDRESS = os.getenv('HOST', '0.0.0.0')
EXT_PORT = os.getenv('PORT', 8080)


########################################################
# should be unique
EXT_NAME = 'test-extension'
EXT_DESCRIPTION = 'test extension description'

# author email
EXT_EMAIL = 'you.public.email@domain'

# address, at which this extension is listening
EXT_BASE_URL = f'https://{os.getenv("HEROKU_APP_NAME", "")}.herokuapp.com:443'

# Cookie of the owner of this extension. Required only for register_extension.py script.
USER_COOKIE = ''
