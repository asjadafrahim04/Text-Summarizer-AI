import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

def summarizer(rawdocs):
    
    stopwords = list(STOP_WORDS)
    
   
    try:
        nlp = spacy.load('en_core_web_sm')
    except OSError:
        print("ERROR: spaCy model 'en_core_web_sm' not found!")
        print("Run: python -m spacy download en_core_web_sm")
        return "Model not found. Please install spaCy model.", rawdocs, 0, 0
    
    doc = nlp(rawdocs)
    
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq:
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1
    
    if word_freq:
        max_freq = max(word_freq.values())
        for word in word_freq:
            word_freq[word] = word_freq[word] / max_freq
    else:
        
        return rawdocs, rawdocs, len(rawdocs.split()), 0
    
    sent_tokens = [sent for sent in doc.sents]
    
    
    sent_score = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq:
                if sent not in sent_score:
                    sent_score[sent] = word_freq[word.text]
                else:
                    sent_score[sent] += word_freq[word.text]
    
    select_len = max(1, int(len(sent_tokens) * 0.3))
    summary_sentences = nlargest(select_len, sent_score, key=sent_score.get)
    
    summary_sentences.sort(key=lambda x: x.start)
    
    final_summary = ' '.join([sent.text for sent in summary_sentences])
    
    len_original = len(rawdocs.split())
    len_summary = len(final_summary.split())
    
    return final_summary, rawdocs, len_original, len_summary