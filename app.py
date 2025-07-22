import streamlit as st
from datetime import datetime
from xhtml2pdf import pisa
from io import BytesIO
from jinja2 import Template
from groq import Groq
from dotenv import load_dotenv
import os

# Load Groq API key
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=groq_api_key)

# PDF conversion helper
def convert_html_to_pdf(source_html):
    result = BytesIO()
    pisa_status = pisa.CreatePDF(source_html, dest=result)
    if pisa_status.err:
        return None
    return result

# HTML wrapper to insert content into PDF with proper formatting
html_template = """
<html>
<head>
  <style>
    body { font-family: Arial, sans-serif; font-size: 12pt; line-height: 1.6; margin: 2cm; }
    .date { text-align: right; margin-bottom: 20px; }
    .address { margin-bottom: 20px; }
    .subject { font-weight: bold; margin-bottom: 20px; }
    .salutation { margin-bottom: 15px; }
    .content { margin-bottom: 30px; text-align: justify; }
    .closing { margin-bottom: 50px; }
    .signature { display: flex; justify-content: space-between; }
    .sign-left, .sign-right { width: 45%; }
    .footer { margin-top: 30px; font-size: 10pt; }
  </style>
</head>
<body>
{{ content }}
</body>
</html>
"""

st.title("🤖 PASC Permission Letter Generator")

with st.form("letter_form"):
    current_date = st.date_input("Current Date", value=datetime.today())
    authority = st.text_input("To (Authority)", value="The Estate Manager")
    organisation = st.text_input("Organisation", value="SCTR's Pune Institute of Computer Technology, Pune")
    event_name = st.text_input("Event Name", value="Crack Internship with PASC")
    event_date = st.date_input("Event Date", value=datetime.today())
    event_time = st.text_input("Event Time", value="3:30 PM to 6:30 PM")
    venue = st.text_input("Venue", value="Auditorium")
    purpose = st.text_area("Purpose", value="to guide students in preparing for and securing internships by sharing insights, strategies, and real experiences")

    your_name = st.text_input("Your Name", value="Aashlesh Wawge")
    your_role = st.text_input("Your Role", value="Secretary, PASC")
    counselor_name = st.text_input("Counselor Name", value="Dr. Geetanjali Kale")
    counselor_role = st.text_input("Counselor Role", value="Counselor, PASC")

    submitted = st.form_submit_button("Generate Letter")

if submitted:
    st.info("📨 Generating permission letter...")
    formatted_date = current_date.strftime("%d/%m/%Y")
    formatted_event_date = event_date.strftime("%dth %B")
    
    # Create formatted letter directly instead of using Groq
    letter_body = f"""
    <div class="date">Date: {formatted_date}</div>
    
    <div class="address">
    To,<br>
    {authority},<br>
    {organisation}.<br>
    </div>
    
    <div class="subject">
    Subject: Request for Permission to Use {venue} for PASC Session - "{event_name}"
    </div>
    
    <div class="salutation">
    Respected Sir,
    </div>
    
    <div class="content">
    We, the members of the PICT ACM Student Chapter (PASC), are organizing a session 
    titled "{event_name}" on {formatted_event_date} from {event_time}. This session 
    aims {purpose}.
    <br><br>
    We kindly request your permission to conduct the session in the {venue}. We assure 
    you that all resources provided will be used responsibly and the venue will be maintained 
    properly.
    </div>
    
    <div class="closing">
    Thanking you in anticipation,<br>
    Yours Sincerely,
    </div>
    
    <div class="signature">
    <div class="sign-left">
    {your_name}<br>
    ({your_role})
    </div>
    <div class="sign-right">
    {counselor_name}<br>
    ({counselor_role})
    </div>
    </div>
    
    <div class="footer">
    PICT ACM Student Chapter<br>
    Pune Institute of Computer Technology,<br>
    Dhankawadi, Pune, Maharashtra-411043<br>
    Website: pict.acm.org<br>
    Email: acm.pict@gmail.com
    </div>
    """

    st.success("✅ Letter generated successfully")
    st.markdown("### ✉️ Preview:")
    st.write(letter_body, unsafe_allow_html=True)

    # Render to PDF
    template = Template(html_template)
    rendered_html = template.render(content=letter_body)
    pdf = convert_html_to_pdf(rendered_html)

    if pdf:
        filename = f"Permission_Letter_{datetime.now().strftime('%H%M%S')}.pdf"
        st.download_button("📥 Download PDF", data=pdf.getvalue(), file_name=filename, mime="application/pdf")
    else:
        st.error("❌ PDF generation failed. Try again.")
