from typing import Optional, Awaitable, Any

import logging
import traceback
import ujson

from aiohttp import ClientSession, BasicAuth
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application

from config import EXT_ADDRESS, EXT_PORT, RF_BACKEND_BASE_URL, EXT_BASE_URL


class BaseHandler(RequestHandler):
    @property
    def session_id(self):
        return self.request.headers.get('Session-Id')

    @property
    def map_id(self):
        return self.get_query_argument('mapId')

    @property
    def node_id(self):
        return self.get_query_argument('nodeId')

    @property
    def user_id(self):
        return self.get_query_argument('userId')

    @property
    def user_token(self):
        return self.request.headers['Rf-Extension-Token']

    # === Methods ===

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        """
        Implement this method to handle streamed request data.
        """
        pass

    def write_error(self, status_code: int, **kwargs: Any) -> None:
        self.set_header('Content-Type', 'application/json')

        lines = traceback.format_exception(*kwargs['exc_info'])

        self.finish({
            'error': {
                'code': status_code,
                'message': self._reason,
                'traceback': lines,
            }
        })

    def get(self, *args, **kwargs):
        self.finish('I\'m alive!')

    def post(self, *args, **kwargs):
        self.finish({
            'message': 'I\'m alive!',
        })


class MapsHandler(BaseHandler):
    def post(self, map_id):
        """
        This method handles assigning the extension to the map.
        Here, the extension can verify, that the map is satisfying some preconditions.
        It can be required types, nodes, etc.
        If everything is OK, the handler must response with the status 200.
        Otherwise, the handler can response with the status 400 and the body, which will describe the problem.
        This handler will be called at the extension registration to verify,
        that the extension is up and works.
        :param map_id: id of the map
        """

        # This is persistence extension user token. It allow to use RF API from special user (with limitations),
        #  listen event queue.
        # !!! This is single chance to get service token.
        service_token = self.request.headers['Rf-Extension-Token']

        logging.info(f'Extension assigned to map with id {map_id}, service token: {service_token}')

        self.finish()

    def delete(self, map_id):
        """
        This method handles removing the extension from the map.
        If the extension have some data associated to the map, it must be deleted here.
        All subsequent requests to the map will be rejected with 403 status.
        This handler will be called at the extension registration to verify,
        that the extension is up and works.
        :param map_id: id of the map
        """
        logging.info(f'Extension deleted from map with id {map_id}')

        self.finish()


class NotifyCommandHandler(BaseHandler):
    async def post(self):
        """
        This is an example command handler, that returns request arguments and the title of the node,
        at which it was called.
        """

        # Build response
        await self.finish({
            'notify': {
                # Id of the user, that started this command.
                'userId': self.user_id,
                # User session, that allows to send notifications back to the user interface in the browser
                'session': self.session_id,
                # Notification Text
                'content': f'Hello, RedForester!',
                # notification display style one of DEFAULT, PRIMARY, SUCCESS, DANGER, WARNING, INFO
                'style': 'SUCCESS',
                # notification display time in milliseconds
                'durationMs': 4 * 1000,
                # cancel URL may not be set
                'urlCancel': None,
                # Positive response URL, may not be set
                'urlContinue': None
            }
        })


class NotifyFromKvCommandHandler(BaseHandler):
    async def post(self):
        """
        Open dialog using KV
        """
        # creating a new aiohttp session with Basic Auth using user extension and user token as password
        _session: ClientSession = ClientSession(
            # Temporary user token, that allows the extension to access the RedForester API.
            auth=BasicAuth(login='extension', password=self.user_token),
            json_serialize=ujson.dumps,
        )

        async with _session.post(
            RF_BACKEND_BASE_URL + '/notify/notification/map/' + self.map_id,
            json={
                'user_id': self.user_id,
                'notification_type': 'info',
                'notification_text': 'Hello again RedForester'
            }
        ) as response:
            data = await response.text("utf-8")
            if response.status == 200:
                logging.info('Dialog has been created')
            else:
                logging.error(f'Dialog has NOT been created: {data}')

            await _session.close()


class DialogFromKvCommandHandler(BaseHandler):
    async def post(self):
        """
        Open dialog using KV
        """
        # creating a new aiohttp session with Basic Auth using user extension and user token as password
        _session: ClientSession = ClientSession(
            # Temporary user token, that allows the extension to access the RedForester API.
            auth=BasicAuth(login='extension', password=self.user_token),
            json_serialize=ujson.dumps,
        )

        async with _session.post(
            RF_BACKEND_BASE_URL + '/notify/dialog/map/' + self.map_id,
            json={
                'user_id': self.user_id,
                'dialog_src': EXT_BASE_URL,
                'dialog_size': {
                    'width': '300',
                    'height': '400'
                }
            }
        ) as response:
            data = await response.text("utf-8")
            if response.status == 200:
                logging.info('Dialog has been created')
            else:
                logging.error(f'Dialog has NOT been created: {data}')

            await _session.close()


class IframeCommandHandler(BaseHandler):
    async def post(self):
        """
        Command handler that open iframe
        """

        await self.finish({
            'iframe': {
                'url': EXT_BASE_URL,  # url that will be open by RF client
                # optional fields
                # used to indicate iframe width and height in pixels
                'width': 300,
                'height': 400,
            }
        })


class WithErrorCommandHandler(BaseHandler):
    async def post(self):
        """
        This is an example command handler, that open iframe
        """

        raise Exception('The value of this command is incorrect')


class OpenUrlCommandHandler(BaseHandler):
    async def post(self):
        """
        This is an example command handler, that open iframe
        """

        await self.finish({
            'url': {
                'url': EXT_BASE_URL
            }
        })


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG
    )

    # init tornado handlers
    app = Application([
        (r'/', BaseHandler),
        (r'/api/is-alive', BaseHandler),
        (r'/api/maps/(.+)', MapsHandler),
        # CMDs
        (r'/api/commands/notify', NotifyCommandHandler),
        (r'/api/commands/notify_from_kv', NotifyFromKvCommandHandler),
        (r'/api/commands/dialog_from_kv', DialogFromKvCommandHandler),
        (r'/api/commands/iframe', IframeCommandHandler),
        (r'/api/commands/with_error', WithErrorCommandHandler),
        (r'/api/commands/url', OpenUrlCommandHandler)
    ])

    app.listen(EXT_PORT, EXT_ADDRESS)
    logging.info(f'Run on {EXT_ADDRESS}:{EXT_PORT}')

    IOLoop.current().start()
