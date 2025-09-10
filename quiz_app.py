from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import BaseOutputParser
import streamlit as st
import os
import re
import hashlib
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
# Fixed typo: tempertaure -> temperature
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", 
                             temperature=0.9, 
                             top_p=0.95,
                             google_api_key = api_key)

# ---------------- Improved parser ----------------
class QuizParser(BaseOutputParser):
    def parse(self, text: str):
        # Clean the text first
        text = text.strip()
        
        # Extract questions with improved regex
        questions = re.findall(r"<Question-(\d+)>(.*?)<(?:/Question-\d+|option-1>)", text, re.DOTALL)
        
        # Extract options for each question
        all_options = []
        for i in range(1, len(questions) + 1):
            question_options = []
            for j in range(1, 5):  # Assuming 4 options per question
                option_pattern = f"<option-{j}>(.*?)</option-{j}>"
                matches = re.findall(option_pattern, text, re.DOTALL)
                if len(matches) >= i:  # Get the i-th occurrence for the i-th question
                    question_options.append(matches[i-1].strip())
            all_options.append(question_options)
        
        # Extract answers with improved regex
        answers = re.findall(r"<answer-(\d+)>(.*?)</answer-\d+>", text, re.DOTALL)
        
        quiz = []
        for i, (q_num, q_text) in enumerate(questions):
            q_opts = all_options[i] if i < len(all_options) else []
            # Find corresponding answer
            q_ans = "N/A"
            for ans_num, ans_text in answers:
                if int(ans_num) == int(q_num):
                    q_ans = ans_text.strip()
                    break
            
            quiz.append({
                "question": q_text.strip(),
                "options": q_opts,
                "answer": q_ans
            })
        
        return quiz

parser = QuizParser()

# ---------------- Improved prompt with uniqueness ----------------
def create_the_quiz_prompt_template():
    template = """
    You are an expert quiz maker for technical fields.
    Create a quiz with {num_of_questions} {type} questions 
    about the following concept/context: {quiz_context} having {hardness} level of question.
    
    {uniqueness_instruction}
    
    Rules:
    - Each question must be *unique* and cover different aspects of the topic.
    - Avoid common textbook questions.
    - Try to cover different subtopics for variety.
    - Make sure the correct answer is one of the four options provided.
    - Be very specific with the formatting.

    Follow this EXACT format:

    <Questions:>
        <Question-1>Your first question here?
            <option-1>Option A text</option-1>
            <option-2>Option B text</option-2>
            <option-3>Option C text</option-3>
            <option-4>Option D text</option-4>
        
        <Question-2>Your second question here?
            <option-1>Option A text</option-1>
            <option-2>Option B text</option-2>
            <option-3>Option C text</option-3>
            <option-4>Option D text</option-4>
    
    <Answers:>
        <answer-1>Exact text of correct option for question 1</answer-1>
        <answer-2>Exact text of correct option for question 2</answer-2>
        
    Important: The answer must EXACTLY match one of the four options provided for each question.
    """
    return PromptTemplate.from_template(template)

def create_quiz_chain():
    prompt = create_the_quiz_prompt_template()
    return prompt | llm | parser

# ---------------- Enhanced session state initialization ----------------
if "quiz" not in st.session_state:
    st.session_state.quiz = None
if "user_answers" not in st.session_state:
    st.session_state.user_answers = []
if "answered" not in st.session_state:
    st.session_state.answered = []
if "score" not in st.session_state:
    st.session_state.score = None
if "generated_context" not in st.session_state:
    st.session_state.generated_context = ""
if "quiz_history" not in st.session_state:
    st.session_state.quiz_history = set()  # Track generated quizzes for uniqueness
if "generation_count" not in st.session_state:
    st.session_state.generation_count = 0

# ---------------- helper functions ----------------
def record_choice(q_index, widget_key):
    selected = st.session_state.get(widget_key)
    st.session_state.user_answers[q_index] = selected
    st.session_state.answered[q_index] = True

def normalize(text):
    if text is None:
        return ""
    return re.sub(r'[^a-zA-Z0-9]', '', text).lower()

def create_quiz_hash(context, level, num_questions, count):
    """Create a unique hash for quiz generation to ensure uniqueness"""
    content = f"{context}_{level}_{num_questions}_{count}"
    return hashlib.md5(content.encode()).hexdigest()

def get_uniqueness_instruction(context, level, num_questions):
    """Generate instruction for uniqueness based on generation count"""
    count = st.session_state.generation_count
    if count == 0:
        return "This is the first quiz generation for this topic."
    else:
        return f"This is attempt #{count + 1}. Generate completely different questions from previous attempts. Focus on different aspects, subtopics, or angles of the concept."

# ---------------- Streamlit UI ----------------
st.title("MCQ Quiz App:")
st.write("Generate a quiz with your given context:")

context = st.text_area("Write your context")
level = st.selectbox("Enter your level:", ['Easy','Medium','Hard'])
num_of_questions = st.number_input("Number of questions", min_value=1, max_value=5, step=1)
q_type = st.selectbox("Type of question:", ['multiple-choice'])

# ---------------- Generate Quiz ----------------
if st.button("Generate Quiz"):
    if not context.strip():
        st.error("Please provide a context for the quiz!")
    else:
        # Increment generation count for uniqueness
        if context == st.session_state.generated_context:
            st.session_state.generation_count += 1
        else:
            st.session_state.generation_count = 0
        
        # Create uniqueness instruction
        uniqueness_instruction = get_uniqueness_instruction(context, level, num_of_questions)
        
        with st.spinner("Generating quiz..."):
            try:
                chain = create_quiz_chain()
                quiz = chain.invoke({
                    "num_of_questions": num_of_questions,
                    "type": q_type,
                    "quiz_context": context,
                    "hardness": level,
                    "uniqueness_instruction": uniqueness_instruction
                })

                if not quiz or len(quiz) == 0:
                    st.warning("⚠️ Quiz could not be generated. Try again with a different context.")
                else:
                    # Validate quiz structure
                    valid_quiz = True
                    for i, q in enumerate(quiz):
                        if not q.get('question') or not q.get('options') or len(q.get('options', [])) < 4:
                            st.error(f"Question {i+1} is incomplete. Please regenerate the quiz.")
                            valid_quiz = False
                            break
                    
                    if valid_quiz:
                        st.session_state.quiz = quiz
                        st.session_state.user_answers = [None] * len(quiz)
                        st.session_state.answered = [False] * len(quiz)
                        st.session_state.score = None
                        st.session_state.generated_context = context
                        
                        st.success(f"✅ Generated {len(quiz)} questions successfully!")
                        
            except Exception as e:
                st.error(f"Error generating quiz: {str(e)}")
                st.info("Please try again with a different context or parameters.")

# ---------------- Show Quiz ----------------
if st.session_state.quiz:
    quiz = st.session_state.quiz
    st.subheader("Generated Quiz")
    
    # Display generation info
    st.info(f"Generation #{st.session_state.generation_count + 1} for this context")

    for i, q in enumerate(quiz):
        st.markdown(f"**Q{i+1}: {q['question']}**")
        
        # Ensure we have valid options
        options = q.get("options", [])
        if len(options) < 4:
            st.error(f"Question {i+1} has incomplete options. Please regenerate the quiz.")
            continue
            
        widget_key = f"q_{i}_choice"

        st.radio(
            label=f"Select your answer for Q{i+1}:",
            options=options,
            key=widget_key,
            index=None,
            on_change=record_choice,
            args=(i, widget_key),
        )

        # Enhanced Feedback with debug info
        if st.session_state.answered[i]:
            selected = st.session_state.user_answers[i]
            correct_answer = q["answer"]
            
            # # Debug information (can be commented out in production)
            # with st.expander(f"Debug info for Q{i+1}", expanded=False):
            #     st.write(f"Selected: '{selected}'")
            #     st.write(f"Correct: '{correct_answer}'")
            #     st.write(f"Selected normalized: '{normalize(selected)}'")
            #     st.write(f"Correct normalized: '{normalize(correct_answer)}'")
            
            if normalize(selected) == normalize(correct_answer):
                st.markdown(
                    f"<div style='background-color:#28a745;color:white;padding:8px;border-radius:6px;margin:5px 0'>✅ Correct! {selected}</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"<div style='background-color:#dc3545;color:white;padding:8px;border-radius:6px;margin:5px 0'>❌ Incorrect: {selected}</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div style='background-color:#17a2b8;color:white;padding:8px;border-radius:6px;margin:5px 0'>💡 Correct answer: {correct_answer}</div>",
                    unsafe_allow_html=True,
                )

# ---------------- Submit Quiz ----------------
if st.session_state.quiz and st.button("Submit Quiz"):
    correct = 0
    total = len(st.session_state.quiz)
    
    for idx, q in enumerate(st.session_state.quiz):
        user_answer = st.session_state.user_answers[idx]
        if user_answer and normalize(user_answer) == normalize(q["answer"]):
            correct += 1
    
    st.session_state.score = f"{correct} out of {total}"
    
    # Show detailed results
    percentage = (correct / total) * 100
    if percentage >= 80:
        st.balloons()  # 🎈 THIS IS THE BALLOON FEATURE! 🎈
        st.success(f"🎉 Excellent! Final Score: {st.session_state.score} ({percentage:.1f}%)")
    elif percentage >= 60:
        st.success(f"👍 Good job! Final Score: {st.session_state.score} ({percentage:.1f}%)")
    else:
        st.warning(f"📚 Keep studying! Final Score: {st.session_state.score} ({percentage:.1f}%)")

# Reset button
if st.session_state.quiz:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reset Quiz"):
            st.session_state.quiz = None
            st.session_state.user_answers = []
            st.session_state.answered = []
            st.session_state.score = None
            st.rerun()
    
    with col2:
        # Show progress
        if st.session_state.quiz:
            answered_count = sum(st.session_state.answered)
            total_questions = len(st.session_state.quiz)
            st.metric("Progress", f"{answered_count}/{total_questions} answered")




