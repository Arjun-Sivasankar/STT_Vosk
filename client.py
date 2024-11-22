# import asyncio
# import websockets
# import sounddevice as sd

# SAMPLERATE = 16000
# BLOCKSIZE = 4000  # Keep this block size small for real-time processing

# async def send_audio(websocket):
#     loop = asyncio.get_event_loop()  # Get the main event loop

#     def callback(indata, frames, time, status):
#         if status:
#             print(f"Audio Status: {status}")
#         # Convert the indata to bytes (buffer to bytes)
#         loop.call_soon_threadsafe(send_audio_data, websocket, indata)

#     def send_audio_data(websocket, indata):
#         # Convert the indata to bytes and send it over the WebSocket
#         asyncio.create_task(websocket.send(bytes(indata)))

#     print("Capturing audio. Speak now...")
#     with sd.RawInputStream(samplerate=SAMPLERATE, blocksize=BLOCKSIZE, dtype='int16', channels=1, callback=callback):
#         await asyncio.Future()  # Keep the client running

# async def main():
#     try:
#         async with websockets.connect("ws://localhost:8765") as websocket:
#             await asyncio.gather(send_audio(websocket))
#     except Exception as e:
#         print(f"Connection error: {e}")

# if __name__ == "__main__":
#     asyncio.run(main())

import asyncio
import websockets
import pyaudio

# Audio Configuration
SAMPLE_RATE = 16000
CHUNK = 4000

# Server IP and Port
SERVER_IP = "172.16.102.236"
SERVER_PORT = 8765
SERVER_URI = f"ws://{SERVER_IP}:{SERVER_PORT}"

async def stream_audio():
    # Initialize PyAudio
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    print("Connecting to server...")
    async with websockets.connect(SERVER_URI) as websocket:
        print("Connected to server. Streaming audio...")
        try:
            while True:
                # Read audio from the microphone
                audio_data = stream.read(CHUNK, exception_on_overflow=False)
                
                # Send audio data to server
                await websocket.send(audio_data)
                
                # Receive transcription response from server
                response = await websocket.recv()
                print(f"Server: {response}")
        except websockets.exceptions.ConnectionClosed as e:
            print(f"Connection closed: {e}")
        except KeyboardInterrupt:
            print("\nStopping client.")
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()

if __name__ == "__main__":
    asyncio.run(stream_audio())

