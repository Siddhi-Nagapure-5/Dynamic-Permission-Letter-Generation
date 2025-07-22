# PASC Event Management Project  
## 📄 Dynamic Permission Letter Generator

This feature—implemented by Siddhi Nagapure, Sarang Rao, and Jay Kotwal—is part of the larger PASC Event Management project. It enables organizers to generate official venue permission letters matching the exact PASC letterhead format, complete with dynamic details, logo, alignment, and signature blocks.

---

## 🚀 Overview

- **Automates official letter creation** for PASC events (e.g., request to use auditorium).
- **Customizes every detail:** authority, event, date, purpose, signatories.
- **Outputs**: professional PDF matching [this sample](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/45281319/2062711e-766b-4436-bf18-997cc7686bb7/Auditorium-permmission-internship.pdf)
- **No manual editing:** All formatting, font, and branding are preserved.

---

## 🖼️ Demo

<img width="1916" height="1075" alt="Screenshot 2025-07-22 120535" src="https://github.com/user-attachments/assets/43c73eee-9bba-46a6-93b4-84266dafb00e" />


---

## 💡 How It Works

1. Fill a user-friendly web form (date, authority, event name, etc.).
2. The app uses an HTML template and logo to create a visually identical permission letter.
3. Preview the letter and download the ready-to-sign PDF.

---

## 🎯 Features

- Streamlit web app with instant PDF downloads
- Dynamic letterhead (logo and footer)
- Perfect alignment for signature blocks and official fields
- Inputs for dual signatories (Secretary & Counselor)
- Matches PASC/PICT official letter requirements

---

## ⚙️ Requirements

- Python 3.8+
- [streamlit](https://streamlit.io/)
- [jinja2](https://palletsprojects.com/p/jinja/)
- [xhtml2pdf](https://xhtml2pdf.readthedocs.io/en/latest/)

---

## 🏁 Getting Started

1. **Clone this repository**
    ```
    git clone https://github.com/your-org/pasc-event-management.git
    cd pasc-event-management/permission-letter
    ```
2. **Install dependencies**
    ```
    pip install streamlit jinja2 xhtml2pdf
    ```
3. **Add your logo**
   - Place the official PASC logo as `logo.png` in your project directory.

4. **Run the app**
    ```
    streamlit run app.py
    ```

5. **Open your browser** at `http://localhost:8501` and use the app.

---

## ✍️ Inputs

- Authority Name
- Organisation Name
- Event Title
- Event Date & Time
- Purpose of Event
- Your Name/Role (e.g. Secretary, PASC)
- Counselor Name/Role

---

## 🗂️ Output

- A print-ready PDF letter  
- Precisely matches the official sample: [Sample PDF](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/45281319/2062711e-766b-4436-bf18-997cc7686bb7/Auditorium-permmission-internship.pdf)

---

## 👥 Team

- Siddhi Nagapure
- Sarang Rao
- Jay Kotwal

---

## 📫 Contact

For questions or suggestions
