# audio_processor placeholder
import whisper
import os

model = whisper.load_model("base")

def process_audio(file_path):
    try:
        result = model.transcribe(file_path, language='en')
        
        transcription = result['text']
        
        metadata = {
            'language': result.get('language', 'unknown'),
            'duration': result.get('duration', 0)
        }
        
        return transcription.strip(), metadata
    
    except Exception as e:
        return f"Error processing audio: {str(e)}", {}

def process_video(file_path):
    return process_audio(file_path)
