import streamlit as st
import pandas as pd
import random
import os

# Page configuration
st.set_page_config(
    page_title="Design Heuristics Viewer",
    page_icon="📇",
    layout="wide"
)

# Load custom CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("📇 Design Heuristics Card Viewer")

# Read CSV data
df = pd.read_csv("attached_assets/Hueristics Guide 02.csv")

# Drop empty rows and columns
df = df.dropna(how='all').fillna('')

# Store displayed cards in session state
if 'displayed_cards' not in st.session_state:
    st.session_state.displayed_cards = []

# Random card selection
if st.button("Show Random Card"):
    random_index = random.randint(0, len(df) - 1)
    st.session_state.displayed_cards.append(random_index)

# Function to remove card
def remove_card(index):
    st.session_state.displayed_cards.remove(index)

# Display random cards in grid
if st.session_state.displayed_cards:
    for i in range(0, len(st.session_state.displayed_cards), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(st.session_state.displayed_cards):
                card_index = st.session_state.displayed_cards[i + j]
                selected_row = df.iloc[card_index]
                with cols[j]:
                    st.markdown(
                        f"""
                        <div class="card highlight">
                            <h3>{selected_row['TITLE']}</h3>
                        """,
                        unsafe_allow_html=True
                    )
                    # Try both PNG and JPG formats
                    image_base = f"Images/{selected_row['TITLE'].lower().replace(' ', '_')}"
                    image_path = None
                    if os.path.exists(f"{image_base}.png"):
                        image_path = f"{image_base}.png"
                    elif os.path.exists(f"{image_base}.jpg"):
                        image_path = f"{image_base}.jpg"
                    
                    if image_path:
                        from PIL import Image
                        img = Image.open(image_path)
                        # Only rotate JPG images (assuming PNGs are correctly oriented)
                        if image_path.endswith('.jpg'):
                            img = img.rotate(0, expand=True)
                        st.image(img, use_container_width=True)
                    st.markdown(
                        f"""
                            <p><strong>Category:</strong> {selected_row['CATEGORY']}</p>
                            <p><strong>Design Question:</strong> {selected_row['DESIGN QUESTION and PROMPTS']}</p>
                            <p><strong>Additional Information:</strong> {selected_row['TEXT / ADDITIONAL INFORMATION / EXAMPLES']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    if st.button("Remove", key=f"remove_{card_index}_{i}_{j}"):
                        remove_card(card_index)
                        st.rerun()

# Display all cards
st.header("All Cards")
cols = st.columns(3)
for idx, row in df.iterrows():
    if pd.notna(row['TITLE']):  # Only display rows with a title
        with cols[idx % 3]:
            # Create button for card selection
            if st.button(f"View Card: {row['TITLE']}", key=f"card_{idx}"):
                st.session_state.displayed_cards.append(idx)
                st.rerun()
            st.markdown(
                f"""
                <div class="card">
                    <h3>{row['TITLE']}</h3>
                    <p><strong>Category:</strong> {row['CATEGORY']}</p>
                    <p><strong>Design Question:</strong> {row['DESIGN QUESTION and PROMPTS']}</p>
                    <p><strong>Additional Information:</strong> {row['TEXT / ADDITIONAL INFORMATION / EXAMPLES']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
