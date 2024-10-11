import pandas as pd
import random
import os
from tqdm import tqdm
from llm_annotation import analyze_cartoon_caption


model = "gpt-4o-mini"

# Load the main dataset
data_file = "./caption_contest_data.csv"
df = pd.read_csv(data_file)[["contest_number", "image_url", "human_description", "top_caption_1"]]

# Load the examples dataset
examples_file = "./trope_detection_ICL_examples.csv"
examples_df = pd.read_csv(examples_file)

# Number of suggestions to generate per entry
NUM_SUGGESTIONS = 2

# Initialize a dictionary to store suggestions
suggestions_dict = {}

for index, row in tqdm(df.iterrows(), total=len(df)):
    if index > 3:
        break
    key = (row['contest_number'], row['top_caption_1'])
    suggestions = []
    for _ in range(NUM_SUGGESTIONS):
        print(f"Generating suggestion {_ + 1} for {key}")
        suggestion = analyze_cartoon_caption(row, examples_df, model=model)
        suggestions.append(suggestion)
    suggestions_dict[key] = suggestions

# Convert the dictionary to a DataFrame for easier handling
suggestions_df = pd.DataFrame([
    {
        'contest_number': key[0],
        'caption': key[1],
        'suggestions': suggestions
    }
    for key, suggestions in suggestions_dict.items()
])

# Convert suggestions list to string before saving
suggestions_df['suggestions'] = suggestions_df['suggestions'].apply(lambda x: str(x))

# Save the pre-generated suggestions
output_dir = "./pre_generated_llm_suggestions"
os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(output_dir, f"{model}.csv")
suggestions_df.to_csv(output_file, index=False)

print(f"Pre-generated LLM suggestions saved to {output_file}")
