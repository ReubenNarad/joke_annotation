import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO, StringIO
import os
import random
import boto3
import json
import time
import numpy as np
from streamlit.components.v1 import html

# S3 Configuration
s3 = boto3.client('s3',
    aws_access_key_id=st.secrets["aws_credentials"]["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=st.secrets["aws_credentials"]["AWS_SECRET_ACCESS_KEY"],
    region_name=st.secrets["aws_credentials"]["AWS_DEFAULT_REGION"]
)
BUCKET_NAME = 'joke-annotation'

# Load the CSV file from a local path
@st.cache_data(ttl=3600, max_entries=1)
def load_data():
    file_path = './caption_contest_data.csv'
    df = pd.read_csv(file_path)
    # Ensure all caption columns exist
    required_cols = ['top_caption_1', 'top_caption_2', 'top_caption_3']
    for col in required_cols:
        if col not in df.columns:
            df[col] = ''
    return df

# Initialize session state for annotations
if 'annotated_data' not in st.session_state:
    st.session_state.annotated_data = pd.DataFrame(columns=[
        'image_url', 'contest_number', 'caption',
        'element_1', 'element_2', 'element_3', 'element_4'
    ])

# Initialize session state for clearing fields
if 'clear_fields' not in st.session_state:
    st.session_state.clear_fields = False

# Initialize session state for current index and caption
if 'current_index' not in st.session_state:
    data = load_data()
    st.session_state.current_index = random.randint(0, len(data)-1)
    st.session_state.current_caption_idx = random.randint(0, 2)

# Function to upload annotation to S3
def upload_annotation_to_s3(annotation_data):
    timestamp = int(time.time())
    filename = f"annotation_{timestamp}.json"
    try:
        # Convert int64 to int for JSON serialization
        for key, value in annotation_data.items():
            if isinstance(value, np.int64):
                annotation_data[key] = int(value)
        
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=filename,
            Body=json.dumps(annotation_data),
            ContentType='application/json'
        )
        st.success(f"Saved!")
    except Exception as e:
        st.error(f"Failed to upload annotation to S3: {e}")

# Add this function near the top with other function definitions
def scroll_to_top():
    # Javascript to scroll to the top of the page
    js = '''
        <script>
            window.parent.document.querySelector('section.main').scrollTo(0, 0);
        </script>
    '''
    html(js)

# Add this near the top of the UI section, before the title
tab1, tab2 = st.tabs(["Annotate", "Examples"])

with tab1:
    # Move all existing UI content here
    st.title("Joke Explanation Annotation Pipeline")
    
    # Use the stored session state instead of reloading
    data = load_data()
    current_row = data.iloc[st.session_state.current_index]
    caption_col = f'top_caption_{st.session_state.current_caption_idx + 1}'
    current_caption = current_row[caption_col]

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

    # Display the caption and description
    st.markdown(f"<h4 style='text-align: center;'>{current_caption}</h4>", unsafe_allow_html=True)
    st.markdown(f"<text style='text-align: center;font-size: 20px;color: gray;'>{current_row['human_description']}</text>", unsafe_allow_html=True)

    # Update the index and caption index without rerunning
    if st.button("Skip", type="secondary"):
        st.session_state.current_index = random.randint(0, len(data)-1)
        st.session_state.current_caption_idx = random.randint(0, 2)
        st.session_state.clear_fields = True
        scroll_to_top()

    # Use session state to control form display
    if 'submitted' in st.session_state and st.session_state.submitted:
        st.success("Annotation saved!")
        st.session_state.submitted = False
    else:
        with st.form(key='annotation_form'):
            annotations = []
            for i in range(4):
                element_col = f"element_{i+1}"
                default_value = "" if st.session_state.clear_fields else st.session_state.get(element_col, "")
                annotation = st.text_area(f"Component {i+1}", value=default_value, key=element_col)
                annotations.append(annotation)

            submit_button = st.form_submit_button("Next")
            
            if submit_button:
                st.session_state.submitted = True
                st.session_state.annotations = annotations
                scroll_to_top()
                # No rerun needed, just update the UI

    # Handle form processing outside the form
    if st.session_state.get('submitted', False):
        with st.spinner('Saving annotation...'):
            annotation_dict = {
                'contest_number': current_row['contest_number'],
                'image_url': current_row['image_url'],
                'caption': current_caption,
                'element_1': st.session_state.annotations[0] if len(st.session_state.annotations) > 0 else "",
                'element_2': st.session_state.annotations[1] if len(st.session_state.annotations) > 1 else "",
                'element_3': st.session_state.annotations[2] if len(st.session_state.annotations) > 2 else "",
                'element_4': st.session_state.annotations[3] if len(st.session_state.annotations) > 3 else "",
                'timestamp': int(time.time())
            }
            upload_annotation_to_s3(annotation_dict)
            
            # Clear old states before setting new ones
            for key in list(st.session_state.keys()):
                if key.startswith('element_'):
                    del st.session_state[key]
            
            # Choose new random cartoon and caption
            st.session_state.current_index = random.randint(0, len(data)-1)
            st.session_state.current_caption_idx = random.randint(0, 2)
            st.session_state.clear_fields = True
            st.session_state.submitted = False
            
            # Clear the annotations from session state
            if 'annotations' in st.session_state:
                del st.session_state.annotations
                
            # Force clear cache for the current page
            st.cache_data.clear()
            
            scroll_to_top()
            st.rerun()

    # Reset clear_fields after the form is displayed
    st.session_state.clear_fields = False

with tab2:
    st.title("Examples")
    
    # Load examples data
    examples_df = pd.read_csv("./trope_detection_ICL_examples.csv")
    
    for _, row in examples_df.iterrows():
        with st.container():
            # Display contest number (centered)
            st.markdown(f"<h3 style='text-align: center;'>Contest {row['contest_number']}</h3>", unsafe_allow_html=True)
            
            # Display the image
            try:
                response = requests.get(row['image_url'])
                img = Image.open(BytesIO(response.content))
                col1, col2, col3 = st.columns([1,2,1])
                with col2:
                    st.image(img, width=400, use_column_width=True)
            except Exception as e:
                st.error(f"Error loading image: {e}")
            
            # Display the caption (centered)
            st.markdown(f"<h4 style='text-align: center;'>{row['top_caption_1']}</h4>", unsafe_allow_html=True)
            
            # Display the example annotation as bullet points
            st.markdown(f"**Example Annotation:**")
            # Split the example text on newlines and create bullet points
            points = row['example'].split('\n')
            for point in points:
                if point.strip():  # Only create bullet point if there's content
                    st.markdown(f"• {point.strip()}")
            
            # Add a divider between examples
            st.divider()

# Usage:
# python -m streamlit run app.py

