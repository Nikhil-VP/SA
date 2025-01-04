import asyncio
import websockets
import json
from typing import Dict, Set

class SignalingServer:
    def __init__(self):
        self.rooms: Dict[str, Set[websockets.WebSocketServerProtocol]] = {}

    async def register(self, websocket, room_id):
        if room_id not in self.rooms:
            self.rooms[room_id] = set()
        self.rooms[room_id].add(websocket)

    async def unregister(self, websocket, room_id):
        if room_id in self.rooms:
            self.rooms[room_id].remove(websocket)
            if not self.rooms[room_id]:
                del self.rooms[room_id]

    async def handle_connection(self, websocket, path):
        try:
            async for message in websocket:
                data = json.loads(message)
                room_id = data.get('room')
                
                if not room_id:
                    continue

                if websocket not in self.rooms.get(room_id, set()):
                    await self.register(websocket, room_id)

                # Broadcast the message to all other clients in the same room
                if room_id in self.rooms:
                    for client in self.rooms[room_id]:
                        if client != websocket:
                            await client.send(message)

        finally:
            # Clean up on disconnection
            for room_id in list(self.rooms.keys()):
                if websocket in self.rooms[room_id]:
                    await self.unregister(websocket, room_id)

async def main():
    server = SignalingServer()
    async with websockets.serve(server.handle_connection, "localhost", 8765):
        print("Signaling server running on ws://localhost:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main()) 