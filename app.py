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
if "is_playing" not in st.session_state:
    st.session_state.is_playing = False
if "should_speak" not in st.session_state:
    st.session_state.should_speak = False

st.title("🔢 Auto-Tambola Caller with Voice")
st.write("Click 'Play' to start auto-calling every 5 seconds. Use 'Pause' to halt at any point.")

# Sidebar Controls
with st.sidebar:
    st.header("Game Controls")
    
    # Reset Game Button
    if st.button("Reset / Start New Game", type="primary"):
        st.session_state.called_numbers = []
        st.session_state.current_number = None
        st.session_state.game_over = False
        st.session_state.is_playing = False
        st.session_state.should_speak = False
        st.rerun()
        
    st.markdown("---")
    st.write(f"**Numbers Called:** {len(st.session_state.called_numbers)} / 90")


# Core Auto-Calling Fragment System
@st.fragment(run_every=3.0 if st.session_state.is_playing and not st.session_state.game_over else None)
def auto_caller_loop():
    # 1. If playing, draw a number automatically on the 5-second tick
    if st.session_state.is_playing and not st.session_state.game_over:
        remaining = [n for n in range(1, 91) if n not in st.session_state.called_numbers]
        if remaining:
            next_num = random.choice(remaining)
            st.session_state.called_numbers.append(next_num)
            st.session_state.current_number = next_num
            st.session_state.should_speak = True
        else:
            st.session_state.game_over = True
            st.session_state.is_playing = False

    # 2. CREATE COLUMNS INSIDE THE FRAGMENT TO AVOID THE ERROR
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Controls & Current Number")
        
        # Play / Pause Toggle Buttons
        if st.session_state.game_over:
            st.error("All 90 numbers have been called! Game Over.")
        elif not st.session_state.is_playing:
            if st.button("▶️ Play (Auto Call)", use_container_width=True):
                st.session_state.is_playing = True
                st.rerun()
        else:
            if st.button("⏸️ Pause", use_container_width=True):
                st.session_state.is_playing = False
                st.rerun()

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
            
            # Browser Voice Synthesis triggering
            if st.session_state.should_speak:
                speech_text = f"Number {st.session_state.current_number}"
                st.components.v1.html(
                    f"""
                    <script>
                        var msg = new SpeechSynthesisUtterance("{speech_text}");
                        msg.rate = 0.9;
                        window.speechSynthesis.speak(msg);
                    </script>
                    """,
                    height=0,
                )
                st.session_state.should_speak = False
        else:
            st.info("Click Play to start generating numbers.")

    with col2:
        st.subheader("The Board")
        # Generate the 90-number grid view
        for row in range(9):
            grid_cols = st.columns(10)
            for col_idx in range(10):
                num = row * 10 + col_idx + 1
                
                if num in st.session_state.called_numbers:
                    if num == st.session_state.current_number:
                        grid_cols[col_idx].markdown(f"<div style='text-align:center; background-color:#ff4b4b; color:white; font-weight:bold; border-radius:5px; padding:5px;'>{num}</div>", unsafe_allow_html=True)
                    else:
                        grid_cols[col_idx].markdown(f"<div style='text-align:center; background-color:#29b5e8; color:white; font-weight:bold; border-radius:5px; padding:5px;'>{num}</div>", unsafe_allow_html=True)
                else:
                    grid_cols[col_idx].markdown(f"<div style='text-align:center; color:#b0b0b0; border: 1px solid #e0e0e0; border-radius:5px; padding:5px;'>{num}</div>", unsafe_allow_html=True)

# Run the app's interactive loop
auto_caller_loop()
