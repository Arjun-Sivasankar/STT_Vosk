import asyncio
import websockets
import pyaudio
import signal
import sys

# Audio Configuration
SAMPLE_RATE = 16000
CHUNK = 4000

# Server IP and Port
SERVER_IP = "172.16.102.236"  # Replace with your server IP
SERVER_PORT = 8765
SERVER_URI = f"ws://{SERVER_IP}:{SERVER_PORT}"

# Global flag to stop streaming
stop_streaming = False

def signal_handler(sig, frame):
    """Handle Ctrl+C signal to terminate the client gracefully."""
    global stop_streaming
    print("\nCtrl+C detected. Stopping transcription...")
    stop_streaming = True

async def stream_audio():
    """Stream audio to the server."""
    global stop_streaming

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
        print("Connected to server. Streaming audio... (Press Ctrl+C to stop)")
        try:
            while not stop_streaming:
                # Read audio from the microphone
                audio_data = stream.read(CHUNK, exception_on_overflow=False)
                
                # Send audio data to server
                await websocket.send(audio_data)
                
                # Receive transcription response from server
                response = await websocket.recv()
                print(f"Server: {response}")
        except websockets.exceptions.ConnectionClosed as e:
            print(f"Connection closed: {e}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            print("Closing audio stream...")
            stream.stop_stream()
            stream.close()
            audio.terminate()
            print("Client stopped.")

if __name__ == "__main__":
    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Run the asyncio event loop
    try:
        asyncio.run(stream_audio())
    except KeyboardInterrupt:
        # Handle cases where signal handler might not catch SIGINT
        print("\nExiting transcription client...")



