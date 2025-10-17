import unittest
from unittest.mock import Mock, MagicMock, patch
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.poet import AIPoet
from core.judge import PoetryJudge
from core.document_processor import DocumentProcessor
from config.settings import POET_PERSONAS, JUDGING_CRITERIA

class TestDocumentProcessor(unittest.TestCase):
    """Test document text extraction"""
    
    def setUp(self):
        self.processor = DocumentProcessor()
    
    def test_text_extraction_fallback(self):
        """Test that processor handles unknown file types gracefully"""
        mock_file = Mock()
        mock_file.type = "application/unknown"
        
        result = self.processor.extract_text(mock_file)
        self.assertIsNone(result)
    
    def test_pdf_extraction_structure(self):
        """Test PDF extraction logic structure"""
        self.assertTrue(hasattr(DocumentProcessor, '_extract_from_pdf'))
    
    def test_docx_extraction_structure(self):
        """Test DOCX extraction logic structure"""
        self.assertTrue(hasattr(DocumentProcessor, '_extract_from_docx'))
    
    def test_image_extraction_structure(self):
        """Test image OCR extraction structure"""
        self.assertTrue(hasattr(DocumentProcessor, '_extract_from_image'))

class TestPoet(unittest.TestCase):
    """Test AI Poet functionality"""
    
    def setUp(self):
        self.mock_client = Mock()
        self.poet_config = POET_PERSONAS['romantic']
        self.poet = AIPoet(self.mock_client, 'romantic', self.poet_config)
    
    def test_poet_initialization(self):
        """Test poet initializes with correct attributes"""
        self.assertEqual(self.poet.persona_key, 'romantic')
        self.assertEqual(self.poet.name, 'Aurora')
        self.assertEqual(len(self.poet.verses_created), 0)
    
    def test_verse_parsing(self):
        """Test parsing of verse response format"""
        response_text = """LINE: The stars whisper secrets in the night
SOURCE: Document mentions stellar observations"""
        
        result = self.poet._parse_verse_response(response_text)
        
        self.assertIn('line', result)
        self.assertIn('source', result)
        self.assertIn('poet', result)
        self.assertEqual(result['line'], 'The stars whisper secrets in the night')
        self.assertTrue('stellar observations' in result['source'])
    
    def test_verse_parsing_malformed(self):
        """Test parsing handles malformed responses"""
        response_text = "Random text without proper format"
        
        result = self.poet._parse_verse_response(response_text)
        self.assertIn('line', result)
        self.assertIn('source', result)

class TestJudge(unittest.TestCase):
    """Test Poetry Judge functionality"""
    
    def setUp(self):
        self.mock_client = Mock()
        self.judge = PoetryJudge(self.mock_client)
    
    def test_judge_initialization(self):
        """Test judge initializes with correct criteria"""
        self.assertEqual(self.judge.criteria, JUDGING_CRITERIA)
        self.assertEqual(len(self.judge.judgments), 0)
    
    def test_weighted_score_calculation(self):
        """Test weighted score calculation is correct"""
        scores = {
            'factual_grounding': 8,
            'poetic_quality': 7,
            'coherence': 9,
            'originality': 6,
            'emotional_impact': 8
        }
        
        result = self.judge._calculate_weighted_score(scores)
        expected = 8*0.25 + 7*0.20 + 9*0.20 + 6*0.20 + 8*0.15
        
        self.assertAlmostEqual(result, expected, places=2)
    
    def test_json_parsing_valid(self):
        """Test parsing of valid JSON judgment"""
        json_response = """{
            "verse_a_scores": {
                "factual_grounding": 8,
                "poetic_quality": 7,
                "coherence": 8,
                "originality": 7,
                "emotional_impact": 8
            },
            "verse_b_scores": {
                "factual_grounding": 7,
                "poetic_quality": 8,
                "coherence": 7,
                "originality": 8,
                "emotional_impact": 7
            },
            "verse_a_reasoning": "Good connection to source",
            "verse_b_reasoning": "Strong imagery",
            "winner": "Aurora",
            "final_verdict": "Aurora wins"
        }"""
        
        result = self.judge._parse_judgment(json_response)
        
        self.assertIn('verse_a_scores', result)
        self.assertIn('winner', result)
        self.assertEqual(result['winner'], 'Aurora')
    
    def test_json_parsing_invalid(self):
        """Test parsing handles invalid JSON gracefully"""
        invalid_response = "This is not JSON at all"
        
        result = self.judge._parse_judgment(invalid_response)
        self.assertIn('verse_a_scores', result)
        self.assertIn('verse_b_scores', result)
        self.assertEqual(result['verse_a_scores']['factual_grounding'], 5)
    
    def test_final_statistics_empty(self):
        """Test statistics with no judgments"""
        result = self.judge.get_final_statistics()
        self.assertIsNone(result)
    
    def test_final_statistics_calculation(self):
        """Test statistics calculation with sample judgments"""
        self.judge.judgments = [
            {
                'winner': 'Aurora',
                'verse_a_total': 8.0,
                'verse_b_total': 7.5,
                'poet_a_name': 'Aurora',
                'poet_b_name': 'Echo' 
            },
            {
                'winner': 'Echo',
                'verse_a_total': 7.0,
                'verse_b_total': 8.5,
                'poet_a_name': 'Aurora',
                'poet_b_name': 'Echo'  
            }
        ]
        
        stats = self.judge.get_final_statistics()
        
        self.assertEqual(stats['poet_a_wins'], 1)
        self.assertEqual(stats['poet_b_wins'], 1)
        self.assertEqual(stats['poet_a_avg_score'], 7.5)  
        self.assertEqual(stats['poet_b_avg_score'], 8.0)  

class TestConfiguration(unittest.TestCase):
    """Test configuration settings"""
    
    def test_poet_personas_structure(self):
        """Test that poet personas have required fields"""
        required_fields = ['name', 'full_title', 'style', 'approach', 'color', 'icon']
        
        for persona_key, persona in POET_PERSONAS.items():
            for field in required_fields:
                self.assertIn(field, persona, 
                    f"Persona {persona_key} missing field {field}")
    
    def test_judging_criteria_structure(self):
        """Test that judging criteria have required fields"""
        required_fields = ['weight', 'description']
        
        for criterion, details in JUDGING_CRITERIA.items():
            for field in required_fields:
                self.assertIn(field, details,
                    f"Criterion {criterion} missing field {field}")
    
    def test_judging_weights_sum(self):
        """Test that judging weights sum to 1.0"""
        total_weight = sum(details['weight'] for details in JUDGING_CRITERIA.values())
        self.assertAlmostEqual(total_weight, 1.0, places=2,
            msg="Judging criteria weights should sum to 1.0")
    
    def test_poet_personas_count(self):
        """Test that the correct number of poet personas are defined"""
        self.assertEqual(len(POET_PERSONAS), 6, 
                         f"Expected 6 poet personas, but found {len(POET_PERSONAS)}")

if __name__ == '__main__':
    unittest.main()