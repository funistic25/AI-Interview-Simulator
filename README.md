# 🎙️ AI Interview Simulator — Voice-Based Practice System

> A smart, voice-driven **AI Interview Practice Tool** powered by **Google Cloud (TTS/STT)** and **Gemini AI**.  
> Simulate real product interviews, get adaptive follow-up questions, and improve structured thinking — all through natural conversation.

---

## 🚀 Overview

This project turns your terminal into an **AI interviewer** 🎤  
It asks you questions out loud, listens to your voice responses, and uses **Gemini AI** to generate the **next relevant question** — just like a real interviewer.

🧠 Perfect for Product Management and Analytical interview prep!

---

## 🧩 Features

✅ **Five Interview Types**
- 🧮 Guesstimate — Logical estimation & numerical reasoning  
- 🧠 Root Cause — Structured problem diagnosis  
- 💡 Product Design — Creative user-focused problem solving  
- 🔧 Product Improvement — Analyzing and enhancing products  
- 📊 Product Metrics — Data-driven success measurement  

✅ **Voice Interaction**
- Text-to-Speech (TTS) asks questions aloud  
- Speech-to-Text (STT) captures and transcribes your voice answers

✅ **Auto Save**
- Conversation transcripts (`conversation.txt`)  
- Audio responses (`audio/answer_X.wav`)  
- Subtitle files (`subtitles/answer_X.srt`)

---

## 🧰 Tech Stack

| Component      | Technology                        |
|----------------|-----------------------------------|
| AI Model       | Google Gemini                     |
| Voice Input    | Google Cloud Speech-to-Text       |
| Voice Output   | Google Cloud Text-to-Speech       |
| Language       | Python 3.9+                       |
| Audio Handling | sounddevice, soundfile, playsound |

---

## ⚙️ Setup Guide

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/AI-Interview-Simulator.git
cd AI-Interview-Simulator
```

### 2️⃣ Create & Activate a Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate      # macOS/Linux
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Add Your Credentials
Create `config.py`:
```python
GOOGLE_CREDENTIALS_PATH = r"path/to/your/google_credentials.json"
GEMINI_API_KEY = "your_api_key_here"
```

### 5️⃣ Run the Program
```bash
python googlecode.py
```

---

## 📁 Output Files

| File | Description |
|------|--------------|
| conversation.txt | Full transcript of all Q&A |
| audio/ | Contains recorded answers |
| subtitles/ | Auto-generated SRT subtitles |
| tts_output_X.wav | AI-spoken questions |

---

## 🔒 Security Notes
- Do **not** commit your keys or JSON credentials to GitHub.  
- Add`*.json` to `.gitignore`.
---

## 💡 Example Flow

```
Q1: Let's start with a product design question. Could you describe a product you’d like to create?
A1: Sure! I’d build a productivity app for students.

Q2: Nice! How would you prioritize the first set of features for launch?
A2: I’d focus on scheduling, reminders, and progress tracking.
```

---

## 🧑‍💻 Author

**Samiullah Syed Hussain**  
AI & Product Enthusiast | ML Developer | Blockchain Explorer  
💼 [LinkedIn](https://linkedin.com/in/samiullahsyedhussain) • ✍️ [Hashnode](https://[hashnode.com/@thethinkforge])

**Sriniketh Jeevangi**  
Tech & AI Enthusiast | React & MERN Stack | Full Stack Developer  
💼 [LinkedIn](https://linkedin.com/in/srinikethjeevangi)

---

## 📜 License
MIT License — free to use and modify with attribution.

---

⭐ **If you like this project, consider giving it a star on GitHub!**
