import asyncio
import websockets
from vosk import Model, KaldiRecognizer
import json

# Path to your VOSK model
MODEL_PATH = "en-us"
model = Model(lang=MODEL_PATH) 

# Function to store the final transcription in a file
def store_transcription(transcription):
    with open("transcriptions.txt", "a") as f:
        f.write(f"{transcription}\n")
        print(f"Final Transcription saved: {transcription}")

# Handle client connections
async def handle_client(websocket):  # Removed 'path'
    print("Client connected.")
    recognizer = KaldiRecognizer(model, 16000)
    
    try:
        async for message in websocket:
            print(f"Received data: {len(message)} bytes")  # Debug incoming data size
            if recognizer.AcceptWaveform(message):
                result = json.loads(recognizer.Result())
                transcription = result.get("text", "")
                print(f"Full Transcription: {transcription}")
                # Save final transcription to file
                store_transcription(transcription)
                await websocket.send(f"Transcription: {transcription}")
            else:
                partial = json.loads(recognizer.PartialResult())
                partial_text = partial.get("partial", "")
                print(f"Partial Transcription: {partial_text}")
                await websocket.send(f"Partial Transcription: {partial_text}")
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e}")
    except Exception as e:
        print(f"Error: {e}")

# Main function to start the server
async def main():
    print("Server starting...")
    async with websockets.serve(handle_client, "172.16.102.236", 8765):  # No 'path' required
        print("Server is running. Waiting for connections...")
        await asyncio.Future()  # Keeps the server running

if __name__ == "__main__":
    asyncio.run(main())
