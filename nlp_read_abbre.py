'''find the real meaning from abbrevation
this function helps to read the original text
read it into human understandable form
then we can use the result from this function 
to find the tone of the sentence or censored bad words'''
import dill
import pandas as pd

abbre_df = pd.read_csv("nlp_abbre_en.csv")
abbre_dict=df.set_index('abbre')['meaning'].to_dict()

def read_abbre(word):
    read_abbre=""
    for i in word.split():
        for k,v in abbre_dict.items():
            if i in k:
                i = i.replace(k,v) 
        read_abbre = read_abbre+" "+i
    return read_abbre
    
#with open('/read_abbre.pkl', 'wb') as f:
#    dill.dump(abbre_df, f)
#    dill.dump(abbre_dict, f)
#    dill.dump(read_abbre, f)
