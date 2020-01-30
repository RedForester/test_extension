import requests

from config import *


def register_extension():
    # make a call to the RedForester to register this extension
    resp = requests.post(f'{RF_BACKEND_BASE_URL}/extensions', json={
        'name': EXT_NAME,
        'description': EXT_DESCRIPTION,
        # The address where the methodology is launched in the format of protocol: // host: port / url.
        # Only necessary if the methodology has action type commands
        'baseUrl': EXT_BASE_URL,
        'email': EXT_EMAIL,
        'commands': [
            {
                'name': 'Send notify',
                'type': {
                    'action': 'notify',
                },
                'description': 'just notify'
            },
            {
                'name': 'Send notify using KV',
                'type': {
                    'action': 'notify_from_kv',
                },
                'description': 'just notify but with KV',
                'showRules': [
                    {
                        # Show on all map nodes
                        'allNodes': True,
                    },
                ],
            },
            {
                'name': 'Open url',
                'type': {
                    'action': 'url',
                },
                'description': 'open url in new tab',
                'showRules': [
                    {
                        # Show on nodes of this type
                        'selfType': 'CustomType1',
                    },
                ],
            },
            {
                'name': 'Command-url',
                'type': {
                    'url': f'${EXT_BASE_URL}/',
                },
                'description': 'open url in new tab',
                'showRules': [
                    {
                        # Show on nodes of this type
                        'selfType': 'CustomType1',
                    },
                ],
            },
            {
                'name': 'Open IFrame',
                'type': {
                    'action': 'iframe',
                },
                'description': 'just open iframe',
                'showRules': [
                    {
                        # Show on all descendants of a node of this type
                        'descendantOfType': 'CustomType1',
                    },
                ],
            },
            {
                'name': 'Throw error',
                'type': {
                    'action': 'with_error',
                },
                'description': 'show notification about error',
                'showRules': [
                    {
                        # Show on map root
                        'root': True,
                    },
                ],
            },
        ],
        # Types of nodes, necessary methodologies for work
        'requiredTypes': [
            {
                'name': 'CustomType1',
                'properties': [
                    {
                        'name': 'Field1',
                        'category': 'TEXT',
                        'argument': 'TEXT_SIMPLE',
                    }
                ],
            },
        ],
    }, headers={
        'Cookie': USER_COOKIE
    })
    if resp.ok:
        print(f'success, extension data = {resp.json()}')
    else:
        print(f'error, status code = {resp.status_code}, message = {resp.text}')


if __name__ == '__main__':
    register_extension()
