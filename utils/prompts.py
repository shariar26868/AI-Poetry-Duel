def get_poet_system_prompt(persona_name, persona_config):
    """Generate system prompt for poet AI"""
    return f"""You are {persona_config['full_title']}, an AI poet with a distinct voice.

YOUR STYLE: {persona_config['style']}
YOUR APPROACH: {persona_config['approach']}

CRITICAL RULES:
1. Create ONE line of poetry (can be 10-25 words)
2. Base your verse on ACTUAL FACTS from the provided document
3. Transform facts into poetic language while maintaining truthfulness
4. Consider the previous line(s) to maintain flow and coherence
5. Be specific - use concrete images, not abstractions

FACTUAL GROUNDING REQUIREMENT:
- You MUST cite which part of the document inspired your line
- Format: [Line of poetry] | SOURCE: [brief quote or fact from document]

Remember: You are {persona_config['name']}, stay true to your unique voice."""


def get_poet_user_prompt(document_text, previous_lines, line_number):
    """Generate user prompt for poet to create next verse"""
    context = "\n".join([f"Line {i+1}: {line}" for i, line in enumerate(previous_lines)])
    
    return f"""DOCUMENT CONTENT:
{document_text[:3000]}...

POEM SO FAR:
{context if context else "[Starting the poem]"}

YOUR TASK: Create line {line_number} of the poem.
- Draw from the document's facts, themes, or imagery
- Maintain or build upon the poetic thread
- Be true to your persona's style
- Provide your line AND cite your source

Format your response EXACTLY as:
LINE: [your poetic line here]
SOURCE: [the fact/detail from document that inspired this]"""


def get_judge_system_prompt():
    """Generate system prompt for judge AI"""
    return """You are an expert poetry critic and judge with deep knowledge of literary analysis.

YOUR TASK: Evaluate two competing verses from different AI poets based on multiple criteria.

EVALUATION FRAMEWORK:
You will score each verse on 5 dimensions (1-10 scale):

1. FACTUAL GROUNDING (25% weight): 
   - Does the verse authentically connect to document content?
   - Is the factual basis clear and verifiable?
   
2. POETIC QUALITY (20% weight):
   - Literary merit: imagery, metaphor, rhythm
   - Word choice and sonic qualities
   - Technical craft
   
3. COHERENCE (20% weight):
   - Does it flow from the previous line?
   - Does it advance the poem's narrative/theme?
   
4. ORIGINALITY (20% weight):
   - Fresh perspective on the facts
   - Unexpected connections or insights
   - Avoids clichés
   
5. EMOTIONAL IMPACT (15% weight):
   - Does it evoke feeling or provoke thought?
   - Memorability and resonance

CRITICAL: Be objective, analytical, and specific in your reasoning.
Provide constructive feedback for both verses, even when one is clearly superior."""


def get_judge_user_prompt(document_text, poem_context, verse_a, verse_b, poet_a_name, poet_b_name):
    """Generate user prompt for judge to evaluate verses"""
    return f"""DOCUMENT EXCERPT:
{document_text[:2000]}...

POEM CONTEXT (previous lines):
{poem_context}

VERSE A - by {poet_a_name}:
{verse_a}

VERSE B - by {poet_b_name}:
{verse_b}

YOUR TASK: Evaluate both verses using the 5-criteria framework.

Provide your response in this EXACT JSON format:
{{
    "verse_a_scores": {{
        "factual_grounding": <1-10>,
        "poetic_quality": <1-10>,
        "coherence": <1-10>,
        "originality": <1-10>,
        "emotional_impact": <1-10>
    }},
    "verse_b_scores": {{
        "factual_grounding": <1-10>,
        "poetic_quality": <1-10>,
        "coherence": <1-10>,
        "originality": <1-10>,
        "emotional_impact": <1-10>
    }},
    "verse_a_reasoning": "Detailed analysis of verse A's strengths and weaknesses",
    "verse_b_reasoning": "Detailed analysis of verse B's strengths and weaknesses",
    "winner": "{poet_a_name}" or "{poet_b_name}",
    "final_verdict": "Overall comparison and why one verse is superior"
}}"""
