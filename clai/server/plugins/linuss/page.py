

import re
import string
import numpy as np
import pandas as pd
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from utils.analysis import *

class Page:
    def __init__(self, path):
        self.path = path
        self.page = self.getPage(self.path)
        self.main_title = self.page[0]
        self.main_text = self.page[0:]
        self.word_frequency = {}
    
    def getPage(self, path):
        try:
            file = open(path, 'r')
            man_page = file.readlines()
            file.close()
            return man_page    
        except:
            raise IOError(f'Error opening the following man page: {path}')
    
    def similarity_analysis(self, article, is_smart, ndx, d2v_model, w2v_model, index2word_set):
        """
        Function: To be used in Corpus class to perform analysis between main article and comparison article
        ============================================================================
           Parameters
           ----------
           Article to be analyzed against main article.

           Returns
           ----------
           Returns Pandas series to be used in forming a dataframe result."""
        ## Check main title tier

        # if(is_smart == True):
        #     a_vec = d2v_model.infer_vector(self.pre_process(self.main_title))
        #     b_vec = d2v_model.infer_vector(article.pre_process(article.main_title))
        #     main_title_comparison = vec_cosine_analysis(a_vec, b_vec)
        #     if is_over_threshold(main_title_comparison):
        #         main_title_tier = True
        #     else:
        #         return pd.Series({'Main Title Tier': main_title_comparison, 'Secondary Title Tier': None, 'Main Analysis': None})

        #     ## Check sub title tier
        #     article.get_secondary_titles()
        #     a_vec = d2v_model.infer_vector(self.pre_process(self.secondary_titles))
        #     b_vec = d2v_model.infer_vector(article.pre_process(article.secondary_titles))
        #     secondary_title_comparison = vec_cosine_analysis(a_vec, b_vec)
        #     if is_over_threshold(secondary_title_comparison):
        #         secondary_title_tier = True
        #     else:
        #         return pd.Series({'Main Title Tier': main_title_comparison, 'Secondary Title Tier': secondary_title_comparison, 'Main Analysis': None})
        # else: 
        main_title_comparison = None;
        secondary_title_comparison = None;
        
        ## Since we got this far we should get the main text and wrod count of the article
        article.get_main_text()
        article.get_word_frequency()
        
        ## And now perform the main analysis 
        a_vec = d2v_model.infer_vector(self.main_text)
        b_vec = d2v_model.infer_vector(article.main_text)
        analysis = vec_cosine_analysis(a_vec, b_vec)
        return pd.Series({'Main Title Tier': main_title_comparison, 'Secondary Title Tier': secondary_title_comparison, 'Main Analysis':analysis})
        
            
    
    def get_secondary_titles(self):
        # Check length to make sure secondary_titles list hasn't already been filled. Don't want duplicate data messing us up. 
        if(len(self.secondary_titles) == 0):
            for secondary_title in self.soup.find_all("h2"):
                self.secondary_titles += " " + secondary_title.get_text()
    
    def w2v_vector(self, text, model, index2word_set):
        """
        Function: To get word2vec average vector of provided text
        ============================================================================
           Parameters
           ----------
           Text to be word2vec'd

           Returns
           ----------
           Word2Vec average vector of provided text."""
        num_features = model.wv.vectors.shape[1];
        featureVec = np.zeros((num_features,), dtype="float32")
        nwords = 0

        for word in text:
            if word in index2word_set:
                nwords = nwords+1
                featureVec = np.add(featureVec, model[word])

        if nwords>0:
            featureVec = np.divide(featureVec, nwords)
        return featureVec
        
        
                
    def get_main_text(self):
        """
        Function: self.main_text set to <string> pre-processed main text of article.
        ============================================================================
           Parameters
           ----------
           Takes no parameters.

           Returns
           ----------
           Returns nothing."""
        
    
        
        # Prepares text for analysis.
        self.main_text = self.pre_process(''.join(self.main_text))
    
    def get_word_frequency(self):
        """ 
        Function: gets word frequencies for article and stores in self.word_frequency dictionary. 
        ===========================================
           Parameters
           ----------
           Takes no paramaters

           Returns
           ----------
           Returns word frequency. Result is stored in self.word_frequency"""
        
        self.word_frequency = Counter(self.main_text)
        return self.word_frequency
        
        
    def filter_corpus_stopwords(self, corpus_stop_words):
        """ 
        Function: removes all occurences of the most frequent words in the corpus from self.word_frequency. This function should only be called from within a corpus class method.
        ===========================================
        Parameters
        ----------
        <list> corpus stop words

        Returns
        ----------
        No return. self.word_frequency"""
        
        filtered_text = Counter({})
        for k, v in self.word_frequency.items():
            if not k in corpus_stop_words:
                filtered_text[k] = v
                
        self.word_frequency = filtered_text
    
    
    def pre_process(self, text):
        """
        Function: pre-processes text to prepare for analysis. 
        =====================================================
           Parameters
           ----------
           Takes <string> text to be pre-processed.

           Returns
           ----------
           Returns <dict> of pre-processed text."""
        
        # Cleaing the text
        processed_article = text.lower()
        
        # Preparing the dataset
        all_words = word_tokenize(processed_article)
        processed_article = re.sub('[^a-zA-Z]', ' ', processed_article )
        processed_article = re.sub(r'\s+', ' ', processed_article)
        
        # Removing Stop Words
        processed_text = []
        for w in all_words:
            if not w in stopwords.words('english') and not w in string.punctuation:
                processed_text.append(w)
        
        return processed_text

    
    def get_related(self):
        """ Function: Get list of related articles
            =====================================================
                Parameters
                ----------
                This function takes no paramater 
                
                Returns
                -------
                If related articles exist, they are returned in a list. Else returns false. 
               
               """
        return [Page('./diff.py')]
