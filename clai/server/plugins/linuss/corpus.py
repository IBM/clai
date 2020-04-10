
import pandas as pd
from collections import Counter

from page import Page
from utils.merge import mergeDict


class Corpus:
    def __init__(self, main_page):
        self.main_page = Page(main_page)
        self.articles = []
        self.corpus_stopwords = []
        self.D2Vmodel = None
        self.W2Vmodel = None
        self.fill_type = ""
        
    def fill_corpus(self, size, mode):
        """Function: Fills corpus by getting related articles, starting with the main article and
           using the other articles that are found until the corpus meets the set size parameter.  
           ============================================================================
           Parameters
           ----------
           Desired size of final corpus.

           Returns
           ----------
           No return. Corpus articles are stored in self.articles"""
                
        if(mode == "all_related"):
            # Start filling corpus with artiles related to main article
            self.articles = self.main_page.get_related()
            # Keep track of current article using article counter
            article_counter = 0

            while len(self.articles) < size:
                related_articles = self.articles[article_counter].get_related()
                if(related_articles != False):
                    self.articles.extend(self.articles[article_counter].get_related())
                article_counter +=1
    
        
        self.fill_type = "all_related"
                   
        
    def similarity_analysis(self, is_smart, d2v_model, w2v_model, index2word_set):
        """Function: Analyzes all corpus against corpus main article and returns results in pandas dataframe.
           ============================================================================
           Parameters
           ----------
           <boolean> Determines whether or not multi-tiered analysis is used. 

           Returns
           ----------
           Returns pandas dataframe with analysis results"""
        
        ## Pre-process main article
        # self.main_page.get_secondary_titles()
        self.main_page.get_main_text()
        self.main_page.get_word_frequency()
        
        #itialize Pandas Dataframe to store results
        index = []
        for article in self.articles:
            if(article.main_title not in index):
                index.append(article.main_title)

        columns = ["Main Title Tier", "Secondary Title Tier", "Main Analysis"]
        results = pd.DataFrame(index=index, columns=columns)

        ## Actually do the analysis
        ndx = 1 #dex for d2v tagging purposes
        for article in self.articles:
            results.loc[article.main_title] = self.main_page.similarity_analysis(article, is_smart, ndx, d2v_model, w2v_model, index2word_set)
            ndx = ndx + 1
        
        return results
    
    def filter_corpus_by_frequency(self, *args):
        """Function: Finds a variable amount (default 3) of the most frequent words in the corpus. 
           These words are then removed from all of the article.word_frequency[] dictionaries. 
           ============================================================================
           Parameters
           ----------
           (Optional) <int> Number of stop words to get. Default is 3. 

           Returns
           ----------
           No return. Filters most frequent words in corpus out of all articles word_frequency dictionaries."""

        
        ## Lets loop through the articles in the corpus, get each articles word_frequency count, and merge them into a common dictionary.
        # ...this will be fun
        total_frequency = {}
        for article in self.articles:
            total_frequency = mergeDict(total_frequency, article.get_word_frequency())
        total_frequency = Counter(total_frequency)
        ## Okay now that's done, let's get the most frequently found words in the corpus (aka our new corpus stop words).
        
        # Check if optional paramater was passed. 
        if(len(args) == 1):
            count = args[0]
        else:
            count = 3

        # Get 3 most frequently found words and store them in corpus_stopwords list. 
        self.corpus_stopwords = [item[0] for item in total_frequency.most_common(count)]
        
        # Loop through all articles in corpus, filtering out the newly obtained corpus stop words.
        for article in self.articles:
            article.filter_corpus_stopwords(self.corpus_stopwords)