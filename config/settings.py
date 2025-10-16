MODEL_NAME = "gpt-4o"  
MAX_TOKENS = 2000
TEMPERATURE = 0.7
POET_PERSONAS = {
    "romantic": {
        "name": "Aurora",
        "full_title": "Aurora (The Romantic)",
        "style": "Focuses on emotion, nature metaphors, flowing rhythm, and sensory imagery",
        "approach": "Seeks beauty and emotional truth in facts",
        "color": "#ff69b4",
        "icon": ""
    },
    "modernist": {
        "name": "Echo",
        "full_title": "Echo (The Modernist)",
        "style": "Sharp imagery, fragmented thoughts, unexpected juxtapositions, contemporary language",
        "approach": "Finds stark truth and irony in factual details",
        "color": "#4169e1",
        "icon": ""
    }
}
# Judging criteria weights
JUDGING_CRITERIA = {
    "factual_grounding": {
        "weight": 0.25,
        "description": "How well the verse connects to actual document content"
    },
    "poetic_quality": {
        "weight": 0.20,
        "description": "Literary merit: imagery, metaphor, rhythm, word choice"
    },
    "coherence": {
        "weight": 0.20,
        "description": "How well the verse fits with previous lines"
    },
    "originality": {
        "weight": 0.20,
        "description": "Creative interpretation and fresh perspective"
    },
    "emotional_impact": {
        "weight": 0.15,
        "description": "Ability to evoke feeling or insight"
    }
}
MIN_VERSES = 6
MAX_VERSES = 12
DEFAULT_VERSES = 8