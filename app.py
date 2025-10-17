import os
import gradio as gr
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from core.poet import AIPoet
from core.judge import PoetryJudge
from core.document_processor import DocumentProcessor
from core.audio_generator import AudioGenerator
from config.settings import POET_PERSONAS, JUDGING_CRITERIA, DEFAULT_VERSES, MIN_VERSES, MAX_VERSES

# Load environment variables
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Get API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Please set it in .env file")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

def process_document(file):
    """Process uploaded document and extract text"""
    if file is None:
        return "❌ Please upload a document first!", gr.update(interactive=False)
    
    try:
        document_text = DocumentProcessor.extract_text(file)
        
        if not document_text or len(document_text.strip()) < 100:
            return "❌ Could not extract sufficient text. Please upload a different file.", gr.update(interactive=False)
        
        text_preview = document_text[:500] + "..." if len(document_text) > 500 else document_text
        return f"✅ Document processed successfully!\n\n**Preview:**\n{text_preview}", gr.update(interactive=True)
    
    except Exception as e:
        return f"❌ Error processing document: {str(e)}", gr.update(interactive=False)

def run_poetry_duel(file, persona_a, persona_b, num_verses, progress=gr.Progress()):
    """Run the complete poetry duel automatically"""
    
    if file is None:
        return "❌ Please upload a document first!", "", "", "", None
    
    if persona_a == persona_b:
        return "❌ Please select two different poet personas!", "", "", "", None
    
    try:
        progress(0, desc="Processing document...")
        
        # Extract text
        document_text = DocumentProcessor.extract_text(file)
        
        if not document_text or len(document_text.strip()) < 100:
            return "❌ Could not extract sufficient text from document.", "", "", "", None
        
        progress(0.05, desc="Initializing poets...")
        
        # Initialize poets
        poet_a_config = POET_PERSONAS[persona_a]
        poet_b_config = POET_PERSONAS[persona_b]
        
        poet_a = AIPoet(client, persona_a, poet_a_config)
        poet_b = AIPoet(client, persona_b, poet_b_config)
        judge = PoetryJudge(client)
        
        poem_lines = []
        poet_names = []
        
        # Intro
        duel_info = f"""
# 🎭 Poetry Duel Arena

**{poet_a.name}** ({poet_a_config['icon']} {poet_a_config['full_title']}) 🆚 **{poet_b.name}** ({poet_b_config['icon']} {poet_b_config['full_title']})

Total Rounds: {num_verses}

---
"""
        
        all_rounds_display = ""
        
        # Run all rounds
        for round_num in range(1, num_verses + 1):
            progress(0.05 + (0.75 * round_num / num_verses), 
                    desc=f"Round {round_num}/{num_verses}: Poets creating verses...")
            
            # Both poets create verses
            verse_a_data = poet_a.create_verse(document_text, poem_lines, round_num)
            verse_b_data = poet_b.create_verse(document_text, poem_lines, round_num)
            
            verse_a = verse_a_data['line']
            verse_b = verse_b_data['line']
            
            progress(0.05 + (0.75 * (round_num - 0.5) / num_verses), 
                    desc=f"Round {round_num}/{num_verses}: Judge evaluating...")
            
            # Judge evaluates
            poem_context = "\n".join([f"Line {i+1}: {line}" for i, line in enumerate(poem_lines)])
            judgment = judge.judge_verses(
                document_text,
                poem_context,
                verse_a,
                verse_b,
                poet_a.name,
                poet_b.name
            )
            
            # Add winning verse to poem
            if judgment['winner'] == poet_a.name:
                poem_lines.append(verse_a)
                poet_names.append(poet_a.name)
            elif judgment['winner'] == poet_b.name:
                poem_lines.append(verse_b)
                poet_names.append(poet_b.name)
            else:
                # Tie - use higher score
                if judgment['verse_a_total'] >= judgment['verse_b_total']:
                    poem_lines.append(verse_a)
                    poet_names.append(poet_a.name)
                else:
                    poem_lines.append(verse_b)
                    poet_names.append(poet_b.name)
            
            # Format round results
            round_display = f"""
## 🎯 Round {round_num}/{num_verses}

### Verses:

**{poet_a.name} {poet_a_config['icon']}:**
> {verse_a}

*Source: {verse_a_data['source']}*

**{poet_b.name} {poet_b_config['icon']}:**
> {verse_b}

*Source: {verse_b_data['source']}*

---

### Judge's Evaluation:

**Scores:**
- {poet_a.name}: **{judgment['verse_a_total']}/10**
- {poet_b.name}: **{judgment['verse_b_total']}/10**

**Winner: {judgment['winner']}** 🏆

<details>
<summary><b>Detailed Score Breakdown</b></summary>

**{poet_a.name}'s Scores:**
"""
            
            for criterion, score in judgment['verse_a_scores'].items():
                weight = JUDGING_CRITERIA[criterion]['weight']
                round_display += f"- {criterion.replace('_', ' ').title()}: {score}/10 (weight: {weight})\n"
            
            round_display += f"\n**{poet_b.name}'s Scores:**\n"
            
            for criterion, score in judgment['verse_b_scores'].items():
                weight = JUDGING_CRITERIA[criterion]['weight']
                round_display += f"- {criterion.replace('_', ' ').title()}: {score}/10 (weight: {weight})\n"
            
            round_display += f"""
**Judge's Reasoning:**

*{poet_a.name}:* {judgment['verse_a_reasoning']}

*{poet_b.name}:* {judgment['verse_b_reasoning']}

**Final Verdict:** {judgment['final_verdict']}

</details>

---

"""
            
            all_rounds_display += round_display
        
        progress(0.85, desc="Generating final poem...")
        
        # Final poem
        poem_display = "# 📜 Final Collaborative Poem\n\n"
        for i, (line, poet) in enumerate(zip(poem_lines, poet_names), 1):
            poet_config = next((p for p in POET_PERSONAS.values() if p['name'] == poet), None)
            icon = poet_config['icon'] if poet_config else "✍️"
            poem_display += f"**{i}.** {line} *— {icon} {poet}*\n\n"
        
        progress(0.90, desc="Calculating statistics...")
        
        # Final statistics
        stats = judge.get_final_statistics()
        
        stats_display = f"""
# 📊 Final Statistics

## 🏆 Round Victories
- **{poet_a.name} {poet_a_config['icon']}:** {stats['poet_a_wins']} wins
- **{poet_b.name} {poet_b_config['icon']}:** {stats['poet_b_wins']} wins

## 📈 Average Scores
- **{poet_a.name}:** {stats['poet_a_avg_score']}/10
- **{poet_b.name}:** {stats['poet_b_avg_score']}/10

"""
        
        if stats['poet_a_wins'] > stats['poet_b_wins']:
            stats_display += f"### 👑 Overall Champion: {poet_a.name} {poet_a_config['icon']}!\n"
        elif stats['poet_b_wins'] > stats['poet_a_wins']:
            stats_display += f"### 👑 Overall Champion: {poet_b.name} {poet_b_config['icon']}!\n"
        else:
            stats_display += "### 🤝 It's a Tie! Both poets performed equally well.\n"
        
        progress(0.95, desc="Generating audio...")
        
        # Generate audio
        audio_path = None
        try:
            audio_buffer = AudioGenerator.generate_poem_audio(poem_lines, poet_names)
            audio_path = "poem_audio.mp3"
            with open(audio_path, "wb") as f:
                f.write(audio_buffer.getvalue())
        except Exception as e:
            stats_display += f"\n\n⚠️ Audio generation failed: {str(e)}"
        
        progress(1.0, desc="Complete!")
        
        status = f"✅ Poetry duel completed! {num_verses} rounds finished successfully."
        
        return status, duel_info, all_rounds_display, poem_display, stats_display, audio_path
        
    except Exception as e:
        return f"❌ Error: {str(e)}", "", "", "", "", None

# Create Gradio Interface
with gr.Blocks(title="🎭 Poetry Duel Arena", theme=gr.themes.Soft()) as app:
    
    gr.Markdown("""
    # 🎭 Poetry Duel Arena
    ### AI Poets Transform Documents into Collaborative Poetry
    
    Two AI poets with distinct personas compete to create the best verses based on your document.
    An AI judge evaluates each round, and the winning verses form a collaborative poem.
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📄 Step 1: Upload Document")
            file_input = gr.File(
                label="Upload PDF, DOCX, TXT, or Image",
                file_types=[".pdf", ".docx", ".txt", ".png", ".jpg", ".jpeg"]
            )
            
            gr.Markdown("### 🎨 Step 2: Select Poets")
            
            persona_a = gr.Dropdown(
                choices=list(POET_PERSONAS.keys()),
                value=list(POET_PERSONAS.keys())[0] if POET_PERSONAS else "romantic",
                label="First Poet",
                info="Select the first AI poet persona"
            )
            
            persona_b = gr.Dropdown(
                choices=list(POET_PERSONAS.keys()),
                value=list(POET_PERSONAS.keys())[1] if len(POET_PERSONAS) > 1 else list(POET_PERSONAS.keys())[0],
                label="Second Poet",
                info="Select the second AI poet persona"
            )
            
            num_verses = gr.Slider(
                minimum=MIN_VERSES,
                maximum=MAX_VERSES,
                value=DEFAULT_VERSES,
                step=1,
                label="Number of Verses",
                info="How many rounds of competition?"
            )
            
            gr.Markdown("### 🚀 Step 3: Start Duel")
            start_btn = gr.Button("🎬 Start Poetry Duel", variant="primary", size="lg")
            
            status_text = gr.Textbox(label="Status", interactive=False, lines=2)
        
        with gr.Column(scale=2):
            gr.Markdown("### 🎭 Duel Information")
            duel_info = gr.Markdown("")
            
            gr.Markdown("### 📜 Final Collaborative Poem")
            poem_output = gr.Markdown("")
            
            gr.Markdown("### 📊 Final Statistics")
            stats_output = gr.Markdown("")
            
            audio_output = gr.Audio(label="🔊 Listen to the Poem", type="filepath")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 🎯 Round-by-Round Details")
            rounds_output = gr.Markdown("")
    
    gr.Markdown("""
    ---
    ### 📖 About the Poets
    
    Choose from multiple AI poet personas, each with unique styles:
    - **Aurora (Romantic) 🌹:** Emotion, nature metaphors, flowing rhythm
    - **Echo (Modernist) ⚡:** Sharp imagery, fragmented thoughts, contemporary language
    - **Sophocles (Classical) 🏛️:** Formal structure, elevated language, epic themes
    - **Basho (Haiku) 🍃:** Minimalist, nature-focused, present moment
    - **Dali (Surrealist) 🎨:** Dream logic, bizarre imagery, subconscious
    - **Kerouac (Beat) 🎷:** Stream of consciousness, jazz rhythms, raw energy
    
    ### 🎯 Judging Criteria
    - **Factual Grounding** (25%): Connection to document content
    - **Poetic Quality** (20%): Literary merit and craft
    - **Coherence** (20%): Flow with previous lines
    - **Originality** (20%): Fresh perspective
    - **Emotional Impact** (15%): Ability to evoke feeling
    """)
    
    # Connect button
    start_btn.click(
        fn=run_poetry_duel,
        inputs=[file_input, persona_a, persona_b, num_verses],
        outputs=[status_text, duel_info, rounds_output, poem_output, stats_output, audio_output]
    )

if __name__ == "__main__":
    app.launch()