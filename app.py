
import streamlit as st
from src.agents.agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain,
)

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ResearchAI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- Main App ---------- */

    .stApp {
        background-color: #0e1117;
    }

    /* ---------- Header ---------- */

    .main-header {
        padding: 1rem 0 0.5rem 0;
    }

    .main-title {
        font-size: 2.7rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
        color: #ffffff;
    }

    .subtitle {
        color: #9ca3af;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }

    /* ---------- Agent Cards ---------- */

    .agent-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 14px;
        padding: 18px;
        text-align: center;
        min-height: 130px;
    }

    .agent-icon {
        font-size: 2rem;
        margin-bottom: 5px;
    }

    .agent-title {
        font-weight: 700;
        color: #ffffff;
        font-size: 1rem;
    }

    .agent-description {
        color: #8b949e;
        font-size: 0.82rem;
        margin-top: 5px;
    }

    /* ---------- Section Headers ---------- */

    .section-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #ffffff;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
    }

    /* ---------- Result Cards ---------- */

    .result-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }

    /* ---------- Status ---------- */

    .status-running {
        color: #58a6ff;
        font-weight: 600;
    }

    .status-success {
        color: #3fb950;
        font-weight: 600;
    }

    /* ---------- Sidebar ---------- */

    section[data-testid="stSidebar"] {
        background-color: #0b0f14;
        border-right: 1px solid #21262d;
    }

    /* ---------- Buttons ---------- */

    .stButton > button {
        width: 100%;
        border-radius: 9px;
        font-weight: 600;
        padding: 0.65rem;
    }

    /* ---------- Text Area ---------- */

    textarea {
        border-radius: 10px !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🔬 ResearchAI")

    st.caption("Multi-Agent Research Assistant")

    st.divider()

    st.markdown("### ⚙️ Research Pipeline")

    st.markdown(
        """
        **🔎 Search Agent**

        Finds recent and reliable sources.

        **📖 Reader Agent**

        Scrapes the most relevant resource.

        **✍️ Writer Agent**

        Generates the research report.

        **🧐 Critic Agent**

        Reviews the final report.
        """
    )

    st.divider()

    st.markdown("### 💡 Tips")

    st.info(
        """
        For better results, provide a specific
        research topic.

        Example:

        `Latest advancements in RAG systems`
        """
    )

# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="main-header">
        <div class="main-title">🔬 ResearchAI</div>
        <div class="subtitle">
            Multi-Agent Research Assistant powered by LangChain
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# RESEARCH INPUT
# ============================================================

st.markdown(
    '<div class="section-title">🎯 What would you like to research?</div>',
    unsafe_allow_html=True,
)

topic = st.text_area(
    "Research Topic",
    placeholder=(
        "Example: Latest developments in Agentic AI and "
        "multi-agent systems"
    ),
    height=100,
    label_visibility="collapsed",
)

start_research = st.button(
    "🚀 Start Research",
    type="primary",
    use_container_width=True,
)

# ============================================================
# PIPELINE VISUALIZATION
# ============================================================

st.markdown(
    '<div class="section-title">⚡ Research Pipeline</div>',
    unsafe_allow_html=True,
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div class="agent-card">
            <div class="agent-icon">🔎</div>
            <div class="agent-title">Search Agent</div>
            <div class="agent-description">
                Finds reliable sources
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="agent-card">
            <div class="agent-icon">📖</div>
            <div class="agent-title">Reader Agent</div>
            <div class="agent-description">
                Scrapes useful content
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="agent-card">
            <div class="agent-icon">✍️</div>
            <div class="agent-title">Writer Agent</div>
            <div class="agent-description">
                Creates research report
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        """
        <div class="agent-card">
            <div class="agent-icon">🧐</div>
            <div class="agent-title">Critic Agent</div>
            <div class="agent-description">
                Reviews report quality
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# RUN RESEARCH
# ============================================================

if start_research:

    if not topic.strip():
        st.warning("⚠️ Please enter a research topic first.")

    else:

        st.divider()

        st.markdown(
            '<div class="section-title">🔄 Research in Progress</div>',
            unsafe_allow_html=True,
        )

        # ----------------------------------------------------
        # STEP 1 — SEARCH
        # ----------------------------------------------------

        with st.status(
            "🔎 Search Agent is researching...",
            expanded=True,
        ) as search_status:

            st.write(
                "Searching for recent, reliable and detailed information..."
            )

            try:

                search_agent = build_search_agent()

                search_results = search_agent.invoke(
                    {
                        "messages": [
                            (
                                "user",
                                f"Find recent, reliable and detailed "
                                f"information about: {topic}",
                            )
                        ]
                    }
                )

                search_content = search_results["messages"][-1].content

                search_status.update(
                    label="✅ Search Agent completed",
                    state="complete",
                )

            except Exception as e:

                search_status.update(
                    label="❌ Search Agent failed",
                    state="error",
                )

                st.error(f"Search Agent Error: {e}")
                st.stop()

        # ----------------------------------------------------
        # STEP 2 — READER
        # ----------------------------------------------------

        with st.status(
            "📖 Reader Agent is scraping resources...",
            expanded=True,
        ) as reader_status:

            st.write(
                "Analyzing search results and selecting the "
                "most relevant resource..."
            )

            try:

                reader_agent = build_reader_agent()

                reader_result = reader_agent.invoke(
                    {
                        "messages": [
                            (
                                "user",
                                f"""
Based on the following search results about '{topic}',
pick the most relevant URL and scrape it for deeper content.

Search Results:

{search_content}
""",
                            )
                        ]
                    }
                )

                scraped_content = reader_result[
                    "messages"
                ][-1].content

                reader_status.update(
                    label="✅ Reader Agent completed",
                    state="complete",
                )

            except Exception as e:

                reader_status.update(
                    label="❌ Reader Agent failed",
                    state="error",
                )

                st.error(f"Reader Agent Error: {e}")
                st.stop()

        # ----------------------------------------------------
        # STEP 3 — WRITER
        # ----------------------------------------------------

        with st.status(
            "✍️ Writer Agent is creating the report...",
            expanded=True,
        ) as writer_status:

            st.write(
                "Combining search results and scraped content..."
            )

            try:

                research_combined = (
                    f"SEARCH RESULTS:\n"
                    f"{search_content}\n\n"
                    f"DETAILED SCRAPED CONTENT:\n"
                    f"{scraped_content}"
                )

                report = writer_chain.invoke(
                    {
                        "topic": topic,
                        "research": research_combined,
                    }
                )

                writer_status.update(
                    label="✅ Writer completed",
                    state="complete",
                )

            except Exception as e:

                writer_status.update(
                    label="❌ Writer failed",
                    state="error",
                )

                st.error(f"Writer Error: {e}")
                st.stop()

        # ----------------------------------------------------
        # STEP 4 — CRITIC
        # ----------------------------------------------------

        with st.status(
            "🧐 Critic Agent is reviewing...",
            expanded=True,
        ) as critic_status:

            st.write(
                "Evaluating the generated report for quality "
                "and accuracy..."
            )

            try:

                feedback = critic_chain.invoke(
                    {
                        "report": report,
                    }
                )

                critic_status.update(
                    label="✅ Critic completed",
                    state="complete",
                )

            except Exception as e:

                critic_status.update(
                    label="❌ Critic failed",
                    state="error",
                )

                st.error(f"Critic Error: {e}")
                st.stop()

        # ====================================================
        # RESULTS
        # ====================================================

        st.divider()

        st.markdown(
            '<div class="section-title">📊 Research Results</div>',
            unsafe_allow_html=True,
        )

        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "🔎 Search Results",
                "📖 Scraped Content",
                "📄 Final Report",
                "🧐 Critic Review",
            ]
        )

        # ----------------------------------------------------
        # SEARCH RESULTS
        # ----------------------------------------------------

        with tab1:

            st.markdown("### 🔎 Search Agent Results")

            st.markdown(
                """
                The Search Agent found the following
                information and resources:
                """
            )

            st.markdown(search_content)

        # ----------------------------------------------------
        # SCRAPED CONTENT
        # ----------------------------------------------------

        with tab2:

            st.markdown("### 📖 Deep Research")

            st.markdown(
                """
                The Reader Agent selected and scraped
                the most relevant resource.
                """
            )

            st.markdown(scraped_content)

        # ----------------------------------------------------
        # FINAL REPORT
        # ----------------------------------------------------

        with tab3:

            st.markdown("### 📄 Research Report")

            st.markdown(
                f"**Research Topic:** {topic}"
            )

            st.divider()

            st.markdown(report)

            st.download_button(
                label="⬇️ Download Report",
                data=report,
                file_name="research_report.md",
                mime="text/markdown",
                use_container_width=True,
            )

        # ----------------------------------------------------
        # CRITIC
        # ----------------------------------------------------

        with tab4:

            st.markdown("### 🧐 Critic Review")

            st.markdown(
                """
                The Critic Agent reviewed the generated
                research report.
                """
            )

            st.markdown(feedback)

        # ====================================================
        # SUCCESS
        # ====================================================

        st.success(
            "🎉 Research pipeline completed successfully!"
        )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Built with LangChain • Streamlit • Multi-Agent Architecture"
)

