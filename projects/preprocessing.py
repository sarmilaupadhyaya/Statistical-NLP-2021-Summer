import re
import os
import string

import nltk
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktLanguageVars


class BulletPointLangVars(PunktLanguageVars):
    sent_end_chars = ('.', '?', '!', '•','।')

tokenizer = PunktSentenceTokenizer(lang_vars = BulletPointLangVars())


class Preprocessing:
    def __init__(self, language='en', data_dir=None):
        
        self.file_path = data_dir
        self.language = language
        
    def read_file(self):
        """

        """
        
        total_data = ''
        if os.path.isdir(self.file_path):
            for file in os.listdir(self.file_path):
                file_path = os.path.join(self.file_path, file)
                with open(file_path, "r") as f:
                    total_data += f.read()
        else:
            with open(self.file_path, "r") as f:
                    total_data += " "+ f.read()
                    
        return total_data
       
    

    def clear_data(self):
        """
        """
        total_data = self.read_file()
        
        def deEmojify(text):
        
            regrex_pattern = re.compile(pattern = "["
                                        u"\U0001F600-\U0001F64F"  # emoticons
                                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                       "]+", flags = re.UNICODE)
            return regrex_pattern.sub(r'',text)
        
        def remove_alpha(text):
            
            text = "".join(i for i in text if i in [".","।","?","!",","] or 2432 <= ord(i) <= 2559 or ord(i)== 32)
            return re.sub(' +', ' ', text)
        
        #replace trailing punctuation by single one
        pattern  = r'(?<=[^!?।.,>$%&-][!?।.,>$%&-])[!?।.,>$%& -]+(?<! )'
        total_data = re.sub(pattern, ' ', total_data)
        
        if self.language == "be":
            #remove alphabets
            total_data = remove_alpha(total_data)
            # remove emojis
            total_data = deEmojify(total_data)
        
        total_data = tokenizer.tokenize(total_data)
        total_data = [sentence.replace("\n"," ").replace("*"," ").replace('`',"'").rstrip() for sentence in total_data]
        return "\n".join(total_data)
        
        return total_data
        
def train_test_split(data,ratio=0.2):
    """

    """
    
    data = data.split("\n")
    train_data, test_data = data[:int(len(data)*(1-ratio))], data[int(len(data)*(1-ratio)):]
    return train_data, test_data
    
        
