# streamer.py
import cv2
import asyncio
import websockets

async def stream_video():
    uri = "ws://localhost:8000/ws/stream"
    async with websockets.connect(uri) as websocket:
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            _, buffer = cv2.imencode('.jpg', frame)
            await websocket.send(buffer.tobytes())
        cap.release()

if __name__ == "__main__":
    # For Windows and other OS where the default event loop policy is different
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(stream_video())

