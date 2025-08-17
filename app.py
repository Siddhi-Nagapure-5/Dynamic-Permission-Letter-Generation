# Dynamic Permission Letter Generator
# Fixed: Gemini prompt, logo alignment, and template rendering issues 

import streamlit as st
from datetime import datetime
from xhtml2pdf import pisa
from io import BytesIO
from jinja2 import Template
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel('gemini-2.0-flash')

# Logo placeholders
left_logo = "images.png"
middle_logo = "download.png"
right_logo = "download (1).png"

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
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .header img {
            height: 80px;
        }
        .date {
            text-align: right;
            margin: 20px 0;
        }
        .subject {
            font-weight: bold;
            text-decoration: underline;
            margin: 20px 0;
        }
        .body-text {
            text-align: justify;
        }
        .closing {
            margin-top: 30px;
        }
        .signature-container {
            display: flex;
            justify-content: space-between;
            margin-top: 50px;
        }
        .signature-left, .signature-right {
            text-align: left;
        }
        .signature-left p, .signature-right p {
            margin: 0;
        }
        .footer {
            margin-top: 60px;
            border-top: 1px solid #000;
            padding-top: 10px;
            font-size: 0.9em;
            text-align: center;
        }
        /* Custom styles for the borders */
        .border-line {
            border-top: 1px solid #000;
            margin: 20px 0;
        }
    </style>
</head>
<body>
        <div class="header">
        <img src="{{ left_logo | default('/images.png') }}" alt="PICT Logo">
        <img src="{{ middle_logo | default('/download (1).png') }}" alt="PASC Logo">
        <img src="{{ right_logo | default('/download.png') }}" alt="ACM Logo">
    </div>

        <div class="date">
        Date: {{ current_date | default("17th August 2025") }}
    </div>

        <p>
        To,<br>
        {{ authority | default("The Principal") }},<br>
        {{ organisation | default("PICT, Pune") }}.
    </p>

        <p class="subject">
        Subject: Request for Permission to Use {{venue}} for PASC Session - 
        “{{ event_name | default("Tech Talk on AI Innovations") }}”
    </p>

        <div class="body-text">
        <p>Respected Sir,</p>
        <p>
            {{ content | default("We, the members of the PICT ACM Student Chapter (PASC), 
            would like to request your kind permission to use the auditorium 
            for conducting our upcoming session.") }}
        </p>
        <p>
            {{ request | default("The event is scheduled on 20th August 2025 from 10:00 AM to 1:00 PM. 
            We kindly seek your approval to proceed with the arrangements.") }}
        </p>
        <p>
            Thanking you in anticipation,<br>
            Yours sincerely,
        </p>
    </div>

        <table style="width: 100%; border-collapse: collapse; margin-top: 50px;">
    <tr>
        <td style="width: 50%; text-align: left; vertical-align: top;">
            <p>{{ your_name | default("Sarang Rao") }}</p>
            <p>{{ your_role | default("Chairperson, PASC") }}</p>
        </td>
        <td style="width: 50%; text-align: right; vertical-align: top;">
            <p>{{ counselor_name | default("Prof. ABC XYZ") }}</p>
            <p>{{ counselor_role | default("Faculty Counselor, PASC") }}</p>
        </td>
    </tr>
</table>
    
        <div class="border-line"></div>

        <div class="footer">
        <p>
            PICT ACM Student Chapter<br>
            Pune Institute of Computer Technology,<br>
            Dhankawadi, Pune, Maharashtra-411043<br>
            Website: pict.acm.org | Email: {{ email | default("pasc@pict.edu") }}
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
        # Generate dynamic request paragraph based on venue
        request_text = f"We kindly request your permission to use the {venue} for this event. We assure you that we will maintain the decorum and cleanliness of the {venue.lower()} and follow all guidelines."
        
        rendered_html = template.render(
            left_logo=left_logo,
            middle_logo=middle_logo,
            right_logo=right_logo,
            current_date=formatted_date,
            authority=authority,
            organisation=organisation,
            event_name=event_name,
            content=letter_content,
            request=request_text,
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
