import os
import sys
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv

# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ============================================================
# IMPORT SHARED UTILITIES
# ============================================================

from utils.document_formatter import format_docx, format_pdf


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv(PROJECT_ROOT / ".env")

API_URL = os.getenv(
    "LEGALEASE_API_URL",
    "http://127.0.0.1:8000/generate"
)


# ============================================================
# STREAMLIT CONFIG
# ============================================================

st.set_page_config(
    page_title="LegalEase TN",
    page_icon="⚖️",
    layout="centered",
)


# ============================================================
# HEADER
# ============================================================

st.title("⚖️ LegalEase TN")
st.caption("AI-Powered Legal Document Generator")

st.subheader("Document Details")


# ============================================================
# INPUTS
# ============================================================

document_type = st.selectbox(
    "Document Type",
    [
        "Employment Contract",
        "Lease Agreement",
        "Non-Disclosure Agreement (NDA)",
        "General Agreement",
    ],
)

parties = st.text_area(
    "Parties",
    placeholder="Example: ABC Company and John Doe",
    height=90,
)

terms = st.text_area(
    "Terms",
    placeholder=(
        "Enter terms separated by semicolons.\n"
        "Example: Salary: ₹30000 per month; "
        "Working hours: 9 AM to 6 PM; "
        "Probation: 3 months"
    ),
    height=140,
)

effective_date = st.date_input("Effective Date")


# ============================================================
# GENERATE DOCUMENT
# ============================================================

if st.button(
    "Generate Document",
    type="primary",
    use_container_width=True,
):

    if not parties.strip():
        st.error("Please enter the parties.")
        st.stop()

    if not terms.strip():
        st.error("Please enter the terms.")
        st.stop()

    payload = {
        "document_type": document_type,
        "parties": parties.strip(),
        "terms": terms.strip(),
        "effective_date": effective_date.strftime("%Y-%m-%d"),
    }

    try:

        response = requests.post(
            API_URL,
            json=payload,
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

        st.session_state["generated_content"] = data["content"]
        st.session_state["generated_type"] = data["document_type"]

        st.success("Document generated successfully.")

    except requests.RequestException as exc:

        detail = ""

        if getattr(exc, "response", None) is not None:

            try:
                error_data = exc.response.json()
                detail = error_data.get("detail", "")

            except Exception:
                detail = exc.response.text

        st.error(
            f"Document generation failed: "
            f"{detail or str(exc)}"
        )


# ============================================================
# DOCUMENT PREVIEW + EDIT
# ============================================================

if "generated_content" in st.session_state:

    st.subheader("Document Preview")

    edited = st.text_area(
        "Edit Document",
        value=st.session_state["generated_content"],
        height=650,
    )

    st.session_state["generated_content"] = edited


    # ========================================================
    # DOCUMENT FORMATTING
    # ========================================================

    try:

        docx_data = format_docx(
            edited,
            document_type=st.session_state["generated_type"],
        )

        pdf_data = format_pdf(
            edited,
            document_type=st.session_state["generated_type"],
        )

    except Exception as exc:

        st.error(
            f"Document formatting failed: {exc}"
        )

        st.stop()


    # ========================================================
    # DOWNLOAD BUTTONS
    # ========================================================

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            "Download DOCX",
            data=docx_data,
            file_name="LegalEase_TN_Document.docx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            use_container_width=True,
        )

    with col2:

        st.download_button(
            "Download PDF",
            data=pdf_data,
            file_name="LegalEase_TN_Document.pdf",
            mime="application/pdf",
            use_container_width=True,
        )