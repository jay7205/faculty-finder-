import streamlit as st
import sys
import os
import pandas as pd
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import DatabaseManager
from src.config import DATABASE_PATH
from src.recommender import FacultyRecommender

st.set_page_config(
    page_title="Faculty Engine",
    layout="wide",
    initial_sidebar_state="auto"
)

@st.cache_resource
def load_system():
    db = DatabaseManager(DATABASE_PATH)
    try:
        recommender = FacultyRecommender()
    except Exception:
        recommender = None
    return db, recommender

db, recommender = load_system()

if 'active_profile' not in st.session_state:
    st.session_state.active_profile = None

def view_profile(faculty):
    st.session_state.active_profile = faculty

def exit_profile():
    st.session_state.active_profile = None

st.markdown("""
<style>
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }
    
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 0rem !important;
        max-width: 98% !important;
    }

    [data-testid="stVerticalBlock"] {
        gap: 0.4rem !important;
    }

    .faculty-card-box {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 4px;
        padding: 0.75rem;
    }

    .prof-name {
        color: #58a6ff;
        font-weight: 600;
        font-size: 0.95rem;
        margin: 0.5rem 0 0.25rem 0;
    }

    .main-title {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }

    .spec-text {
        font-size: 0.75rem;
        color: #8b949e;
        line-height: 1.3;
        margin-bottom: 10px;
    }

    .match-pill {
        background-color: rgba(56, 139, 253, 0.1);
        color: #58a6ff;
        border: 1px solid rgba(56, 139, 253, 0.4);
        padding: 1px 6px;
        border-radius: 4px;
        font-size: 0.65rem;
        font-weight: 700;
        float: right;
    }

    .stButton > button {
        width: 100% !important;
        background-color: #21262d !important;
        color: #c9d1d9 !important;
        border: 1px solid #30363d !important;
        font-size: 0.7rem !important;
        padding: 0.2rem 0.4rem !important;
        border-radius: 4px !important;
        height: 28px !important;
    }

    .stButton > button:hover {
        border-color: #8b949e !important;
        background-color: #30363d !important;
        color: #ffffff !important;
    }

    .stSidebar {
        background-color: #0d1117 !important;
        border-left: 1px solid #30363d !important;
    }

    #MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Faculty Finder Intelligence</div>', unsafe_allow_html=True)

if st.session_state.active_profile:
    st.info(f"Viewing Details for: **{st.session_state.active_profile['name']}**")

search_col, _ = st.columns([1, 1])
with search_col:
    q = st.text_input("", placeholder="Search competencies, research topics, or names...", label_visibility="collapsed")

if q:
    if recommender:
        with st.spinner("AI Analysis..."):
            results = recommender.recommend(q, top_n=21)
    else:
        results = []
    st.caption(f"Semantic Ranking Results ({len(results)})")
else:
    results = db.get_all_faculty()[:12]
    st.caption("Active Directory Overview")

for i in range(0, len(results), 3):
    rows = st.columns(3, gap="medium")
    for j in range(3):
        if i + j < len(results):
            f = results[i + j]
            with rows[j]:
                with st.container(border=True):
                    m_row = st.columns([1, 1])
                    with m_row[0]:
                        st.caption(f"ID #{f['id']}")
                    with m_row[1]:
                        if 'match_score' in f:
                            st.markdown(f'<span class="match-pill">{f["match_score"]}% MATCH</span>', unsafe_allow_html=True)
                    
                    avatar = f['image_url'] if f['image_url'] != "Not Provided" else "https://via.placeholder.com/100"
                    st.image(avatar, width=70)
                    
                    st.markdown(f'<div class="prof-name">{f["name"]}</div>', unsafe_allow_html=True)
                    clipped_spec = f['specialization'][:80] + "..." if len(f['specialization']) > 80 else f['specialization']
                    st.markdown(f'<div class="spec-text">{clipped_spec}</div>', unsafe_allow_html=True)
                    
                    if f.get('matching_keywords'):
                        kws = " ".join([f"#{k.lower()}" for k in f['matching_keywords']])
                        st.markdown(f'<p style="color:#6e7681; font-size:0.6rem; margin-bottom:8px;">{kws}</p>', unsafe_allow_html=True)
                    else:
                        st.write("") 

                    btn_row = st.columns(2)
                    with btn_row[0]:
                        st.button("Details", key=f"det_{f['id']}_{i}", on_click=view_profile, args=(f,))
                    with btn_row[1]:
                        slug = f['raw_source_file'].replace('.html', '')
                        st.link_button("Profile", f"https://www.daiict.ac.in/faculty/{slug}")

if st.session_state.active_profile:
    f = st.session_state.active_profile
    with st.sidebar:
        st.write(f"### {f['name']}")
        if f['image_url'] != "Not Provided":
            st.image(f['image_url'], use_container_width=True)
        
        st.divider()
        st.markdown("**Research Domain**")
        st.caption(f['specialization'])
        
        st.markdown("**Academic Biography**")
        with st.container(height=350, border=False):
            st.markdown(f['biography'])
            
        st.markdown("**Educational Background**")
        st.caption(f['education'])
        
        st.markdown("**Contact Information**")
        st.code(f['email'])
        
        st.write("")
        if st.button("Close Viewer", type="primary", on_click=exit_profile):
            st.rerun()

st.divider()
st.caption("Engine v2.9 Stable | Semantic Intelligence Node | Minimalist Dark Architecture")
