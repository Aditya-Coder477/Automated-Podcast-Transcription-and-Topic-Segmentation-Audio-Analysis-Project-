from faster_whisper import WhisperModel
import os

class FasterPodcastTranscriber:
    def __init__(self, model_size="tiny", device="cpu", compute_type="int8"):
        """
        Initializes the Faster-Whisper model.
        
        Args:
            model_size (str): "tiny", "base", "small", "medium", "large-v2"
            device (str): "cpu" or "cuda" (if you have an NVIDIA GPU)
            compute_type (str): "int8" is fastest for CPU. Use "float16" for GPU.
        """
        print(f"⚡ Loading Faster-Whisper ({model_size}) on {device}...")
        try:
            self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        except Exception as e:
            print(f"⚠️ Error loading Faster-Whisper: {e}")
            raise e

    def transcribe(self, audio_path):
        """
        Transcribes audio using the optimized engine.
        Returns: (full_text, segments_list)
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        print(f"   🎙️ Transcribing {os.path.basename(audio_path)}...")
        
        # Run Transcription
        # beam_size=1 is fastest (greedy search). Increase to 5 for slightly better accuracy but slower speed.
        segments, info = self.model.transcribe(audio_path, beam_size=1)

        # Faster-Whisper returns a generator, so we must loop through it to get results
        formatted_segments = []
        full_text_parts = []

        print(f"   Detected language: {info.language} with probability {info.language_probability}")

        for segment in segments:
            text = segment.text.strip()
            if text:
                formatted_segments.append({
                    "start": segment.start,
                    "end": segment.end,
                    "text": text,
                    # Compatibility with your old code structure
                    "timestamp": (segment.start, segment.end) 
                })
                full_text_parts.append(text)
                
                # Optional: Print progress dots to show it's working
                print(".", end="", flush=True)

        print("\n   ✅ Transcription Complete!")
        return " ".join(full_text_parts), formatted_segments