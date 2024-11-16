import json
import random
import pickle
from keras.models import load_model
from nltk.stem import PorterStemmer
import numpy as np
model = load_model('/content/drive/MyDrive/ML_datasets/Final_year_project/Chatbot/chatbot_model.h5')
intents = json.loads(open('/content/drive/MyDrive/ML_datasets/Final_year_project/Chatbot/intents.json').read())
words = pickle.load(open('/content/drive/MyDrive/ML_datasets/Final_year_project/Chatbot/words.pkl','rb'))
classes = pickle.load(open('/content/drive/MyDrive/ML_datasets/Final_year_project/Chatbot/classes.pkl','rb'))
msg = list()
text = str()
ps = PorterStemmer()

def clean_up_sentence(sentence):
    # tokenize the pattern - splitting words into array
    sentence_words = sentence.split(' ')
    # stemming every word - reducing to base form
    sentence_words = [ps.stem(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for words that exist in sentence
def bag_of_words(sentence, words, show_details=True):
    # tokenizing patterns
    sentence_words = clean_up_sentence(sentence)  
    # bag of words - vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,word in enumerate(words):
            if word == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % word)
    return(np.array(bag))

def predict_class(sentence):
    # filter below  threshold predictions
    p = bag_of_words(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sorting strength probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def responsed(msg1):
    msg.append(msg1)
    ints = predict_class(msg1)
    res = getResponse(ints, intents)
    return res,ints

def chat(msg):
    try:
        res,ints = responsed(msg)
        return res,ints
    except:
        return -1,-1

# print("Chatbot : Hey there, Wassup ?")
# # responded function takes text of user and returns chatbot output
# for i in range(999999):
#     m = input("User : ")
#     try:
#       res,ints = responsed(m)
#       print("Chatbot : "+res)
#       if ints[0]['intent']== 'goodbye':
#         break
#     except:
#       print("Sorry,I coundt understand")