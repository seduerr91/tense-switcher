from change_tense import *

text_to_change_tense = 'The sun is shining.'
tense1 = 'future' #past, present
tense2 = 'past' #past, present

# change_tense(text_to_change_tense, text_to_change_tense)
print("Original: ", text_to_change_tense)
print("Future: ", change_tense(text_to_change_tense, tense1))
print("Past: ", change_tense(text_to_change_tense, tense2))
