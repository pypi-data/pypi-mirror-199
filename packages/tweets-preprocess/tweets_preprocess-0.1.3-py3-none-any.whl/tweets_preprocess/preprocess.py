import regex
import re
import pandas as pd
import numpy as np
        
class Preprocess:
           
    """
    Instantiate a Preprocess operation.
    This removes the hashtags, mentions, urls, emojis from the tweets.
    It has a length constraint on the tweets
    Supported file format is a csv file
    
    :param data: The data.
    :type csv-file: csv-file
    """
    
    def __init__(self,data,text_column):
        self.data = data
        self.text_column = text_column
    
    def process(self):
        

        EMAIL_REGEX_STR = r'\S*@\S*'
        MENTION_REGEX_STR = r'@\S*'
        HASHTAG_REGEX_STR = r'#\S+'
        URL_REGEX_STR = r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*'

        ### Preprocessing 
        texts = self.data[self.text_column].values.tolist()
        remove_regex = regex.compile(f'({EMAIL_REGEX_STR}|{MENTION_REGEX_STR}|{HASHTAG_REGEX_STR}|{URL_REGEX_STR})')
        texts = [regex.sub(remove_regex, '', text) for text in texts]
        texts = [text.strip() for text in texts]
        texts = [text if len(text)>35 else "" for text in texts]
        
        emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    
        
        texts = [re.sub(emoj, '', i) for i in texts]
        
        return texts
        