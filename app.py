import streamlit as st
from openai import OpenAI
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv  
from core.poet import AIPoet
from core.judge import PoetryJudge
from core.document_processor import DocumentProcessor
from core.audio_generator import AudioGenerator
from config.settings import POET_PERSONAS, JUDGING_CRITERIA, DEFAULT_VERSES
from utils.scoring import display_score_breakdown
load_dotenv()
if 'poem_lines' not in st.session_state:
    st.session_state.poem_lines = []
if 'judgments' not in st.session_state:
    st.session_state.judgments = []
if 'document_text' not in st.session_state:
    st.session_state.document_text = None

def main():
    st.title("🎭 AI Poetry Duel")
    st.markdown("### Where Two AI Poets Compete, and One Judge Decides")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("OpenAI API Key not found!")
        st.info("""
        **How to set up your API key:**
        1. Create a `.env` file in your project root
        2. Add this line: `OPENAI_API_KEY=your_api_key_here`
        3. Or set environment variable: `export OPENAI_API_KEY='your_key'`
        
        Get your API key from: https://platform.openai.com/api-keys
        """)
        st.stop()
    st.sidebar.success(f"API Key loaded: ...{api_key[-8:]}")
    with st.sidebar:
        st.header("⚙️ Configuration")  
        st.divider() 
        num_verses = st.slider("Number of verses", 1, 12, DEFAULT_VERSES)
        st.divider()
        st.subheader("Meet the Poets")
        for persona_key, persona in POET_PERSONAS.items():
            st.markdown(f"**{persona['icon']} {persona['full_title']}**")
            st.caption(persona['style'])
            st.markdown("")
        st.divider()
        st.subheader("Judging Criteria")
        for criterion, details in JUDGING_CRITERIA.items():
            st.markdown(f"**{criterion.replace('_', ' ').title()}** ({details['weight']*100}%)")
            st.caption(details['description'])
    tab1, tab2, tab3 = st.tabs(["Upload & Generate", "Judgment Details", "Audio (Bonus)"])
    
    with tab1:
        st.header("Upload Your Document")
        uploaded_file = st.file_uploader(
            "Choose a file (PDF, DOCX, TXT, or Image)",
            type=['pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg']
        )
        
        if uploaded_file:
            with st.spinner("Extracting text from document..."):
                try:
                    document_text = DocumentProcessor.extract_text(uploaded_file)
                    st.session_state.document_text = document_text
                    
                    st.success(f"Extracted {len(document_text)} characters")
                    
                    with st.expander("Preview document content"):
                        st.text(document_text[:500] + "...")
                except Exception as e:
                    st.error(f"Error extracting text: {str(e)}")
        
        if st.session_state.document_text and st.button("🎭 Start Poetry Duel", type="primary"):
            generate_poetry_duel(api_key, st.session_state.document_text, num_verses)
    
    with tab2:
        display_judgment_details()
    
    with tab3:
        display_audio_section()
def generate_poetry_duel(api_key, document_text, num_verses):
    """Main function to orchestrate the poetry duel"""
    try:
        client = OpenAI(api_key=api_key)
        poet_romantic = AIPoet(client, "romantic", POET_PERSONAS["romantic"])
        poet_modernist = AIPoet(client, "modernist", POET_PERSONAS["modernist"])
        judge = PoetryJudge(client)
        
        st.session_state.poem_lines = []
        st.session_state.judgments = []
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        poem_display = st.empty()
        for i in range(num_verses):
            current_poet = poet_romantic if i % 2 == 0 else poet_modernist
            other_poet = poet_modernist if i % 2 == 0 else poet_romantic
            
            status_text.text(f"{current_poet.name} is creating verse {i+1}...")
            
            try:
                verse_current = current_poet.create_verse(
                    document_text, 
                    [line['line'] for line in st.session_state.poem_lines],
                    i + 1
                )
                
                verse_other = other_poet.create_verse(
                    document_text,
                    [line['line'] for line in st.session_state.poem_lines],
                    i + 1
                )
            
                status_text.text(f"Judge is evaluating verses...")
                
                poem_context = "\n".join([f"Line {j+1}: {line['line']}" for j, line in enumerate(st.session_state.poem_lines)])
                
                judgment = judge.judge_verses(
                    document_text,
                    poem_context,
                    f"{verse_current['line']}\nSOURCE: {verse_current['source']}",
                    f"{verse_other['line']}\nSOURCE: {verse_other['source']}",
                    current_poet.name,
                    other_poet.name
                )
                
                winning_verse = verse_current if judgment['winner'] == current_poet.name else verse_other
                st.session_state.poem_lines.append(winning_verse)
                st.session_state.judgments.append(judgment)
                
                poem_html = generate_poem_html(st.session_state.poem_lines)
                poem_display.markdown(poem_html, unsafe_allow_html=True)
                
                progress_bar.progress((i + 1) / num_verses)
                
            except Exception as e:
                error_message = str(e)
                if "insufficient_quota" in error_message or "429" in error_message:
                    st.error(f"**OpenAI API Quota Exceeded**")
                    st.warning("""
                    **Solutions:**
                    1. Check your billing at: https://platform.openai.com/account/billing
                    2. Add payment method and credits
                    3. Wait for quota reset
                    4. Use a different API key
                    """)
                    break  
                else:
                    st.error(f"Error generating verse {i+1}: {error_message}")
                    st.warning("Attempting to continue with next verse...")
                    continue
        if st.session_state.poem_lines:
            status_text.text("Poetry duel complete!")
            display_final_statistics(judge)
        else:
            status_text.text("No verses were generated. Please check your API key and quota.")
            
    except Exception as e:
        st.error(f"Fatal error: {str(e)}")
        if "authentication" in str(e).lower() or "api key" in str(e).lower():
            st.error("Invalid API key. Please check your OPENAI_API_KEY in .env file")


def generate_poem_html(poem_lines):
    """Generate HTML for displaying the poem"""
    html = "<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px;'>"
    html += "<h2 style='color: white; text-align: center; margin-bottom: 20px;'>The Collaborative Poem</h2>"
    
    for i, verse in enumerate(poem_lines):
        poet_config = POET_PERSONAS["romantic"] if verse['poet'] == "Aurora" else POET_PERSONAS["modernist"]
        
        html += f"""
        <div style='margin: 15px 0; padding: 15px; background: rgba(255,255,255,0.1); border-left: 4px solid {poet_config['color']}; border-radius: 8px;'>
            <p style='color: white; font-size: 18px; font-style: italic; margin: 0;'>{verse['line']}</p>
            <p style='color: rgba(255,255,255,0.7); font-size: 12px; margin-top: 8px;'>
                — {poet_config['icon']} {verse['poet']} 
                <span style='font-style: italic;'>({verse['source'][:60]}...)</span>
            </p>
        </div>
        """
    
    html += "</div>"
    return html


def display_judgment_details():
    """Display detailed judgment information"""
    if not st.session_state.judgments:
        st.info("No judgments yet. Generate a poem first!")
        return
    
    st.header("⚖️ Detailed Judgments")
    
    for i, judgment in enumerate(st.session_state.judgments):
        with st.expander(f"Verse {i+1} Judgment"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Aurora (Romantic)")
                st.metric("Total Score", judgment['verse_a_total'])
                for criterion, score in judgment['verse_a_scores'].items():
                    st.metric(criterion.replace('_', ' ').title(), score)
                st.markdown(f"**Analysis:** {judgment['verse_a_reasoning']}")
            
            with col2:
                st.subheader("Echo (Modernist)")
                st.metric("Total Score", judgment['verse_b_total'])
                for criterion, score in judgment['verse_b_scores'].items():
                    st.metric(criterion.replace('_', ' ').title(), score)
                st.markdown(f"**Analysis:** {judgment['verse_b_reasoning']}")
            
            st.markdown(f"### Winner: {judgment['winner']}")
            st.markdown(f"**Verdict:** {judgment['final_verdict']}")


def display_final_statistics(judge):
    """Display overall statistics"""
    stats = judge.get_final_statistics()
    
    if not stats:
        return
    
    st.header("Final Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Aurora Wins", stats['poet_a_wins'])
    with col2:
        st.metric("Echo Wins", stats['poet_b_wins'])
    with col3:
        st.metric("Aurora Avg Score", stats['poet_a_avg_score'])
    with col4:
        st.metric("Echo Avg Score", stats['poet_b_avg_score'])


def display_audio_section():
    """Display audio generation section"""
    if not st.session_state.poem_lines:
        st.info("Generate a poem first to create audio!")
        return
    
    st.header("🎵 Audio Narration (Bonus Feature)")
    
    if st.button("Generate Audio"):
        with st.spinner("Generating audio..."):
            try:
                poem_lines = [verse['line'] for verse in st.session_state.poem_lines]
                poet_names = [verse['poet'] for verse in st.session_state.poem_lines]
                
                audio_buffer = AudioGenerator.generate_poem_audio(poem_lines, poet_names)
                
                st.audio(audio_buffer, format='audio/mp3')
                st.success("Audio generated successfully!")
            except Exception as e:
                st.error(f"Error generating audio: {str(e)}")


if __name__ == "__main__":
    main()

