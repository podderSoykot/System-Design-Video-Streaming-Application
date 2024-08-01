# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from jinja2 import Template
import os
import asyncio

app = FastAPI()

# HTML template for the video player
html = """
<!DOCTYPE html>
<html>
<head>
    <title>Live Streaming</title>
</head>
<body>
    <h1>Live Stream</h1>
    <video id="video" width="600" controls autoplay></video>
    <script>
        const video = document.getElementById('video');
        const ws = new WebSocket(`ws://${location.host}/ws/stream`);
        
        const mediaSource = new MediaSource();
        video.src = URL.createObjectURL(mediaSource);
        
        let sourceBuffer;
        mediaSource.addEventListener('sourceopen', () => {
            sourceBuffer = mediaSource.addSourceBuffer('video/mp4; codecs="avc1.42E01E, mp4a.40.2"');
            sourceBuffer.addEventListener('updateend', () => {
                // Handle any additional logic after buffering
            });
        });

        ws.onmessage = function(event) {
            if (sourceBuffer && !sourceBuffer.updating) {
                sourceBuffer.appendBuffer(new Uint8Array(event.data));
            }
        };
        
        ws.onclose = function() {
            alert("WebSocket connection closed");
        };
    </script>
</body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    video_path = r"E:/Torent/Udemy Key English Grammar Rules Needed for IELTS 7+/1. Lectures/1. Present Time.mp4"
    
    if not os.path.exists(video_path):
        await websocket.close(code=4000)  # Close connection with error code if file not found
        return
    
    try:
        with open(video_path, 'rb') as video_file:
            while True:
                data = video_file.read(1024 * 512)  # Read in chunks of 512KB
                if not data:
                    break
                await websocket.send_bytes(data)
                await asyncio.sleep(0.1)  # Small delay to control streaming rate
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("WebSocket connection closed")


