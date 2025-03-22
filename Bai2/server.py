import asyncio
import websockets
from websockets import protocol
import json

connected_peers = {}

async def handler(websocket):
    try:
        async for message in websocket:
            try:
                data = json.loads(message)

                # Đăng ký Peer
                if data["type"] == "register":
                    peer_id = data["peer_id"]
                    connected_peers[peer_id] = websocket
                    print(f"✅ Peer {peer_id} joined")

                # Xử lý tin nhắn
                elif data["type"] == "message":
                    to_peer = data["to"]
                    if to_peer in connected_peers:
                        # Kiểm tra kết nối trước khi gửi
                        if connected_peers[to_peer].state == protocol.State.OPEN:
                            try:
                                await connected_peers[to_peer].send(json.dumps({
                                    "type": "message",
                                    "from": data["from"],
                                    "text": data["text"]
                                }))
                                print(f"📩 {data['from']} -> {data['to']}: {data['text']}")
                            except websockets.exceptions.ConnectionClosedError as e:
                                print(f"❌ Failed to send message: {e}")
                                del connected_peers[to_peer]
                        else:
                            print(f"⚠️ Connection to Peer {to_peer} is already closed.")
                            del connected_peers[to_peer]
                    else:
                        print(f"⚠️ Peer {to_peer} not found")
                        await websocket.send(json.dumps({"type": "error", "message": "Peer not found"}))
            except json.JSONDecodeError:
                print(f"❌ Failed to decode message: {message}")

    except websockets.exceptions.ConnectionClosedOK:
        print("✅ Connection closed gracefully.")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"❌ Connection closed unexpectedly: {e}")
    except Exception as e:
        print(f"❌ Unexpected error in handler: {e}")

    finally:
        # Remove peer khi kết nối bị đóng
        peer_id = None
        for p_id, ws in connected_peers.items():
            if ws == websocket:
                peer_id = p_id
                break
        if peer_id:
            del connected_peers[peer_id]
            print(f"❌ Peer {peer_id} disconnected")

async def main():
    server = await websockets.serve(handler, "localhost", 8080) 
    print("✅ WebSocket server running at ws://localhost:8080")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
