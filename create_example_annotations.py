import pandas as pd

df = pd.read_csv("./caption_contest_data.csv")[["contest_number", "image_url", "human_description", "top_caption_1"]]

examples = [
    '''STRUCTURAL ELEMENT: Double meaning of "common"
    Explanation: The caption uses "common" to mean both "commoner" (as opposed to the king) and "common cold". This clever connection resolves the juxtaposing elements of the cartoon: the king and the doctor's office setting.

    STRUCTURAL ELEMENT: Mild diagnosis with stern tone
    Explanation: The doctor's relatively mild diagnosis is delivered with a stern tone. This is humorous because the patient is a king, who would likely despise anything "common".

    COGNITIVE MECHANISM: Mockery of royal sensibilities
    Explanation: Typically, being told something is "worse than a cold" would imply a serious condition. However, the punchline reveals it's actually a milder, more ordinary ailment.''',

    '''STRUCTURAL ELEMENT: "Whistle while you work" reference
    Explanation: This phrase refers to a musical number in the 1937 movie Snow White, involving animals joyfully working together. The characters in the cartoon are Snow White and the Seven Dwarfs, directly connecting to this reference.

    COGNITIVE MECHANISM: Corporate speak in fairytale setting
    Explanation: The use of "Workplace Morale" juxtaposes the fairytale setting. The caption "explains" the rollerskates as a workplace morale booster, creating a humorous contrast.''',

    '''STRUCTURAL ELEMENT: Wordplay with "raze" and "raise"
    Explanation: The caption mixes "raze a village" (as in, to burn down) with "raise a family". This pun connects the juxtaposing elements of the barbarians, who might burn down a village, with a wedding, which is about starting a family.

    COGNITIVE MECHANISM: Resolves incongruity
    Explanation: The juxtaposing elements of the wedding and barbarians are tied together by the wordplay.''',

    '''COGNITIVE MECHANISM: Absurd implication
    Explanation: The tiny person's comment implies that the regular sized person deemed the pizza "not what we ordered", and that it was taken as a personal insult.''',
    
    '''STRUCTURAL ELEMENT: Reference to common magic trick
    Explanation: Sawing an assistant in half is a canonical magic trick for stage magicians. The character on the bench is dressed as a stage magician, directly connecting to this reference.

    STRUCTURAL ELEMENT: "When was the last time you saw them" trope
    Explanation: This is a commonly referenced phrase in depictions of criminal court. The judge in the cartoon appears to be barking at the magician, fitting this context.

    COGNITIVE MECHANISM: Absurd implication
    Explanation: The judge specifying "either half" implies that the last time the magician saw the victim, they were still in half, and that a crime was committed during the magic show. This prompts the viewer to imagine the cartoon characters in this comedic situation.'''
]

# Limit the DataFrame to the length of the examples
df = df.head(len(examples))

for index, row in df.iterrows():
    # Add the example to the DataFrame
    df.loc[index, 'example'] = examples[index]

# Save as data/trope_detection_ICL_examples.csv
df.to_csv("./trope_detection_ICL_examples.csv", index=False)

