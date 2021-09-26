# -*- coding: utf-8 -*-
import string
import spacy
from spacy.symbols import NOUN
from pattern.en import conjugate, PAST, PRESENT, SINGULAR, PLURAL

input_string = '''Phil, Bob and Tom are not going to the school and they have fun doing this.'''
tense = 'past'

SUBJ_DEPS = {'agent', 'csubj', 'csubjpass', 'expl', 'nsubj', 'nsubjpass'}

nlp = spacy.load('en_core_web_sm')

# Remove spaces before/after punctuation
def fix_punctuation(text_out: str):
    for char in string.punctuation:
        if char in """(<['""":
            text_out = text_out.replace(char+' ', char)
        else:
            text_out = text_out.replace(' '+char, char)
    for char in ["-", "“", "‘"]:
        text_out = text_out.replace(char+' ', char)
    for char in ["…", "”", "'s", "n't"]:
        text_out = text_out.replace(' '+char, char)
    return text_out

# Returns subjects that are in conjunction with another subject
def _get_conjuncts(tok):
    return [right for right in tok.rights if right.dep_ == 'conj']

# Returns True if noun is in plural
def is_plural_noun(token):
    if token.doc.has_annotation("TAG") is False:
        raise ValueError('token is not POS-tagged')
    return True if token.pos == NOUN and token.lemma != token.lower else False

# Returns all subjects (plus the conjuncted ones)
def get_subjects_of_verb(verb):
    if verb.dep_ == "aux" and list(verb.ancestors):
        return get_subjects_of_verb(list(verb.ancestors)[0])
    subjs = [tok for tok in verb.lefts if tok.dep_ in SUBJ_DEPS]
    subjs.extend(tok for subj in subjs for tok in _get_conjuncts(subj))
    if not len(subjs):
        ancestors = list(verb.ancestors)
        if len(ancestors) > 0:
            return get_subjects_of_verb(ancestors[0])
    return subjs

# Checks if verb needs to be pluralized because there is more than one subject or the subject is in plural
def is_plural_verb(token):
    if token.doc.has_annotation("TAG") is False:
        raise ValueError('token is not POS-tagged')
    subjects = get_subjects_of_verb(token)
    if not len(subjects):
        return False
    plural_score = sum([is_plural_noun(x) for x in subjects])/len(subjects)
    multiple_subjects_singular  = len(subjects)
    return max(plural_score, multiple_subjects_singular) > 1.5

def preserve_caps(word, newWord):
    if word[0] >= 'A' and word[0] <= 'Z':
        newWord = newWord.capitalize()
    return newWord

def identify_person(words):
    subjects = [x.text for x in get_subjects_of_verb(words[-1])]
    if ('I' in subjects) or ('we' in subjects) or ('We' in subjects):
        person = 1
    elif ('you' in subjects) or ('You' in subjects):
        person = 2
    else:
        person = 3
    return person

def identify_number(words):
    if is_plural_verb(words[-1]):
        number = PLURAL
    else:
        number = SINGULAR
    return number

def negation_handler(words, out, tense):
    if words[-2].text + words[-1].text in ('didnot', 'donot', 'willnot', "didn't", "don't", "won't"):
        if tense == PAST:
            out[-2] = 'did'
        elif tense == PRESENT:
            out[-2] = 'do'
        else:
            out.pop(-2)
    return out

def future_perfect_and_progressives_handler(words, out):
    if words[-1].text in ('have', 'has') and len(list(words[-1].ancestors)) and words[-1].dep_ == 'aux':
        out.pop(-1)
    return out

def transform_if_future(words, out, to_tense): 
    if to_tense == 'future':
        if not (out[-1] == 'will' or out[-1] == 'be'):
            out.append('will')
        if words[-2].text == 'will' and words[-2].tag_ == 'NN':
            out.append('will')
    return out

def is_verb_for_modification(words):
    return (words[-2].text == 'will' and words[-2].tag_ == 'MD' and words[-1].tag_ == 'VB') or \
                words[-1].tag_ in ('VBD', 'VBP', 'VBZ', 'VBN') or \
                (not words[-2].text in ('to', 'not') and words[-1].tag_ == 'VB')

def lookup_tense(to_tense):
    tense_lookup = {'future': 'inf', 'present': PRESENT, 'past': PAST}
    tense = tense_lookup[to_tense]
    return tense

def if_not_future_will_remover(words, out):
    if (words[-2].text == 'will' and words[-2].tag_ == 'MD') or words[-2].text == 'had':
        out.pop(-1)
    return out

def set_this_tense(words, tense):
    if words[-2].text in ('were', 'am', 'is', 'are', 'was') or (words[-2].text == 'be' and len(words) > 2 and words[-3].text == 'will'):
        this_tense = tense_lookup['past']
    else:
        this_tense = tense
    return this_tense

def conjugation_params(words, tense):
    tense = set_this_tense(words, tense)
    person = identify_person(words)
    number = identify_number(words)
    return tense, person, number

def deal_with_future_tense(words, out, to_tense):
    out = if_not_future_will_remover(words, out)
    out = transform_if_future(words, out, to_tense)
    return out

def change_tense(text, to_tense, nlp=nlp):
    doc = nlp(text)
    tense = lookup_tense(to_tense)
    out = []
    words = []
    out.append(doc[0].text)
    
    for word in doc:
        words.append(word)
        if len(words) == 1:
            continue
        if(is_verb_for_modification(words)):
            out = deal_with_future_tense(words, out, to_tense)
            out.append(preserve_caps(words[-1].text, conjugate(words[-1].text, conjugation_params(words, tense))))
        else:
            out.append(words[-1].text)
        out = negation_handler(words, out, tense)
        out = future_perfect_and_progressives_handler(words, out)
    return fix_punctuation(' '.join(out))