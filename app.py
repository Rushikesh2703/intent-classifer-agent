import streamlit as st
from agent import classify_intent
from analyzer import analyze_query

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Intent Classifier",
    page_icon="🧠",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
    <style>
        .main-title {
            font-size: 36px;
            font-weight: 700;
            text-align: center;
            margin-bottom: 20px;
        }
        .card {
            padding: 20px;
            border-radius: 12px;
            background-color: #111827;
            border: 1px solid #1f2937;
            margin-top: 20px;
        }
        .intent-text {
            font-size: 22px;
            font-weight: 600;
        }
        .confidence-text {
            font-size: 16px;
            margin-top: 10px;
        }
        .section-header {
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            margin-bottom: 4px;
            padding: 4px 10px;
            border-radius: 4px;
            display: inline-block;
        }
        .dim-value {
            font-size: 20px;
            font-weight: 700;
            margin: 4px 0 8px 0;
        }
        .dim-desc {
            font-size: 13px;
            color: #9ca3af;
            margin-bottom: 8px;
        }
        .tag {
            display: inline-block;
            padding: 2px 10px;
            border-radius: 999px;
            font-size: 11px;
            font-weight: 600;
            margin-right: 4px;
            margin-top: 4px;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown('<div class="main-title">🧠 AI Intent Classifier</div>', unsafe_allow_html=True)

# ---------------- TABS ----------------
tab1, tab2 = st.tabs(["Simple Classifier", "Multi-Dimension Analysis"])


# ════════════════════════════════════════
# TAB 1 — Original simple classifier
# ════════════════════════════════════════
with tab1:
    st.write("Enter a message below")

    user_input = st.text_area("Type Below", height=120, key="simple_input")

    if st.button("Classify Intent", key="simple_btn"):
        if user_input.strip() == "":
            st.warning("Please enter a message.")
        else:
            try:
                result = classify_intent(user_input)

                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="intent-text">Intent: {result.intent}</div>',
                    unsafe_allow_html=True
                )
                st.markdown(
                    f'<div class="confidence-text">Confidence: {round(result.confidence * 100, 2)}%</div>',
                    unsafe_allow_html=True
                )
                st.progress(result.confidence)
                st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error: {str(e)}")


# ════════════════════════════════════════
# TAB 2 — Multi-dimension analysis
# ════════════════════════════════════════
with tab2:
    st.write("Analyze your query across 5 dimensions: Intent · Category · Features · Relationship · Product")

    user_input2 = st.text_area("Type your product query", height=120, key="multi_input")

    if st.button("Analyze Query", key="multi_btn"):
        if user_input2.strip() == "":
            st.warning("Please enter a message.")
        else:
            with st.spinner("Analyzing across all dimensions..."):
                try:
                    result = analyze_query(user_input2)

                    st.markdown("---")

                    # ── 1. USER INTENT ──────────────────────────────
                    st.markdown(
                        '<span class="section-header" style="background:#0e2a3a;color:#00d4ff;">🔵 USER INTENT</span>',
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f'<div class="dim-value" style="color:#00d4ff;">{result.user_intent.label}</div>',
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f'<div class="dim-desc">{result.user_intent.description}</div>',
                        unsafe_allow_html=True
                    )
                    st.progress(result.user_intent.confidence,
                                text=f"Confidence: {round(result.user_intent.confidence * 100)}%")

                    st.markdown("---")

                    # ── 2. CATEGORY ─────────────────────────────────
                    st.markdown(
                        '<span class="section-header" style="background:#1e1040;color:#a78bfa;">🟣 CATEGORY</span>',
                        unsafe_allow_html=True
                    )
                    cat_text = result.category.primary
                    if result.category.secondary:
                        cat_text += f" &nbsp;·&nbsp; <span style='color:#6b7280;font-size:14px;'>also: {result.category.secondary}</span>"
                    st.markdown(
                        f'<div class="dim-value" style="color:#a78bfa;">{cat_text}</div>',
                        unsafe_allow_html=True
                    )
                    st.progress(result.category.confidence,
                                text=f"Confidence: {round(result.category.confidence * 100)}%")

                    st.markdown("---")

                    # ── 3. FEATURE KNOWLEDGE ────────────────────────
                    st.markdown(
                        '<span class="section-header" style="background:#0a2a1e;color:#34d399;">🟢 FEATURE KNOWLEDGE</span>',
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f'<div class="dim-value" style="color:#34d399;">{result.feature_knowledge.depth} Knowledge</div>',
                        unsafe_allow_html=True
                    )
                    tags_html = " ".join([
                        f'<span class="tag" style="background:#0a2a1e;color:#34d399;border:1px solid #34d39944;">{t}</span>'
                        for t in result.feature_knowledge.topics
                    ])
                    st.markdown(tags_html, unsafe_allow_html=True)
                    st.progress(result.feature_knowledge.confidence,
                                text=f"Confidence: {round(result.feature_knowledge.confidence * 100)}%")

                    st.markdown("---")

                    # ── 4. RELATIONSHIP ─────────────────────────────
                    st.markdown(
                        '<span class="section-header" style="background:#2a1e00;color:#fbbf24;">🟡 RELATIONSHIP</span>',
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f'<div class="dim-value" style="color:#fbbf24;">{result.relationship.type}</div>',
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f'<div class="dim-desc">{result.relationship.connection}</div>',
                        unsafe_allow_html=True
                    )
                    if result.relationship.entities:
                        entity_html = " ".join([
                            f'<span class="tag" style="background:#2a1e00;color:#fbbf24;border:1px solid #fbbf2444;">{e}</span>'
                            for e in result.relationship.entities
                        ])
                        st.markdown(entity_html, unsafe_allow_html=True)

                    st.markdown("---")

                    # ── 5. PRODUCT ──────────────────────────────────
                    st.markdown(
                        '<span class="section-header" style="background:#2a0f1a;color:#fb7185;">🔴 PRODUCT</span>',
                        unsafe_allow_html=True
                    )
                    product_name = result.product.identified or "Not Identified"
                    st.markdown(
                        f'<div class="dim-value" style="color:#fb7185;">{product_name} &nbsp;<span style="font-size:13px;color:#6b7280;">· {result.product.domain}</span></div>',
                        unsafe_allow_html=True
                    )
                    if result.product.tags:
                        tag_html = " ".join([
                            f'<span class="tag" style="background:#1a1a2a;color:#94a3b8;border:1px solid #94a3b844;">{t}</span>'
                            for t in result.product.tags
                        ])
                        st.markdown(tag_html, unsafe_allow_html=True)
                    st.progress(result.product.confidence,
                                text=f"Confidence: {round(result.product.confidence * 100)}%")

                except Exception as e:
                    st.error(f"Error: {str(e)}")