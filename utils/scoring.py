import streamlit as st
from config.settings import JUDGING_CRITERIA


def display_score_breakdown(scores, poet_name):
    """Display a visual breakdown of scores"""
    st.subheader(f"{poet_name}'s Score Breakdown")
    
    total = 0
    for criterion, score in scores.items():
        weight = JUDGING_CRITERIA[criterion]['weight']
        weighted_score = score * weight
        total += weighted_score
        
        st.markdown(f"**{criterion.replace('_', ' ').title()}**")
        st.progress(score / 10)
        st.caption(f"Score: {score}/10 | Weighted: {weighted_score:.2f}")
    
    st.metric("Total Weighted Score", f"{total:.2f}")