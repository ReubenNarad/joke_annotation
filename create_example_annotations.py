import pandas as pd

df = pd.read_csv("./caption_contest_data.csv")[["contest_number", "image_url", "human_description", "top_caption_1"]]

examples = {}


examples[660] = '''The caption plays on the double meaning of "common" to mean both "commoner" (as opposed to the king) and "common cold".
The caption mocks royal sensibilities-- despite "common" meaning mild, because the king dislikes "common" things, he's told it is worse.'''
examples[661] = '''This refers to a musical number "Whistle While You Work" in the 1937 movie Snow White, involving animals joyfully working together. The characters in the cartoon are Snow White and the Seven Dwarfs, directly connecting to this reference.
The use of "Workplace Morale" juxtaposes the fairytale setting. The caption "explains" the rollerskates as a workplace morale booster, creating a humorous contrast.'''
examples[662] = '''The caption uses wordplay with "raze a village" (as in, to burn down) with "raise a family".'''
examples[663] = '''The tiny person's comment implies that the regular sized person deemed the pizza "not what we ordered", and that it was taken as a personal insult.'''
examples[664] = '''Connects the theme of limited visibility of a person to the court setting (a witness sees a victim) to the magic trick of sawing a person in half (seeing only one half at a time).'''
examples[665] = '''The Shark is implying that the person is the groceries, playing on the idea that sharks eat people.
The phrase is a common lighthearted sentence, contrasting with the shark's dark intention.'''
examples[666] = '''The therapist sitting in an ear would connect the furniture to their respective roles; The patient speaking is in a mouth, so the therapist listening would be in an ear.'''
examples[667] = '''Tearing down walls for an "open floor plan" is a trope in home rennovation shows.
An "open floor plan" maze would be easier for the mice, as they could bypass the maze and go right to the cheese.
An "open floor plan" would be easier to assemble, a common frustration when assembling Ikea-style furniture.'''
examples[668] = '''This plays on dual meanings of "burn", as in the literal act of burning, and the figurative act of being hurt.'''
examples[669] = '''This plays on dual meanings of "routine", as in a child's bedtime routine, and a comedian's standup routine.'''
examples[671] = '''The mammoth implies that the tiny cavemen are lighting fires on its back, which would be uncomfortable.
The caption plays on the hypothesis that humans' discovery of fire caused the overhunting of mammoths, leading to their extinction.'''
examples[672] = '''It is implied that the medicine being prescried caused the doctor to look like a mouse.
It is a trope for doctors to experiment with the medicine they prescribe.'''
examples[673] = '''Calling the prince "Dave" and pointing out that he's 35 subverts the fairytale theme of Rapunzel, replacing it with a snarky modern tone.'''
examples[674] = '''This plays on the trope of dogs fighting over a ball in a park, framing the werewolf as just a really scary dog.
The light common phrase juxtaposes the dire situation.'''
examples[675] = '''This plays on the double meaning of "oddly suited", as in the figurative meaning of being well matched, and the literal meaning of wearing odd suits for the occasion.'''
examples[676] = '''This refers to the term "hunter-gatherer", implying that the wife is criticizing his hunting.
It is a trope for couples to dole specific responsibilities, then criticise the other person's performance.'''
examples[677] = '''The cat is directing the human to upgrade its food to the fancy human tuna, playing on the idea that cats only like humans because they feed them.
Giving a cat Ahi tuna is outrageous, as it is a very expensive type of tuna.'''
examples[678] = '''The caption plays on the dual meaning of "wind up", as in the figurative meaning of ending up together, and the literal fact that their necks are wound up.'''
examples[679] = '''Succulents are known for being easy to take care of.
A mad king executing his friends and allies is a trope.'''
examples[680] = '''Fish on menus are often unavailable, and in this setting, it's because the bear is catching the fish to order.
The dismissive tone of the customer ignores the obvious effort the bear is making to catch the fish.'''
examples[681] = '''This plays on the dual meaning of "pinch," as in inappropriately grabbing someone's butt, and literally pinching with his crab pincers.
It also plays on the dual meaning of being in "hot water", as in being scolded, and being boiled like a crab.'''



# Limit the DataFrame to the length of the examples
df = df.head(len(examples))

for index, row in df.iterrows():
    # Add the example to the DataFrame
    df.loc[index, 'example'] = examples[row['contest_number']]

# Save as data/trope_detection_ICL_examples.csv
df.to_csv("./trope_detection_ICL_examples.csv", index=False)

