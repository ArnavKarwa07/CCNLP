import io
from typing import Dict

import evaluate
import pandas as pd
import streamlit as st
from transformers import pipeline


st.set_page_config(page_title="Assignment 5 Summarization UI", layout="wide")


@st.cache_resource
def load_summarizer(model_name: str):
    return pipeline("summarization", model=model_name)


@st.cache_resource
def load_metrics():
    rouge_metric = evaluate.load("rouge")
    bleu_metric = evaluate.load("bleu")
    return rouge_metric, bleu_metric


def read_uploaded_text(uploaded_file) -> str:
    suffix = uploaded_file.name.lower().split(".")[-1]

    if suffix == "txt":
        return uploaded_file.read().decode("utf-8", errors="ignore")

    if suffix == "pdf":
        try:
            from pypdf import PdfReader
        except ImportError:
            raise RuntimeError("PDF support requires pypdf. Install with: pip install pypdf")

        reader = PdfReader(io.BytesIO(uploaded_file.read()))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages)

    if suffix == "docx":
        try:
            import docx
        except ImportError:
            raise RuntimeError("DOCX support requires python-docx. Install with: pip install python-docx")

        document = docx.Document(io.BytesIO(uploaded_file.read()))
        return "\n".join(paragraph.text for paragraph in document.paragraphs)

    raise RuntimeError("Unsupported file type. Please upload .txt, .pdf, or .docx")


def build_reference_summary(text: str) -> str:
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    if not sentences:
        return text[:1000]

    sampled = sentences[::2]
    reference = ". ".join(sampled)
    if reference and not reference.endswith("."):
        reference += "."
    return reference


def evaluate_summary(summary: str, reference: str, rouge_metric, bleu_metric) -> Dict[str, float]:
    rouge_scores = rouge_metric.compute(predictions=[summary], references=[reference])
    bleu_scores = bleu_metric.compute(predictions=[summary], references=[[reference]])

    return {
        "ROUGE-1": round(float(rouge_scores["rouge1"]), 4),
        "ROUGE-L": round(float(rouge_scores["rougeL"]), 4),
        "BLEU": round(float(bleu_scores["bleu"]), 4),
    }


def truncate_for_model(text: str, tokenizer, max_tokens: int) -> str:
    token_ids = tokenizer.encode(text, truncation=True, max_length=max_tokens)
    return tokenizer.decode(token_ids, skip_special_tokens=True)


def model_token_limit(tokenizer) -> int:
    limit = getattr(tokenizer, "model_max_length", 1024)
    # Some tokenizers expose very large sentinels; cap to a practical BART/T5-safe limit.
    if not isinstance(limit, int) or limit > 100000:
        return 1024
    return max(256, limit)


def main():
    st.title("Assignment 5: File Summarization + Evaluation")
    st.write(
        "Upload a file, generate two summaries (descriptive and informative), "
        "and compare their ROUGE/BLEU performance."
    )

    with st.sidebar:
        st.header("Model Settings")
        model_name = st.selectbox(
            "Summarization model",
            [
                "sshleifer/distilbart-cnn-12-6",
                "facebook/bart-large-cnn",
                "sshleifer/distilbart-xsum-12-6",
            ],
            index=0,
        )
        max_input_tokens = st.slider("Max input tokens", min_value=256, max_value=1024, value=900, step=64)

    uploaded_file = st.file_uploader("Upload document", type=["txt", "pdf", "docx"])

    if not uploaded_file:
        st.info("Upload a file to begin.")
        return

    try:
        text = read_uploaded_text(uploaded_file)
    except RuntimeError as exc:
        st.error(str(exc))
        return

    text = text.strip()
    if not text:
        st.error("The uploaded file appears empty.")
        return

    st.subheader("Input Overview")
    st.write(f"Characters: {len(text):,}")

    with st.spinner("Loading model and generating summaries..."):
        summarizer = load_summarizer(model_name)
        rouge_metric, bleu_metric = load_metrics()
        tokenizer = summarizer.tokenizer

        token_limit = model_token_limit(tokenizer)
        safe_user_limit = min(max_input_tokens, token_limit - 8)

        # Keep room for the descriptive prompt prefix to avoid encoder index overflow.
        descriptive_prefix = "This text is about: "
        prefix_tokens = len(tokenizer.encode(descriptive_prefix, add_special_tokens=False))
        descriptive_input_limit = max(128, safe_user_limit - prefix_tokens - 8)

        informative_input = truncate_for_model(text, tokenizer, safe_user_limit)
        descriptive_input = truncate_for_model(text, tokenizer, descriptive_input_limit)

        descriptive_raw = summarizer(
            f"{descriptive_prefix}{descriptive_input}",
            truncation=True,
            max_new_tokens=35,
            min_length=10,
            do_sample=False,
        )[0]["summary_text"]
        descriptive_summary = f"This document provides an overview of {descriptive_raw.strip()}."

        informative_summary = summarizer(
            informative_input,
            truncation=True,
            max_new_tokens=220,
            min_length=60,
            do_sample=False,
        )[0]["summary_text"]

        reference_summary = build_reference_summary(informative_input)

        descriptive_scores = evaluate_summary(descriptive_summary, reference_summary, rouge_metric, bleu_metric)
        informative_scores = evaluate_summary(informative_summary, reference_summary, rouge_metric, bleu_metric)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Summary 1: Descriptive")
        st.write(descriptive_summary)

    with col2:
        st.subheader("Summary 2: Informative")
        st.write(informative_summary)

    st.subheader("Reference Summary (for automatic evaluation)")
    st.caption("Proxy reference is built by selecting alternate sentences from the truncated input text.")
    st.write(reference_summary)

    scores_df = pd.DataFrame(
        [
            {"Summary Type": "Descriptive", **descriptive_scores},
            {"Summary Type": "Informative", **informative_scores},
        ]
    )

    st.subheader("Performance Evaluation")
    st.dataframe(scores_df, use_container_width=True)

    st.bar_chart(scores_df.set_index("Summary Type")[["ROUGE-1", "ROUGE-L", "BLEU"]])


if __name__ == "__main__":
    main()