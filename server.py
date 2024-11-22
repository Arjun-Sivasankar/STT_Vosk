# import asyncio
# import websockets
# from vosk import Model, KaldiRecognizer
# import json
# from flask import Flask, render_template, jsonify
# from flask_socketio import SocketIO
# import threading

# # Path to your VOSK model
# MODEL_PATH = "en-us"
# model = Model(lang=MODEL_PATH)

# # Flask app for the webpage
# app = Flask(__name__)
# socketio = SocketIO(app, cors_allowed_origins="*")

# # File to store transcriptions
# TRANSCRIPTION_FILE = "transcriptions.json"

# # Initialize the JSON file if it doesn't exist
# def initialize_transcription_file():
#     try:
#         with open(TRANSCRIPTION_FILE, "r") as f:
#             json.load(f)  # Check if valid JSON exists
#     except (FileNotFoundError, json.JSONDecodeError):
#         with open(TRANSCRIPTION_FILE, "w") as f:
#             json.dump({"transcriptions": []}, f)

# # Function to store the final transcription in the JSON file and emit to webpage
# def store_transcription(transcription):
#     with open(TRANSCRIPTION_FILE, "r") as f:
#         data = json.load(f)
#     data["transcriptions"].append(transcription)
#     with open(TRANSCRIPTION_FILE, "w") as f:
#         json.dump(data, f, indent=4)
#     print(f"Final Transcription saved: {transcription}")
#     # Emit the transcription to connected webpage clients
#     socketio.emit("final_transcription", {"text": transcription})

# # Route to serve the webpage
# @app.route("/")
# def index():
#     return render_template("index.html")

# # Route to serve transcriptions as JSON
# @app.route("/transcriptions", methods=["GET"])
# def get_transcriptions():
#     try:
#         with open(TRANSCRIPTION_FILE, "r") as f:
#             data = json.load(f)
#         return jsonify(data)
#     except FileNotFoundError:
#         return jsonify({"transcriptions": []})

# # Handle WebSocket client connections for audio transcription
# async def handle_client(websocket):
#     print("Audio client connected.")
#     recognizer = KaldiRecognizer(model, 16000)
#     try:
#         async for message in websocket:
#             print(f"Received data: {len(message)} bytes")
#             if recognizer.AcceptWaveform(message):
#                 result = json.loads(recognizer.Result())
#                 transcription = result.get("text", "")
#                 print(f"Full Transcription: {transcription}")
#                 # Save final transcription and send to webpage
#                 store_transcription(transcription)
#                 await websocket.send(f"Transcription: {transcription}")
#             else:
#                 partial = json.loads(recognizer.PartialResult())
#                 partial_text = partial.get("partial", "")
#                 print(f"Partial Transcription: {partial_text}")
#                 await websocket.send(f"Partial Transcription: {partial_text}")
#     except websockets.exceptions.ConnectionClosed as e:
#         print(f"Connection closed: {e}")
#     except Exception as e:
#         print(f"Error: {e}")

# # Run WebSocket server for audio transcription
# async def start_audio_websocket():
#     print("WebSocket server for audio starting...")
#     async with websockets.serve(handle_client, "0.0.0.0", 8765):
#         print("WebSocket server is running. Waiting for connections...")
#         await asyncio.Future()  # Keep the server running

# # Run Flask server for webpage
# def start_flask_server():
#     socketio.run(app, host="0.0.0.0", port=5000)

# # Main function to start both servers
# if __name__ == "__main__":
#     initialize_transcription_file()  # Initialize the transcription file
#     # Run Flask server in a separate thread
#     threading.Thread(target=start_flask_server, daemon=True).start()
#     # Run WebSocket server in the main thread
#     asyncio.run(start_audio_websocket())


# import asyncio
# import websockets
# from vosk import Model, KaldiRecognizer
# import json
# from flask import Flask, render_template, jsonify
# import threading

# # Path to your VOSK model
# MODEL_PATH = "en-us"
# model = Model(lang=MODEL_PATH)

# # Flask app for the webpage
# app = Flask(__name__)

# # File to store transcriptions
# TRANSCRIPTION_FILE = "transcriptions.json"

# # Initialize the JSON file if it doesn't exist
# def initialize_transcription_file():
#     try:
#         with open(TRANSCRIPTION_FILE, "r") as f:
#             json.load(f)  # Check if valid JSON exists
#     except (FileNotFoundError, json.JSONDecodeError):
#         with open(TRANSCRIPTION_FILE, "w") as f:
#             json.dump({"transcriptions": []}, f)

# # Function to store the final transcription in the JSON file
# def store_transcription(transcription):
#     with open(TRANSCRIPTION_FILE, "r") as f:
#         data = json.load(f)
#     data["transcriptions"].append(transcription)
#     with open(TRANSCRIPTION_FILE, "w") as f:
#         json.dump(data, f, indent=4)
#     print(f"Final Transcription saved: {transcription}")

# # Route to serve the webpage
# @app.route("/")
# def index():
#     return render_template("index.html")

# # Route to serve transcriptions as JSON
# @app.route("/transcriptions", methods=["GET"])
# def get_transcriptions():
#     try:
#         with open(TRANSCRIPTION_FILE, "r") as f:
#             data = json.load(f)
#         return jsonify(data)
#     except FileNotFoundError:
#         return jsonify({"transcriptions": []})

# # Handle WebSocket client connections for audio transcription
# async def handle_client(websocket):
#     print("Audio client connected.")
#     recognizer = KaldiRecognizer(model, 16000)
#     try:
#         async for message in websocket:
#             print(f"Received data: {len(message)} bytes")
#             if recognizer.AcceptWaveform(message):
#                 result = json.loads(recognizer.Result())
#                 transcription = result.get("text", "")
#                 print(f"Full Transcription: {transcription}")
#                 # Save final transcription
#                 store_transcription(transcription)
#                 await websocket.send(f"Transcription: {transcription}")
#             else:
#                 partial = json.loads(recognizer.PartialResult())
#                 partial_text = partial.get("partial", "")
#                 print(f"Partial Transcription: {partial_text}")
#                 await websocket.send(f"Partial Transcription: {partial_text}")
#     except websockets.exceptions.ConnectionClosed as e:
#         print(f"Connection closed: {e}")
#     except Exception as e:
#         print(f"Error: {e}")

# # Run WebSocket server for audio transcription
# async def start_audio_websocket():
#     print("WebSocket server for audio starting...")
#     async with websockets.serve(handle_client, "0.0.0.0", 8765):
#         print("WebSocket server is running. Waiting for connections...")
#         await asyncio.Future()

# # Run Flask server for webpage
# def start_flask_server():
#     app.run(host="0.0.0.0", port=5000)

# # Main function to start both servers
# if __name__ == "__main__":
#     initialize_transcription_file()  # Initialize the transcription file
#     # Run Flask server in a separate thread
#     threading.Thread(target=start_flask_server, daemon=True).start()
#     # Run WebSocket server in the main thread
#     asyncio.run(start_audio_websocket())


import asyncio
import websockets
from vosk import Model, KaldiRecognizer
import json
from flask import Flask, render_template, jsonify
import threading
from time import time

# Path to your VOSK model
MODEL_PATH = "en-us"
model = Model(lang=MODEL_PATH)

# Flask app for the webpage
app = Flask(__name__)

# File to store transcriptions
TRANSCRIPTION_FILE = "transcriptions.json"

# Initialize the JSON file if it doesn't exist
def initialize_transcription_file():
    try:
        with open(TRANSCRIPTION_FILE, "r") as f:
            json.load(f)  # Check if valid JSON exists
    except (FileNotFoundError, json.JSONDecodeError):
        with open(TRANSCRIPTION_FILE, "w") as f:
            json.dump({"transcriptions": []}, f)

# Function to store the final transcription with timestamps in the JSON file
def store_transcription(transcription):
    with open(TRANSCRIPTION_FILE, "r") as f:
        data = json.load(f)
    
    # Append transcription with timestamps
    data["transcriptions"].append(transcription)
    
    with open(TRANSCRIPTION_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Final Transcription saved: {transcription}")

# Route to serve the webpage
@app.route("/")
def index():
    return render_template("index.html")

# Route to serve transcriptions as JSON
@app.route("/transcriptions", methods=["GET"])
def get_transcriptions():
    try:
        with open(TRANSCRIPTION_FILE, "r") as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"transcriptions": []})

# Handle WebSocket client connections for audio transcription
async def handle_client(websocket):
    print("Audio client connected.")
    recognizer = KaldiRecognizer(model, 16000)
    start_time = time()  # Start timestamp for the current segment
    try:
        async for message in websocket:
            print(f"Received data: {len(message)} bytes")
            if recognizer.AcceptWaveform(message):
                result = json.loads(recognizer.Result())
                transcription_text = result.get("text", "")
                
                # End timestamp for the current segment
                end_time = time()

                # Prepare transcription with timestamps
                transcription = {
                    "start": start_time,
                    "end": end_time,
                    "text": transcription_text
                }

                # Store and log the transcription
                store_transcription(transcription)

                # Update start_time for the next segment
                start_time = time()

                # Send the transcription to the client
                await websocket.send(json.dumps(transcription))
            else:
                partial = json.loads(recognizer.PartialResult())
                partial_text = partial.get("partial", "")
                print(f"Partial Transcription: {partial_text}")
                await websocket.send(json.dumps({"partial": partial_text}))
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e}")
    except Exception as e:
        print(f"Error: {e}")

# Run WebSocket server for audio transcription
async def start_audio_websocket():
    print("WebSocket server for audio starting...")
    async with websockets.serve(handle_client, "0.0.0.0", 8765):
        print("WebSocket server is running. Waiting for connections...")
        await asyncio.Future()

# Run Flask server for webpage
def start_flask_server():
    app.run(host="0.0.0.0", port=5000)

# Main function to start both servers
if __name__ == "__main__":
    initialize_transcription_file()  # Initialize the transcription file
    # Run Flask server in a separate thread
    threading.Thread(target=start_flask_server, daemon=True).start()
    # Run WebSocket server in the main thread
    asyncio.run(start_audio_websocket())
