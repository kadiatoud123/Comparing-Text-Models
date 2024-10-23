#finalproject.py (Final Project)
import math 

# helper function
def clean_text(txt):
    """ takes a string of text txt as a parameter and returns a list containing the words in txt after it has been “cleaned”
    """
    for symbol in """.,?"'!;:""":
        txt = txt.lower().replace(symbol, '')
        
    return txt.split()

def stem(s):
    """ returns the stem of s
    """
    stem = ''
    
    exceptions = {'weed':'weed', 'historys':'historys', 'thats':'thats', 'themes':
                  'themes', 'theres':'theres', 'turned':'turned', 'dreaming':'dreaming'}
    
    for key in exceptions:
        if s == key:
            return exceptions[key]
    
    if len(s) > 3:
        if s[-1] == 'e':
            stem = s[:-1]
            
        elif s[-1] == 'y':
            stem = s[:-1] + 'i'
            
        elif s[-3:] == 'ing':
            if s[-4] == s[-5]:
                stem = s[:-4]
            else:
                stem = s[:-3]
                
        elif s[-1] == 's':
            if s[-2:] == 'es':
                stem = s[:-3]
            elif s[-4:-1]== 'ing':
                stem= s[:-4]
            else:
                stem = s[:-1]
                
        elif s[-2:] == 'ed':
            if s[-3] == s[-4]:
                stem = s[:-3]
            else: 
                stem = s[:-2]
                
        
        elif s[-3:] == 'ify':
            stem = s[:-3]
            
        elif s[-2:] == 'er':
            stem = s[:-2]
            
        elif s[-4:] == 'ness':
            stem = s[:-4]
            
        elif s[-3:] == 'ery':
            stem = s[:-2]
            
        elif s[-4:] == 'ical':
            stem = s[:-2]
            
        
    return stem


def compare_dictionaries(d1, d2):
    """ takes two feature dictionaries d1 and d2 as inputs, and computes and return their log similarity scores
    """
    if d1 == {}:
        return -50
    
    else:
        score = 0
        total = 0
        for val in d1:
            total += d1[val]
            
        for key in d2:
            
            if key in d1:
                score += (d2[key] * (math.log(d1[key] / total)))
            
            else:
                score += d2[key] * math.log(0.5 / total)
    
    return score

def sentence_length(s):
    """ helper function that returns a list of sentences in a string s
    """
    s = s.replace('!', '.')
    s = s.replace('?', '.')

    words = s.split('.')

    
    
    return words[:-1]

        
class TextModel:
    
    def __init__(self, model_name):
        """ constructs a new TextModel object by accepting a string model_name as a parameter
            and initializes name, words, and word_lengths
        """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.punctuation_freq = {}
        
        
    def __repr__(self):
        """ returns a string that includes the name of the model as well as the sizes of the dictionaries 
            for each feature of the text
        """
        s = 'text model name: ' + self.name
        s += '\n  number of words: ' + str(len(self.words))
        s += '\n  number of word lengths: ' + str(len(self.word_lengths))
        s += '\n  number of stems: ' + str(len(self.stems))
        s += '\n  number of sentence lengths: ' + str(len(self.sentence_lengths))
        s += '\n  number of punctuation marks: ' + str(self.punctuation_freq)
        
        return s
    
    def add_string(self, s):
        """ adds a string of text s to the model by augmenting the feature dictionaries defined in the constructor
        """
        sens = sentence_length(s)
        
        for i in range(len(sens)):
            words = len(sens[i].split())
            
            if words in self.sentence_lengths:
                self.sentence_lengths[words] += 1
            
            else:
                self.sentence_lengths[words] = 1
        
        for char in s:
            if char in """.,?"'!;:""":
                if char in self.punctuation_freq:
                    self.punctuation_freq[char] += 1
                
                else:
                    self.punctuation_freq[char] = 1
                
        word_list = clean_text(s)
        
        for w in word_list:
            if w in self.words:
                self.words[w] += 1
            else:
                self.words[w] = 1
                
        for w in self.words:
            if len(w) in self.word_lengths:
                self.word_lengths[len(w)] += self.words[w]
            else:
                self.word_lengths[len(w)] = self.words[w]
                
                
                
        for w in word_list:
            if stem(w) in self.stems:
                self.stems[w] += 1
            else:
                self.stems[w] = 1
                
    def add_file(self, filename):
        """ adds all of the text in the file identified by filename to the model
        """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        text= f.read()
        self.add_string(text)
        
    def save_model(self):
       """ demonstrates how to write a Python dictionary to an easily-readable file.
       """
       
       filename = self.name + '_' + 'words'
       f = open(filename, 'w')
       f.write(str(self.words))
       f.close()
       
       filename2 = self.name + '_' + 'word_lengths'
       f2 = open(filename2, 'w')
       f2.write(str(self.word_lengths))
       f2.close()

       filename3 = self.name + '_' + 'stems'
       f3 = open(filename3, 'w')
       f3.write(str(self.stems))
       f3.close()

       
       filename4 = self.name + '_' + 'sentence_lengths'
       f4 = open(filename4, 'w')
       f4.write(str(self.sentence_lengths))
       f4.close()

       
       filename5 = self.name + '_' + 'punctuations'
       f5 = open(filename5, 'w')
       f5.write(str(self.punctuation_freq))
       f5.close()

    def read_model(self):
         """ reads the stored dictionaries for the called TextModel object from their files and assigns them to the attributes of the called TextModel
         """ 
         filename = self.name + '_' + 'words'
         f = open(filename, 'r')
         d_str = f.read()
         f.close()
         self.words= dict(eval(d_str))
         
         filename2 = self.name + '_' + 'word_lengths'
         f = open(filename2, 'r')
         d_str = f.read()
         f.close()
         self.word_lengths= dict(eval(d_str))
         
         filename3 = self.name + '_' + 'stems'
         f = open(filename3, 'r')
         d_str = f.read()
         f.close()
         self.stems= dict(eval(d_str))

         
         filename4 = self.name + '_' + 'sentence_lengths'
         f = open(filename4, 'r')
         d_str = f.read()
         f.close()
         self.sentence_lengths= dict(eval(d_str))
         
         filename5 = self.name + '_' + 'punctuations'
         f = open(filename5, 'r')
         d_str = f.read()
         f.close()
         self.punctuation_freq = dict(eval(d_str))
         
    
    def similarity_scores(self, other):
        """ that computes and returns a list of log similarity scores measuring the similarity of self and other 
        """
        word_score = compare_dictionaries(other.words, self.words)
        wordlen_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        stem_score = compare_dictionaries(other.stems, self.stems)
        senlen_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        punct_score = compare_dictionaries(other.punctuation_freq, self.punctuation_freq)
        
        list = [word_score, wordlen_score, stem_score, senlen_score, punct_score]
       
        return list
    
    def classify(self, source1, source2):
        """ compares the called TextModel object (self) to two other “source” TextModel objects (source1 and source2) and determines which of these other TextModels is the more likely source of the called TextModel
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        
        rscores1 = [round(val, 3) for val in scores1]
        rscores2 = [round(val, 3) for val in scores2]
        print(('scores for ') + str(source1.name) + ': ' + str(rscores1))
        print(('scores for ') + str(source2.name) + ': ' + str(rscores2))
        
        score1_count = 0
        score2_count = 0
        
        for i in range(len(scores1)):
            if rscores1[i] >= rscores2[i]:
                score1_count += 1
            else:
                score2_count += 1
                
        if score1_count > score2_count:
            print(self.name + ' is more likely to have come from ' + source1.name)
        else:
            print(self.name + ' is more likely to have come from ' + source2.name)
            
                
            
def test():
    """ tests add_string method using different sources
    """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)               
        
def run_tests():
    """ saves and adds the file for both sources and other models to then classify its similarities
    """

    source1 = TextModel('Shakespeare')
    source1.save_model()
    source1.add_file('shakespeare.txt')

    source2 = TextModel('Maya Angelou')
    source2.save_model()
    source2.add_file('mayaangelou.txt')

    new1 = TextModel('WR120')
    new1.add_file('paperexcerpt.txt')
    new1.classify(source1, source2)
    print('\n')
    
    new2 = TextModel('George Chapman')
    new2.add_file('gchapman.txt')
    new2.classify(source1, source2)
    print('\n')
    
    new3 = TextModel('Vietnam War')
    new3.add_file('vietnam.txt')
    new3.classify(source1, source2)
    print('\n')
    
    new4 = TextModel('JK Rowling')
    new4.add_file('jkr.txt')
    new4.classify(source1, source2)
    
    
    
    
    
    
    

    
   
        
            