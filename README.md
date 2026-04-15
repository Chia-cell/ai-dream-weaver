# 🌙 AI Dream Weaver

> Explore AI's "dream" generation and compare human vs AI creative associations.

## 📌 Project Overview

This project is an extension of my course project *"Can AI Dream of Electric Sheep?"* It provides an interactive web application where users can:

- Generate **dream-like texts** using a large language model (Zhipu AI `glm-4-flash`), with selectable styles (sci-fi, nightmare, childhood, abstract).
- Recursively **evolve** a dream by continuing from the previous output, simulating the fluidity of human dreams.
- Play a **creative association game**: given a word, compare your association with the AI's, and visualize the differences using word clouds.

The goal is to explore the boundary of AI's generative "creativity" and to provide a hands‑on tool for discussing whether machines can dream.

## 🚀 Live Demo (Optional)

If deployed on Streamlit Cloud, you can try it here: [Link to your deployed app] (optional)

## 🛠️ Tech Stack

- **Frontend & Interaction**: Streamlit
- **Language Model**: Zhipu AI (`glm-4-flash`, free tier)
- **Visualization**: Matplotlib, WordCloud
- **Environment**: Python 3.10+

## 📁 Project Structure
ai-dream-weaver/
├── app.py # Main Streamlit application
├── test_zhipu.py # Simple test script for API
├── requirements.txt # Python dependencies
├── .env # API key (not uploaded)
├── .gitignore # Ignored files
└── README.md # This file


## 🧪 Getting Started

###  Clone the repository

git clone https://github.com/your-username/ai-dream-weaver.git
cd ai-dream-weaver

python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt

Register at Zhipu AI Open Platform
Create an API key from the console
Create a .env file in the project root and add:
ZHIPUAI_API_KEY=your_api_key_here

streamlit run app.py

Your browser will open at http://localhost:8501.

🎯 Features
Multi‑style dream generation – Choose from 4 different dream themes.

Recursive dream evolution – Build a longer, evolving dream narrative.

Creative association test – Collect and compare human and AI associations.

Word cloud visualization – See the differences in association patterns.

Adjustable parameters – Control randomness (temperature) and output length.

📝 Notes
The AI model used is glm-4-flash, which is free and fast. It may sometimes output Chinese; the prompts are designed to encourage English output.

The association game currently uses English words to avoid font issues in word clouds.

Your API key is kept safe via .env and is not uploaded to GitHub.

🤔 Reflections
This project helped me understand:

How to integrate a real LLM API into an interactive application.

The importance of prompt engineering for controlling output style.

The difference between human and AI associations – AI tends to be more literal (co-occurrence), while humans often use metaphor.

📄 License
This project is for educational purposes.

👤 Author
Your Name – [Chia-cell]

🙏 Acknowledgements
Zhipu AI for providing free API access.

Streamlit for making interactive apps so easy.

My course instructor for inspiring the original question "Can AI dream of electric sheep?"
