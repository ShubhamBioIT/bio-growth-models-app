import streamlit as st
import numpy as np
from random import shuffle
import matplotlib.pyplot as plt

st.set_page_config(page_title="Biological Growth Models", layout="wide")

st.title("📈 Interactive Bioinformatics Growth Models")
st.markdown("""
Welcome! This tool helps you explore two fundamental models in population biology:

1. **Exponential Growth (Unlimited Resources)**  
2. **Logistic Growth (Limited Resources)**

Use the sliders below to set values and visualize population growth over time.
""")

# --- Diagrammatic Model Explanation ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("🌱 Exponential Growth")
    st.markdown(
        """
        <div style='background-color:#e6ffe6; padding:10px; border-radius:10px; color:black;'>
            <b>Imagine a world with endless food and space.</b><br>
            Every individual can reproduce freely.<br>
            <span style='color:green; font-weight:bold;'>Population doubles, triples, and keeps going up fast!</span><br>
            <i style='color:black;'>Example: Bacteria in a fresh petri dish.</i>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.subheader("🌳 Logistic Growth")
    st.markdown(
        """
        <div style='background-color:#e6f0ff; padding:10px; border-radius:10px; color:black;'>
            <b>Now imagine resources are limited.</b><br>
            As the population grows, food and space run out.<br>
            <span style='color:blue; font-weight:bold;'>Growth slows and levels off at a maximum size (carrying capacity, K).</span><br>
            <i style='color:black;'>Example: Deer in a forest, fish in a pond.</i>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # --- Collapsible Downbar for Model Sketches ---
with st.expander("Show Model Sketches (click to expand)", expanded=False):
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            # Exponential Growth Sketch (smaller, black background)
            fig_exp, ax_exp = plt.subplots(figsize=(2, 1.2), facecolor='black')
            t_exp = np.linspace(0, 5, 200)
            N_exp = np.exp(t_exp)
            ax_exp.plot(t_exp, N_exp, color='lime', linewidth=2)
            ax_exp.set_title("J-shaped Exponential Curve", fontsize=8, color='lime')
            ax_exp.set_xticks([])
            ax_exp.set_yticks([])
            for spine in ax_exp.spines.values():
                spine.set_visible(False)
            ax_exp.set_facecolor('black')
            ax_exp.annotate("Rapid growth!", xy=(3, np.exp(3)), xytext=(1, 40),
                            arrowprops=dict(facecolor='lime', shrink=0.05, width=1.5),
                            fontsize=7, color='lime')
            st.pyplot(fig_exp, use_container_width=False)

        with col_exp2:
            # Logistic Growth Sketch (smaller, black background)
            fig_log, ax_log = plt.subplots(figsize=(2, 1.2), facecolor='black')
            t_log = np.linspace(0, 8, 200)
            K = 100
            N_log = K / (1 + 9 * np.exp(-1.2 * t_log))
            ax_log.plot(t_log, N_log, color='cyan', linewidth=2)
            ax_log.axhline(K, color='red', linestyle='--', linewidth=1)
            ax_log.set_title("S-shaped Logistic Curve", fontsize=8, color='cyan')
            ax_log.set_xticks([])
            ax_log.set_yticks([])
            for spine in ax_log.spines.values():
                spine.set_visible(False)
            ax_log.set_facecolor('black')
            # Place annotation below the curve
            ax_log.annotate(
            "Carrying capacity (K)",
            xy=(7, K), xytext=(5.5, K-40),
            arrowprops=dict(facecolor='red', shrink=0.05, width=1.5, headwidth=6),
            fontsize=7, color='red', ha='center'
            )
            st.pyplot(fig_log, use_container_width=False)

st.markdown("---")

# Sidebar: Global Inputs
st.sidebar.header("🔧 Adjust Model Parameters")
model_choice = st.sidebar.radio("Choose Growth Model", ["Exponential Growth", "Logistic Growth"])
N0 = st.sidebar.number_input("Initial Population (N₀)", min_value=1, value=100)
r = st.sidebar.slider("Growth Rate (r)", 0.01, 1.0, 0.3, step=0.01)
time = st.sidebar.slider("Time Duration (t)", 1, 50, 20)

t = np.linspace(0, time, 500)

# --- Exponential Growth ---
if model_choice == "Exponential Growth":
    st.header("📘 Exponential Growth Model")
    st.latex(r"N(t) = N_0 \cdot e^{rt}")
    st.markdown(
        "<div style='background-color:#f0fff0; padding:10px; border-radius:10px; color:black;'>"
        "<b>Key Points:</b><br>"
        "• <span style='color:green;'>Population grows faster and faster!</span><br>"
        "• No limits: food, space, and resources are infinite.<br>"
        "• <b>Real-life:</b> Early phase of bacteria or yeast in lab.</div>",
        unsafe_allow_html=True,
    )

    N = N0 * np.exp(r * t)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(t, N, color='green', linewidth=3, label='Exponential Growth')
    ax.fill_between(t, N, color='lightgreen', alpha=0.3)
    ax.set_xlabel("Time", fontsize=12)
    ax.set_ylabel("Population", fontsize=12)
    ax.set_title("Unlimited Growth Curve (J-shaped)", fontsize=14, color='green')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()
    st.pyplot(fig)

    st.info(f"After {time} time units, the population reaches approximately **{int(N[-1])}**.")

    st.markdown(
        "<div style='background-color:#e6ffe6; padding:10px; border-radius:10px; color:black;'>"
        "<b>Why does this happen?</b><br>"
        "Every individual can reproduce, so the more you have, the faster the population grows!"
        "</div>",
        unsafe_allow_html=True,
    )

# --- Logistic Growth ---
else:
    st.header("📗 Logistic Growth Model")
    st.latex(r"\frac{dN}{dt} = rN\left(1 - \frac{N}{K} \right)")
    st.markdown(
        "<div style='background-color:#f0f8ff; padding:10px; border-radius:10px; color:black;'>"
        "<b>Key Points:</b><br>"
        "• <span style='color:blue;'>Growth slows as resources run out.</span><br>"
        "• <b>Carrying capacity (K):</b> The maximum population the environment can support.<br>"
        "• <b>Real-life:</b> Animals in a forest, fish in a pond.</div>",
        unsafe_allow_html=True,
    )

    K = st.sidebar.number_input("Carrying Capacity (K)", min_value=N0+1, value=1000)

    # Euler's Method Simulation
    def logistic_growth(N, r, K):
        return r * N * (1 - N / K)

    N = np.zeros(len(t))
    N[0] = N0
    dt = t[1] - t[0]
    for i in range(1, len(t)):
        N[i] = N[i-1] + logistic_growth(N[i-1], r, K) * dt

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(t, N, color='blue', linewidth=3, label='Logistic Growth')
    ax.axhline(K, color='red', linestyle='--', label='Carrying Capacity (K)')
    ax.fill_between(t, N, color='lightblue', alpha=0.3)
    ax.set_xlabel("Time", fontsize=12)
    ax.set_ylabel("Population", fontsize=12)
    ax.set_title("Limited Growth (S-shaped Curve)", fontsize=14, color='blue')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()
    st.pyplot(fig)

    st.success(f"Population approaches the carrying capacity (K = {K}). Final value: **{int(N[-1])}**")

    st.markdown(
        "<div style='background-color:#e6f0ff; padding:10px; border-radius:10px; color:black;'>"
        "<b>Why does this happen?</b><br>"
        "As the population gets close to K, there isn't enough food or space for everyone, so growth slows and stops."
        "</div>",
        unsafe_allow_html=True,
    )

# --- Interactive Quiz ---

def show_quiz(questions):
    st.markdown("### 🧠 Quick Quiz: Test Your Understanding!")
    user_answers = []
    with st.form("quiz_form"):
        for idx, q in enumerate(questions):
            st.markdown(f"**Q{idx+1}. {q['question']}**")
            options = q['options'][:]
            user_answers.append(
                st.radio(
                    f"Select your answer for Q{idx+1}",
                    options,
                    key=f"quiz_q{idx+1}",
                    index=None  # No answer selected by default
                )
            )
            st.markdown("---")
        submitted = st.form_submit_button("Submit Answers 🚀")
    if submitted:
        score = 0
        feedback = []
        for i, q in enumerate(questions):
            if user_answers[i] == q['answer']:
                score += 1
                feedback.append(f"✅ Q{i+1}: Correct!")
            else:
                feedback.append(f"❌ Q{i+1}: Incorrect. Correct answer: **{q['answer']}**")
        st.markdown(
            f"<div style='background-color:#000; color:#fff; padding:15px; border-radius:10px;'><h4>Your Score: {score} / {len(questions)}</h4></div>",
            unsafe_allow_html=True
        )
        for fb in feedback:
            st.markdown(fb)

if model_choice == "Exponential Growth":
    quiz_questions = [
        {
            "question": "What happens to the population if the growth rate (r) increases?",
            "options": [
                "Population grows faster",
                "Population decreases",
                "Population stays the same",
                "Population reaches a maximum"
            ],
            "answer": "Population grows faster"
        },
        {
            "question": "Which of these is a real-life example of exponential growth?",
            "options": [
                "Bacteria in a fresh petri dish",
                "Deer in a forest",
                "Fish in a pond",
                "Humans in a crowded city"
            ],
            "answer": "Bacteria in a fresh petri dish"
        },
        {
            "question": "What shape does the exponential growth curve have?",
            "options": [
                "J-shaped",
                "S-shaped",
                "Flat line",
                "U-shaped"
            ],
            "answer": "J-shaped"
        }
    ]
else:
    quiz_questions = [
        {
            "question": "What is the carrying capacity (K) in logistic growth?",
            "options": [
                "Maximum population the environment can support",
                "Initial population",
                "Growth rate",
                "Time duration"
            ],
            "answer": "Maximum population the environment can support"
        },
        {
            "question": "What happens as the population approaches K?",
            "options": [
                "Growth slows down and stops",
                "Population decreases rapidly",
                "Growth rate increases",
                "Population becomes zero"
            ],
            "answer": "Growth slows down and stops"
        },
        {
            "question": "What shape does the logistic growth curve have?",
            "options": [
                "S-shaped",
                "J-shaped",
                "Straight line",
                "Bell-shaped"
            ],
            "answer": "S-shaped"
        }
    ]

with st.expander("🧩 Take the Model Quiz!"):
    show_quiz(quiz_questions)

# Footer
st.markdown("---")
st.caption("Built by Shubham | Powered by Streamlit + NumPy + Matplotlib")
