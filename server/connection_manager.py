import asyncio
import json
import logging
from multiprocessing import Process
from aiohttp import web, WSMsgType

class ConnectionManagerProcess(Process):
    def __init__(self, pipe_conn):
        super(ConnectionManagerProcess, self).__init__()
        logging.basicConfig()
        self.USERS = set()
        self.pipe_conn = pipe_conn

        # read index site once to avoid repeat reads
        with open('./site/index.html', 'r') as file:
            self.index_site = file.read()

    async def get_end_condition(self):
        """check pipe for end condition and yield to event loop if not found"""
        while True:
            data = self.pipe_conn.poll()
            if data is not False:
                return data
            else:
                await asyncio.sleep(0.0001)

    async def check_for_end_condition(self):
        """call get_end_condition and stop the loop if message is stop"""
        end_cond = await self.get_end_condition()
        if end_cond[0] == "stop":
            self.pipe_conn.close()
            self.event_loop.stop()
        else:
            await self.check_for_end_condition()

    async def register(self, websocket):
        print("registering user")
        self.USERS.add(websocket)

    async def unregister(self, websocket):
        self.USERS.remove(websocket)

    async def send_data(self, data):
        self.pipe_conn.send(data)

    async def websocket_handler(self, request):
        """handle incoming websocket connection request"""
        ws = web.WebSocketResponse()
        await self.register(ws)
        try:
            await ws.prepare(request)
            await ws.send_str(json.dumps({"type": "state", "value": 1}))

            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    if len(data) >= 1:
                        await self.send_data(data)
                    else:
                        logging.error("unsupported event: {}", data)
                elif msg.type == WSMsgType.ERROR:
                    print('ws connection closed with exception %s' %
                        ws.exception())
        finally:
            await self.unregister(ws)
            print('websocket connection closed')

    async def handle_site_request(self, request):
        resp = web.Response(text=self.index_site, content_type="text/html")
        return resp

    async def handle_static_file_request(self, request):
        try:
            name = request.match_info['name']
            with open('./site/' + name, 'r') as file:
                resp = web.Response(text=file.read(), content_type="text/html")
                return resp
        except:
            print('unable to find such file')
            resp = web.Response()
            resp.set_status(404)
            return resp
            


    def run(self):
        # WS server example that synchronizes state across clients
        self.event_loop = asyncio.get_event_loop()
        
        # initialize web app and add relevant routes
        app = web.Application()
        app.add_routes([web.get('/', self.handle_site_request),
                        web.get('/ws', self.websocket_handler),
                        web.get('/{name}', self.handle_static_file_request)])

        try:
            # add web app setup to event loop
            runner = web.AppRunner(app)
            self.event_loop.run_until_complete(runner.setup())
            # add web app listening to event loop
            site = web.TCPSite(runner, 'localhost', 8080)
            self.event_loop.run_until_complete(site.start())
            # add listening for end condition to event loop
            self.event_loop.run_until_complete(self.check_for_end_condition())
            
            self.event_loop.run_forever()
        except KeyboardInterrupt:
            print("shutting down server")
            self.event_loop.close()