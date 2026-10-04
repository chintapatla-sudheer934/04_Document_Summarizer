import streamlit as st
import fitz
from transformers import pipeline

st.title("PDF and Text Summarizer")
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
uploaded = st.file_uploader("Upload PDF or TXT", type=["pdf","txt"])
if uploaded:
    if uploaded.name.lower().endswith(".pdf"):
        doc = fitz.open(stream=uploaded.read(), filetype="pdf")
        text = "\\n".join(page.get_text() for page in doc)
    else:
        text = uploaded.read().decode("utf-8", errors="ignore")
    st.text_area("Extracted text", text[:5000], height=180)
    if st.button("Summarize"):
        if not text.strip():
            st.warning("No readable text found.")
        else:
            # Split long text into manageable chunks.
            chunks = [text[i:i+2500] for i in range(0, min(len(text),15000),2500)]
            summaries = [load_summarizer()(c, max_length=120, min_length=25, do_sample=False)[0]["summary_text"] for c in chunks if len(c.split()) > 30]
            st.subheader("Summary")
            st.write(" ".join(summaries) if summaries else "Document is too short to summarize.")
