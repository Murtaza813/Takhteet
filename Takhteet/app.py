import streamlit as st
import pandas as pd
from datetime import datetime
import calendar
from fpdf import FPDF
import base64

# Page configuration
st.set_page_config(
    page_title="Quran Hifz Takhteet Generator",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to match your design
st.markdown("""
<style>
    /* Main container */
    .main {
        background: linear-gradient(135deg, #f0fdf4 0%, #f0fdfa 100%);
        padding: 2rem;
    }
    
    /* Cards */
    .stCard {
        background: white;
        border-radius: 1rem;
        padding: 2rem;
        box-shadow: 0 10px 40px rgba(16, 185, 129, 0.1);
        margin-bottom: 2rem;
    }
    
    /* Buttons */
    .stButton button {
        border-radius: 0.5rem;
        font-weight: 600;
        transition: all 0.3s;
        border: none;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }
    
    /* Input fields */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        border-radius: 0.5rem;
        border: 2px solid #e5e7eb;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus {
        border-color: #10b981;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
    }
    
    /* Radio buttons */
    .stRadio label {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .stRadio label:hover {
        border-color: #10b981;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1f2937;
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
    }
    
    th {
        background-color: #10b981 !important;
        color: white !important;
        font-weight: 600;
        padding: 1rem !important;
    }
    
    td {
        padding: 0.75rem !important;
        border: 1px solid #e5e7eb;
    }
    
    tr:nth-child(even) {
        background-color: #f9fafb;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #f8fafc;
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
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .day-card h4 {
        margin-top: 0;
        color: #1f2937;
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

def get_murajjah_for_day(day_number, murajjah_option):
    """Get murajjah for a specific day"""
    if murajjah_option == "No Murajjah":
        return "Teacher will assign"
    
    if murajjah_option == "Manual Selection":
        day_key = f"day{(day_number % 6) + 1}"
        selected = st.session_state.manual_murajjah[day_key]
        if selected:
            return ", ".join([f"Para {s}" for s in selected])
        return "Not assigned"
    
    # Auto Generate
    current_sipara = st.session_state.current_sipara
    is_backward = "Backward" in st.session_state.direction
    
    if is_backward:
        completed = list(range(30, current_sipara, -1))
    else:
        completed = [30] + list(range(1, current_sipara))
    
    if not completed:
        return "No completed paras"
    
    paras_per_day = max(1, len(completed) // 6)
    start_idx = (day_number % 6) * paras_per_day
    end_idx = min(start_idx + paras_per_day, len(completed))
    
    if start_idx >= len(completed):
        return "Revision Day"
    
    day_paras = completed[start_idx:end_idx]
    return ", ".join([f"Para {p}" for p in day_paras])

def calculate_schedule():
    """Calculate the complete schedule"""
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
                current_page = start_page - sum(pattern[:i])
            else:
                current_page = start_page + sum(pattern[:i])
            
            if is_backward and current_page < end_page:
                current_page = end_page
            elif not is_backward and current_page > end_page:
                current_page = end_page
            
            schedule.append({
                'page': round(current_page, 1),
                'amount': amount
            })
    else:
        amount = 0.5 if "0.5" in daily_amount else 1.0
        current_page = start_page
        for i in range(working_days):
            schedule.append({
                'page': current_page,
                'amount': amount
            })
            if is_backward:
                current_page -= amount
                if current_page < end_page:
                    current_page = end_page
            else:
                current_page += amount
                if current_page > end_page:
                    current_page = end_page
    
    # Create full monthly schedule
    full_schedule = []
    jadeen_idx = 0
    weekday_counter = 0
    
    for day in range(1, days_in_month + 1):
        date = datetime(year, month, day)
        day_name = calendar.day_name[date.weekday()][:3]
        
        if day in all_holidays:
            full_schedule.append({
                'Date': day,
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
                juzz_hali = f"{int(jadeen['page'])-1}-{int(jadeen['page'])+8} (skip {int(jadeen['page'])})"
            else:
                start = max(1, jadeen['page'] - 10)
                end = jadeen['page'] - 1
                juzz_hali = f"{int(start)}-{int(end)}" if start <= end else "None"
            
            # Calculate murajjah
            murajjah = get_murajjah_for_day(weekday_counter, murajjah_option)
            
            full_schedule.append({
                'Date': day,
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

def create_pdf():
    """Create PDF from schedule - RELIABLE VERSION"""
    try:
        pdf = FPDF()
        pdf.add_page()
        
        # Title
        pdf.set_font('Arial', 'B', 18)
        pdf.text(10, 20, 'Quran Hifz Takhteet')
        
        # Info
        pdf.set_font('Arial', '', 12)
        student_name = st.session_state.get('student_name', 'Student')
        pdf.text(10, 30, f'Student: {student_name}')
        pdf.text(10, 37, f'Month: {st.session_state.month}/{st.session_state.year}')
        
        # Fix direction text
        direction = st.session_state.direction.replace("→", "to")
        pdf.text(10, 44, f'Direction: {direction}')
        
        # Table position
        y_position = 50
        
        # Header
        pdf.set_font('Arial', 'B', 10)
        col_width = pdf.w / 5
        
        headers = ['Date', 'Day', 'Jadeen', 'Juzz Hali', 'Murajjah']
        for i, header in enumerate(headers):
            pdf.set_xy(10 + i * col_width, y_position)
            pdf.cell(col_width, 10, header, 1, 0, 'C')
        
        y_position += 10
        
        # Data
        pdf.set_font('Arial', '', 9)
        for day in st.session_state.schedule:
            # Color for holidays
            if day['isHoliday']:
                pdf.set_fill_color(254, 202, 202)
            else:
                pdf.set_fill_color(255, 255, 255)
            
            # Clean text
            jadeen = str(day['Jadeen']).replace("—", "-")
            juzz_hali = str(day['Juzz Hali']).replace("—", "-")
            murajjah = str(day['Murajjah']).replace("—", "-")
            
            # Draw row
            pdf.set_xy(10, y_position)
            pdf.cell(col_width, 8, str(day['Date']), 1, 0, 'C', 1)
            pdf.cell(col_width, 8, day['Day'], 1, 0, 'C', 1)
            pdf.cell(col_width, 8, jadeen, 1, 0, 'C', 1)
            pdf.cell(col_width, 8, juzz_hali, 1, 0, 'C', 1)
            pdf.cell(col_width, 8, murajjah, 1, 0, 'C', 1)
            
            y_position += 8
            
            # Add new page if needed
            if y_position > pdf.h - 20:
                pdf.add_page()
                y_position = 20
        
        # Get PDF as bytes - SIMPLE AND RELIABLE
        import tempfile
        import os
        
        # Create temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            temp_path = tmp.name
        
        # Save PDF to temp file
        pdf.output(temp_path)
        
        # Read PDF bytes
        with open(temp_path, 'rb') as f:
            pdf_bytes = f.read()
        
        # Clean up temp file
        try:
            os.unlink(temp_path)
        except:
            pass
        
        return pdf_bytes
        
    except Exception as e:
        st.error(f"Error in create_pdf: {e}")
        # Return empty bytes
        return b""

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
            - 📊 **PDF export**
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
                index=11
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
                    value=1,
                    step=1
                )
                st.session_state.end_page = st.number_input(
                    "**Target Jadeen Page**",
                    min_value=1,
                    max_value=604,
                    value=50,
                    step=1
                )
            
            st.session_state.current_sipara = st.slider(
                "**Current Sipara (Para)**",
                min_value=1,
                max_value=30,
                value=27
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
        st.markdown(f"""
        <div class="stCard">
            <h2>Takhteet for {st.session_state.student_name} - {st.session_state.month}/{st.session_state.year}</h2>
            <p style='color: #10b981; font-weight: 600;'>({st.session_state.direction})</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create DataFrame for display
        df = pd.DataFrame(st.session_state.schedule)
        display_df = df[['Date', 'Day', 'Jadeen', 'Juzz Hali', 'Murajjah']]
        
        # Convert to HTML for styling
        def highlight_holidays(row):
            if st.session_state.schedule[row.name]['isHoliday']:
                return ['background-color: #fef2f2'] * len(row)
            return [''] * len(row)
        
    # Display schedule if exists
    if st.session_state.schedule:
        st.markdown("---")
        
        # REMOVED THE DUPLICATE TITLE HERE
        # The title is already shown in the main card above
        
        # Create DataFrame for display
        df = pd.DataFrame(st.session_state.schedule)
        display_df = df[['Date', 'Day', 'Jadeen', 'Juzz Hali', 'Murajjah']]
        
        # Convert to HTML for styling
        def highlight_holidays(row):
            if st.session_state.schedule[row.name]['isHoliday']:
                return ['background-color: #fef2f2'] * len(row)
            return [''] * len(row)
        
        # Display as styled table
        st.dataframe(
            display_df.style.apply(highlight_holidays, axis=1),
            use_container_width=True,
            height=600
        )
        
        # SIMPLE PDF Download button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            try:
                # Generate PDF
                pdf_bytes = create_pdf()
                
                # Verify PDF was created successfully
                if pdf_bytes and len(pdf_bytes) > 100:
                    # Simple download button
                    st.download_button(
                        label="📥 Download PDF",
                        data=pdf_bytes,
                        file_name=f"takhteet_{st.session_state.student_name}_{st.session_state.month}_{st.session_state.year}.pdf",
                        mime="application/pdf",
                        type="primary",
                        use_container_width=True
                    )
                    
                else:
                    st.error("PDF generation failed. Please try again.")
                    
            except Exception as e:
                st.error(f"Error creating PDF: {str(e)}")

if __name__ == "__main__":
    main()
