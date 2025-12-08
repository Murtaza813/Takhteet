import streamlit as st
import pandas as pd
from datetime import datetime
import calendar
from fpdf import FPDF
import base64
import tempfile
import os
import re
try:
    from arabic_reshaper import reshape
    from bidi.algorithm import get_display
    ARABIC_SUPPORT = True
except:
    ARABIC_SUPPORT = False

# Page configuration
st.set_page_config(
    page_title="Quran Hifz Takhteet Generator",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Replace the st.markdown CSS section with this MOBILE-OPTIMIZED version:

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* === CRITICAL: HIDE KEYBOARD ARROW TEXT EVERYWHERE === */
    /* Hide the header element that shows "keyboard_double_arrow" */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* Hide Fork/GitHub icons area */
    [data-testid="stHeaderActionElements"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Hide the toolbar completely */
    .stApp > header {
        display: none !important;
    }
    
    /* Alternative - hide the specific decoration element */
    [data-testid="stDecoration"] {
        display: none !important;
    }
    
    /* Force hide any material icon text */
    .material-icons, .material-icons-round {
        font-size: 0 !important;
        color: transparent !important;
        text-indent: -9999px !important;
    }
    
    /* === GLOBAL RESET === */
    * {
        font-family: 'Inter', -apple-system, sans-serif !important;
        letter-spacing: -0.01em;
    }
    
    /* === MAIN CONTAINER === */
    .main, .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
    }
    
    [data-theme="light"] .main,
    [data-theme="light"] .stApp {
        background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%) !important;
    }
    
    .block-container {
        padding: 1.5rem 1rem 3rem 1rem !important;
        max-width: 1600px !important;
    }
    
    /* === SIDEBAR - COMPLETELY FIXED FOR MOBILE === */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 50%, #3b82f6 100%) !important;
        border-right: none !important;
        box-shadow: 4px 0 40px rgba(59, 130, 246, 0.3);
    }
    
    /* All sidebar content MUST be white */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] *,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] li,
    section[data-testid="stSidebar"] div {
        color: white !important;
    }
    
    /* Sidebar heading */
    section[data-testid="stSidebar"] h1 {
        font-size: 1.5rem !important;
        font-weight: 800 !important;
        text-align: center;
        padding: 1rem 0.5rem !important;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        line-height: 1.3 !important;
        margin-bottom: 1.5rem !important;
        color: white !important;
    }
    
    /* === CRITICAL: EXPANDER HEADERS - MAXIMUM VISIBILITY === */
    section[data-testid="stSidebar"] .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.2) !important;
        border: 2px solid rgba(255, 255, 255, 0.4) !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        padding: 1.2rem !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px);
        color: white !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* CRITICAL: Force all text inside expander header to be white */
    section[data-testid="stSidebar"] .streamlit-expanderHeader * {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] .streamlit-expanderHeader p {
        color: white !important;
        font-weight: 800 !important;
        font-size: 1.15rem !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3) !important;
        margin: 0 !important;
    }
    
    section[data-testid="stSidebar"] .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.3) !important;
        border-color: rgba(255, 255, 255, 0.6) !important;
    }
    
    /* === CRITICAL: EXPANDER ARROWS - ULTRA BRIGHT === */
    section[data-testid="stSidebar"] .streamlit-expanderHeader svg,
    section[data-testid="stSidebar"] svg {
        fill: white !important;
        stroke: white !important;
        opacity: 1 !important;
        color: white !important;
        width: 28px !important;
        height: 28px !important;
        min-width: 28px !important;
        filter: drop-shadow(0 0 8px rgba(255,255,255,0.8)) !important;
    }
    
    /* Force ALL SVG elements to be white */
    section[data-testid="stSidebar"] svg path,
    section[data-testid="stSidebar"] svg circle,
    section[data-testid="stSidebar"] svg rect,
    section[data-testid="stSidebar"] svg polygon,
    section[data-testid="stSidebar"] svg line,
    section[data-testid="stSidebar"] svg polyline {
        fill: white !important;
        stroke: white !important;
        opacity: 1 !important;
    }
    
    /* === EXPANDER CONTENT - HIGH CONTRAST === */
    section[data-testid="stSidebar"] .streamlit-expanderContent {
        background: rgba(0, 0, 0, 0.4) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 0 0 12px 12px !important;
        margin-top: -5px !important;
        padding: 1.2rem !important;
        color: white !important;
    }
    
    /* List items - MAXIMUM VISIBILITY */
    section[data-testid="stSidebar"] .streamlit-expanderContent ol,
    section[data-testid="stSidebar"] .streamlit-expanderContent ul {
        padding-left: 1.8rem !important;
        margin: 0.5rem 0 !important;
    }
    
    section[data-testid="stSidebar"] .streamlit-expanderContent li {
        color: white !important;
        margin: 0.7rem 0 !important;
        padding: 0.4rem 0 !important;
        line-height: 1.7 !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        text-shadow: 0 1px 3px rgba(0,0,0,0.5) !important;
    }
    
    /* Make sure text inside lists is visible */
    section[data-testid="stSidebar"] .streamlit-expanderContent li * {
        color: white !important;
    }
    
    /* Emoji/bullet markers */
    section[data-testid="stSidebar"] .streamlit-expanderContent li::marker {
        color: white !important;
    }
    
    /* === SIDEBAR BUTTONS === */
    section[data-testid="stSidebar"] .stButton > button {
        background: rgba(255, 255, 255, 0.15) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        font-weight: 600 !important;
        color: white !important;
        transition: all 0.3s ease !important;
        margin: 0.5rem 0 !important;
        width: 100% !important;
    }
    
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255, 255, 255, 0.25) !important;
        transform: translateX(-5px);
        box-shadow: 0 4px 20px rgba(255, 255, 255, 0.2);
    }
    
    /* Sidebar dividers */
    section[data-testid="stSidebar"] hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        margin: 1.5rem 0;
    }
    
    /* === HEADER SECTION === */
    .header-container {
        text-align: center;
        margin-bottom: 2rem;
        padding: 2rem 1.5rem;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(16, 185, 129, 0.15));
        border-radius: 20px;
        border: 1px solid rgba(59, 130, 246, 0.3);
        backdrop-filter: blur(10px);
    }
    
    [data-theme="light"] .header-container {
        background: white;
        border-color: rgba(59, 130, 246, 0.2);
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
    }
    
    .header-container h1 {
        font-size: 2.2rem !important;
        font-weight: 900 !important;
        background: linear-gradient(135deg, #3b82f6 0%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 !important;
        line-height: 1.2 !important;
    }
    
    /* === MODERN CARDS === */
    .stCard, .modern-card {
        background: rgba(30, 41, 59, 0.7) !important;
        border: 1px solid rgba(71, 85, 105, 0.5) !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        margin-bottom: 1.5rem !important;
        backdrop-filter: blur(20px) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-theme="light"] .stCard,
    [data-theme="light"] .modern-card {
        background: white !important;
        border-color: #e2e8f0 !important;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08) !important;
    }
    
    /* === HEADINGS === */
    h1, h2, h3, h4, h5, h6 {
        color: #f1f5f9 !important;
        font-weight: 700 !important;
    }
    
    [data-theme="light"] h1,
    [data-theme="light"] h2,
    [data-theme="light"] h3,
    [data-theme="light"] h4 {
        color: #1e293b !important;
    }
    
    h2 {
        font-size: 1.5rem !important;
        margin-bottom: 1rem !important;
        color: #f1f5f9 !important;
    }
    
    h4 {
        font-size: 1.15rem !important;
        color: #60a5fa !important;
        margin-bottom: 1rem !important;
        font-weight: 700 !important;
    }
    
    [data-theme="light"] h4 {
        color: #1e40af !important;
    }
    
    /* === PRIMARY BUTTONS === */
    .stButton > button[kind="primary"],
    .stButton > button:not([kind="secondary"]) {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.85rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.4) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        width: 100% !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(59, 130, 246, 0.6) !important;
    }
    
    /* === SECONDARY BUTTONS === */
    .stButton > button[kind="secondary"] {
        background: rgba(71, 85, 105, 0.4) !important;
        color: #e2e8f0 !important;
        border: 2px solid rgba(71, 85, 105, 0.6) !important;
        border-radius: 12px !important;
        padding: 0.85rem 1.5rem !important;
        font-weight: 600 !important;
        backdrop-filter: blur(10px);
        width: 100% !important;
    }
    
    [data-theme="light"] .stButton > button[kind="secondary"] {
        background: white !important;
        color: #64748b !important;
        border-color: #cbd5e1 !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        border-color: #3b82f6 !important;
        background: rgba(59, 130, 246, 0.25) !important;
        color: #f1f5f9 !important;
    }
    
    /* === INPUT FIELDS === */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: rgba(51, 65, 85, 0.7) !important;
        border: 2px solid rgba(100, 116, 139, 0.6) !important;
        border-radius: 12px !important;
        padding: 0.85rem 1rem !important;
        color: #f1f5f9 !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
        backdrop-filter: blur(10px);
        transition: all 0.2s ease;
    }
    
    [data-theme="light"] .stTextInput > div > div > input,
    [data-theme="light"] .stNumberInput > div > div > input {
        background: white !important;
        border-color: #cbd5e1 !important;
        color: #1e293b !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25) !important;
    }
    
    /* === SELECTBOX - FULL TEXT VISIBLE === */
    .stSelectbox > div > div {
        background: rgba(51, 65, 85, 0.7) !important;
        border: 2px solid rgba(100, 116, 139, 0.6) !important;
        border-radius: 12px !important;
        color: #f1f5f9 !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
        backdrop-filter: blur(10px);
        min-height: 52px !important;
        padding: 0.5rem 1rem !important;
    }
    
    [data-theme="light"] .stSelectbox > div > div {
        background: white !important;
        border-color: #cbd5e1 !important;
        color: #1e293b !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        padding: 0.75rem 1rem !important;
        min-height: 52px !important;
        display: flex !important;
        align-items: center !important;
    }
    
    .stSelectbox [data-baseweb="select"] span {
        color: #f1f5f9 !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        white-space: normal !important;
        overflow: visible !important;
    }
    
    [data-theme="light"] .stSelectbox [data-baseweb="select"] span {
        color: #1e293b !important;
    }
    
    .stSelectbox svg {
        fill: #cbd5e1 !important;
        width: 24px !important;
        height: 24px !important;
    }
    
    /* === LABELS === */
    .stTextInput label,
    .stNumberInput label,
    .stSelectbox label,
    .stSlider label {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-bottom: 0.75rem !important;
        display: block !important;
    }
    
    [data-theme="light"] .stTextInput label,
    [data-theme="light"] .stNumberInput label,
    [data-theme="light"] .stSelectbox label,
    [data-theme="light"] .stSlider label {
        color: #475569 !important;
    }
    
    /* === SLIDER === */
    .stSlider > div > div > div {
        background: rgba(71, 85, 105, 0.6) !important;
        border-radius: 10px;
        height: 8px !important;
    }
    
    [data-theme="light"] .stSlider > div > div > div {
        background: #e2e8f0 !important;
    }
    
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #3b82f6, #10b981) !important;
    }
    
    .stSlider [role="slider"] {
        background: white !important;
        border: 3px solid #3b82f6 !important;
        width: 26px !important;
        height: 26px !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.5) !important;
    }
    
    /* Slider value display */
    .stSlider [data-testid="stTickBar"] > div {
        color: #f87171 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
    
    /* === TABLE === */
    .dataframe {
        border: none !important;
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4) !important;
    }
    
    .dataframe thead tr th {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%) !important;
        color: white !important;
        font-weight: 800 !important;
        padding: 1rem !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border: none !important;
    }
    
    .dataframe tbody tr {
        background: rgba(30, 41, 59, 0.6) !important;
    }
    
    [data-theme="light"] .dataframe tbody tr {
        background: white !important;
    }
    
    .dataframe tbody tr:nth-child(even) {
        background: rgba(51, 65, 85, 0.4) !important;
    }
    
    [data-theme="light"] .dataframe tbody tr:nth-child(even) {
        background: #f8fafc !important;
    }
    
    .dataframe tbody tr td {
        padding: 0.9rem !important;
        color: #e2e8f0 !important;
        border-color: rgba(71, 85, 105, 0.3) !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }
    
    [data-theme="light"] .dataframe tbody tr td {
        color: #334155 !important;
        border-color: #e2e8f0 !important;
    }
    
    /* === DAY CARDS - ULTRA COMPACT VERSION === */
    .day-card, .day-card-compact {
        background: rgba(51, 65, 85, 0.5) !important;
        border: 2px solid rgba(71, 85, 105, 0.6) !important;
        border-radius: 16px !important;
        padding: 0.8rem !important;
        margin-bottom: 0.8rem !important;
        backdrop-filter: blur(10px);
        width: 100% !important;
    }
    
    [data-theme="light"] .day-card,
    [data-theme="light"] .day-card-compact {
        background: #f8fafc !important;
        border-color: #cbd5e1 !important;
    }
    
    .day-card strong {
        color: #10b981 !important;
        font-size: 1.2rem !important;
        font-weight: 900 !important;
        display: block;
        margin-bottom: 0.6rem !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3) !important;
        background: linear-gradient(135deg, #10b981, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    [data-theme="light"] .day-card strong {
        color: #059669 !important;
        text-shadow: none !important;
    }
    
    /* ULTRA COMPACT: Tiny sipara buttons */
    .day-card-compact .stButton > button,
    .day-card .stButton > button {
        padding: 0.35rem 0.15rem !important;
        font-size: 0.75rem !important;
        min-height: 30px !important;
        height: 30px !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
    }
    
    /* Remove all column gaps */
    .day-card-compact .stColumn,
    .day-card .stColumn {
        padding: 0.08rem !important;
        min-width: 0 !important;
    }
    
    /* Force row containers to be compact */
    .day-card-compact .row-widget,
    .day-card .row-widget {
        gap: 0.15rem !important;
        margin-bottom: 0.15rem !important;
    }
    
    /* Compact captions */
    .day-card-compact .stCaption,
    .day-card .stCaption {
        margin-top: 0.5rem !important;
        font-size: 0.8rem !important;
    }
    
    /* === MESSAGES === */
    .stSuccess {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.25), rgba(16, 185, 129, 0.15)) !important;
        color: #6ee7b7 !important;
        border-radius: 12px !important;
        border: 2px solid rgba(16, 185, 129, 0.5) !important;
        padding: 1rem !important;
        font-weight: 600 !important;
    }
    
    [data-theme="light"] .stSuccess {
        background: #d1fae5 !important;
        color: #065f46 !important;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.25), rgba(239, 68, 68, 0.15)) !important;
        color: #fca5a5 !important;
        border-radius: 12px !important;
        border: 2px solid rgba(239, 68, 68, 0.5) !important;
    }
    
    [data-theme="light"] .stError {
        background: #fee2e2 !important;
        color: #991b1b !important;
    }
    
    /* === CAPTIONS === */
    .stCaption {
        color: #94a3b8 !important;
        font-weight: 500 !important;
    }
    
    [data-theme="light"] .stCaption {
        color: #64748b !important;
    }
    
    /* === DIVIDER === */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(71, 85, 105, 0.5), transparent);
        margin: 2rem 0;
    }
    
    /* === SCROLLBAR === */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 41, 59, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        border-radius: 10px;
    }
    
    /* === MOBILE RESPONSIVE === */
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem 0.75rem !important;
        }
        
        .header-container h1 {
            font-size: 1.75rem !important;
        }
        
        h2 {
            font-size: 1.35rem !important;
        }
        
        h4 {
            font-size: 1.05rem !important;
        }
        
        .stButton > button {
            padding: 0.75rem 1.5rem !important;
            font-size: 0.95rem !important;
        }
        
        section[data-testid="stSidebar"] h1 {
            font-size: 1.3rem !important;
        }
        
        /* CRITICAL: Force day cards to display in SINGLE COLUMN on mobile */
        .stColumn {
            width: 100% !important;
            max-width: 100% !important;
            flex: 0 0 100% !important;
        }
        
        /* Make day card container ultra compact */
        .day-card, .day-card-compact {
            width: 100% !important;
            margin-bottom: 1rem !important;
            padding: 0.7rem 0.5rem !important;
        }
        
        /* ULTRA COMPACT: Tiny buttons on mobile */
        .day-card-compact .stButton > button,
        .day-card .stButton > button {
            padding: 0.3rem 0.1rem !important;
            font-size: 0.7rem !important;
            min-height: 28px !important;
            height: 28px !important;
            border-width: 1px !important;
        }
        
        /* Remove all spacing between columns */
        .day-card-compact .stColumn,
        .day-card .stColumn {
            padding: 0.05rem !important;
            min-width: 0 !important;
        }
        
        /* Compact row spacing */
        .day-card-compact [data-testid="column"],
        .day-card [data-testid="column"] {
            padding: 0.05rem !important;
        }
        
        /* Smaller day heading on mobile */
        .day-card strong,
        .day-card-compact strong {
            font-size: 1.1rem !important;
            margin-bottom: 0.5rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)
# Initialize session state
if 'schedule' not in st.session_state:
    st.session_state.schedule = None
if 'student_name' not in st.session_state:
    st.session_state.student_name = "Student"
if 'direction' not in st.session_state:
    st.session_state.direction = "Backward (30 → 1)"
if 'manual_murajjah' not in st.session_state:
    st.session_state.manual_murajjah = {
        'day1': [], 'day2': [], 'day3': [], 
        'day4': [], 'day5': [], 'day6': []
    }
if 'show_manual_murajjah' not in st.session_state:
    st.session_state.show_manual_murajjah = False

# Sipara ranges
sipara_ranges = {
    1: (1, 21), 2: (22, 41), 3: (42, 61), 4: (62, 81), 5: (82, 101),
    6: (102, 121), 7: (122, 141), 8: (142, 161), 9: (162, 181),
    10: (182, 201), 11: (202, 221), 12: (222, 241), 13: (242, 261),
    14: (262, 281), 15: (282, 301), 16: (302, 321), 17: (322, 341),
    18: (342, 361), 19: (362, 381), 20: (382, 401), 21: (402, 421),
    22: (422, 441), 23: (442, 461), 24: (462, 481), 25: (482, 501),
    26: (502, 521), 27: (522, 541), 28: (542, 561), 29: (562, 581), 30: (582, 604)
}

def toggle_sipara(day, sipara):
    """Toggle sipara selection for manual murajjah"""
    if sipara in st.session_state.manual_murajjah[day]:
        st.session_state.manual_murajjah[day].remove(sipara)
    else:
        st.session_state.manual_murajjah[day].append(sipara)
        st.session_state.manual_murajjah[day].sort()

def get_murajjah_for_day(day_number, murajjah_option, for_pdf=False):
    """Get murajjah for a specific day"""
    if murajjah_option == "No Murajjah":
        return "Teacher will assign" if not for_pdf else ""
    
    if murajjah_option == "Manual Selection":
        day_key = f"day{(day_number % 6) + 1}"
        selected = st.session_state.manual_murajjah[day_key]
        if selected:
            # For PDF, return just numbers, for display return "Para X"
            if for_pdf:
                return ", ".join([str(s) for s in selected])
            else:
                return ", ".join([f"Para {s}" for s in selected])
        return "Not assigned" if not for_pdf else ""
    
    # Auto Generate
    current_sipara = st.session_state.current_sipara
    is_backward = "Backward" in st.session_state.direction
    
    if is_backward:
        # For backward direction: All siparas from 30 down to (but NOT including) current_sipara
        # If on sipara 21, you've completed 30, 29, 28, ..., 22 (not 21 itself)
        completed = list(range(30, current_sipara, -1))
    else:
        # For forward direction: All siparas from 1 up to (but NOT including) current_sipara
        # If on sipara 21, you've completed 1, 2, 3, ..., 20 (not 21 itself)
        completed = list(range(1, current_sipara))
    
    if not completed or len(completed) == 0:
        return "Revision Day" if not for_pdf else "Revision"
    
    # Distribute completed paras evenly across 6 days
    paras_per_day = max(1, len(completed) // 6)
    remainder = len(completed) % 6
    
    # Calculate start and end indices for this day
    day_index = day_number % 6
    start_idx = day_index * paras_per_day + min(day_index, remainder)
    end_idx = start_idx + paras_per_day + (1 if day_index < remainder else 0)
    
    if start_idx >= len(completed):
        return "Revision Day" if not for_pdf else "Revision"
    
    day_paras = completed[start_idx:end_idx]
    
    # Remove duplicates and sort
    day_paras = sorted(list(set(day_paras)))
    
    if for_pdf:
        # For PDF: return just numbers
        return ", ".join([str(p) for p in day_paras])
    else:
        # For display: return "Para X"
        return ", ".join([f"Para {p}" for p in day_paras])

def generate_schedule(start_juz, days_in_month):
    """Generate schedule data for PDF - FIXED VERSION"""
    schedule = {}
    current_page = st.session_state.start_page
    current_juz = start_juz
    is_backward = "Backward" in st.session_state.direction
    
    # Get holidays
    sundays = []
    for d in range(1, days_in_month + 1):
        if datetime(st.session_state.year, st.session_state.month, d).weekday() == 6:
            sundays.append(d)
    
    last_days = []
    extra_holidays = st.session_state.get('extra_holidays', 4)
    for i in range(days_in_month, days_in_month - extra_holidays, -1):
        if i not in sundays:
            last_days.append(i)
    
    all_holidays = sorted(set(sundays + last_days))
    
    # Calculate jadeen schedule (same as calculate_schedule function)
    days_in_month = calendar.monthrange(st.session_state.year, st.session_state.month)[1]
    start_page = st.session_state.start_page
    end_page = st.session_state.end_page
    daily_amount = st.session_state.daily_amount
    is_backward = "Backward" in st.session_state.direction
    total_pages = abs(end_page - start_page) + 1
    
    # Calculate working days
    working_days = days_in_month - len(all_holidays)
    
    schedule_list = []
    if daily_amount == "Mixed (0.5 & 1 page)":
        full_page_days = int(total_pages - (total_pages / 2))
        current_page = start_page
        day_count = 0
        
        pattern = []
        for i in range(working_days):
            if day_count < full_page_days and (i % 3 == 0 or working_days - i <= full_page_days - day_count):
                pattern.append(1)
                day_count += 1
            else:
                pattern.append(0.5)
        
        for i in range(working_days):
            amount = pattern[i]
            if is_backward:
                current_page_val = start_page - sum(pattern[:i])
            else:
                current_page_val = start_page + sum(pattern[:i])
            
            if is_backward and current_page_val < end_page:
                current_page_val = end_page
            elif not is_backward and current_page_val > end_page:
                current_page_val = end_page
            
            schedule_list.append({
                'page': round(current_page_val, 1),
                'amount': amount
            })
    else:
        amount = 0.5 if "0.5" in daily_amount else 1.0
        current_page_val = start_page
        for i in range(working_days):
            schedule_list.append({
                'page': current_page_val,
                'amount': amount
            })
            if is_backward:
                current_page_val -= amount
                if current_page_val < end_page:
                    current_page_val = end_page
            else:
                current_page_val += amount
                if current_page_val > end_page:
                    current_page_val = end_page
    
    # Now create the schedule for each day
    jadeen_idx = 0
    weekday_counter = 0
    
    for day in range(1, days_in_month + 1):
        if day in all_holidays:
            schedule[day] = {'isHoliday': True}
            continue
        
        # Get jadeen for this day
        jadeen = schedule_list[jadeen_idx]
        
        # Calculate juz range
        if is_backward:
            juz_range = f"{int(jadeen['page'])-1}-{int(jadeen['page'])+8}"
        else:
            start = max(1, jadeen['page'] - 10)
            end = jadeen['page'] - 1
            juz_range = f"{int(start)}-{int(end)}" if start <= end else "None"
        
        # Get murajjah for PDF (just numbers)
        murajjah = get_murajjah_for_day(weekday_counter, st.session_state.murajjah_option, for_pdf=True)
        
        schedule[day] = {
            'current_page': str(int(jadeen['page'])),
            'juz_range': juz_range,
            'murajjah': murajjah,
            'isHoliday': False
        }
        
        jadeen_idx += 1
        weekday_counter += 1
        if weekday_counter >= 6:
            weekday_counter = 0
    
    return schedule

def calculate_schedule():
    """Calculate the complete schedule with actual calendar dates - SHOW SOLUTIONS TO REACH TARGET"""
    month = st.session_state.month
    year = st.session_state.year
    direction = st.session_state.direction
    start_page = st.session_state.start_page
    end_page = st.session_state.end_page
    daily_amount = st.session_state.daily_amount
    extra_holidays = st.session_state.extra_holidays
    murajjah_option = st.session_state.murajjah_option
    
    # Get days in month
    days_in_month = calendar.monthrange(year, month)[1]
    
    # Calculate TOTAL PAGES NEEDED
    total_pages_needed = abs(end_page - start_page) + 1
    
    # Get Sundays (MANDATORY holidays)
    sundays = []
    for day in range(1, days_in_month + 1):
        if datetime(year, month, day).weekday() == 6:
            sundays.append(day)
    
    # Calculate maximum available working days (only Sundays as holidays)
    max_working_days = days_in_month - len(sundays)
    
    # Calculate current working days with user's settings
    current_working_days = days_in_month - len(sundays) - extra_holidays
    
    # Calculate minimum days needed based on daily amount
    if "0.5" in daily_amount:
        # If 0.5 page daily: need 2 days per page
        min_days_needed = total_pages_needed * 2
        avg_pages_per_day = 0.5
    elif "Mixed" in daily_amount:
        # Mixed: average 0.75 pages per day, so need roughly 1.33 days per page
        min_days_needed = int(total_pages_needed / 0.75) + 1
        avg_pages_per_day = 0.75
    else:
        # 1 page daily
        min_days_needed = total_pages_needed
        avg_pages_per_day = 1.0
    
    # CHECK: Can we reach target with current settings?
    can_reach_target = current_working_days >= min_days_needed
    
    if not can_reach_target:
        # TARGET CANNOT BE REACHED! Show solutions
        
        st.error(f"""
        ❌ **TARGET CANNOT BE REACHED WITH CURRENT PLAN!**
        
        **Current Settings:**
        - Target pages: {total_pages_needed}
        - Working days available: {current_working_days}
        - Daily amount: {daily_amount}
        - Extra holidays: {extra_holidays}
        
        **You need at least {min_days_needed} working days, but only have {current_working_days}.**
        """)
        
        # SHOW SOLUTIONS SECTION
        st.markdown("---")
        st.markdown("### 🎯 Solutions to Reach Your Target")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Solution 1: Reduce holidays
            reduce_to = max(0, extra_holidays - (min_days_needed - current_working_days))
            new_working_days = min(max_working_days, current_working_days + (min_days_needed - current_working_days))
            pages_with_this = min(total_pages_needed, current_working_days * avg_pages_per_day)
            status1 = "✅ REACH TARGET" if max_working_days >= min_days_needed else "❌ STILL NOT ENOUGH"
            
            st.markdown(f"""
            #### **Solution 1: Reduce Holidays**
            **What to do:**
            - Keep same daily amount: **{daily_amount}**
            - Reduce extra holidays from **{extra_holidays}** to **{reduce_to}**
            
            **Result:**
            - Working days: **{new_working_days}** (was {current_working_days})
            - Can complete: **{pages_with_this}** pages
            - Status: **{status1}**
            """)
            
            if max_working_days >= min_days_needed:
                st.success(f"**Action needed:** Reduce holidays to {reduce_to}")
            else:
                st.error("Even with NO extra holidays, you still can't reach target!")
        
        with col2:
            # Solution 2: Increase daily amount
            if "0.5" in daily_amount:
                new_amount = "1 page daily"
                new_min_days = total_pages_needed  # 1 page per day
                can_reach_with_this = current_working_days >= new_min_days
                status2 = "✅ REACH TARGET" if can_reach_with_this else "❌ STILL NOT ENOUGH"
            elif "Mixed" in daily_amount:
                new_amount = "1 page daily"
                new_min_days = total_pages_needed
                can_reach_with_this = current_working_days >= new_min_days
                status2 = "✅ REACH TARGET" if can_reach_with_this else "❌ STILL NOT ENOUGH"
            else:
                new_amount = "Already at maximum"
                new_min_days = min_days_needed
                can_reach_with_this = False
                status2 = "❌ ALREADY AT MAX"
            
            st.markdown(f"""
            #### **Solution 2: Increase Daily Amount**
            **What to do:**
            - Change from **{daily_amount}** to **{new_amount}**
            - Keep holidays: **{extra_holidays}**
            
            **Result:**
            - Working days needed: **{new_min_days}** (was {min_days_needed})
            - You have: **{current_working_days}** days
            - Status: **{status2}**
            """)
            
            if can_reach_with_this:
                st.success(f"**Action needed:** Change to {new_amount}")
            else:
                st.warning("Already at maximum daily amount")
        
        with col3:
            # Solution 3: Combination (reduce holidays + increase amount)
            best_solution = ""
            best_action = ""
            
            if "0.5" in daily_amount:
                # Try 1 page daily first
                new_min_days_1page = total_pages_needed
                if max_working_days >= new_min_days_1page:
                    holidays_needed = max(0, days_in_month - len(sundays) - new_min_days_1page)
                    best_solution = f"**1 page daily** with **{holidays_needed}** holidays"
                    best_action = f"Change to 1 page daily and set holidays to {holidays_needed}"
                elif "Mixed" in daily_amount:
                    # Try Mixed
                    new_min_days_mixed = int(total_pages_needed / 0.75) + 1
                    if max_working_days >= new_min_days_mixed:
                        holidays_needed = max(0, days_in_month - len(sundays) - new_min_days_mixed)
                        best_solution = f"**Mixed pages** with **{holidays_needed}** holidays"
                        best_action = f"Keep Mixed pages and set holidays to {holidays_needed}"
            elif "Mixed" in daily_amount:
                # Try 1 page daily
                new_min_days_1page = total_pages_needed
                if max_working_days >= new_min_days_1page:
                    holidays_needed = max(0, days_in_month - len(sundays) - new_min_days_1page)
                    best_solution = f"**1 page daily** with **{holidays_needed}** holidays"
                    best_action = f"Change to 1 page daily and set holidays to {holidays_needed}"
            
            st.markdown(f"""
            #### **Solution 3: Best Combination**
            **Recommended solution:**
            {best_solution if best_solution else "No combination works!"}
            
            **To reach target you need:**
            - Minimum working days: **{total_pages_needed}** (for 1 page daily)
            - Available maximum: **{max_working_days}** days
            """)
            
            if best_solution:
                st.success(f"**Best action:** {best_action}")
            else:
                st.error("Even with maximum adjustments, target cannot be reached!")
        
        # FINAL CHECK - If IMPOSSIBLE even with all adjustments
        if max_working_days < total_pages_needed:
            st.markdown("---")
            st.error(f"""
            ⚠️ **IMPOSSIBLE TO REACH TARGET THIS MONTH!**
            
            **Reason:** You need {total_pages_needed} pages but only have {max_working_days} maximum working days.
            
            **Solutions:**
            1. **Reduce target** - Choose closer end page
            2. **Extend timeline** - Split across multiple months
            3. **Start earlier** - Begin from different page
            """)
            
            # Show what IS possible
            possible_pages = int(max_working_days * avg_pages_per_day)
            st.info(f"""
            **What IS possible with current settings:**
            - Maximum pages you can complete: **{possible_pages}**
            - Suggested new target: **Page {start_page + possible_pages if direction == 'Forward (1 → 30)' else start_page - possible_pages}**
            """)
            
            return None
        
        # If we get here, it means adjustments ARE possible
        st.markdown("---")
        st.success("""
        **📝 Choose one of the solutions above and adjust your settings accordingly, then click "Generate Takhteet" again.**
        """)
        
        return None
    
    # ================ TARGET CAN BE REACHED - GENERATE SCHEDULE ================
    
    # Get extra holidays from end of month
    last_days = []
    for i in range(days_in_month, days_in_month - extra_holidays, -1):
        if i not in sundays:
            last_days.append(i)
    
    all_holidays = sorted(set(sundays + last_days))
    working_days = days_in_month - len(all_holidays)
    
    # Calculate jadeen schedule
    is_backward = "Backward" in direction
    total_pages = abs(end_page - start_page) + 1
    
    schedule = []
    
    if daily_amount == "Mixed (0.5 & 1 page)":
        full_page_days = int(total_pages - (total_pages / 2))
        current_page = start_page
        day_count = 0
        
        pattern = []
        for i in range(working_days):
            if day_count < full_page_days and (i % 3 == 0 or working_days - i <= full_page_days - day_count):
                pattern.append(1)
                day_count += 1
            else:
                pattern.append(0.5)
        
        for i in range(working_days):
            amount = pattern[i]
            if is_backward:
                current_page_val = start_page - sum(pattern[:i])
            else:
                current_page_val = start_page + sum(pattern[:i])
            
            if is_backward and current_page_val < end_page:
                current_page_val = end_page
            elif not is_backward and current_page_val > end_page:
                current_page_val = end_page
            
            schedule.append({
                'page': round(current_page_val, 1),
                'amount': amount
            })
    else:
        amount = 0.5 if "0.5" in daily_amount else 1.0
        current_page_val = start_page
        for i in range(working_days):
            schedule.append({
                'page': current_page_val,
                'amount': amount
            })
            if is_backward:
                current_page_val -= amount
                if current_page_val < end_page:
                    current_page_val = end_page
            else:
                current_page_val += amount
                if current_page_val > end_page:
                    current_page_val = end_page
    
    # Create full monthly schedule - FOLLOWING ACTUAL CALENDAR DATES
    full_schedule = []
    jadeen_idx = 0
    weekday_counter = 0
    
    # Get actual calendar for the selected month
    cal = calendar.Calendar()
    month_days = cal.itermonthdays2(year, month)  # Returns (day_of_month, weekday)
    
    pages_completed = 0
    
    for day_num, weekday in month_days:
        if day_num == 0:  # Skip days from other months
            continue
            
        date = datetime(year, month, day_num)
        day_name = calendar.day_name[weekday][:3]
        
        if day_num in all_holidays:
            full_schedule.append({
                'Date': day_num,
                'Day': day_name,
                'Jadeen': 'OFF',
                'Juzz Hali': '—',
                'Murajjah': '—',
                'isHoliday': True
            })
        else:
            if jadeen_idx < len(schedule):
                jadeen = schedule[jadeen_idx]
                pages_completed += jadeen['amount']
                
                # Calculate juzz hali
                if is_backward:
                    juzz_hali = f"{int(jadeen['page'])-1}-{int(jadeen['page'])+8}"
                else:
                    start = max(1, jadeen['page'] - 10)
                    end = jadeen['page'] - 1
                    juzz_hali = f"{int(start)}-{int(end)}" if start <= end else "None"
                
                # Calculate murajjah (with "Para" prefix for display)
                murajjah = get_murajjah_for_day(weekday_counter, murajjah_option, for_pdf=False)
                
                full_schedule.append({
                    'Date': day_num,
                    'Day': day_name,
                    'Jadeen': f"{int(jadeen['page'])} ({'full' if jadeen['amount'] == 1 else 'half'})",
                    'Juzz Hali': juzz_hali,
                    'Murajjah': murajjah,
                    'isHoliday': False
                })
                
                jadeen_idx += 1
                weekday_counter += 1
                if weekday_counter >= 6:
                    weekday_counter = 0
    
    st.session_state.schedule = full_schedule
    
    # SHOW SUCCESS SUMMARY
    st.success(f"""
    ✅ **Target Successfully Reached!**
    
    📊 **Schedule Summary:**
    - **Total Pages to Complete:** {total_pages_needed}
    - **Working Days:** {working_days}
    - **Holidays:** {len(all_holidays)} (Sundays: {len(sundays)}, Extra: {extra_holidays})
    - **Daily Amount:** {daily_amount}
    - **Pages Completed:** {pages_completed:.1f} / {total_pages_needed}
    - **Completion Date:** Day {working_days} of month
    """)
    
    return full_schedule

def format_arabic(text):
    """Format Arabic text for RTL display"""
    if ARABIC_SUPPORT and isinstance(text, str) and any('\u0600' <= c <= '\u06FF' for c in text):
        try:
            reshaped_text = reshape(text)
            return get_display(reshaped_text)
        except:
            return text
    return text

def create_pdf(student_name, selected_month_name, selected_year, start_juz, days_in_month):
    """Create PDF in PORTRAIT orientation with 15 days per page"""
    try:
        # Create PDF in PORTRAIT mode
        pdf = FPDF(orientation='P')
        pdf.set_auto_page_break(auto=False)  # Manual page breaks
        
        # Add custom font for Arabic if available
        use_arabic = ARABIC_SUPPORT
        
        # Get schedule data
        if st.session_state.schedule:
            schedule_data = st.session_state.schedule
        else:
            schedule_data = generate_schedule(start_juz, days_in_month)
        
        # Split into two pages: days 1-15 and days 16-31
        first_half = [d for d in schedule_data if d['Date'] <= 15]
        second_half = [d for d in schedule_data if d['Date'] > 15]
        
        # Page 1: Days 1-15
        pdf.add_page()
        draw_pdf_page(pdf, student_name, selected_month_name, selected_year, first_half, use_arabic, page_num=1)
        
        # Page 2: Days 16-31
        if second_half:
            pdf.add_page()
            draw_pdf_page(pdf, student_name, selected_month_name, selected_year, second_half, use_arabic, page_num=2)
        
        # Return PDF as bytes
        pdf_output = pdf.output()
        
        if isinstance(pdf_output, bytearray):
            return bytes(pdf_output)
        elif isinstance(pdf_output, str):
            return pdf_output.encode('latin-1')
        else:
            return pdf_output
            
    except Exception as e:
        st.error(f"Error creating PDF: {str(e)}")
        import traceback
        st.error(traceback.format_exc())
        return None

def draw_pdf_page(pdf, student_name, month_name, year, days_data, use_arabic, page_num):
    """Draw a single page of the PDF with 15 days - FULL PAGE WIDTH"""
    
    # Title - Handle long student names by auto-adjusting font size
    title = f"{student_name} - {month_name} {year}"
    pdf.set_font('Helvetica', 'B', 16)
    
    # Check if title is too long and reduce font size if needed
    title_width = pdf.get_string_width(title)
    max_title_width = 190  # Maximum width for title
    
    if title_width > max_title_width:
        # Reduce font size proportionally
        new_font_size = 16 * (max_title_width / title_width)
        new_font_size = max(12, new_font_size)  # Don't go below 12pt
        pdf.set_font('Helvetica', 'B', new_font_size)
    
    pdf.cell(0, 10, title, 0, 1, 'C')
    pdf.ln(3)
    
    # Add "Monthly Plan" subtitle
    if use_arabic:
        try:
            pdf.add_font('Arabic', '', 'arial.ttf', uni=True)
            pdf.add_font('Arabic', 'B', 'arialbd.ttf', uni=True)
            pdf.set_font('Arabic', 'B', 14)
        except:
            use_arabic = False
    
    if use_arabic:
        arabic_title = format_arabic("تخطيط شهري")
        pdf.cell(0, 10, arabic_title, 0, 1, 'C')
    else:
        pdf.set_font('Helvetica', 'B', 14)
        pdf.cell(0, 10, "Monthly Plan", 0, 1, 'C')
    
    # Add page indicator
    pdf.set_font('Helvetica', 'I', 10)
    if len(days_data) > 0:
        start_day = days_data[0]['Date']
        end_day = days_data[-1]['Date']
        pdf.cell(0, 8, f"Days {start_day}-{end_day}", 0, 1, 'C')
    pdf.ln(5)
    
    # FULL PAGE COLUMN WIDTHS - Adjusted to use maximum space
    total_width = 185  # Slightly reduced to prevent overflow
    start_x = (210 - total_width) / 2  # Center the table on page
    
    # OPTIMIZED COLUMN WIDTHS FOR FULL PAGE
    col_widths = [
        total_width * 0.25,   # Notes - 25%
        total_width * 0.16,   # Target Achieved? - 16%
        total_width * 0.16,   # Murajaah - 16%
        total_width * 0.12,   # Juzz Hali - 12%
        total_width * 0.10,   # New Page - 10% (reduced)
        total_width * 0.11,   # Amount - 11%
        total_width * 0.10    # Date - 10%
    ]
    
    # Headers - RTL order
    if use_arabic:
        headers = [
            format_arabic("ملاحظات"),          # Notes
            format_arabic("هدف حاصل كيڈو؟"),   # Target Achieved?
            format_arabic("المراجعة"),         # Murajaah
            format_arabic("جز حالی"),          # Juzz Hali
            format_arabic("الجديد"),           # New Page (simplified)
            format_arabic("كمية"),             # Amount (simplified)
            format_arabic("التاريخ")           # Date
        ]
    else:
        headers = [
            "Notes",            # 25%
            "Target Achieved?", # 16%
            "Murajaah",         # 16%
            "Juzz Hali",        # 12%
            "New Page",         # 10%
            "Amount",           # 11%
            "Date"              # 10%
        ]
    
    # Set starting X position
    pdf.set_x(start_x)
    
    # Draw table headers - SLIGHTLY DEEPER BLUE BACKGROUND
    pdf.set_draw_color(50, 50, 50)    # DARKER BLACK BORDERS (was 100,100,100)
    pdf.set_line_width(0.35)          # Slightly thicker borders
    pdf.set_fill_color(153, 204, 255)  # SLIGHTLY MORE BLUE (was 173,216,230) - More vibrant blue
    pdf.set_text_color(0, 0, 0)       # BLACK TEXT
    
    # Write headers in REVERSE order for RTL
    for i in range(6, -1, -1):
        if use_arabic and i >= 2:
            try:
                pdf.set_font('Arabic', 'B', 9)
            except:
                pdf.set_font('Helvetica', 'B', 9)
        else:
            pdf.set_font('Helvetica', 'B', 9)
        
        pdf.cell(col_widths[i], 8, headers[i], 1, 0, 'C', True)
    
    pdf.ln()
    
    # ===== DYNAMIC ROW HEIGHT CALCULATION =====
    # Calculate available height after headers and before footer
    available_height = 270 - pdf.get_y() - 25  # Subtract footer space (25mm)
    
    if len(days_data) > 0:
        # Calculate optimal row height to fill available space
        row_height = available_height / len(days_data)
        # Keep row height between 7-10mm for readability
        row_height = min(10, max(7, row_height))
    else:
        row_height = 8.5  # Default if no data
    # ===== END ROW HEIGHT CALCULATION =====
    
    # Draw table rows for this page's days
    for idx, day_schedule in enumerate(days_data):
        day = day_schedule['Date']
        is_holiday = day_schedule['isHoliday']
        
        # Set starting X for each row
        pdf.set_x(start_x)
        
        # Set default background (white for normal days)
        if is_holiday:
            # Light background for holidays - Slightly darker gray for better contrast
            pdf.set_fill_color(235, 235, 235)
            fill = True
        else:
            # White background for regular days
            pdf.set_fill_color(255, 255, 255)
            fill = False
        
        # Set font for content - BLACKER TEXT
        if use_arabic:
            try:
                pdf.set_font('Arabic', '', 8)
                pdf.set_text_color(0, 0, 0)  # Pure black text
            except:
                pdf.set_font('Helvetica', '', 8)
                pdf.set_text_color(0, 0, 0)  # Pure black text
        else:
            pdf.set_font('Helvetica', '', 8)
            pdf.set_text_color(0, 0, 0)  # Pure black text
        
        # Prepare cell data with TRUNCATED text if needed
        if is_holiday:
            cell_data = [
                "",  # Notes
                "",  # Target
                format_arabic("عطلة") if use_arabic else "Holiday",  # Murajaah
                "",  # Juzz Hali
                "",  # New Page
                "",  # Amount
                str(day)  # Date
            ]
        else:
            # Extract data from schedule
            jadeen_text = day_schedule['Jadeen']
            juzz_hali = day_schedule['Juzz Hali']
            murajjah = day_schedule['Murajjah']
            
            # Parse Jadeen text
            page_number = ""
            amount = ""
            if "(" in jadeen_text:
                page_part = jadeen_text.split("(")[0].strip()
                amount_part = jadeen_text.split("(")[1].replace(")", "").strip()
                page_number = page_part
                amount = amount_part.capitalize()
            
            # Clean up Murajjah - remove "Para" prefix and truncate if too long
            if murajjah and murajjah != "—":
                murajjah_clean = murajjah.replace("Para", "").replace("para", "").strip()
                # Truncate if too long (more than 15 chars)
                if len(murajjah_clean) > 15:
                    murajjah_clean = murajjah_clean[:12] + "..."
            else:
                murajjah_clean = ""
            
            # Clean up Juzz Hali - truncate if too long
            clean_juzz_hali = juzz_hali if juzz_hali != "None" else ""
            if len(clean_juzz_hali) > 10:
                clean_juzz_hali = clean_juzz_hali[:8] + "..."
            
            # Truncate page number if too long
            if len(page_number) > 8:
                page_number = page_number[:6] + "..."
            
            cell_data = [
                "",  # Notes
                "",  # Target
                murajjah_clean,  # Murajaah
                clean_juzz_hali,  # Juzz Hali
                page_number,  # New Page
                amount,  # Amount
                str(day)  # Date
            ]
        
        # Write row data in reverse order (RTL)
        for i in range(6, -1, -1):
            cell_content = cell_data[i]
            
            # Set alignment
            align = 'C'
            if i == 6:  # Date
                align = 'R'
            elif i == 0:  # Notes
                align = 'L'
            
            # Format Arabic if needed
            if use_arabic and isinstance(cell_content, str) and any('\u0600' <= c <= '\u06FF' for c in cell_content):
                cell_content = format_arabic(cell_content)
            
            if cell_content is None:
                cell_content = ""
            
            # Ensure text fits in cell - but only truncate if really necessary
            text_width = pdf.get_string_width(str(cell_content))
            if text_width > col_widths[i] - 4:  # 2mm padding on each side
                # Find how many characters fit
                chars_to_keep = int(len(str(cell_content)) * ((col_widths[i] - 4) / text_width))
                chars_to_keep = max(1, chars_to_keep - 3)  # Leave room for "..."
                cell_content = str(cell_content)[:chars_to_keep] + "..."
            
            pdf.cell(col_widths[i], row_height, str(cell_content), 1, 0, align, fill)
        
        pdf.ln()
    
    # Footer note
    pdf.set_y(275)
    
    # Footer with black text
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(0, 0, 0)  # Black text
    pdf.cell(0, 8, "Note: Right columns for student, left for teacher", 0, 0, 'C')
    
    # Add page number at bottom right
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_xy(170, 282)
    pdf.cell(20, 5, f"Page {page_num}", 0, 0, 'R')
        
def render_manual_murajjah_section():
    """Render the manual murajjah selection interface - MOBILE OPTIMIZED"""
    if st.session_state.murajjah_option == "Manual Selection":
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            if st.button(
                f"{'Hide' if st.session_state.show_manual_murajjah else 'Setup'} Manual Murajjah",
                type="primary",
                use_container_width=True
            ):
                st.session_state.show_manual_murajjah = not st.session_state.show_manual_murajjah
                st.rerun()
        
        if st.session_state.show_manual_murajjah:
            st.markdown('<div class="stCard">', unsafe_allow_html=True)
            st.markdown("#### 📋 Select Siparas for Each Day")
            
            # Display all 6 days in a single column (stacked vertically)
            days = ['day1', 'day2', 'day3', 'day4', 'day5', 'day6']
            day_names = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6']
            
            # Render each day card one after another (no columns)
            for day, day_name in zip(days, day_names):
                render_day_card(day, day_name)
            
            st.markdown('</div>', unsafe_allow_html=True)

def render_day_card(day_key, day_name):
    """Render a card for selecting siparas - COMPACT CALENDAR GRID (6x5)"""
    st.markdown(f'<div class="day-card-compact">', unsafe_allow_html=True)
    
    # Day heading
    st.markdown(f'<div style="color: #10b981; font-size: 1.3rem; font-weight: 900; margin-bottom: 0.8rem; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">📅 {day_name}</div>', unsafe_allow_html=True)
    
    # COMPACT GRID: 5 rows x 6 columns = 30 siparas (like a calendar)
    for row in range(5):
        cols = st.columns(6)
        for col_idx in range(6):
            sipara = row * 6 + col_idx + 1
            if sipara <= 30:
                with cols[col_idx]:
                    is_selected = sipara in st.session_state.manual_murajjah[day_key]
                    if st.button(
                        str(sipara),
                        key=f"{day_key}_{sipara}",
                        type="primary" if is_selected else "secondary",
                        use_container_width=True
                    ):
                        toggle_sipara(day_key, sipara)
                        st.rerun()
    
    # Show selected siparas
    selected = st.session_state.manual_murajjah[day_key]
    if selected:
        st.caption(f"✅ Selected: {', '.join(map(str, selected))}")
    else:
        st.caption("⚪ No siparas selected")
    
    st.markdown('</div>', unsafe_allow_html=True)
# Main App
def main():
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h1>📖 Quran Hifz Takhteet</h1>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        with st.expander("📋 How to Use", expanded=True):
            st.markdown("""
            1. **Fill in student details**
            2. **Select month/year**
            3. **Choose Hifz direction**
            4. **Set Jadeen pages**
            5. **Generate schedule**
            6. **Download PDF**
            """)
        
        st.markdown("---")
        
        with st.expander("✨ Features", expanded=True):
            st.markdown("""
            - 🎯 **Backward & Forward Hifz**
            - 📅 **Monthly schedule generator**
            - 📄 **Jadeen tracking**
            - 🔄 **Murajjah planning**
            - 📊 **PDF export (Portrait)**
            """)
        
        st.markdown("---")
        st.markdown("Made with ❤️ for Huffaz")

    # Main Content
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center;'>
            <h1>Takhteet</h1>
            <div style='color: #6b7280; font-size: 1rem; margin-bottom: 0.5rem;'>
                Made with ❤️ for Huffaz
            </div>
         </div>   
        """, unsafe_allow_html=True)
    
    # Main card
    with st.container():
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        
        # Hifz Direction
        st.markdown("#### 🎯 Hifz Direction")
        direction_cols = st.columns(2)
        with direction_cols[0]:
            if st.button("← Backward (30 → 1)", 
                        type="primary" if st.session_state.direction == "Backward (30 → 1)" else "secondary",
                        use_container_width=True):
                st.session_state.direction = "Backward (30 → 1)"
                st.rerun()
        with direction_cols[1]:
            if st.button("Forward (1 → 30) →", 
                        type="primary" if st.session_state.direction == "Forward (1 → 30)" else "secondary",
                        use_container_width=True):
                st.session_state.direction = "Forward (1 → 30)"
                st.rerun()
        
        st.markdown("---")
        
        # Form inputs in grid - REORDERED FIELDS
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.student_name = st.text_input(
                "**Student Name**",
                placeholder="Enter student name",
                value=st.session_state.get('student_name', '')
            )
            
            # YEAR comes before MONTH
            st.session_state.year = st.number_input(
                "**Year**",
                min_value=2024,
                max_value=2030,
                value=2025,
                step=1
            )
            
            # MONTH after YEAR
            st.session_state.month = st.selectbox(
                "**Month**",
                options=list(range(1, 13)),
                format_func=lambda x: datetime(2000, x, 1).strftime('%B'),
                index=11  # Default to December
            )
            
            if "Backward" in st.session_state.direction:
                st.session_state.start_page = st.number_input(
                    "**Start Jadeen Page**",
                    min_value=1,
                    max_value=604,
                    value=527,
                    step=1
                )
                st.session_state.end_page = st.number_input(
                    "**End Jadeen Page (Target)**",
                    min_value=1,
                    max_value=604,
                    value=511,
                    step=1
                )
            else:
                st.session_state.start_page = st.number_input(
                    "**Current Jadeen Page**",
                    min_value=1,
                    max_value=604,
                    value=418,
                    step=1
                )
                st.session_state.end_page = st.number_input(
                    "**Target Jadeen Page**",
                    min_value=1,
                    max_value=604,
                    value=430,
                    step=1
                )
        
        with col2:
            # DAILY JADEEN AMOUNT moved here (after end page)
            st.session_state.daily_amount = st.selectbox(
                "**Daily Jadeen Amount**",
                options=["0.5 page daily", "1 page daily", "Mixed (0.5 & 1 page)"],
                index=2
            )
            
            # Rest of the fields
            st.session_state.current_sipara = st.slider(
                "**Current Sipara (Para)**",
                min_value=1,
                max_value=30,
                value=21
            )
            
            st.session_state.extra_holidays = st.number_input(
                "**Extra Holidays (besides Sundays)**",
                min_value=0,
                max_value=10,
                value=4,
                step=1
            )
            
            st.session_state.murajjah_option = st.selectbox(
                "**Murajjah Option**",
                options=["No Murajjah", "Manual Selection", "Auto Generate"],
                index=2
            )
        
        # Manual Murajjah Section
        render_manual_murajjah_section()

        # Generate button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✨ Generate Takhteet", type="primary", use_container_width=True):
                with st.spinner("Checking if target can be reached..."):
                    result = calculate_schedule()
                    if result:  # Only show success and rerun if schedule was actually generated
                        st.success("Schedule generated successfully!")
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display schedule if exists
    if st.session_state.schedule:
        st.markdown("---")
        month_name = datetime(2000, st.session_state.month, 1).strftime('%B')
        
        st.markdown(f"""
        <div class="stCard">
            <h2>Takhteet for {st.session_state.student_name} - {month_name} {st.session_state.year}</h2>
            <p style='color: #10b981; font-weight: 600;'>({st.session_state.direction})</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create DataFrame for display
        df = pd.DataFrame(st.session_state.schedule)
        display_df = df[['Date', 'Day', 'Jadeen', 'Juzz Hali', 'Murajjah']]
        
        # Sort by Date
        display_df = display_df.sort_values('Date')
        
        # Convert to HTML for styling
        def highlight_holidays(row):
            for day_data in st.session_state.schedule:
                if day_data['Date'] == row['Date'] and day_data['isHoliday']:
                    return ['background-color: #fef2f2'] * len(row)
            return [''] * len(row)
        
        # Display as styled table
        st.dataframe(
            display_df.style.apply(highlight_holidays, axis=1),
            use_container_width=True,
            height=600
        )
        
        # PDF Download button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            try:
                # Get month name for PDF
                month_name = datetime(2000, st.session_state.month, 1).strftime('%B')
                
                # Get days in month
                days_in_month = calendar.monthrange(st.session_state.year, st.session_state.month)[1]
                
                # Generate PDF with correct parameters
                pdf_bytes = create_pdf(
                    student_name=st.session_state.student_name,
                    selected_month_name=month_name,
                    selected_year=st.session_state.year,
                    start_juz=st.session_state.current_sipara,
                    days_in_month=days_in_month
                )
                
                # Verify PDF was created successfully
                if pdf_bytes:
                    # Create download button
                    st.download_button(
                        label="📥 Download PDF (Portrait)",
                        data=pdf_bytes,
                        file_name=f"takhteet_{st.session_state.student_name}_{month_name}_{st.session_state.year}.pdf",
                        mime="application/pdf",
                        type="primary",
                        use_container_width=True
                    )
                else:
                    st.error("PDF generation failed. Please try again.")
                    
            except Exception as e:
                st.error(f"Error creating PDF: {str(e)}")
                import traceback
                st.error(traceback.format_exc())

if __name__ == "__main__":
    main()






