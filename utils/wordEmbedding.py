import numpy as  np
import pandas as pd
import spacy

def poem_generator(verses, word, n_sents=4):
    nlp = spacy.load("es_core_news_lg")
    init_str = nlp(word)
    sentences=pd.DataFrame.from_dict(verses)
    sup_index= sentences.shape[0]
    poem_id = int()
    poem =[]
    for i in range(n_sents):
        rand_sent_index = np.random.randint(0, sup_index, size=30)
        sent_list = list(sentences.sentence.iloc[rand_sent_index])
        docs = nlp.pipe(sent_list)
        sim_list = []
        for sent in docs:
            similarity = (init_str.similarity(sent))
            sim_list.append(similarity)
        df_1 = pd.DataFrame({'similarity' : sim_list, 'doc_id' : sentences.doc_id.iloc[rand_sent_index] }, index=rand_sent_index)
        df_1 = df_1[df_1.doc_id != poem_id]
        df_1.sort_values(by='similarity', inplace=True, ascending=False)
        sent_index= df_1.index[0]
        sent = sentences.sentence[sent_index]
        replace_dict = {'\n' :  '', '\r' :  ''}
        for x,y in replace_dict.items():
            sent = sent.replace(x, y)
        poem.append(sent)    
        poem_id = df_1.doc_id.iloc[0]
        init_str = nlp(sent) 
    return poem

def format_poem(text):
    text = text[:1].upper() + text[1:]
    text = text[:] + '.'
    return text
