import os
import json
import queue
import pyaudio
from vosk import Model, KaldiRecognizer

# Initialize Vosk Model
# MODEL_PATH = "vosk-model-small-en-us"  # Replace with your model path
# if not os.path.exists(MODEL_PATH):
#     print("Please download the model from https://alphacephei.com/vosk/models and unpack it here.")
#     exit(1)

model = Model(lang="en-us")

# Audio configuration
SAMPLE_RATE = 16000  # Required sample rate for Vosk
CHUNK = 4000  # Buffer size

# Initialize recognizer
recognizer = KaldiRecognizer(model, SAMPLE_RATE)
recognizer.SetWords(True)

# Create a queue to handle audio data
audio_queue = queue.Queue()

def audio_callback(in_data, frame_count, time_info, status):
    """Callback to store audio chunks in the queue."""
    audio_queue.put(in_data)
    return (in_data, pyaudio.paContinue)

def main():
    # Initialize PyAudio
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK,
        stream_callback=audio_callback
    )
    stream.start_stream()

    print("Listening... Press Ctrl+C to stop.")

    try:
        while True:
            # Read data from queue
            if not audio_queue.empty():
                data = audio_queue.get()

                # Recognize speech
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    print(f"Text: {result.get('text', '')}")  # Print the transcribed text
                else:
                    partial_result = json.loads(recognizer.PartialResult())
                    print(f"Partial: {partial_result.get('partial', '')}")  # Print partial results
    except KeyboardInterrupt:
        print("\nStopping transcription.")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

if __name__ == "__main__":
    main()
