import re
import nltk
import random
import string

try:
    STOPWORDS = set(nltk.corpus.stopwords.words('english'))
except:
    nltk.download("stopwords")
    nltk.download('punkt')
    STOPWORDS = set(nltk.corpus.stopwords.words('english'))

BOOLEAN_STRINGS = ["true", "false", "yes", "no", "1", "0"]

def multi_space_to_single_space(string):
    return re.sub(' +', ' ', string)

def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False
    
def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
    
def generate_random_str(size: int=6, chars=string.ascii_uppercase + string.digits)-> string:
    return ''.join(random.choice(chars) for _ in range(size))

def remove_punctuation(string):
    # The thrid argument of str.maketrans is a string of characters to be removed
    return string.translate(str.maketrans('', '', string.punctuation))
