import os
import streamlit as st

from chatbot import generate_response
from rag import extract_pdf_text

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="DecodeGPT",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------------------------
# CREATE UPLOADS FOLDER
# --------------------------------------------------

os.makedirs(
    "uploads",
    exist_ok=True
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("🤖 DecodeGPT")

    st.markdown(
        "AI Knowledge Assistant"
    )

    if st.button("🆕 New Chat"):

        st.session_state.messages = []
        st.session_state.pdf_text = ""

        st.rerun()

    st.divider()

    st.subheader("📄 Upload PDF")

    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type=["pdf"]
    )

# --------------------------------------------------
# PDF PROCESSING
# --------------------------------------------------

if uploaded_file:

    pdf_path = os.path.join(
        "uploads",
        uploaded_file.name
    )

    with open(
        pdf_path,
        "wb"
    ) as f:

        f.write(
            uploaded_file.getbuffer()
        )

    st.sidebar.success(
        "PDF Uploaded Successfully"
    )

    try:

        pdf_text = extract_pdf_text(
            pdf_path
        )

        st.session_state.pdf_text = pdf_text

        st.sidebar.write(
            f"Characters: {len(pdf_text)}"
        )

        with st.expander(
            "📖 PDF Preview"
        ):

            st.write(
                pdf_text[:2000]
            )

    except Exception as e:

        st.error(
            f"Error reading PDF: {e}"
        )

# --------------------------------------------------
# MAIN PAGE
# --------------------------------------------------

st.title("🤖 DecodeGPT")

st.caption(
    "Personal AI Assistant with Memory & Document Intelligence"
)

# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

prompt = st.chat_input(
    "Ask anything..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner(
            "Thinking..."
        ):

            response = generate_response(
                prompt,
                st.session_state.get(
                    "pdf_text",
                    ""
                )
            )

            st.markdown(
                response
            )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )