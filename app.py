# Dynamic Permission Letter Generator
# Fixed: Gemini prompt, logo alignment, and template rendering issues
# Fixed the logos and signature alignment

import streamlit as st
from datetime import datetime
from xhtml2pdf import pisa
from io import BytesIO
from jinja2 import Template
from dotenv import load_dotenv
import os
import google.generativeai as genai
import base64

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel('gemini-2.0-flash')

# Function to encode image to Base64
def get_image_as_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Logo placeholders - Update paths to your actual logo files
# Assuming the images are in the same directory as the script.
try:
    pict_logo_base64 = get_image_as_base64("download.png")
    acm_logo_base64 = get_image_as_base64("download (1).png")
    pasc_logo_base64 = get_image_as_base64("images.png")
except FileNotFoundError:
    st.error("Logo files not found. Please ensure 'download.png', 'download (1).png', and 'images.png' are in the same directory.")
    st.stop()

def convert_html_to_pdf(source_html):
    result = BytesIO()
    pisa_status = pisa.CreatePDF(source_html, dest=result)
    if pisa_status.err:
        return None
    return result

def generate_with_gemini(prompt):
    try:
        response = gemini_model.generate_content(
            contents=prompt,
            generation_config={'temperature': 0.7}
        )
        return response.text.strip()
    except Exception as e:
        print(f"Gemini error: {e}")
        return None

# Helper for day suffix
def format_day_suffix(date_obj):
    day = date_obj.day
    suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    return f"{day}{suffix} {date_obj.strftime('%B')}"

# ---------------- Streamlit UI ----------------
st.title("🤖 PASC Permission Letter Generator")

with st.form("letter_form"):
    st.markdown("#### Event Details")
    current_date = st.date_input("Current Date", value=datetime.today())
    authority = st.text_input("To (Authority)", value="The Estate Manager")
    organisation = st.text_input("Organisation", value="SCTR's Pune Institute of Computer Technology, Pune")
    event_name = st.text_input("Event Name", value="Crack Internship with PASC")
    event_date = st.date_input("Event Date", value=datetime.today())
    event_time = st.text_input("Event Time", value="3:30 PM to 6:30 PM")
    venue = st.text_input("Venue", value="Auditorium")

    st.markdown("#### Letter Content")
    purpose = st.text_area("Purpose", value="To guide students in preparing for and securing internships by sharing insights, strategies, and real experiences.")

    st.markdown("#### Your Details")
    your_name = st.text_input("Your Name", value="Aashlesh Wawge")
    your_role = st.text_input("Your Role", value="Secretary, PASC")
    counselor_name = st.text_input("Counselor Name", value="Dr. Geetanjali Kale")
    counselor_role = st.text_input("Counselor Role", value="Counselor, PASC")
    email = st.text_input("Email", value="acm.pict@gmail.com")

    submitted = st.form_submit_button("Generate Letter")

# ---------------- Processing ----------------
if submitted:
    st.info("📨 Generating permission letter...")

    formatted_date = current_date.strftime("%d/%m/%Y")
    formatted_event_date = format_day_suffix(event_date)

    # Build prompt for Gemini
    prompt = f"""
Write ONLY the main body paragraph for a formal permission letter. Do not include any headers, footers, greetings, or signatures.

Details:
- Event: {event_name}
- Date: {formatted_event_date} at {event_time}
- Venue: {venue}
- Purpose: {purpose}
- Organization: PICT ACM Student Chapter (PASC)

Write a single paragraph explaining the event and its purpose. Be formal and polite.

Example format:
We, the members of the PICT ACM Student Chapter (PASC), are organizing a session titled "{event_name}" on {formatted_event_date} at {event_time}. This session aims to {purpose}.

Return ONLY the paragraph content, no other text.
"""

    # HTML Template (PDF clone style)
    html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Permission Letter</title>
    <style>
        body {
            font-family: "Times New Roman", serif;
            line-height: 1.6;
            margin: 40px 60px;
            color: #000;
        }
        .header-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        .header-table td {
            text-align: center;
            vertical-align: top;
            padding: 0 10px;
        }
        .header-table td:first-child {
            text-align: left;
        }
        .header-table td:last-child {
            text-align: right;
        }
        .header-table img {
            height: 80px;
        }
        .header-text {
            font-size: 0.8em;
            line-height: 1.2;
        }
        .address-date {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 20px;
        }
        .right-align {
            text-align: right;
        }
        .subject {
            font-weight: bold;
            text-decoration: underline;
            margin: 20px 0;
        }
        .body-text {
            text-align: justify;
        }
        .signatures {
            display: flex;
            justify-content: space-between;
            margin-top: 40px;
        }
        .signature-section {
            text-align: left;
            margin-top: 50px;
            display: flex;
            justify-content: space-between;
        }
        .signature-block {
            line-height: 1.2;
        }
        .contact-info {
            margin-top: 60px;
            border-top: 1px solid #000;
            padding-top: 10px;
            font-size: 0.9em;
            text-align: center;
        }
    </style>
</head>
<body>
    <table class="header-table">
        <tr>
            <td>
                <img src="data:image/png;base64,{{ pasc_logo }}" alt="PASC Logo">
            </td>
            <td>
                <img src="data:image/png;base64,{{ pict_logo }}" alt="PICT Logo">
            </td>
            <td>
                <img src="data:image/png;base64,{{ acm_logo }}" alt="ACM Logo">
            </td>
        </tr>
    </table>

    <div class="address-date">
      <div>
        <p>To,</p>
        <p>{{ authority }},</p>
        <p>{{ organisation }}.</p>
      </div>
      <div class="right-align">
        <p>Date: {{ current_date }}</p>
      </div>
    </div>

    <p><strong>Subject: Request for Permission to Use {{ venue }} for PASC Session - “{{ event_name }}”</strong></p>

    <p>Respected Sir,</p>
    <p class="body-text">{{ content }}</p>
    <p>We kindly request your permission to conduct the session in the {{ venue }}. We assure you that all resources provided will be used responsibly and the venue will be maintained properly.</p>

    <p>Thanking you in anticipation,<br>Yours Sincerely,</p>

    <table style="width: 100%; border-collapse: collapse;">
        <tr>
            <td style="width: 50%; text-align: left; vertical-align: top;">
                <p>{{ your_name }}</p>
                <p>{{ your_role }}</p>
            </td>
            <td style="width: 50%; text-align: right; vertical-align: top;">
                <p>{{ counselor_name }}</p>
                <p>{{ counselor_role }}</p>
            </td>
        </tr>
    </table>
    
    <div class="contact-info">
        <p>
            PICT ACM Student Chapter<br>
            Pune Institute of Computer Technology,<br>
            Dhankawadi, Pune, Maharashtra-411043<br>
            Website: pict.acm.org | Email: {{ email }}
        </p>
    </div>
</body>
</html>
'''

    # Generate content with Gemini
    letter_content = generate_with_gemini(prompt)

    if not letter_content:
        st.error("❌ Failed to generate letter content. Please try again.")
    else:
        # Render Jinja2 template
        template = Template(html_template)
        
        rendered_html = template.render(
            pict_logo=pict_logo_base64,
            acm_logo=acm_logo_base64,
            pasc_logo=pasc_logo_base64,
            current_date=formatted_date,
            authority=authority,
            organisation=organisation,
            event_name=event_name,
            content=letter_content,
            your_name=your_name,
            your_role=your_role,
            counselor_name=counselor_name,
            counselor_role=counselor_role,
            email=email
        )

        # Convert to PDF
        pdf_result = convert_html_to_pdf(rendered_html)
        
        if pdf_result:
            st.success("✅ Permission letter generated successfully!")
            st.download_button(
                label="Download Permission Letter",
                data=pdf_result.getvalue(),
                file_name=f"permission_letter_{formatted_event_date}.pdf",
                mime="application/pdf"
            )
        else:
            st.error("❌ Failed to convert letter to PDF.")
