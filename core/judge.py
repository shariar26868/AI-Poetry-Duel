from openai import OpenAI  
import json
from config.settings import MODEL_NAME, MAX_TOKENS, JUDGING_CRITERIA
from utils.prompts import get_judge_system_prompt, get_judge_user_prompt
class PoetryJudge:
    """
    AI Judge that evaluates verses using a multi-dimensional rubric
    
    Design Philosophy:
    - Objective, criteria-based evaluation
    - Transparent scoring with detailed reasoning
    - Weighted scoring across multiple dimensions
    """
    
    def __init__(self, client):
        self.client = client
        self.criteria = JUDGING_CRITERIA
        self.judgments = []
        
    def judge_verses(self, document_text, poem_context, verse_a, verse_b, poet_a_name, poet_b_name):
        """
        Evaluate two competing verses
        
        Returns: dict with scores, reasoning, and winner
        """
        system_prompt = get_judge_system_prompt()
        user_prompt = get_judge_user_prompt(
            document_text, 
            poem_context, 
            verse_a, 
            verse_b, 
            poet_a_name, 
            poet_b_name
        )
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            max_tokens=MAX_TOKENS,
            temperature=0.3,  
            response_format={"type": "json_object"},  
            messages=[
                {"role": "system", "content": system_prompt + "\n\nIMPORTANT: You must respond with valid JSON only."},
                {"role": "user", "content": user_prompt}
            ]
        )
        content = response.choices[0].message.content
        judgment = self._parse_judgment(content)
        judgment['verse_a_total'] = self._calculate_weighted_score(judgment['verse_a_scores'])
        judgment['verse_b_total'] = self._calculate_weighted_score(judgment['verse_b_scores'])
        judgment['poet_a_name'] = poet_a_name
        judgment['poet_b_name'] = poet_b_name        
        self.judgments.append(judgment)     
        return judgment  
    def _parse_judgment(self, response_text):
        """Parse judge's JSON response"""
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            return {
                "verse_a_scores": {k: 5 for k in self.criteria.keys()},
                "verse_b_scores": {k: 5 for k in self.criteria.keys()},
                "verse_a_reasoning": "Error parsing judgment",
                "verse_b_reasoning": "Error parsing judgment",
                "winner": "tie",
                "final_verdict": "Unable to parse judgment"
            }
    
    def _calculate_weighted_score(self, scores):
        """Calculate weighted total score"""
        total = 0
        for criterion, score in scores.items():
            weight = self.criteria[criterion]['weight']
            total += score * weight
        return round(total, 2)
    
    def get_final_statistics(self):
        """Calculate final statistics across all judgments"""
        if not self.judgments:
            return None
        poet_a_wins = 0
        poet_b_wins = 0   
        for judgment in self.judgments:
            poet_a_name = judgment.get('poet_a_name')
            poet_b_name = judgment.get('poet_b_name')
            winner = judgment.get('winner')
            
            if winner == poet_a_name:
                poet_a_wins += 1
            elif winner == poet_b_name:
                poet_b_wins += 1
        poet_a_avg = sum(j['verse_a_total'] for j in self.judgments) / len(self.judgments)
        poet_b_avg = sum(j['verse_b_total'] for j in self.judgments) / len(self.judgments)
        
        return {
            "poet_a_wins": poet_a_wins,
            "poet_b_wins": poet_b_wins,
            "poet_a_avg_score": round(poet_a_avg, 2),
            "poet_b_avg_score": round(poet_b_avg, 2)
        }




