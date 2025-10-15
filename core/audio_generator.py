
from gtts import gTTS
import io


class AudioGenerator:
    """
    Generates audio narration of the poem (Bonus Feature)
    
    Uses Google Text-to-Speech for simplicity
    Can be enhanced with more sophisticated TTS systems
    """
    
    @staticmethod
    def generate_poem_audio(poem_lines, poet_names):
        """
        Generate audio file of the complete poem
        
        Returns: BytesIO object containing MP3 audio
        """
        # Compile full poem text with poet attributions
        full_text = "A collaborative poem.\n\n"
        
        for i, (line, poet) in enumerate(zip(poem_lines, poet_names)):
            full_text += f"{line}\n"
        
        # Generate speech
        tts = gTTS(text=full_text, lang='en', slow=False)
        
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        return audio_buffer