import streamlit as st
import random
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os
from dotenv import load_dotenv
from zhipuai import ZhipuAI

# ---------- Load environment ----------
load_dotenv()
API_KEY = os.getenv("ZHIPUAI_API_KEY")
if not API_KEY:
    st.error("ZHIPUAI_API_KEY not found. Please set it in .env file.")
    st.stop()

client = ZhipuAI(api_key=API_KEY)

# ---------- Dream style prompts (English) ----------
DREAM_STYLES = {
    "Sci-Fi Dream": "You are a dream generator. The user wants you to describe a sci-fi dream involving spaceships, aliens, and futuristic cities. Generate a surreal dream description in English.",
    "Nightmare": "You are a dream generator. The user wants you to describe a nightmare with a dark, scary, and threatening atmosphere. Generate a dream description in English.",
    "Childhood Dream": "You are a dream generator. The user wants you to describe a childhood dream that is warm, innocent, and slightly magical. Generate a dream description in English.",
    "Abstract Dream": "You are a dream generator. The user wants you to describe an abstract dream full of illogical, poetic, and fragmented images. Generate a dream description in English."
}

# Word list for association game (English)
WORD_LIST = ["cloud", "mirror", "key", "river", "shadow", "clock", "kite", "candle", "stairs", "window"]

# ---------- Helper: call Zhipu API ----------
def query_zhipu(prompt, max_tokens=150, temperature=0.9):
    try:
        response = client.chat.completions.create(
            model="glm-4-flash",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=0.95
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"API error: {str(e)}"

# ---------- Page config ----------
st.set_page_config(page_title="AI Dream Weaver", page_icon="🌙", layout="centered")
st.title("🌙 AI Dream Weaver")
st.caption("Exploring AI's 'dream' generation vs human creativity | A course extension project")

# Sidebar parameters
st.sidebar.header("⚙️ Generation Parameters")
temp = st.sidebar.slider("Dream Randomness (Temperature)", 0.5, 1.5, 1.0, 0.05)
max_len = st.sidebar.slider("Max length (tokens)", 50, 250, 120)

# ---------- Tabs ----------
tab1, tab2 = st.tabs(["🌌 Dream Generator", "🧠 Creative Association"])

# ========== TAB 1: DREAM GENERATOR ==========
with tab1:
    st.subheader("✨ Multi‑style Dream Generator (with Recursive Evolution)")
    style = st.selectbox("Select dream style", list(DREAM_STYLES.keys()))

    if "current_dream" not in st.session_state:
        st.session_state.current_dream = ""
    if "dream_history" not in st.session_state:
        st.session_state.dream_history = []

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌠 Generate New Dream"):
            with st.spinner("AI is dreaming..."):
                prompt = DREAM_STYLES[style]
                generated = query_zhipu(prompt, max_tokens=max_len, temperature=temp)
                st.session_state.current_dream = generated
                st.session_state.dream_history = [generated]
                st.rerun()
    with col2:
        if st.button("🔄 Continue Dreaming (Evolve)") and st.session_state.current_dream:
            with st.spinner("Dream is evolving..."):
                continuation_prompt = f"Continue the following dream by adding a new scene or image, maintaining the same style. Do not repeat existing content.\n\nCurrent dream: {st.session_state.current_dream}\n\nContinuation:"
                new_segment = query_zhipu(continuation_prompt, max_tokens=max_len, temperature=temp)
                if new_segment and "error" not in new_segment.lower():
                    st.session_state.current_dream += " " + new_segment
                    st.session_state.dream_history.append(new_segment)
                    st.rerun()

    if st.session_state.current_dream:
        st.markdown("### 🌙 Current Dream")
        st.success(st.session_state.current_dream)
        with st.expander("📜 Dream Evolution History"):
            for i, seg in enumerate(st.session_state.dream_history):
                st.write(f"**Segment {i+1}:** {seg}")
    else:
        st.info("Click 'Generate New Dream' to start experiencing AI's dream world.")

# ========== TAB 2: CREATIVE ASSOCIATION ==========
with tab2:
    st.subheader("🧠 Human vs AI Creative Association")
    st.write("Given an English word, type your association, then see what AI associates.")

    # Initialize session state
    if "word_idx" not in st.session_state:
        st.session_state.word_idx = random.randint(0, len(WORD_LIST)-1)
    if "human_assoc" not in st.session_state:
        st.session_state.human_assoc = []
    if "ai_assoc" not in st.session_state:
        st.session_state.ai_assoc = []
    if "used_words" not in st.session_state:
        st.session_state.used_words = []

    current_word = WORD_LIST[st.session_state.word_idx]
    st.markdown(f"### 🔤 Current word: **{current_word}**")

    human_input = st.text_input("Your association (a word or short phrase):", key="human_input")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit & Ask AI"):
            if human_input.strip():
                st.session_state.human_assoc.append(human_input.strip())
                with st.spinner("AI is thinking..."):
                    prompt = f"When I think of the word '{current_word}', what do I associate it with? Give only one word or short phrase, no explanation."
                    ai_response = query_zhipu(prompt, max_tokens=20, temperature=0.8)
                    ai_word = ai_response.split('\n')[0].strip()[:30]
                    st.session_state.ai_assoc.append(ai_word)
                    st.session_state.used_words.append(current_word)
                    # Move to next word
                    st.session_state.word_idx = random.randint(0, len(WORD_LIST)-1)
                    st.rerun()
            else:
                st.warning("Please enter your association first.")
    with col2:
        if st.button("Skip this word"):
            st.session_state.word_idx = random.randint(0, len(WORD_LIST)-1)
            st.rerun()

    if len(st.session_state.human_assoc) > 0:
        st.markdown("### 📊 Comparison Results")
        data = {
            "Word": st.session_state.used_words,
            "Human Association": st.session_state.human_assoc,
            "AI Association": st.session_state.ai_assoc
        }
        st.dataframe(data)

        st.markdown("#### ☁️ Word Cloud Comparison")
        fig, axes = plt.subplots(1, 2, figsize=(10, 4))
        human_text = " ".join(st.session_state.human_assoc)
        ai_text = " ".join(st.session_state.ai_assoc)

        if human_text:
            wc_human = WordCloud(width=200, height=200, background_color="white").generate(human_text)
            axes[0].imshow(wc_human, interpolation="bilinear")
            axes[0].axis("off")
            axes[0].set_title("Human Associations")
        else:
            axes[0].text(0.5, 0.5, "No data", ha="center")

        if ai_text:
            wc_ai = WordCloud(width=200, height=200, background_color="white").generate(ai_text)
            axes[1].imshow(wc_ai, interpolation="bilinear")
            axes[1].axis("off")
            axes[1].set_title("AI Associations")
        else:
            axes[1].text(0.5, 0.5, "No data", ha="center")

        plt.tight_layout()
        st.pyplot(fig)

        st.markdown("#### 🔍 Preliminary Observation")
        st.write(f"Compared **{len(st.session_state.human_assoc)}** pairs of associations.")
        st.caption("Note: AI associations tend to be direct (e.g., 'cloud→rain'), while humans may be more abstract (e.g., 'cloud→cotton'). Try more examples to see the difference.")

        if st.button("Reset all association data"):
            st.session_state.human_assoc = []
            st.session_state.ai_assoc = []
            st.session_state.used_words = []
            st.rerun()
    else:
        st.info("Enter your association and submit to start collecting comparison data.")