# 🎭 Poetry Duel Arena

Transform your documents into collaborative poetry through AI competition!

## 🌟 What is Poetry Duel?

Poetry Duel Arena is an innovative application where two AI poets with distinct personas compete to create the best verses based on your uploaded document. An AI judge evaluates each round, and the winning verses combine to form a beautiful collaborative poem.

## ✨ Features

- 📄 **Multi-format Support**: Upload PDF, DOCX, TXT, or images (with OCR)
- 🎨 **Distinct Poet Personas**: 
  - **Aurora** (Romantic): Emotional, nature-inspired, flowing verses
  - **Echo** (Modernist): Sharp, fragmented, contemporary style
- 🎯 **AI Judge**: Objective evaluation across 5 criteria
- 🔊 **Audio Output**: Listen to your generated poem
- 📊 **Detailed Analytics**: Round-by-round judgments and final statistics

## 🎯 How It Works

1. **Upload** a document (research paper, article, story, etc.)
2. **Select** two different poet personas
3. **Choose** the number of verses (6-12)
4. **Watch** as poets compete and the judge decides
5. **Enjoy** the final collaborative poem with audio narration

## 📊 Judging Criteria

Each verse is evaluated on:
- **Factual Grounding** (25%): Connection to document content
- **Poetic Quality** (20%): Literary merit and craft
- **Coherence** (20%): Flow with previous lines
- **Originality** (20%): Fresh perspective and creativity
- **Emotional Impact** (15%): Ability to evoke feeling

## 🚀 Deployment on HuggingFace

### Setup

1. Create a new Space on HuggingFace
2. Select "Gradio" as the SDK
3. Upload all files from the repository
4. Add your OpenAI API key to the Secrets:
   - Key: `OPENAI_API_KEY`
   - Value: Your OpenAI API key

### Project Structure

```
poetry-duel/
├── app.py                    # Main Gradio application
├── requirements.txt          # Python dependencies
├── README.md                # This file
│
├── core/                    # Core logic modules
│   ├── poet.py             # AI poet with personas
│   ├── judge.py            # Evaluation system
│   ├── document_processor.py # File parsing
│   └── audio_generator.py  # Text-to-speech
│
├── utils/                   # Utility functions
│   ├── prompts.py          # AI prompts
│   └── scoring.py          # Score calculations
│
└── config/                  # Configuration
    └── settings.py         # Models, personas, criteria
```

## 🔑 API Key Setup

This app requires an OpenAI API key. In HuggingFace Spaces:

1. Go to your Space Settings
2. Navigate to "Repository secrets"
3. Add a new secret:
   - **Name**: `OPENAI_API_KEY`
   - **Value**: Your OpenAI API key (starts with `sk-`)

## 💡 Example Use Cases

- Turn academic papers into poetic summaries
- Create artistic interpretations of news articles
- Generate creative takes on technical documentation
- Transform historical documents into verse
- Make poetry from scientific findings

## 🎨 Poet Personas

### Aurora (The Romantic) 🌹
- **Style**: Emotional depth, nature metaphors, flowing rhythm
- **Approach**: Seeks beauty and emotional truth in facts
- **Best for**: Documents with human stories, nature content, emotional themes

### Echo (The Modernist) ⚡
- **Style**: Sharp imagery, fragmented structure, contemporary language
- **Approach**: Finds stark truth and irony in details
- **Best for**: Technical documents, data-heavy content, modern topics

## 🛠️ Technology Stack

- **Frontend**: Gradio
- **AI Model**: GPT-4 (via OpenAI API)
- **Text Extraction**: PyPDF2, python-docx, pytesseract
- **Audio Generation**: gTTS (Google Text-to-Speech)

## 📝 License

MIT License - Feel free to use and modify!

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add new poet personas
- Improve judging criteria
- Enhance UI/UX
- Add new document formats
- Improve audio generation

## 🐛 Known Limitations

- OCR quality depends on image clarity
- API rate limits apply based on your OpenAI plan
- Audio generation is basic (gTTS) - can be enhanced
- Processing time increases with document length

## 📧 Support

For issues or questions, please open an issue on the repository.

---

*Made with ❤️ using AI and poetry*