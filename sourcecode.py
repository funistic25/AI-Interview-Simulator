import os
import sounddevice as sd
import soundfile as sf
from google.cloud import texttospeech, speech
from google import genai
import playsound
import keyboard
import numpy as np

# ---------------------------
# Initialize Google Cloud clients & Gemini
# ---------------------------
GOOGLE_CREDENTIALS_PATH = r"path/to/your/google_credentials.json"

# Your Gemini API key (replace the placeholder with your actual key)
GEMINI_API_KEY = "your_api_key_here"

# Set environment variables programmatically
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CREDENTIALS_PATH
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

# TTS client
tts_client = texttospeech.TextToSpeechClient()

# STT client
stt_client = speech.SpeechClient()

# Gemini API
gemini_api_key = os.environ.get("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("Set GEMINI_API_KEY in your environment variables!")
client = genai.Client(api_key=gemini_api_key)

# ---------------------------
# Create folders if not exist
# ---------------------------
os.makedirs("audio", exist_ok=True)
os.makedirs("subtitles", exist_ok=True)

# ---------------------------
# Functions
# ---------------------------

def speak(text, qnum=None):
    filename = f"tts_output_{qnum}.wav" if qnum else "tts_output.wav"
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)
    response = tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    with open(filename, "wb") as out:
        out.write(response.audio_content)
    playsound.playsound(filename, True)

def record_audio(filename, fs=44100):
    """Record audio from mic until user presses CTRL+B"""
    print("Recording... Press CTRL + B to stop.")
    recording = []

    def callback(indata, frames, time, status):
        if status:
            print(status)
        recording.append(indata.copy())

    with sd.InputStream(samplerate=fs, channels=1, callback=callback):
        while True:
            if keyboard.is_pressed('ctrl+b'):
                print("Recording stopped by user!")
                break
            sd.sleep(100)  # avoid busy-waiting

    audio_array = np.concatenate(recording, axis=0)
    sf.write(filename, audio_array, fs)
    print("Recording saved:", filename)

def audio_to_text(filename):
    """Convert audio to text using Google STT"""
    with open(filename, "rb") as f:
        audio_bytes = f.read()

    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="en-US"
    )

    response = stt_client.recognize(config=config, audio=audio)
    if response.results:
        return response.results[0].alternatives[0].transcript
    return ""

def save_subtitle(filename, text, start_time=0, duration=10):
    """Save subtitle in SRT format"""
    end_time = start_time + duration
    with open(filename, "w", encoding="utf-8") as f:
        f.write("1\n")
        f.write(f"00:00:{start_time:02},000 --> 00:00:{end_time:02},000\n")
        f.write(f"{text}\n")

def generate_next_question(prev_question, prev_answer, conversation, interview_type):
    """
    Generate the next interview question using Gemini based on the latest Q&A and interview type.
    """
    interview_guide = {
        "Root Cause": """
Purpose: Tests analytical and diagnostic skills.
Scenario: A product metric or feature has dropped in performance.
Ask questions that explore causes, data validation, and structured reasoning.
Example: "Engagement dropped by 40%. What could be the possible causes?"
Approach: Clarify the metric, use MECE breakdowns (user, feature, tech, external),
form hypotheses, and propose validation methods.
Skills tested: Analytical thinking, structured reasoning, use of metrics, debugging mindset.
""",
        "Guesstimate": """
Purpose: Tests logical estimation skills.
Scenario: No data available — candidate must estimate logically.
Ask questions that push assumptions, calculations, and sanity checks.
Example: "Estimate how many EVs are sold daily in India."
Approach: Break into logical parts, make clear assumptions, multiply and refine estimates.
Skills tested: Structured problem solving, numerical reasoning, clarity.
""",
        "Product Design": """
Purpose: Tests creativity and structured product thinking.
Scenario: Design a new product or feature for a user problem.
Ask questions that explore user needs, MVP design, features, and success metrics.
Example: "Design a travel planning app for solo travelers."
Approach: Clarify problem, identify user pain points, ideate, prioritize features, define success metrics.
Skills tested: User empathy, creativity, prioritization, holistic product thinking.
""",
        "Product Improvement": """
Purpose: Tests ability to enhance an existing product.
Scenario: Analyze weaknesses and suggest data-driven improvements.
Ask questions that explore user pain points, UX changes, AI explainability, etc.
Example: "How would you improve YouTube recommendations?"
Approach: Identify target users, analyze current gaps, suggest measurable improvements.
Skills tested: Analytical reasoning, creativity, impact orientation.
""",
        "Product Metrics": """
Purpose: Tests understanding of success measurement.
Scenario: Define KPIs or metrics for product features.
Ask questions that explore goal alignment, north star metrics, and guardrails.
Example: "What metrics would you track for a new chat summarization feature?"
Approach: Define goal, primary metric, supporting metrics, guardrails.
Skills tested: Metric design, goal alignment, analytical clarity.
"""
    }

    prompt = f"""
You are a professional technical interviewer at LinkedIn interviewing conducting a **{interview_type} interview**. You are interviewing the candidate for the position at your firm.

Follow the rules in the guide below to craft the next question.

INTERVIEW TYPE GUIDE:
{interview_guide.get(interview_type, "General interview style. Focus on clarity and logical follow-up questions.")}

CONVERSATION SO FAR:
{conversation}

LAST EXCHANGE:
Question: {prev_question}
Answer: {prev_answer}

Now, based on the candidate’s latest answer, ask ONE highly relevant and natural follow-up question.

Your next question should:
- Maintain the same interview style.
- Build upon what the candidate just said.
- Avoid repeating previous questions.
- Be concise, clear, and human-like.

Only output the **next question** (no explanation or commentary).
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )
    return response.text.strip()

# ---------------------------
# Select Interview Type
# ---------------------------
print("Welcome to the AI Interview Practice System!")
print("\nPlease choose the type of interview you want to practice:")
print("1. Root Cause")
print("2. Guesstimate")
print("3. Product Design")
print("4. Product Improvement")
print("5. Product Metrics")

choice = input("\nEnter your choice (1-5): ").strip()

interview_types = {
    "1": "Root Cause",
    "2": "Guesstimate",
    "3": "Product Design",
    "4": "Product Improvement",
    "5": "Product Metrics"
}

interview_type = interview_types.get(choice)
if not interview_type:
    print("Invalid choice. Defaulting to 'Product Design'.")
    interview_type = "Product Design"

print(f"\nStarting {interview_type} interview...")
print("-------------------------------------------------\n")

# ---------------------------
# Conversation setup
# ---------------------------
conversation_file = "conversation.txt"
open(conversation_file, "w").close()  # Clear previous conversation

max_questions = 5
question_count = 0

print("Our Interview begins here!!")

# ---------------------------
# Main loop
# ---------------------------
while question_count < max_questions:
    # Load conversation (keep last 10 lines for context)
    conversation = "\n".join(open(conversation_file, "r", encoding="utf-8").readlines()[-10:])

    # Determine next question
    if question_count == 0:
        next_question = f"Let's start with a {interview_type} question. Please introduce yourself briefly."
    else:
        # Read last Q&A from the conversation file
        lines = open(conversation_file, "r", encoding="utf-8").read().strip().split("\n")
        prev_q_line = [l for l in lines if l.startswith(f"Q{question_count}:")]
        prev_a_line = [l for l in lines if l.startswith(f"A{question_count}:")]
        prev_question = prev_q_line[-1].split(":", 1)[1].strip() if prev_q_line else ""
        prev_answer = prev_a_line[-1].split(":", 1)[1].strip() if prev_a_line else ""

        next_question = generate_next_question(prev_question, prev_answer, conversation, interview_type)

    question_count += 1
    print(f"\nQ{question_count}: {next_question}")
    speak(next_question, qnum=question_count)

    # Record answer
    audio_file = f"audio/answer_{question_count}.wav"
    record_audio(audio_file)  # No duration, stops with CTRL+B

    # Convert to text
    answer_text = audio_to_text(audio_file)
    print(f"A{question_count}: {answer_text}")

    # Save conversation
    with open(conversation_file, "a", encoding="utf-8") as f:
        f.write(f"Q{question_count}: {next_question}\nA{question_count}: {answer_text}\n\n")

    # Save subtitle
    subtitle_file = f"subtitles/answer_{question_count}.srt"
    save_subtitle(subtitle_file, answer_text, start_time=0, duration=10)

print("\nInterview completed. All questions and answers saved.")

