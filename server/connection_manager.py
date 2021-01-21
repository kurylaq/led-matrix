import asyncio
import json
import logging
import websockets
from multiprocessing import Process

class ConnectionManagerProcess(Process):
    def __init__(self, pipe_conn):
        super(ConnectionManagerProcess, self).__init__()
        logging.basicConfig()
        self.STATE = {"value": 0}
        self.USERS = set()
        self.pipe_conn = pipe_conn

    def state_event(self):
            print(json.dumps({"type": "state", **self.STATE}))
            return json.dumps({"type": "state", **self.STATE})


    def users_event(self):
        print(json.dumps({"type": "users", "count": len(self.USERS)}))
        return json.dumps({"type": "users", "count": len(self.USERS)})


    async def check_for_end_condition(self):
        end_cond = self.pipe_conn.recv()
        if end_cond[0] == "stop":
            self.pipe_conn.close()
            self.event_loop.stop()

    async def notify_state(self):
        if self.USERS:  # asyncio.wait doesn't accept an empty list
            message = self.state_event()
            await asyncio.wait([user.send(message) for user in self.USERS])


    async def notify_users(self):
        if self.USERS:  # asyncio.wait doesn't accept an empty list
            message = self.users_event()
            await asyncio.wait([user.send(message) for user in self.USERS])


    async def register(self, websocket):
        self.USERS.add(websocket)
        await self.notify_users()


    async def unregister(self, websocket):
        self.USERS.remove(websocket)
        await self.notify_users()


    async def counter(self, websocket, path):
        # register(websocket) sends user_event() to websocket
        await self.register(websocket)
        try:
            await websocket.send(self.state_event())
            async for message in websocket:
                data = json.loads(message)
                if data["action"] == "minus":
                    self.STATE["value"] -= 1
                    await self.notify_state()
                elif data["action"] == "plus":
                    self.STATE["value"] += 1
                    await self.notify_state()
                else:
                    logging.error("unsupported event: {}", data)
        finally:
            await self.unregister(websocket)

    def run(self):
        # WS server example that synchronizes state across clients
        self.event_loop = asyncio.get_event_loop()

        start_server = websockets.serve(self.counter, "localhost", 6789)

        try:
            self.event_loop.run_until_complete(start_server)
            self.event_loop.run_until_complete(self.check_for_end_condition())
        except KeyboardInterrupt:
            print("shutting down server")