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

# ================ SURAH DATABASE FOR BACKWARD HIFZ ================
# Based on Mushaf Tajweed Dar Al-Maarifah Damascus (604 pages)
# Surahs in BACKWARD order (from end to beginning)

SURAH_DATA_BACKWARD = [
    # Juz 30 (Pages 582-604) - Backward order
    {"surah": 114, "name": "An-Nas", "arabic": "الناس", "start_page": 604, "end_page": 604},
    {"surah": 113, "name": "Al-Falaq", "arabic": "الفلق", "start_page": 604, "end_page": 604},
    {"surah": 112, "name": "Al-Ikhlas", "arabic": "الإخلاص", "start_page": 604, "end_page": 604},
    {"surah": 111, "name": "Al-Masad", "arabic": "المسد", "start_page": 603, "end_page": 603},
    {"surah": 110, "name": "An-Nasr", "arabic": "النصر", "start_page": 603, "end_page": 603},
    {"surah": 109, "name": "Al-Kafirun", "arabic": "الكافرون", "start_page": 603, "end_page": 603},
    {"surah": 108, "name": "Al-Kawthar", "arabic": "الكوثر", "start_page": 602, "end_page": 602},
    {"surah": 107, "name": "Al-Ma'un", "arabic": "الماعون", "start_page": 602, "end_page": 602},
    {"surah": 106, "name": "Quraysh", "arabic": "قريش", "start_page": 602, "end_page": 602},
    {"surah": 105, "name": "Al-Fil", "arabic": "الفيل", "start_page": 601, "end_page": 601},
    {"surah": 104, "name": "Al-Humazah", "arabic": "الهمزة", "start_page": 601, "end_page": 601},
    {"surah": 103, "name": "Al-'Asr", "arabic": "العصر", "start_page": 601, "end_page": 601},
    {"surah": 102, "name": "At-Takathur", "arabic": "التكاثر", "start_page": 600, "end_page": 600},
    {"surah": 101, "name": "Al-Qari'ah", "arabic": "القارعة", "start_page": 600, "end_page": 600},
    {"surah": 100, "name": "Al-'Adiyat", "arabic": "العاديات", "start_page": 599, "end_page": 600},
    {"surah": 99, "name": "Az-Zalzalah", "arabic": "الزلزلة", "start_page": 599, "end_page": 599},
    {"surah": 98, "name": "Al-Bayyinah", "arabic": "البينة", "start_page": 598, "end_page": 599},
    {"surah": 97, "name": "Al-Qadr", "arabic": "القدر", "start_page": 598, "end_page": 598},
    {"surah": 96, "name": "Al-'Alaq", "arabic": "العلق", "start_page": 597, "end_page": 597},
    {"surah": 95, "name": "At-Tin", "arabic": "التين", "start_page": 597, "end_page": 597},
    {"surah": 94, "name": "Ash-Sharh", "arabic": "الشرح", "start_page": 596, "end_page": 596},
    {"surah": 93, "name": "Ad-Duha", "arabic": "الضحى", "start_page": 596, "end_page": 596},
    {"surah": 92, "name": "Al-Layl", "arabic": "الليل", "start_page": 595, "end_page": 596},
    {"surah": 91, "name": "Ash-Shams", "arabic": "الشمس", "start_page": 595, "end_page": 595},
    {"surah": 90, "name": "Al-Balad", "arabic": "البلد", "start_page": 594, "end_page": 594},
    {"surah": 89, "name": "Al-Fajr", "arabic": "الفجر", "start_page": 593, "end_page": 594},
    {"surah": 88, "name": "Al-Ghashiyah", "arabic": "الغاشية", "start_page": 592, "end_page": 592},
    {"surah": 87, "name": "Al-A'la", "arabic": "الأعلى", "start_page": 591, "end_page": 592},
    {"surah": 86, "name": "At-Tariq", "arabic": "الطارق", "start_page": 591, "end_page": 591},
    {"surah": 85, "name": "Al-Buruj", "arabic": "البروج", "start_page": 590, "end_page": 590},
    {"surah": 84, "name": "Al-Inshiqaq", "arabic": "الإنشقاق", "start_page": 589, "end_page": 589},
    {"surah": 83, "name": "Al-Mutaffifin", "arabic": "المطففين", "start_page": 587, "end_page": 589},
    {"surah": 82, "name": "Al-Infitar", "arabic": "الإنفطار", "start_page": 587, "end_page": 587},
    {"surah": 81, "name": "At-Takwir", "arabic": "التكوير", "start_page": 586, "end_page": 586},
    {"surah": 80, "name": "'Abasa", "arabic": "عبس", "start_page": 585, "end_page": 585},
    {"surah": 79, "name": "An-Nazi'at", "arabic": "النازعات", "start_page": 583, "end_page": 584},
    {"surah": 78, "name": "An-Naba'", "arabic": "النبأ", "start_page": 582, "end_page": 583},
    
    # Juz 29 (Pages 562-581)
    {"surah": 77, "name": "Al-Mursalat", "arabic": "المرسلات", "start_page": 580, "end_page": 581},
    {"surah": 76, "name": "Al-Insan", "arabic": "الإنسان", "start_page": 578, "end_page": 580},
    {"surah": 75, "name": "Al-Qiyamah", "arabic": "القيامة", "start_page": 577, "end_page": 578},
    {"surah": 74, "name": "Al-Muddaththir", "arabic": "المدثر", "start_page": 575, "end_page": 577},
    {"surah": 73, "name": "Al-Muzzammil", "arabic": "المزمل", "start_page": 574, "end_page": 575},
    {"surah": 72, "name": "Al-Jinn", "arabic": "الجن", "start_page": 572, "end_page": 573},
    {"surah": 71, "name": "Nuh", "arabic": "نوح", "start_page": 570, "end_page": 571},
    {"surah": 70, "name": "Al-Ma'arij", "arabic": "المعارج", "start_page": 568, "end_page": 570},
    {"surah": 69, "name": "Al-Haqqah", "arabic": "الحاقة", "start_page": 566, "end_page": 568},
    {"surah": 68, "name": "Al-Qalam", "arabic": "القلم", "start_page": 564, "end_page": 566},
    {"surah": 67, "name": "Al-Mulk", "arabic": "الملك", "start_page": 562, "end_page": 564},
    
    # Juz 28 (Pages 542-561)
    {"surah": 66, "name": "At-Tahrim", "arabic": "التحريم", "start_page": 560, "end_page": 561},
    {"surah": 65, "name": "At-Talaq", "arabic": "الطلاق", "start_page": 558, "end_page": 559},
    {"surah": 64, "name": "At-Taghabun", "arabic": "التغابن", "start_page": 556, "end_page": 557},
    {"surah": 63, "name": "Al-Munafiqun", "arabic": "المنافقون", "start_page": 554, "end_page": 555},
    {"surah": 62, "name": "Al-Jumu'ah", "arabic": "الجمعة", "start_page": 553, "end_page": 554},
    {"surah": 61, "name": "As-Saff", "arabic": "الصف", "start_page": 551, "end_page": 552},
    {"surah": 60, "name": "Al-Mumtahanah", "arabic": "الممتحنة", "start_page": 549, "end_page": 551},
    {"surah": 59, "name": "Al-Hashr", "arabic": "الحشر", "start_page": 545, "end_page": 548},
    {"surah": 58, "name": "Al-Mujadila", "arabic": "المجادلة", "start_page": 542, "end_page": 545},
    
    # Juz 27 (Pages 522-541)
    {"surah": 57, "name": "Al-Hadid", "arabic": "الحديد", "start_page": 537, "end_page": 541},
    {"surah": 56, "name": "Al-Waqi'ah", "arabic": "الواقعة", "start_page": 534, "end_page": 537},
    {"surah": 55, "name": "Ar-Rahman", "arabic": "الرحمن", "start_page": 531, "end_page": 534},
    {"surah": 54, "name": "Al-Qamar", "arabic": "القمر", "start_page": 528, "end_page": 531},
    {"surah": 53, "name": "An-Najm", "arabic": "النجم", "start_page": 526, "end_page": 528},
    {"surah": 52, "name": "At-Tur", "arabic": "الطور", "start_page": 523, "end_page": 525},
    {"surah": 51, "name": "Adh-Dhariyat", "arabic": "الذاريات", "start_page": 520, "end_page": 523},
    
    # Juz 26 (Pages 502-521) - Partial surahs
    {"surah": 50, "name": "Qaf", "arabic": "ق", "start_page": 518, "end_page": 520},
    {"surah": 49, "name": "Al-Hujurat", "arabic": "الحجرات", "start_page": 515, "end_page": 517},
    {"surah": 48, "name": "Al-Fath", "arabic": "الفتح", "start_page": 511, "end_page": 515},
    {"surah": 47, "name": "Muhammad", "arabic": "محمد", "start_page": 507, "end_page": 510},
    {"surah": 46, "name": "Al-Ahqaf", "arabic": "الأحقاف", "start_page": 502, "end_page": 506},
    {"surah": 45, "name": "Al-Jathiyah", "arabic": "الجاثية", "start_page": 499, "end_page": 502},
]

# Create lookup dictionaries for easy access
SURAH_BY_NUMBER = {s["surah"]: s for s in SURAH_DATA_BACKWARD}
SURAH_BY_NAME = {s["name"]: s for s in SURAH_DATA_BACKWARD}

def get_surah_at_page(page):
    """Find which surah contains a given page"""
    for surah in SURAH_DATA_BACKWARD:
        if surah["start_page"] <= page <= surah["end_page"]:
            return surah
    return None

def get_next_surah_backward(current_surah_num):
    """Get the next surah in backward sequence (previous surah number)"""
    for i, surah in enumerate(SURAH_DATA_BACKWARD):
        if surah["surah"] == current_surah_num:
            if i + 1 < len(SURAH_DATA_BACKWARD):
                return SURAH_DATA_BACKWARD[i + 1]
    return None

def get_previous_surah_backward(current_surah_num):
    """Get the previous surah in backward sequence (next surah number - going forward)"""
    for i, surah in enumerate(SURAH_DATA_BACKWARD):
        if surah["surah"] == current_surah_num:
            if i - 1 >= 0:
                return SURAH_DATA_BACKWARD[i - 1]
    return None

def generate_backward_schedule(start_surah_num, start_page, daily_amount, working_days):
    """Generate backward schedule based on surah-by-surah progression"""
    schedule = []
    current_surah = SURAH_BY_NUMBER.get(start_surah_num)
    if not current_surah:
        return schedule
    
    current_page = start_page
    current_surah_num = start_surah_num
    day_count = 0
    
    while day_count < working_days:
        if not current_surah:
            break
            
        # Calculate pages left in current surah
        pages_in_surah = current_surah["end_page"] - current_surah["start_page"] + 1
        current_page_in_surah = current_page - current_surah["start_page"]
        pages_left_in_surah = pages_in_surah - current_page_in_surah
        
        if pages_left_in_surah <= 0:
            # Move to next surah in backward sequence
            current_surah = get_next_surah_backward(current_surah_num)
            if not current_surah:
                break
            current_surah_num = current_surah["surah"]
            current_page = current_surah["start_page"]
            continue

        if "0.5" in daily_amount:
            today_amount = 0.5
        else:  # "1 page daily" or any other
            today_amount = 1.0
        
        # Adjust amount if it exceeds pages left in surah
        if today_amount > pages_left_in_surah:
            today_amount = pages_left_in_surah
        
        # Add to schedule
        schedule.append({
            "day": day_count + 1,
            "surah_num": current_surah_num,
            "surah_name": current_surah["name"],
            "page": current_page,
            "amount": today_amount,
            "surah_pages_left": pages_left_in_surah - today_amount
        })
        
        # Update current page
        current_page += today_amount
        
        # If we completed the surah, move to next one
        if current_page > current_surah["end_page"]:
            current_surah = get_next_surah_backward(current_surah_num)
            if current_surah:
                current_surah_num = current_surah["surah"]
                current_page = current_surah["start_page"]
        
        day_count += 1
    
    return schedule

def generate_backward_schedule_with_pattern(start_surah_num, start_page, pattern, working_days):
    """Generate backward schedule with custom pattern"""
    schedule = []
    current_surah = SURAH_BY_NUMBER.get(start_surah_num)
    if not current_surah:
        return schedule
    
    current_page = start_page
    current_surah_num = start_surah_num
    day_count = 0
    
    while day_count < working_days:
        if not current_surah:
            break
            
        # Calculate pages left in current surah
        pages_in_surah = current_surah["end_page"] - current_surah["start_page"] + 1
        current_page_in_surah = current_page - current_surah["start_page"]
        pages_left_in_surah = pages_in_surah - current_page_in_surah
        
        if pages_left_in_surah <= 0:
            # Move to next surah in backward sequence
            current_surah = get_next_surah_backward(current_surah_num)
            if not current_surah:
                break
            current_surah_num = current_surah["surah"]
            current_page = current_surah["start_page"]
            continue
        
        # Get amount from pattern
        today_amount = pattern[day_count % len(pattern)]
        
        # Adjust amount if it exceeds pages left in surah
        if today_amount > pages_left_in_surah:
            today_amount = pages_left_in_surah
        
        # Add to schedule
        schedule.append({
            "day": day_count + 1,
            "surah_num": current_surah_num,
            "surah_name": current_surah["name"],
            "page": current_page,
            "amount": today_amount
        })
        
        # Update current page
        current_page += today_amount
        
        # If we completed the surah, move to next one
        if current_page > current_surah["end_page"]:
            current_surah = get_next_surah_backward(current_surah_num)
            if current_surah:
                current_surah_num = current_surah["surah"]
                current_page = current_surah["start_page"]
        
        day_count += 1
    
    return schedule

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
    """Get murajjah for a specific day with GROUP-BASED distribution"""
    if murajjah_option == "No Murajjah":
        return "Teacher will assign" if not for_pdf else ""
    
    if murajjah_option == "Manual Selection":
        day_key = f"day{(day_number % 6) + 1}"
        selected = st.session_state.manual_murajjah[day_key]
        if selected:
            if for_pdf:
                return ", ".join([str(s) for s in selected])
            else:
                return ", ".join([f"Para {s}" for s in selected])
        return "Not assigned" if not for_pdf else ""
    
    # Auto Generate - GROUP-BASED DISTRIBUTION
    current_sipara = st.session_state.current_sipara
    is_backward = "Backward" in st.session_state.direction
    
    if is_backward:
        # For backward direction: All siparas from 30 down to (but NOT including) current_sipara
        completed = list(range(30, current_sipara, -1))
    else:
        # For forward direction: All siparas from 1 up to (but NOT including) current_sipara
        completed = list(range(1, current_sipara))
    
    if not completed or len(completed) == 0:
        return "Revision Day" if not for_pdf else "Revision"
    
    # GROUP THE COMPLETED SIPARAS (6 groups of 5)
    # Group 1: 1-5, Group 2: 6-10, Group 3: 11-15, etc.
    groups = {}
    for sipara in completed:
        group_num = (sipara - 1) // 5  # 0-based group number
        if group_num not in groups:
            groups[group_num] = []
        groups[group_num].append(sipara)
    
    # Sort groups by group number
    sorted_groups = sorted(groups.items())
    
    # If we have less than 2 groups, just return all siparas
    if len(sorted_groups) < 2:
        day_paras = completed
    else:
        # DISTRIBUTE BY DAY USING ROUND-ROBIN ACROSS GROUPS
        day_paras = []
        day_index = day_number % 6  # Which day of the 6-day cycle
        
        # For each group, take the (day_index)th element
        # This gives us: Day 0: 1st from each group, Day 1: 2nd from each group, etc.
        for group_num, group_siparas in sorted_groups:
            # Sort siparas within each group
            group_siparas.sort()
            
            # Take one sipara from this group based on day_index
            if day_index < len(group_siparas):
                day_paras.append(group_siparas[day_index])
            # If we've taken all from this group, start from beginning
            elif len(group_siparas) > 0:
                day_paras.append(group_siparas[day_index % len(group_siparas)])
    
    # Remove duplicates and sort
    day_paras = sorted(list(set(day_paras)))
    
    if not day_paras:
        return "Revision Day" if not for_pdf else "Revision"
    
    if for_pdf:
        return ", ".join([str(p) for p in day_paras])
    else:
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
    """Calculate the complete schedule with actual calendar dates - SHOW SINGLE SOLUTION"""
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
    
    # ============ NEW: ADAPTIVE MIXED CALCULATION ============
    def find_optimal_mix(total_pages, available_days):
        """Find optimal combination of 0.5 and 1.0 pages to reach target"""
        
        # If we can't even complete with all 1.0 pages
        if available_days < total_pages:
            return None, None  # Impossible
        
        # Try different ratios
        for full_days in range(0, available_days + 1):
            half_days = available_days - full_days
            total_possible = (full_days * 1.0) + (half_days * 0.5)
            
            if total_possible >= total_pages:
                # Found a working combination
                # Create pattern: distribute full days evenly among half days
                pattern = []
                if full_days > 0:
                    # Calculate spacing between full days
                    spacing = max(1, half_days // full_days)
                    half_counter = 0
                    
                    for i in range(available_days):
                        if half_counter >= spacing and full_days > 0:
                            pattern.append(1.0)
                            full_days -= 1
                            half_counter = 0
                        elif half_days > 0:
                            pattern.append(0.5)
                            half_days -= 1
                            half_counter += 1
                        elif full_days > 0:
                            pattern.append(1.0)
                            full_days -= 1
                else:
                    # All half days
                    pattern = [0.5] * available_days
                
                return pattern, total_possible
        
        return None, None

    # Calculate minimum days needed based on daily amount
    if "Mixed" in daily_amount:
        # NEW: Use adaptive mixed calculation
        optimal_pattern, max_possible = find_optimal_mix(total_pages_needed, current_working_days)
        
        if optimal_pattern:
            # We found a pattern that works
            min_days_needed = len(optimal_pattern)
            avg_pages_per_day = sum(optimal_pattern) / len(optimal_pattern)
            can_use_mixed = True
        else:
            # Try with maximum working days (reduce holidays)
            optimal_pattern, max_possible = find_optimal_mix(total_pages_needed, max_working_days)
            if optimal_pattern:
                min_days_needed = len(optimal_pattern)
                avg_pages_per_day = sum(optimal_pattern) / len(optimal_pattern)
                can_use_mixed = True
            else:
                min_days_needed = total_pages_needed  # Need all 1.0 pages
                avg_pages_per_day = 1.0
                can_use_mixed = False
    elif "0.5" in daily_amount:
        # If 0.5 page daily: need 2 days per page
        min_days_needed = total_pages_needed * 2
        avg_pages_per_day = 0.5
        can_use_mixed = True
    else:
        # 1 page daily
        min_days_needed = total_pages_needed
        avg_pages_per_day = 1.0
        can_use_mixed = False
    
    # CHECK: Can we reach target with current settings?
    can_reach_target = current_working_days >= min_days_needed
    
    if not can_reach_target:
        # TARGET CANNOT BE REACHED! Show adaptive solutions
        
        st.error(f"""
        ❌ **TARGET CANNOT BE REACHED WITH CURRENT PLAN!**
        
        **Problem:**
        - You need at least **{min_days_needed:.1f}** working days
        - You only have **{current_working_days}** working days
        - Shortfall: **{min_days_needed - current_working_days:.1f}** days
        """)
        
        # ============ ADAPTIVE SOLUTIONS ============
        solution_found = False
        
        # Solution 1: Try Mixed pattern if not already using it
        if "Mixed" not in daily_amount and can_use_mixed:
            optimal_pattern, max_possible = find_optimal_mix(total_pages_needed, current_working_days)
            if optimal_pattern:
                st.success(f"""
                **✅ SOLUTION: Use Adaptive Mixed Pages**
                
                **Action needed:**
                - Change from **{daily_amount}** to **Mixed (0.5 & 1 page)**
                
                **Result:**
                - Working days needed: **{current_working_days}** (same)
                - Pattern: {optimal_pattern[:10]}...
                - You can complete **{max_possible:.1f}** pages
                """)
                solution_found = True
        
        # Solution 2: Reduce holidays
        if not solution_found and max_working_days >= min_days_needed:
            holidays_needed = max(0, days_in_month - len(sundays) - min_days_needed)
            st.success(f"""
            **✅ SOLUTION: Reduce Holidays**
            
            **Action needed:**
            - Reduce extra holidays from **{extra_holidays}** to **{holidays_needed}**
            
            **Result:**
            - Working days: **{min_days_needed}** (from {current_working_days})
            - You can complete all **{total_pages_needed}** pages
            """)
            solution_found = True
        
        # Solution 3: Increase to 1 page daily (if currently on 0.5 or Mixed)
        if not solution_found and ("0.5" in daily_amount or "Mixed" in daily_amount):
            new_min_days_1page = total_pages_needed
            if max_working_days >= new_min_days_1page:
                holidays_needed = max(0, days_in_month - len(sundays) - new_min_days_1page)
                st.success(f"""
                **✅ SOLUTION: Increase to 1 Page Daily**
                
                **Action needed:**
                - Change from **{daily_amount}** to **1 page daily**
                - Set holidays to **{holidays_needed}**
                
                **Result:**
                - Working days needed: **{new_min_days_1page}** (down from {min_days_needed})
                - You can complete all **{total_pages_needed}** pages
                """)
                solution_found = True
        
        # Solution 4: Try different mixed pattern with reduced holidays
        if not solution_found and "Mixed" in daily_amount:
            # Try with maximum working days
            optimal_pattern, max_possible = find_optimal_mix(total_pages_needed, max_working_days)
            if optimal_pattern:
                holidays_needed = max(0, days_in_month - len(sundays) - max_working_days)
                st.success(f"""
                **✅ SOLUTION: Use Adaptive Mixed with Reduced Holidays**
                
                **Action needed:**
                - Set holidays to **{holidays_needed}**
                - Use adaptive mixed pattern
                
                **Result:**
                - Working days: **{max_working_days}** (from {current_working_days})
                - Pattern: {optimal_pattern[:10]}...
                - You can complete **{max_possible:.1f}** pages
                """)
                solution_found = True
        
        # FINAL CHECK - If IMPOSSIBLE even with all adjustments
        if not solution_found:
            # Check if it's truly impossible
            if max_working_days < total_pages_needed:
                st.error(f"""
                ⚠️ **IMPOSSIBLE TO REACH TARGET THIS MONTH!**
                
                **Reason:** You need {total_pages_needed} pages but only have {max_working_days} maximum working days.
                
                **What you CAN do:**
                - Complete maximum of **{int(max_working_days * avg_pages_per_day)}** pages
                - New target: **Page {start_page + int(max_working_days * avg_pages_per_day) if direction == 'Forward (1 → 30)' else start_page - int(max_working_days * avg_pages_per_day)}**
                """)
            else:
                st.error("""
                ⚠️ **CANNOT FIND A WORKABLE SOLUTION!**
                
                Please try:
                1. Reducing your target pages
                2. Choosing a different month with more days
                3. Reducing your extra holidays
                """)
            
            return None
        
        st.info("""
        **📝 Adjust your settings according to the solution above, then click "Generate Takhteet" again.**
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
    
    if is_backward:
        # ============ BACKWARD SURAH-BASED SCHEDULE ============
        # Get surah for starting page
        start_surah = get_surah_at_page(start_page)
        if not start_surah:
            st.error(f"❌ Page {start_page} is not in the surah database. Please check the page number.")
            return None
        
        # Check if start page is valid within surah
        if start_page < start_surah["start_page"] or start_page > start_surah["end_page"]:
            st.error(f"❌ Page {start_page} is not within {start_surah['name']} (pages {start_surah['start_page']}-{start_surah['end_page']})")
            return None
        
        # Generate backward schedule
        if daily_amount == "Mixed (0.5 & 1 page)":
            # Use adaptive pattern
            optimal_pattern, _ = find_optimal_mix(total_pages, working_days)
            if not optimal_pattern:
                optimal_pattern = [0.5, 0.5, 1, 0.5, 0.5, 1]  # Fallback to default
            
            backward_schedule = generate_backward_schedule_with_pattern(
                start_surah_num=start_surah["surah"],
                start_page=start_page,
                pattern=optimal_pattern,
                working_days=working_days
            )
        else:
            backward_schedule = generate_backward_schedule(
                start_surah_num=start_surah["surah"],
                start_page=start_page,
                daily_amount=daily_amount,
                working_days=working_days
            )
        
        if not backward_schedule:
            st.error("❌ Could not generate backward schedule. Please check your inputs.")
            return None
        
        # Calculate total pages from backward schedule
        total_pages_scheduled = sum(item["amount"] for item in backward_schedule)
        
        # Check if schedule reaches target
        if total_pages_scheduled < total_pages:
            # Show what we CAN achieve
            st.warning(f"""
            ⚠️ **Note: With backward surah progression, you'll complete {total_pages_scheduled:.1f} pages instead of {total_pages}**
            
            **Reason:** Backward progression follows surah boundaries, not simple page counts.
            
            **Actual target reachable:** Page {start_page - total_pages_scheduled if is_backward else start_page + total_pages_scheduled}
            
            **Surahs covered:**
            """)
            
            # Show surahs that WILL be covered
            surahs_covered = {}
            for item in backward_schedule:
                surahs_covered[item["surah_num"]] = item["surah_name"]
            
            if surahs_covered:
                cols = st.columns(3)
                for i, (surah_num, surah_name) in enumerate(sorted(surahs_covered.items())):
                    with cols[i % 3]:
                        st.markdown(f"• {surah_num}. {surah_name}")
            
            # Update total_pages to what's actually achievable
            total_pages = total_pages_scheduled
        
        # Convert backward schedule to the format expected by the rest of the code
        for day_schedule in backward_schedule[:working_days]:
            schedule.append({
                'page': day_schedule["page"],
                'amount': day_schedule["amount"],
                'surah_name': day_schedule["surah_name"],
                'surah_num': day_schedule["surah_num"]
            })
        
    else:
        # ============ FORWARD DIRECTION (ORIGINAL LOGIC WITH ADAPTIVE MIXED) ============
        if daily_amount == "Mixed (0.5 & 1 page)":
            # Use adaptive pattern
            optimal_pattern, _ = find_optimal_mix(total_pages, working_days)
            if not optimal_pattern:
                optimal_pattern = [0.5, 0.5, 1, 0.5, 0.5, 1]  # Fallback
            
            current_page_val = start_page
            for i in range(working_days):
                if i < len(optimal_pattern):
                    amount = optimal_pattern[i]
                else:
                    # Repeat pattern if needed
                    amount = optimal_pattern[i % len(optimal_pattern)]
                
                schedule.append({
                    'page': current_page_val,
                    'amount': amount
                })
                current_page_val += amount
                if current_page_val > end_page:
                    current_page_val = end_page
        else:
            amount = 0.5 if "0.5" in daily_amount else 1.0
            current_page_val = start_page
            for i in range(working_days):
                schedule.append({
                    'page': current_page_val,
                    'amount': amount
                })
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
    ✅ **Schedule Generated Successfully!**
    
    📊 **Schedule Summary:**
    - **Total Pages to Complete:** {total_pages}
    - **Working Days:** {working_days}
    - **Holidays:** {len(all_holidays)} (Sundays: {len(sundays)}, Extra: {extra_holidays})
    - **Daily Amount:** {daily_amount}
    - **Pages Completed:** {pages_completed:.1f} / {total_pages}
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
        
        # === DAILY JADEEN AMOUNT - MUST BE BEFORE backward/forward section ===
        st.session_state.daily_amount = st.selectbox(
            "**Daily Jadeen Amount**",
            options=["0.5 page daily", "1 page daily", "Mixed (0.5 & 1 page)"],
            index=2
        )
        
        # Form inputs in grid
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
                # For backward direction: Surah-based selection
                
                # Create surah options for dropdown
                surah_options = []
                for surah in SURAH_DATA_BACKWARD:
                    surah_text = f"Surah {surah['surah']}: {surah['name']} (pages {surah['start_page']}-{surah['end_page']})"
                    surah_options.append((surah['surah'], surah_text))
                
                # Default to Surah 77 (Al-Mursalat) - common starting point
                default_index = next((i for i, (num, text) in enumerate(surah_options) if num == 77), 0)
                
                # Surah selection
                selected_surah_text = st.selectbox(
                    "**Select Starting Surah**",
                    options=[text for _, text in surah_options],
                    index=default_index,
                    help="Select the surah you're currently memorizing"
                )
                
                # Get selected surah number
                selected_surah_num = None
                for num, text in surah_options:
                    if text == selected_surah_text:
                        selected_surah_num = num
                        break
                
                if selected_surah_num:
                    selected_surah = SURAH_BY_NUMBER[selected_surah_num]
                    
                    # Page within selected surah
                    page_col1, page_col2 = st.columns(2)
                    with page_col1:
                        st.session_state.start_page = st.number_input(
                            "**Starting Page within Surah**",
                            min_value=float(selected_surah["start_page"]),
                            max_value=float(selected_surah["end_page"]),
                            value=float(selected_surah["start_page"]),
                            step=0.5 if "0.5" in st.session_state.daily_amount else 1.0,
                            format="%.1f",
                            help=f"Pages {selected_surah['start_page']}-{selected_surah['end_page']} in {selected_surah['name']}"
                        )
                    
                    with page_col2:
                        # Show surah info
                        st.markdown(f"""
                        <div style='background: rgba(59, 130, 246, 0.1); padding: 10px; border-radius: 10px; margin-top: 25px;'>
                        <p style='margin: 0; font-size: 0.9rem; color: #3b82f6;'><strong>{selected_surah['name']}</strong></p>
                        <p style='margin: 0; font-size: 0.8rem; color: #6b7280;'>Pages: {selected_surah['start_page']}–{selected_surah['end_page']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Target page
                st.session_state.end_page = st.number_input(
                    "**Target Page (Where to stop)**",
                    min_value=1,
                    max_value=604,
                    value=511,
                    step=1,
                    help="The page number where you want to stop memorizing"
                )
                
            else:
                # Forward direction remains the same
                forward_col1, forward_col2 = st.columns(2)
                with forward_col1:
                    st.session_state.start_page = st.number_input(
                        "**Current Jadeen Page**",
                        min_value=1,
                        max_value=604,
                        value=418,
                        step=1
                    )
                with forward_col2:
                    st.session_state.end_page = st.number_input(
                        "**Target Jadeen Page**",
                        min_value=1,
                        max_value=604,
                        value=430,
                        step=1
                    )
        
        with col2:
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
        
        # Create DataFrame for display - ADD SURAH COLUMN FOR BACKWARD
        df = pd.DataFrame(st.session_state.schedule)
        
        if "Backward" in st.session_state.direction:
            # For backward direction: Add surah information
            display_columns = ['Date', 'Day', 'Jadeen', 'Surah', 'Juzz Hali', 'Murajjah']
            
            # Create a new list with surah info
            display_data = []
            for day_data in st.session_state.schedule:
                if not day_data['isHoliday']:
                    # Get surah info for this page
                    page_num = int(day_data['Jadeen'].split()[0]) if day_data['Jadeen'] != 'OFF' else 0
                    surah = get_surah_at_page(page_num) if page_num > 0 else None
                    surah_info = f"{surah['name']}" if surah else ""
                    
                    display_data.append({
                        'Date': day_data['Date'],
                        'Day': day_data['Day'],
                        'Jadeen': day_data['Jadeen'],
                        'Surah': surah_info,
                        'Juzz Hali': day_data['Juzz Hali'],
                        'Murajjah': day_data['Murajjah']
                    })
                else:
                    display_data.append({
                        'Date': day_data['Date'],
                        'Day': day_data['Day'],
                        'Jadeen': 'OFF',
                        'Surah': '—',
                        'Juzz Hali': '—',
                        'Murajjah': '—'
                    })
            
            display_df = pd.DataFrame(display_data)
        else:
            # Forward direction: Original format
            display_columns = ['Date', 'Day', 'Jadeen', 'Juzz Hali', 'Murajjah']
            display_df = df[display_columns]
        
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
        
        # Show schedule summary with surah info for backward
        if "Backward" in st.session_state.direction:
            st.markdown("---")
            with st.expander("📋 Surah Progression Summary", expanded=True):
                # Extract unique surahs from schedule
                surahs_progress = {}
                for day_data in st.session_state.schedule:
                    if not day_data['isHoliday'] and day_data['Jadeen'] != 'OFF':
                        page_num = int(day_data['Jadeen'].split()[0])
                        surah = get_surah_at_page(page_num)
                        if surah:
                            surahs_progress[surah['surah']] = surah['name']
                
                if surahs_progress:
                    st.markdown("**Surahs in this schedule:**")
                    surah_list = []
                    for surah_num in sorted(surahs_progress.keys()):
                        surah_list.append(f"{surah_num}. {surahs_progress[surah_num]}")
                    
                    # Display in columns
                    cols = st.columns(3)
                    for i, surah_item in enumerate(surah_list):
                        with cols[i % 3]:
                            st.markdown(f"• {surah_item}")
        
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














