import streamlit as st
import pandas as pd
from datasets import Dataset
import requests
from PIL import Image
from io import BytesIO
import os
from llm_annotation import analyze_cartoon_caption
import random

# Load the CSV file from a local path
@st.cache_data
def load_data():
    file_path = './caption_contest_data.csv'
    return pd.read_csv(file_path)

# Save the annotations to a new CSV file
def save_annotations(data, file_path):
    data.to_csv(file_path, index=False)

# Convert the DataFrame to a HuggingFace Dataset
def convert_to_hf_dataset(file_path):
    data = pd.read_csv(file_path)
    
    # Enforce data types
    print("Flagging that this was called")
    data['contest_number'] = data['contest_number'].astype(int)
    data['image_url'] = data['image_url'].astype(str)
    data['caption'] = data['caption'].astype(str)
    data['element_1'] = data['element_1'].astype(str)
    data['element_2'] = data['element_2'].astype(str)
    data['element_3'] = data['element_3'].astype(str)
    data['element_4'] = data['element_4'].astype(str)
    
    return Dataset.from_pandas(data)

# Initialize session state for annotations
if 'annotated_data' not in st.session_state:
    if os.path.exists("output.csv") and os.path.getsize("output.csv") > 0:
        st.session_state.annotated_data = pd.read_csv("output.csv")
    else:
        st.session_state.annotated_data = pd.DataFrame(columns=[
            'image_url', 'contest_number', 'caption',
            'element_1', 'element_2', 'element_3', 'element_4'
        ])

# Initialize session state for accepted suggestions
if 'accepted_suggestions' not in st.session_state:
    st.session_state.accepted_suggestions = set()

# Initialize session state for rejected suggestions
if 'rejected_suggestions' not in st.session_state:
    st.session_state.rejected_suggestions = set()

# Initialize session state for clearing fields
if 'clear_fields' not in st.session_state:
    st.session_state.clear_fields = False

# Initialize session state for LLM suggestions
if 'llm_suggestion' not in st.session_state:
    st.session_state.llm_suggestion = []

# Callback function to accept a suggestion
def accept_suggestion(element_index, value):
    # Find the first empty element
    for i in range(1, 5):
        if not st.session_state.get(f"element_{i}"):
            st.session_state[f"element_{i}"] = value
            break
    st.session_state.accepted_suggestions.add(element_index)

# Callback function to reject a suggestion
def reject_suggestion(element_index):
    st.session_state.rejected_suggestions.add(element_index)  # Mark as rejected
    st.warning(f"Rejected suggestion {element_index + 1}")

# Streamlit UI
st.title("Joke Explanation Annotation Pipeline")

# Load data
data = load_data()

# Input for jump to contest number
jump_to_contest = st.number_input("Jump to row", min_value=0, max_value=len(data)-1, value=0)

# Initialize session state for current index
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
# Update current index if jump to contest is used
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("Go!", use_container_width=True):
        st.session_state.current_index = jump_to_contest
        # Reset suggestions when navigating to a new cartoon
        st.session_state.accepted_suggestions = set()
        st.session_state.rejected_suggestions = set()
        st.session_state.llm_suggestion = []
        st.rerun()

# Ensure current_index is within bounds
st.session_state.current_index = min(st.session_state.current_index, len(data)-1)

# Display the current row
current_row = data.iloc[st.session_state.current_index]
# st.write(current_row)

# Display the contest number
st.markdown(f"<h3 style='text-align: center;'>Contest {current_row['contest_number']}</h3>", unsafe_allow_html=True)

# Display the image
image_url = current_row['image_url']
try:
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image(img, width=400, use_column_width=True)
except Exception as e:
    st.error(f"Error loading image: {e}")

# Display the description and top caption
st.markdown(f"<h4 style='text-align: center;'>{current_row['top_caption_1']}</h4>", unsafe_allow_html=True)
st.markdown(f"<text style='text-align: center;font-size: 20px;color: gray;'>{current_row['human_description']}</text>", unsafe_allow_html=True)

# Removed the functionality that checks for existing annotations to improve performance

# Load pre-generated LLM suggestions
@st.cache_data
def load_pre_generated_suggestions():
    file_path = './pre_generated_llm_suggestions/gpt-4o-mini.csv'
    return pd.read_csv(file_path)

pre_generated_suggestions = load_pre_generated_suggestions()

def get_llm_suggestion():
    key = (current_row['contest_number'], current_row['top_caption_1'])
    # Filter the suggestions for the current cartoon and caption
    suggestions_row = pre_generated_suggestions[
        (pre_generated_suggestions['contest_number'] == key[0]) &
        (pre_generated_suggestions['caption'] == key[1])
    ]
    
    if suggestions_row.empty:
        st.error("No pre-generated suggestions available for this entry.")
        return
    
    suggestions = suggestions_row.iloc[0]['suggestions']
    # Convert string representation of list back to actual list
    suggestions = eval(suggestions)
    
    if not suggestions:
        st.error("No suggestions found.")
        return
    
    # Choose a random suggestion
    selected_suggestion = random.choice(suggestions)
    st.session_state.llm_suggestion = [selected_suggestion]

llm_suggestion = {}
examples_df = pd.read_csv("./trope_detection_ICL_examples.csv")

# Replace the existing "Get LLM Suggestion" button and spinner with this:
col1, col2 = st.columns([2, 3])
with col1:
    if st.button("Get LLM Suggestion", use_container_width=True):
        with col2:
            with st.spinner("Generating LLM suggestions..."):
                get_llm_suggestion()

# Display LLM suggestions with individual accept and reject buttons
if 'llm_suggestion' in st.session_state and st.session_state.llm_suggestion:
    for index, value in enumerate(st.session_state.llm_suggestion):
        if index in st.session_state.accepted_suggestions or index in st.session_state.rejected_suggestions:
            continue  # Skip rendering if already accepted or rejected

        col1, col2, col3 = st.columns([7, 2, 2])
        with col1:
            st.text_area(
                f"LLM Suggestion {index + 1}",
                value=value,
                key=f"llm_suggestion_{index}",
                height=100,
                disabled=True,
                label_visibility="collapsed"
            )
        with col2:
            st.button(
                f"Accept",
                key=f"accept_suggestion_{index}",
                on_click=accept_suggestion,
                args=(index, value),
                use_container_width=True
            )
        with col3:
            st.button(
                f"Reject",
                key=f"reject_suggestion_{index}",
                on_click=reject_suggestion,
                args=(index,),
                use_container_width=True
            )

    # Update the annotations list after accepting suggestions
    annotations = [
        st.session_state.get(f"element_{i+1}", "") for i in range(4)
    ]

# Annotation inputs
annotations = []
for i in range(4):
    element_col = f"element_{i+1}"
    # Check if fields should be cleared
    if st.session_state.clear_fields:
        default_value = ""
    else:
        default_value = st.session_state.get(element_col, "")
    
    annotation = st.text_area(f"Element {i+1}", value=default_value, key=element_col)
    annotations.append(annotation)

# Reset the clear_fields flag
if st.session_state.clear_fields:
    st.session_state.clear_fields = False

# Save annotation and move to next
if 'processing' not in st.session_state:
    st.session_state.processing = False

if st.session_state.processing:
    st.warning("Processing your annotation...")
else:
    if st.button("Next"):
        st.session_state.processing = True
        with st.spinner('Saving annotation...'):
            # Create a new row for the annotation
            new_row = pd.DataFrame([{
                'contest_number': current_row['contest_number'],
                'image_url': current_row['image_url'],
                'caption': current_row['top_caption_1'],
                'element_1': annotations[0] if len(annotations) > 0 else "",
                'element_2': annotations[1] if len(annotations) > 1 else "",
                'element_3': annotations[2] if len(annotations) > 2 else "",
                'element_4': annotations[3] if len(annotations) > 3 else ""
            }])
            
            # Remove existing annotation if it exists
            st.session_state.annotated_data = st.session_state.annotated_data[
                ~(
                    (st.session_state.annotated_data['contest_number'] == current_row['contest_number']) &
                    (st.session_state.annotated_data['caption'] == current_row['top_caption_1'])
                )
            ]
            
            # Append the new annotation
            st.session_state.annotated_data = pd.concat(
                [st.session_state.annotated_data, new_row],
                ignore_index=True
            )
            
            # Save the updated annotations
            save_annotations(st.session_state.annotated_data, "output.csv")
        
        # Move to the next index **after** saving
        st.session_state.current_index += 1
        if st.session_state.current_index >= len(data):
            st.session_state.current_index = 0

        # Reset suggestions for the new cartoon
        st.session_state.accepted_suggestions = set()
        st.session_state.rejected_suggestions = set()
        st.session_state.llm_suggestion = []
        
        # Set the flag to clear fields
        st.session_state.clear_fields = True
        
        st.session_state.processing = False
        st.rerun()

# Usage:
# python -m streamlit run annotation.py