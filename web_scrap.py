import subprocess
import sys

# Function to install packages if not installed properly through pip
def install_package(package_name):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"'{package_name}' installed successfully!")
    except Exception as e:
        print(f"Error installing '{package_name}': {e}")

# Install required packages
install_package("requests-html")
install_package("readability-lxml")
install_package("lxml_html_clean directly")
install_package("lxml[html_clean]")
install_package("newspaper3k")
from requests_html import HTMLSession
from readability import Document
from bs4 import BeautifulSoup
import pandas as pd
from newspaper import Article
import nltk
nltk.download('punkt_tab')
from nltk.tokenize import sent_tokenize,word_tokenize
import os
import re
import emoji
import string,time
string.punctuation
import csv

out_file = "Output Data Structure.csv"
with open(out_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(["URL_ID","POSITIVE SCORE","NEGATIVE SCORE","POLARITY SCORE","SUBJECTIVITY SCORE","AVG SENTENCE LENGTH","PERCENTAGE OF COMPLEX WORDS","FOG INDEX","AVG NUMBER OF WORDS PER SENTENCE","COMPLEX WORD COUNT","WORD COUNT","SYLLABLE PER WORD","PERSONAL PRONOUNS","AVG WORD LENGTH"])


input=pd.read_csv('Input.csv')
for index,rows in input.iterrows():
    url=rows['URL']
    uid=rows['URL_ID']
    
    # Create an HTML session and get the webpage content
    
    article = Article(url)
    article.download()
    article.parse()

    article =article.title+article.text
    file_name = f"{uid}.txt"  # Dynamically generate the file name

    with open(file_name, "w", encoding="utf-8") as file:
        file.write(article)

    print(f"{file_name} saved successfully.")
    main_article = article.replace("\n", " ")

    def count_personal_pronouns(text):
        # Define a regex pattern for personal pronouns
        # Use word boundaries (\b) to match entire words only
        
        pattern = r'\b(I|we|We|My|Ours|Us|my|ours|us)\b'

        # Use re.findall to find all matches (case-insensitive)
        matches = re.findall(pattern, text)

        # Count the matches
        pronoun_count = len(matches)

        return pronoun_count

    no_of_per_pronoun=count_personal_pronouns(main_article)
    
    
    sent_tolkenized=sent_tokenize(main_article)
    total_sent=len(sent_tolkenized)
    main_text=emoji.demojize(main_article)
    main_text=main_text.lower()
    
    def remove_html_tags(text):
        pattern = re.compile('<.*?>')
        return pattern.sub(r'', text)

    main_text=remove_html_tags(main_text)
    
    def remove_url(text):
        pattern = re.compile(r'https?://\S+|www\.\S+')
        return pattern.sub(r'', text)

    main_text=remove_url(main_text)
    
    

    punct=string.punctuation
    punct=punct+"“"+"”"+"‘"+"’"+"--"
    punct
    def remove_punct(text):
        for i in text:
            if i in punct:
                text=text.replace(i,"")
        return text

    main_text=remove_punct(main_text)
    main_text

    def remove_emoji(text):
        emoji_pattern = re.compile("["  # emoticons
                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            u"\U00002702-\U000027B0"
                            u"\U000024C2-\U0001F251"
                            "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)
    main_text=remove_emoji(main_text)
    main_text = re.sub(r'\d+', '', main_text)

    
    directory_path = "StopWords-20241205T154736Z-001/StopWords"  # Path to the directory containing the stop words files

    # Walk through the directory to all files for getitng all the stop_words and joining them in one list
    for dirpath, dirnames, filenames in os.walk(directory_path):
        for file_name in filenames:
            file_path = os.path.join(dirpath, file_name)            
            with open(file_path, 'r') as file:
                    stop_words = file.read().lower().splitlines()

    def remove_stop_words(sentence, stop_words):
                words = sentence.split()  # Split the sentence into words
                filtered_words = [word for word in words if word.lower() not in stop_words]  # Remove stop words
                return ' '.join(filtered_words)  # Join back into a sentence
    text=remove_stop_words(main_text,stop_words)       

    word_tekenized=word_tokenize(text)

    total_word_len=0
    for word in word_tekenized:
        total_word_len+=len(word)
    avg_word_len=total_word_len/len(word_tekenized)
        
    file_path="MasterDictionary-20241205T154758Z-001\\MasterDictionary\\negative-words.txt"

    with open(file_path, 'r',encoding="latin-1") as file: #negative_words file contains some text or letters that were not decryptable using utf-8 encoding, thatswhy latin-1 is used here
            neg = file.read().lower().splitlines()

    file_path="MasterDictionary-20241205T154758Z-001\\MasterDictionary\\positive-words.txt"

    with open(file_path, 'r',encoding='latin-1') as file:
            pos = file.read().lower().splitlines()

    #calculating negative and positive words in the article and calculating other variables using them
    neg_emot=0
    pos_emot=0
    for i in word_tekenized:
        if i in neg:
            neg_emot+=1
        if i in pos:
            pos_emot+=1
    neg_score=neg_emot
    pos_score=pos_emot
    polarity_score=(pos_emot-neg_emot)/((pos_emot + neg_emot)+0.000001)
    sub_score=(pos_emot + neg_emot)/(len(word_tekenized)+0.000001)
    
    #calculating syllables and complex words.
    vow=["a","e","i","o","u"]
    complex_words=[]
    tot_syll=0
    for word in word_tekenized:
        # Count vowel groups
        syllables = len(re.findall(r'[aeiouy]+', word))

        # Handle specific cases
        if word.endswith("es") and not word.endswith(("aes", "ees", "oes")):
            syllables -= 1
        if word.endswith("ed") and len(word) > 2 and word[-3] not in "aeiou":
            syllables -= 1
        if word.endswith("e") and len(word) > 1 and word[-2] not in "aeiou":
            syllables -= 1
        # Ensure at least one syllable
        if syllables > 2:
            complex_words.append(word)
        tot_syll+=syllables

    complex_word_count=len(complex_words)
    avg_syll_per_word=tot_syll/len(word_tekenized)
    

    # Open the outfile in write mode which we created initially to store variables
    with open(out_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        #updating variables inn the file
        writer.writerow([uid, pos_score, neg_score,polarity_score,sub_score,len(word_tekenized)/total_sent,complex_word_count/len(word_tekenized),0.4*(len(word_tekenized)/total_sent+complex_word_count/len(word_tekenized)),len(word_tekenized)/total_sent,complex_word_count,len(word_tekenized),avg_syll_per_word,no_of_per_pronoun,avg_word_len])
        print(f"Row {uid} added:")

print(f"CSV file '{out_file}' created!")
    