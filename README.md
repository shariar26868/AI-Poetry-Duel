poetry-duel/
├── app.py                    # Main Streamlit app
├── requirements.txt          # Dependencies
├── README.md                 # Full documentation
├── core/                     # Core logic
│   ├── poet.py              # AI poets with personas
│   ├── judge.py             # Evaluation system
│   ├── document_processor.py # File parsing
│   └── audio_generator.py   # TTS
├── utils/                    # Utilities
│   ├── prompts.py           # All AI prompts
│   └── scoring.py           # Score calculations
├── config/                   # Settings
│   └── settings.py          # Configuration
└── tests/                    # Test suite
    └── test_basic.py        # Unit tests
