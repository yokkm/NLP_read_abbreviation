#from platform import python_version
#print(python_version())
## check current python kernals

#reads read_abbre_main.py
#reads sonar_func.py
from read_abbre_main import *
from sonar_func import *

import warnings
warnings.filterwarnings('ignore')

import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob, Word, Blobber
import tensorflow as tf
from tensorflow.python.keras.backend import set_session
sid = SentimentIntensityAnalyzer()

# Explore vocabulary
import collections
from tqdm import tqdm

from profanity_check import predict, predict_prob
from nltk.tokenize import sent_tokenize, word_tokenize

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from pyspark.sql.types import *

cwd = os.getcwd()
CorrectRepeat_path = os.path.join(cwd, "correct_repeatedBadWords.pkl")
Modeling_path = os.path.join(cwd, "New_allcalled.pkl")

with open(CorrectRepeat_path, 'rb') as f:
    correct_repeatedBadWords=dill.load(f)
    badwords_lst=dill.load(f)
    typeof_bad = dill.load(f)
    badwords = dill.load(f)##
    
with open(Modeling_path, 'rb') as c:
    model = dill.load(c)
    classifier = dill.load(c)
    predictions = dill.load(c)
    dialogue_act_features = dill.load(c)
    max_len = dill.load(c)
    tokenizer = dill.load(c)
import warnings
warnings.filterwarnings('ignore')

def chkchk(word):
    new_words_list=[]
    for index,item in enumerate(word.split()):
        for e in badwords['word']:
            if e == item:
                new_words_list.append(e)
    return new_words_list

def censor(word):
    new_words_list=''
    for i,item in enumerate(word.split()):
        if predict_prob([item])>=0.3 or item in chkchk(word):#(e for e in badwords['word'] if e == item ):#any(badword in item for badword in badwords_lst):
            item = item[0]+'*'*len(item[1:])
        new_words_list += item+" "
        
    return new_words_list
    
'''
a=' 1 h8 night nigga nude fuckkk shittt school mass fuckkkkkkkkkk shooting mast3rb8 suicide retards kill myself m0th3rfuck3r 2MORO'
print('original txt::', a)
print()
print('readable txt::',abbre_then_replace(a) )
print()
print('censored txt::',censor(abbre_then_replace(a)))
print(sonar_check(abbre_then_replace(a)))

#### Expect output ####
# original txt::  1 h8 night nigga nude fuckkk shittt school mass fuckkkkkkkkkk shooting mast3rb8 suicide retards kill myself m0th3rfuck3r 2MORO
# readable txt:: i hate night night nude fuck shitty school mass fuck shooting masturbate suicide retards kill myself motherfucker tomorrow
# censored txt:: i hate night night n*** f*** s***** school mass f*** shooting m********* s****** r****** k*** myself m*********** tomorrow 
# ('hate_speech', 0.5964515083599946, 0.4033855317557128, 0.00016295988429268054)
'''

#6



def comment_type(string):
    s=[]
    com_type=[]
    for i in string.split():
        ss = sid.polarity_scores(i)
        top = ss['compound']
        s.append([top,i])
        com_type.append(i)
    a=min(s)
    min_word = a[1]
    min_word_score = a[0]

    for k in typeof_bad:
        for val in typeof_bad[k]:
            if min_word == val:
                return k
            
    for i in com_type:
        for k in typeof_bad:
            for val in typeof_bad[k]:
                if i == val:
                    return k
    return 'None'
    
#this function reads sentence clean it clean abbreviations then return the toxicity level

def toxicity_level(text):
	### For testing json### please refer to test_sample.json
    #with open("/home/user/Downloads/test_sample.json", "r") as file:
        #text = json.load(file)
        #text = text['comment_text']

#     if request.method =='POST':
#         text = request.json
#         text = text['comment_text']#key: comment_text
        typeflag=''
        line = text
        removerepeatword=abbre_then_replace(text)#correct_repeatedBadWords(text)
        ans=classifier.classify(dialogue_act_features(removerepeatword))
        ss = sid.polarity_scores(removerepeatword)
        sonar_topclass,sonar_hate_score,sonar_offen_score,sonar_none_score = sonar_check(removerepeatword)




        new_words_list = []
        type_tag=[]





        # Process string
        new_string = [removerepeatword]
        new_string = tokenizer.texts_to_sequences(new_string)
        new_string = pad_sequences(new_string, maxlen=max_len, padding='post', truncating='post')


        # Predict
        prediction = model.predict(new_string).tolist()
        #find comment type
        comm_type =comment_type(removerepeatword)

        if comm_type =='obscence':
            typeflag=3
        elif comm_type =='threat' or comm_type =='racial slur'or comm_type=='gender slur' or comm_type =='ethnic slur':
            typeflag=4
        elif comm_type =='None':
            typeflag=1
        elif comm_type =='swear words' or comm_type =='sarcasm':
            typeflag=2
        else:typeflag=1
            

	#[0][0] toxicity
        if sonar_topclass =='neither':
            if ss['compound'] <0:
            #'''tentative to be really harm or a threat need immediately attention'''
            #i will cut myself, and let it bleed
                flag = 4
                new_words_list = censor(removerepeatword)
            elif ss['compound'] <0 and typeflag == 1:
                flag = 4
                new_words_list = censor(removerepeatword)
            else:
                flag=0
                new_words_list = censor(removerepeatword)

        else:
            if sonar_topclass !='neither':
                if ss['pos'] >=0.4 and sonar_none_score >=0:
                    new_words_list = removerepeatword
                    flag = 1
                elif ss['compound'] <=0.05 and ss['neg']>= 0.75:
               # '''comment tend to contain extremely rude/ 
                #offensive comment then will hide but will sent alert as 2'''
                    if typeflag!= 1 and typeflag!=2 and typeflag!=3:
                        new_words_list = censor(removerepeatword)
                        flag =3
                    else:
                        cc='Whole comment is hide'
                        new_words_list.append(cc)
                        flag=2
                elif ss['compound'] <=0.05 and ss['neg']< 0.75:
                    new_words_list = censor(removerepeatword)
                #let's go to the beach bitches
                    flag=3
                else:
                    new_words_list = censor(removerepeatword)
                #i love you asshole
                    flag=1
            else:
                pass

        



        joinwords = "".join(new_words_list)
        printdict = {"OriginalText":text,"FinalOutput":joinwords, "HatespeechType":comm_type
                     , "CommentTag":ans,"AlertLevel": flag, "HatespeechTag":typeflag
                    ,"ss['compound']":ss['compound'],"ss['neg']":ss['neg'],"ss['pos']":ss['pos']
                    ,"sonar_topclass":sonar_topclass,"sonar_hate_score":sonar_hate_score
                     ,"sonar_offen_score":sonar_offen_score,"sonar_none_score":sonar_none_score}
        

        return printdict#jsonify(printdict)
#     else:
#         return None
