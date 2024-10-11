# Cartoon Caption Annotation Tool

This project includes a tool for generating LLM suggestions for cartoon captions and a Streamlit app for annotating these captions.

## Setup

### Install the required packages

```bash
pip install pandas streamlit openai python-dotenv tqdm pillow requests
```

### OpenAI API Key
Create a `.env` file in the root directory and add your OpenAI API key:
OPENAI_API_KEY=your_api_key_here

## Generating LLM Suggestions

To generate LLM suggestions:

```bash
python generate_llm_suggestions.py
```


## Running the Streamlit App

To run the annotation tool:

```bash
streamlit run annotation.py
```

## FIXME

- Model name is hard-coded in `generate_llm_suggestions.py`
- `load_pre_generated_suggestions()` only looks for gpt-4o right now
- You can't reroll the LLM suggestion once you've seen it


## TODO

- Add a skip button (i.e., "I don't get it")
- Generalize the LLM suggestion pipeline for multiple captions per cartoon
- Add authentication/ login
- Replace csv with external db for multiple users

