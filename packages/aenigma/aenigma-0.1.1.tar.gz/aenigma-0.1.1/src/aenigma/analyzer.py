from nltk import download,data,word_tokenize
from syllables import estimate
from statistics import mean

def initialize_nltk():
    '''Downloads punkt nltk package'''
    download('punkt') # Downlaods the Punkt tokenizer


def generate_rcs_list(text: str) -> list:
    '''Takes in a body of text, returns a list of tuples composed of sentences and their relative complexity scores'''
    tokenizer = data.load('tokenizers/punkt/english.pickle') # Load tokenizer
    sentences = tokenizer.tokenize(text) # Generate list of sentences
    chars_to_strip = ',.?!:' # Declare punctuation to strip out when calculating word and syllable counts
    word_counts = [len(word_tokenize(sentence.translate({ord(i): None for i in chars_to_strip}))) for sentence in sentences] # Determine word count for each sentence
    syllable_counts = [sum([estimate(word) for word in word_tokenize(sentence.translate({ord(i): None for i in chars_to_strip}))]) for sentence in sentences] # Determine syllable count for each sentence
    fkscores = [(206.835-(1.015*word_counts[i])-84.6*(syllable_counts[i]/word_counts[i])) for i in range(0, len(word_counts))] # Determine Flesch-Kincaid score for each sentence
    mean_fkscore = mean(fkscores) # Find the mean Flesch-Kincaid score
    return [(sentences[j], round(((((mean_fkscore-fkscores[j])/mean_fkscore)+2)/4),2)) for j in range(0, len(sentences))] # Return a tuple of the sentences and their Relative Complexity Score