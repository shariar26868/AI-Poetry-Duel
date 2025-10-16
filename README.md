# 🎭 AI Poetry Duel

A sophisticated system where two AI poets with distinct personas compete to create factually-grounded poetry from documents, evaluated by a third AI judge using a multi-dimensional rubric.

## 🌟 Key Features

- **🤖 Two AI Poets**: Aurora (Romantic) and Echo (Modernist) with unique voices
- **⚖️ Competitive Generation**: Both poets create each verse, judge selects the best
- **📚 Factual Grounding**: Every verse must cite its source from the document
- **🎯 Multi-Criteria Judging**: 5-dimensional evaluation with transparent scoring
- **🎵 Audio Narration**: Text-to-speech bonus feature
- **📊 Real-time Statistics**: Track performance and winning streaks

## 🏗️ Project Structure

```
poetry-duel/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env                           # API keys (create this)
├── README.md                      # This file
│
├── core/                          # Core logic modules
│   ├── poet.py                   # AI poet with personas
│   ├── judge.py                  # Evaluation system
│   ├── document_processor.py     # File parsing (PDF, DOCX, TXT, Images)
│   └── audio_generator.py        # Text-to-speech
│
├── utils/                         # Utility functions
│   ├── prompts.py               # AI prompts & templates
│   └── scoring.py               # Score calculations
│
├── config/                        # Configuration
│   └── settings.py              # Models, personas, criteria
│
└── tests/                         # Test suite
    └── test_basic.py            # Unit tests
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up API Key
Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=sk-proj-your-api-key-here
```

Get your API key from: https://platform.openai.com/api-keys

### 3. Run the App
```bash
streamlit run app.py
```

### 4. Use the App
1. Upload a document (PDF, DOCX, TXT, or Image)
2. Click "Start Poetry Duel"
3. Watch the poets compete!
4. View detailed judgments and statistics
5. Generate audio narration (optional)

## 📦 Requirements

- Python 3.8+
- OpenAI API key with credits
- Internet connection

## 🎨 How It Works

### The Innovation: Competitive Poetry Generation

```
Document → Extract Text
           ↓
    For each verse:
    ├─ Poet A creates verse
    ├─ Poet B creates verse
    ├─ Judge evaluates both
    └─ Winner's verse added to poem
           ↓
    Complete Poem + Statistics
```

### The Poets

**🌸 Aurora (The Romantic)**
- Style: Emotion, nature metaphors, flowing rhythm
- Approach: Seeks beauty in facts
- Example: *"The ocean whispers secrets in degrees of warmth ascending"*

**⚡ Echo (The Modernist)**  
- Style: Sharp imagery, fragmented thoughts, contemporary language
- Approach: Finds stark truth and irony
- Example: *"Nine-tenths Celsius—the math of melting"*

### The Judge

Evaluates verses on 5 criteria:
1. **Factual Grounding** (25%) - Connection to document
2. **Poetic Quality** (20%) - Literary merit
3. **Coherence** (20%) - Flow with previous lines
4. **Originality** (20%) - Creative interpretation
5. **Emotional Impact** (15%) - Resonance

## 💡 Why This Approach?

| Feature | Benefit |
|---------|---------|
| **Competitive Selection** | Only best verses make the final poem |
| **Factual Grounding** | Prevents AI hallucination |
| **Distinct Personas** | Diverse poetry styles |
| **Transparent Judging** | Mathematical, explainable decisions |
| **Real-time Evaluation** | Iterative quality improvement |

## 🎯 Use Cases

- **Educational**: Transform textbooks into memorable poetry
- **News**: Create poetic summaries of articles
- **Research**: Make scientific papers more accessible
- **Creative**: Reimagine any document as art
- **Business**: Turn reports into engaging narratives

## 🛠️ Configuration

### Change AI Model
Edit `config/settings.py`:
```python
MODEL_NAME = "gpt-4o-mini"  # Cheaper alternative
```

### Adjust Verses
In the sidebar, use the slider (6-12 verses)

### Customize Personas
Edit `config/settings.py` → `POET_PERSONAS`

## 📊 Example Output

**Input**: Climate change report  
**Output**:
```
The ocean whispers secrets in degrees of warmth ascending (Aurora)
Nine-tenths Celsius—the math of melting (Echo)
Where coral gardens once bloomed in crystalline embrace (Aurora)
Now bleached bones, a cemetery of color (Echo)
...
```

**Judge Verdict**: Aurora 5 wins, Echo 3 wins

## 🧪 Running Tests

```bash
python -m pytest tests/ -v
```

## 🐛 Troubleshooting

### "OpenAI API Key not found"
- Check `.env` file exists
- Verify key format: `OPENAI_API_KEY=sk-proj-...`
- Restart the app

### "Quota Exceeded" Error
- Check billing: https://platform.openai.com/account/billing
- Add payment method and credits
- Use `gpt-4o-mini` for cheaper alternative

### "No text extracted"
- Check file format (PDF, DOCX, TXT, PNG, JPG)
- Try a different file
- Ensure file isn't corrupted or password-protected

## 🔮 Future Enhancements

- [ ] More poet personas (Haiku Master, Beat Poet, Surrealist)
- [ ] Multi-language support
- [ ] User voting system
- [ ] Export to PDF with beautiful formatting
- [ ] Style transfer (write like Shakespeare, Dickinson, etc.)
- [ ] Tournament mode (4+ poets, bracket-style)

## 📄 License

MIT License - Feel free to use and modify!

## 🙏 Acknowledgments

Built with:
- **OpenAI GPT-4o** for AI creativity
- **Streamlit** for the interface
- **Python** for the logic

## 👨‍💻 Author

Created as a demonstration of:
- Multi-agent AI systems
- Competitive generation for quality control
- Transparent AI evaluation frameworks
- Factual grounding in creative AI

---
