from openai import OpenAI  
from config.settings import MODEL_NAME, MAX_TOKENS, TEMPERATURE
from utils.prompts import get_poet_system_prompt, get_poet_user_prompt
class AIPoet:
    """
    Represents an AI poet with a specific persona and style
    
    Design principle: Each poet maintains consistency in voice
    while responding creatively to the document and other poet
    """
    
    def __init__(self, client, persona_key, persona_config):
        self.client = client
        self.persona_key = persona_key
        self.config = persona_config
        self.name = persona_config['name']
        self.verses_created = []
        
    def create_verse(self, document_text, previous_lines, line_number):
        """
        Generate a single verse of poetry
        
        Returns: dict with 'line' and 'source' keys
        """
        system_prompt = get_poet_system_prompt(self.name, self.config)
        user_prompt = get_poet_user_prompt(document_text, previous_lines, line_number)
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        content = response.choices[0].message.content
        verse_data = self._parse_verse_response(content)
        self.verses_created.append(verse_data)      
        return verse_data  
    def _parse_verse_response(self, response_text):
        """Parse the poet's response into structured data"""
        lines = response_text.strip().split('\n')
        verse_line = ""
        source = ""
        
        for line in lines:
            if line.startswith("LINE:"):
                verse_line = line.replace("LINE:", "").strip()
            elif line.startswith("SOURCE:"):
                source = line.replace("SOURCE:", "").strip()
        
        return {
            "line": verse_line,
            "source": source,
            "poet": self.name
        }