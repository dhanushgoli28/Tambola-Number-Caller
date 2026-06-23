import streamlit as st
import random

# Set up page configuration
st.set_page_config(page_title="Tambola Number Caller", layout="wide")

# Initialize session state variables if they don't exist
if "called_numbers" not in st.session_state:
    st.session_state.called_numbers = []
if "current_number" not in st.session_state:
    st.session_state.current_number = None
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "should_speak" not in st.session_state:
    st.session_state.should_speak = False

st.title("🔢 Tambola / Housie Number Caller")
st.write("Welcome to the automated Tambola caller! Click 'Next Number' to draw.")

# Sidebar Controls
with st.sidebar:
    st.header("Game Controls")
    
    # Reset Game Button
    if st.button("Reset / Start New Game", type="primary"):
        st.session_state.called_numbers = []
        st.session_state.current_number = None
        st.session_state.game_over = False
        st.session_state.should_speak = False
        st.rerun()
        
    st.markdown("---")
    st.write(f"**Numbers Called:** {len(st.session_state.called_numbers)} / 90")

# Layout: Left for current number, Right for the board
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Current Number")
    
    # Button to draw the next number
    if not st.session_state.game_over:
        if st.button("📢 Next Number", use_container_width=True):
            remaining = [n for n in range(1, 91) if n not in st.session_state.called_numbers]
            
            if remaining:
                next_num = random.choice(remaining)
                st.session_state.called_numbers.append(next_num)
                st.session_state.current_number = next_num
                st.session_state.should_speak = True  # Trigger audio flag
            else:
                st.session_state.game_over = True
    else:
        st.error("All 90 numbers have been called! Game Over.")

    # Display the current massive number
    if st.session_state.current_number:
        st.markdown(
            f"""
            <div style="text-align: center; background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-top: 10px;">
                <h1 style="font-size: 80px; color: #ff4b4b; margin: 0;">{st.session_state.current_number}</h1>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Audio Announcement Trick via HTML/JS
        if st.session_state.should_speak:
            # We construct a text phrase for the caller (e.g., "Number 45")
            speech_text = f"Number {st.session_state.current_number}"
            
            # Injecting JavaScript to speak out loud
            st.components.v1.html(
                f"""
                <script>
                    var msg = new SpeechSynthesisUtterance("{speech_text}");
                    msg.rate = 0.9; // Adjust speed (1.0 is default)
                    window.speechSynthesis.speak(msg);
                </script>
                """,
                height=0,
            )
            # Turn off flag so it doesn't repeat speaking if the page reruns for other reasons
            st.session_state.should_speak = False
    else:
        st.info("Click 'Next Number' to begin the game.")

with col2:
    st.subheader("The Board")
    
    # Generate the 90-number grid view
    for row in range(9):
        cols = st.columns(10)
        for col_idx in range(10):
            num = row * 10 + col_idx + 1
            
            # Highlight if the number has been called
            if num in st.session_state.called_numbers:
                if num == st.session_state.current_number:
                    cols[col_idx].markdown(f"<div style='text-align:center; background-color:#ff4b4b; color:white; font-weight:bold; border-radius:5px; padding:5px;'>{num}</div>", unsafe_allow_html=True)
                else:
                    cols[col_idx].markdown(f"<div style='text-align:center; background-color:#29b5e8; color:white; font-weight:bold; border-radius:5px; padding:5px;'>{num}</div>", unsafe_allow_html=True)
            else:
                cols[col_idx].markdown(f"<div style='text-align:center; color:#b0b0b0; border: 1px solid #e0e0e0; border-radius:5px; padding:5px;'>{num}</div>", unsafe_allow_html=True)
