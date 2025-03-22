import asyncio
import websockets
import json
import random

peer_id = f"{random.randint(1000, 9999)}"

async def listen_messages(ws):
    while True:
        try:
            message = await ws.recv()
            print(f"📥 Raw message received: {message}")  # Log message thô
            try:
                data = json.loads(message)
                if data["type"] == "message":
                    print(f"\n📩 Message from {data['from']}: {data['text']}\n")
                elif data["type"] == "error":
                    print(f"\n⚠️ Error: {data['message']}\n")
            except json.JSONDecodeError:
                print(f"❌ Failed to decode message: {message}")
        except websockets.exceptions.ConnectionClosed:
            print("❌ Connection closed.")
            break
        except Exception as e:
            print(f"❌ Unexpected error in listen_messages: {e}")
            break

async def send_messages(ws):
    while True:
        try:
            to_peer = input("Enter recipient peer ID: ")
            text = input("Enter message: ")
            await ws.send(json.dumps({"type": "message", "from": peer_id, "to": to_peer, "text": text}))
        except Exception as e:
            print(f"❌ Unexpected error in send_messages: {e}")
            break

async def main():
    uri = "ws://localhost:8080"
    while True:
        try:
            async with websockets.connect(uri, ping_interval=10, ping_timeout=5) as ws:
                await ws.send(json.dumps({"type": "register", "peer_id": peer_id}))
                print(f"✅ Connected as {peer_id}")

                await asyncio.gather(
                    listen_messages(ws),
                    send_messages(ws)
                )
        except Exception as e:
            print(f"❌ Connection error: {e}")
            print("🔄 Reconnecting in 5 seconds...")
            await asyncio.sleep(5)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\n❌ Exiting P2P chat.")