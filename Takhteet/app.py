import streamlit as st
import os

# Page configuration
st.set_page_config(
    page_title="Quran Hifz Takhteet Generator",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to remove extra padding
st.markdown("""
<style>
    .main > div {
        padding-top: 0rem;
    }
    .stApp {
        max-width: 100%;
        padding: 0;
    }
    iframe {
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# Function to read HTML file
def read_html_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        # Try different encoding if UTF-8 fails
        with open(file_path, 'r', encoding='latin-1') as file:
            return file.read()

# Main app
def main():
    # Sidebar for information
    with st.sidebar:
        st.title("📖 Quran Hifz Takhteet")
        st.markdown("---")
        st.markdown("""
        ### How to Use:
        1. Fill in student details
        2. Select month/year
        3. Choose Hifz direction
        4. Set Jadeen pages
        5. Generate schedule
        6. Download PDF
        """)
        
        st.markdown("---")
        st.markdown("### Features:")
        st.markdown("""
        - 🎯 Backward & Forward Hifz
        - 📅 Monthly schedule generator
        - 📄 Jadeen tracking
        - 🔄 Murajjah planning
        - 📊 PDF export
        """)
        
        st.markdown("---")
        
        # File uploader for HTML file
        uploaded_file = st.file_uploader("Upload HTML file", type=['html'])
        if uploaded_file is not None:
            # Save the uploaded file
            with open("index.html", "wb") as f:
                f.write(uploaded_file.getvalue())
            st.success("File uploaded successfully!")
            st.rerun()
        
        st.info("Made with ❤️ for Huffaz")

    # Main content
    st.title("Quran Hifz Takhteet Generator")
    
    # Check if HTML file exists
    html_file = "index.html"
    
    if os.path.exists(html_file):
        try:
            # Read HTML content
            html_content = read_html_file(html_file)
            
            # Display HTML with iframe
            st.components.v1.html(html_content, height=1500, scrolling=True)
            
            # Add download button for the HTML file
            with open(html_file, "r", encoding='utf-8') as f:
                html_data = f.read()
            
            st.download_button(
                label="📥 Download HTML File",
                data=html_data,
                file_name="quran_takhteet.html",
                mime="text/html"
            )
            
        except Exception as e:
            st.error(f"Error loading HTML file: {str(e)}")
            st.info("Try uploading your HTML file using the uploader in the sidebar.")
            
            # Show file upload in main area too
            uploaded_file_main = st.file_uploader("Or upload your HTML file here:", type=['html'], key="main_upload")
            if uploaded_file_main is not None:
                with open("index.html", "wb") as f:
                    f.write(uploaded_file_main.getvalue())
                st.success("File uploaded! Please refresh the page.")
                st.rerun()
    
    else:
        st.error(f"HTML file '{html_file}' not found.")
        st.info("Please upload your HTML file using the uploader in the sidebar.")
        
        # Quick help
        with st.expander("ℹ️ Need help?"):
            st.markdown("""
            1. Make sure your original HTML file is named `index.html`
            2. Or upload it using the sidebar uploader
            3. The app will embed your HTML directly
            4. All JavaScript features will work
            """)

if __name__ == "__main__":
    main()