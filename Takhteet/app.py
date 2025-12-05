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

# Replace your current st.markdown CSS section with this updated version:

st.markdown("""
<style>
    /* Main container - Dark mode compatible */
    .main {
        background: linear-gradient(135deg, #f0fdf4 0%, #f0fdfa 100%);
        padding: 2rem;
    }
    
    /* Cards - Dark mode compatible */
    .stCard {
        background: white !important;
        border-radius: 1rem;
        padding: 2rem;
        box-shadow: 0 10px 40px rgba(16, 185, 129, 0.1);
        margin-bottom: 2rem;
    }
    
    /* Text colors for dark mode */
    h1, h2, h3, h4, h5, h6 {
        color: #1f2937 !important;
    }
    
    p, span, div, label {
        color: #1f2937 !important;
    }
    
    /* Buttons */
    .stButton button {
        border-radius: 0.5rem;
        font-weight: 600;
        transition: all 0.3s;
        border: none;
        color: white !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }
    
    /* Input fields */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        border-radius: 0.5rem;
        border: 2px solid #e5e7eb !important;
        background-color: white !important;
        color: #1f2937 !important;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus {
        border-color: #10b981 !important;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
    }
    
    /* Labels */
    label {
        color: #1f2937 !important;
        font-weight: 600 !important;
    }
    
    /* Radio buttons */
    .stRadio > label {
        background: white !important;
        border: 2px solid #e5e7eb !important;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
        color: #1f2937 !important;
    }
    
    .stRadio > label:hover {
        border-color: #10b981 !important;
    }
    
    /* Holiday rows */
    .holiday-row {
        background-color: #fef2f2 !important;
    }
    
    /* Table styling */
    table {
        border-collapse: collapse;
        width: 100%;
        border-radius: 0.5rem;
        overflow: hidden;
        background-color: white !important;
    }
    
    th {
        background-color: #10b981 !important;
        color: white !important;
        font-weight: 600;
        padding: 1rem !important;
    }
    
    td {
        padding: 0.75rem !important;
        border: 1px solid #e5e7eb !important;
        background-color: white !important;
        color: #1f2937 !important;
    }
    
    tr:nth-child(even) {
        background-color: #f9fafb !important;
    }
    
    tr:nth-child(odd) {
        background-color: white !important;
    }
    
    /* Dataframe cells */
    .dataframe th {
        background-color: #10b981 !important;
        color: white !important;
    }
    
    .dataframe td {
        background-color: white !important;
        color: #1f2937 !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #f8fafc !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #1f2937 !important;
    }
    
    /* Manual Murajjah styling */
    .sipara-btn {
        padding: 4px 8px !important;
        margin: 2px !important;
        font-size: 12px !important;
        border-radius: 4px !important;
        min-width: 32px !important;
        height: 28px !important;
    }
    
    .day-card {
        background: white !important;
        border: 2px solid #e5e7eb !important;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .day-card h4 {
        margin-top: 0;
        color: #1f2937 !important;
    }
    
    /* Caption text */
    .stCaption {
        color: #6b7280 !important;
    }
    
    /* Success messages */
    .stSuccess {
        background-color: #d1fae5 !important;
        color: #065f46 !important;
    }
    
    /* Error messages */
    .stError {
        background-color: #fee2e2 !important;
        color: #991b1b !important;
    }
    
    /* Warning messages */
    .stWarning {
        background-color: #fef3c7 !important;
        color: #92400e !important;
    }
    
    /* Info messages */
    .stInfo {
        background-color: #dbeafe !important;
        color: #1e40af !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #f8fafc !important;
        color: #1f2937 !important;
        border-radius: 0.5rem;
    }
    
    .streamlit-expanderContent {
        background-color: white !important;
        color: #1f2937 !important;
    }
    
    /* Override Streamlit's dark mode styles */
    @media (prefers-color-scheme: dark) {
        .main {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
        }
        
        .stCard {
            background: #1e293b !important;
            color: #f1f5f9 !important;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #f1f5f9 !important;
        }
        
        p, span, div, label {
            color: #f1f5f9 !important;
        }
        
        .day-card {
            background: #1e293b !important;
            border-color: #334155 !important;
        }
        
        table, td, tr {
            background-color: #1e293b !important;
            color: #f1f5f9 !important;
            border-color: #334155 !important;
        }
        
        .dataframe th, .dataframe td {
            background-color: #1e293b !important;
            color: #f1f5f9 !important;
        }
        
        .stTextInput input, .stNumberInput input, .stSelectbox select {
            background-color: #1e293b !important;
            color: #f1f5f9 !important;
            border-color: #475569 !important;
        }
        
        .stRadio > label {
            background: #1e293b !important;
            color: #f1f5f9 !important;
            border-color: #475569 !important;
        }
        
        section[data-testid="stSidebar"] {
            background-color: #0f172a !important;
        }
        
        section[data-testid="stSidebar"] * {
            color: #f1f5f9 !important;
        }
        
        .streamlit-expanderHeader {
            background-color: #1e293b !important;
            color: #f1f5f9 !important;
        }
        
        .streamlit-expanderContent {
            background-color: #1e293b !important;
            color: #f1f5f9 !important;
        }
        
        .stSuccess {
            background-color: #064e3b !important;
            color: #a7f3d0 !important;
        }
        
        .stError {
            background-color: #7f1d1d !important;
            color: #fecaca !important;
        }
        
        .stWarning {
            background-color: #78350f !important;
            color: #fef3c7 !important;
        }
        
        .stInfo {
            background-color: #1e3a8a !important;
            color: #dbeafe !important;
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
    """Calculate the complete schedule with actual calendar dates"""
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
    
    # Get Sundays
    sundays = []
    for day in range(1, days_in_month + 1):
        if datetime(year, month, day).weekday() == 6:
            sundays.append(day)
    
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
            jadeen = schedule[jadeen_idx]
            
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
    """Create PDF in PORTRAIT orientation with proper Arabic formatting"""
    try:
        # Create PDF in PORTRAIT mode
        pdf = FPDF(orientation='P')
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        # Add custom font for Arabic if available
        use_arabic = ARABIC_SUPPORT
        
        # Title
        title = f"{student_name} - {selected_month_name} {selected_year}"
        pdf.set_font('Helvetica', 'B', 16)
        pdf.cell(0, 10, title, 0, 1, 'C')
        pdf.ln(5)
        
        # Add "تخطيط شهري" title in Arabic
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
        pdf.ln(10)
        
        # Adjust column widths for PORTRAIT orientation - GIVING MORE WIDTH TO NOTES
        total_width = 190
        
        # NEW COLUMN WIDTHS - Notes gets 25%, others reduced
        col_widths = [
            total_width * 0.25,   # ملاحظات (Notes) - INCREASED TO 25%
            total_width * 0.15,   # هدف حاصل كيڈو؟ (Target) - REDUCED
            total_width * 0.15,   # أجزاء المراجعة (Murajjah) - REDUCED
            total_width * 0.12,   # الجزء الحالي (Juzz Hali) - REDUCED
            total_width * 0.12,   # الجديد صفحة رقم (New Page) - REDUCED
            total_width * 0.11,   # كمية الجديد (Amount) - REDUCED
            total_width * 0.10    # التاريخ (Date) - SMALLEST
        ]
        
        # Headers - RTL order
        if use_arabic:
            headers = [
                format_arabic("ملاحظات"),          # Rightmost - WIDEST
                format_arabic("هدف حاصل كيڈو؟"),   # 
                format_arabic("أجزاء المراجعة"),   # 
                format_arabic("الجزء الحالي"),     # 
                format_arabic("الجديد (صفحة رقم)"),# 
                format_arabic("كمية الجديد"),      # 
                format_arabic("التاريخ")           # Leftmost - NARROWEST
            ]
        else:
            headers = [
                "Notes",            # WIDEST (25%)
                "Target Achieved?", # 
                "Murajjah Parts",   # 
                "Current Juzz",     # 
                "New (Page No.)",   # 
                "Amount",           # 
                "Date"              # NARROWEST (10%)
            ]
        
        # Draw table headers
        pdf.set_fill_color(200, 220, 255)
        pdf.set_font('Helvetica', 'B', 10)
        
        # Write headers in REVERSE order for RTL
        for i in range(6, -1, -1):
            if use_arabic and i >= 2:
                try:
                    pdf.set_font('Arabic', 'B', 10)
                except:
                    pdf.set_font('Helvetica', 'B', 8)
            else:
                pdf.set_font('Helvetica', 'B', 8)
            
            pdf.cell(col_widths[i], 8, headers[i], 1, 0, 'C', True)
        
        pdf.ln()
        
        # Get days data - using the SAME schedule as display
        if st.session_state.schedule:
            # Use the same schedule that was calculated for display
            schedule_data = st.session_state.schedule
        else:
            # Fallback to generate_schedule if needed
            schedule_data = generate_schedule(start_juz, days_in_month)
        
        # Draw table rows
        row_height = 8
        for day_schedule in schedule_data:
            day = day_schedule['Date']
            is_holiday = day_schedule['isHoliday']
            
            # Check if new page is needed
            if pdf.get_y() + row_height > 270:
                pdf.add_page()
                # Redraw headers
                pdf.set_fill_color(200, 220, 255)
                for i in range(6, -1, -1):
                    if use_arabic and i >= 2:
                        try:
                            pdf.set_font('Arabic', 'B', 10)
                        except:
                            pdf.set_font('Helvetica', 'B', 8)
                    else:
                        pdf.set_font('Helvetica', 'B', 8)
                    pdf.cell(col_widths[i], row_height, headers[i], 1, 0, 'C', True)
                pdf.ln()
            
            # Set font for content
            if use_arabic:
                try:
                    pdf.set_font('Arabic', '', 8)
                except:
                    pdf.set_font('Helvetica', '', 8)
            else:
                pdf.set_font('Helvetica', '', 8)
            
            # Prepare cell data
            if is_holiday:
                cell_data = [
                    "",  # Notes - WIDE COLUMN
                    "",  # Target
                    format_arabic("عطلة") if use_arabic else "Holiday",  # Murajjah
                    "",  # Current Juzz
                    "",  # New Page
                    "",  # Amount
                    str(day)  # Date - NARROW COLUMN
                ]
            else:
                # Extract data from schedule
                jadeen_text = day_schedule['Jadeen']
                juzz_hali = day_schedule['Juzz Hali']
                murajjah = day_schedule['Murajjah']
                
                # Parse Jadeen text to get page number and amount
                page_number = ""
                amount = ""
                if "(" in jadeen_text:
                    page_part = jadeen_text.split("(")[0].strip()
                    amount_part = jadeen_text.split("(")[1].replace(")", "").strip()
                    page_number = page_part
                    amount = amount_part.capitalize()
                
                # Clean up Murajjah - remove "Para" prefix for PDF
                if murajjah and murajjah != "—":
                    # Remove "Para" prefix and keep just numbers
                    murajjah_clean = murajjah.replace("Para", "").replace("para", "").strip()
                else:
                    murajjah_clean = ""
                
                # Clean up Juzz Hali
                clean_juzz_hali = juzz_hali if juzz_hali != "None" else ""
                
                cell_data = [
                    "",  # Notes - WIDE COLUMN (for teacher/student notes)
                    "",  # Target
                    murajjah_clean,  # Murajjah (just numbers)
                    clean_juzz_hali,  # Current Juzz
                    page_number,  # New Page
                    amount,  # Amount
                    str(day)  # Date - NARROW COLUMN
                ]
            
            # Write row data
            for i in range(6, -1, -1):
                cell_content = cell_data[i]
                
                # Set alignment
                align = 'C'
                if i == 6:  # Date - right align in narrow column
                    align = 'R'
                elif i == 0:  # Notes - left align for wide column
                    align = 'L'
                elif i == 2 and cell_content == "Holiday":  # Holiday
                    align = 'C'
                elif i == 2 and murajjah_clean:  # Murajjah numbers
                    align = 'C'
                elif i == 3 and clean_juzz_hali:  # Juzz Hali
                    align = 'C'
                
                # Format Arabic if needed
                if use_arabic and isinstance(cell_content, str) and any('\u0600' <= c <= '\u06FF' for c in cell_content):
                    cell_content = format_arabic(cell_content)
                
                if cell_content is None:
                    cell_content = ""
                
                pdf.cell(col_widths[i], row_height, str(cell_content), 1, 0, align)
            
            pdf.ln()
        
        # Footer note
        pdf.ln(10)
        if use_arabic:
            try:
                pdf.set_font('Arabic', '', 8)
            except:
                pdf.set_font('Helvetica', 'I', 8)
            footer = format_arabic("ملاحظة: العمودان الأيمن للطالب واليسار للمعلم")
            pdf.cell(0, 5, footer, 0, 0, 'C')
        else:
            pdf.set_font('Helvetica', 'I', 8)
            pdf.cell(0, 5, "Note: Right columns for student, left for teacher", 0, 0, 'C')
        
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
        
def render_manual_murajjah_section():
    """Render the manual murajjah selection interface"""
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
            
            # Create 3 columns for the 6 days (2 rows)
            col1, col2, col3 = st.columns(3)
            
            days = ['day1', 'day2', 'day3', 'day4', 'day5', 'day6']
            day_names = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6']
            
            for i, (day, day_name) in enumerate(zip(days, day_names)):
                if i < 3:
                    with col1 if i == 0 else col2 if i == 1 else col3:
                        render_day_card(day, day_name)
                else:
                    with col1 if i == 3 else col2 if i == 4 else col3:
                        render_day_card(day, day_name)
            
            st.markdown('</div>', unsafe_allow_html=True)

def render_day_card(day_key, day_name):
    """Render a card for selecting siparas for a day"""
    st.markdown(f'<div class="day-card">', unsafe_allow_html=True)
    st.markdown(f'**{day_name}**')
    
    # Create 6 rows of 5 siparas each
    for row in range(6):
        cols = st.columns(5)
        for col_idx in range(5):
            sipara = row * 5 + col_idx + 1
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
        st.caption(f"Selected: {', '.join(map(str, selected))}")
    else:
        st.caption("No siparas selected")
    
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
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h1>Quran Hifz Takhteet Generator</h1>
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
        
        # Form inputs in grid
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.student_name = st.text_input(
                "**Student Name**",
                placeholder="Enter student name",
                value=st.session_state.get('student_name', '')
            )
            
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
            
            st.session_state.current_sipara = st.slider(
                "**Current Sipara (Para)**",
                min_value=1,
                max_value=30,
                value=21
            )
        
        with col2:
            st.session_state.year = st.number_input(
                "**Year**",
                min_value=2024,
                max_value=2030,
                value=2025,
                step=1
            )
            
            st.session_state.daily_amount = st.selectbox(
                "**Daily Jadeen Amount**",
                options=["0.5 page daily", "1 page daily", "Mixed (0.5 & 1 page)"],
                index=2
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
                with st.spinner("Generating schedule..."):
                    calculate_schedule()
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


