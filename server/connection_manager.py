import asyncio
import json
import logging
import websockets
from multiprocessing import Process
from aiohttp import web

class ConnectionManagerProcess(Process):
    def __init__(self, pipe_conn):
        super(ConnectionManagerProcess, self).__init__()
        logging.basicConfig()
        self.USERS = set()
        self.pipe_conn = pipe_conn

    # def state_event(self):
    #         print(json.dumps({"type": "state", **self.STATE}))
    #         return json.dumps({"type": "state", **self.STATE})

    # async def notify_state(self):
    #     if self.USERS:  # asyncio.wait doesn't accept an empty list
    #         message = self.state_event()
    #         await asyncio.wait([user.send(message) for user in self.USERS])

    async def get_end_condition(self):
        while True:
            data = self.pipe_conn.poll()
            if data is not False:
                return data
            else:
                await asyncio.sleep(0.0001)

    async def check_for_end_condition(self):
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

    async def sendData(self, data):
        self.pipe_conn.send(data)

    async def counter(self, websocket, path):
        # register(websocket) sends user_event() to websocket
        await self.register(websocket)
        try:
            await websocket.send(json.dumps({"type": "state", "value": 1}))
            async for message in websocket:
                data = json.loads(message)
                if "action" in data or 'settings' in data:
                    await self.sendData(data)
                else:
                    logging.error("unsupported event: {}", data)
        finally:
            await self.unregister(websocket)

    async def handle(self, request):
        with open('./site/index.html', 'r') as file:
            resp = web.Response(text=file.read(), content_type="text/html")
            return resp


    def run(self):
        # WS server example that synchronizes state across clients
        self.event_loop = asyncio.get_event_loop()
        
        app = web.Application()
        app.add_routes([web.get('/', self.handle),
                        web.get('/{name}', self.handle)])
        
        start_server = websockets.serve(self.counter, "localhost", 6789)

        try:
            runner = web.AppRunner(app)
            self.event_loop.run_until_complete(runner.setup())
            site = web.TCPSite(runner, 'localhost', 8080)
            self.event_loop.run_until_complete(site.start())

            self.event_loop.run_until_complete(start_server)
            self.event_loop.run_until_complete(self.check_for_end_condition())
            
            self.event_loop.run_forever()
        except KeyboardInterrupt:
            print("shutting down server")