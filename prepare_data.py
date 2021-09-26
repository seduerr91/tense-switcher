import nltk
import os

# Removing this line will cause downloading
# of the wordnet data on each request
nltk.download('wordnet')
nltk.download('wordnet_ic')
nltk.download('sentiwordnet')
os.system("ls /root/nltk_data/corpora")
