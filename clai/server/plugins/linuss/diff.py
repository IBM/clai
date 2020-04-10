#!/usr/bin/env python3
#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import os
import argparse
import gensim
from gensim.models import doc2vec
from gensim.models import Word2Vec
from os import path
import nltk
import time

from corpus import Corpus


def getAllFiles(directory):
    return os.popen(f'find ./{directory} -type f ').read().split('\n')

def buildFileSets(directory):
    # path_set = []
    name_set = []

    for path in getAllFiles(directory):
        filename = path.split('/')[-1]
        # remove the extensions
        name = filename.split('.')[0]
        # path_set.append(path)
        name_set.append(name)

    return set(name_set)
            
def compareDirs(a,b):
   return a.intersection(b)


def getGetPage(name:str):
    if name == "host":
        path = os.popen(f"find ./linux_pages -name '{name}.*'").read().split('\n')[0]
        # try:
        file = open(path, 'r')
        man_page = file.readlines()
        file.close()
        return man_page    
        # except:
        #     print(f'Error opening the following man page: {path}')
        
       

def diffPage(page:str):
    print(page)



## d2v and w2v model building methods.

def build_d2v_model(corpus):
    """Function: Builds d2v model for analysis. Model is loaded from file if it already exists.
       ============================================================================
       Parameters
       ----------
       Corpus to build model on (all_related preferably).

       Returns
       ----------
       Builds, trains, and returns doc2vec model"""
    if(path.exists("D2Vmodel")):
        D2Vmodel = doc2vec.Doc2Vec.load("D2Vmodel")
        return D2Vmodel

    else:
        training_corpus = []
        corpus.main_page.get_main_text()
        training_corpus.append(gensim.models.doc2vec.TaggedDocument(words=corpus.main_page.main_text, tags=[0]))
        tag_counter = 0
        for article in corpus.articles:
            article.get_main_text()
            training_corpus.append(gensim.models.doc2vec.TaggedDocument(words=article.main_text, tags=[tag_counter]))
            tag_counter += 1

        D2Vmodel = gensim.models.doc2vec.Doc2Vec(size=50, min_count=2, iter=10)
        D2Vmodel.build_vocab(training_corpus)
        D2Vmodel.train(training_corpus, total_examples=D2Vmodel.corpus_count, epochs=20)
        D2Vmodel.save("D2Vmodel")
        print ("Doc2vec model was made with all_related corpus")
        return D2Vmodel
        
        
def build_w2v_model(corpus):
    """Function: Builds w2v model for analysis. Model is loaded from file if it already exists.
           ============================================================================
           Parameters
           ----------
           Corpus to build model on (all_related preferably).

           Returns
           ----------
           Builds, trains, and returns word2vec model"""
    if(path.exists("W2Vmodel")):
        w2v_model = Word2Vec.load("W2Vmodel")
        return w2v_model
    
    else: 
        training_corpus = []
        corpus.main_page.get_main_text()
        for word in corpus.main_page.main_text:
            training_corpus.append(word)
            
        for article in corpus.articles:
            for word in article.main_text:
                training_corpus.append(word)
                
        w2v_model = Word2Vec(sentences=training_corpus, min_count = 10, size=300)
        w2v_model.save("W2Vmodel")
        print("Word2Vec model was made with all_related corpus")
        return w2v_model


if __name__ == '__main__':
    # sets = [ buildFileSets(directory) for directory in ['spark_pages', 'z_pages']]
    # print(compareDirs(sets[0], sets[1]))
    # [ diffPage(getGetPage(man_page)) for man_page in compareDirs(sets[0], sets[1]) ]

    start = time.time()
    
    ## Receive args
    parser = argparse.ArgumentParser()
    parser.add_argument("size", type=int)
    args = parser.parse_args()
    
    ## Create and fill corpora 
    corpus_related = Corpus('./linux_pages/man5/host.conf.5')

    corpus_related.fill_corpus(args.size, "all_related")

    
    ## Issue #1 in https://github.com/danielobrien3/HBC-Text-Similarity-Analysis
    #corpus.filter_corpus_by_frequency()
    
    ## Loads model from file. The model is created if it does not yet exist. 
    d2v_model = build_d2v_model(corpus_related)
    w2v_model = build_w2v_model(corpus_related)
    index2word_set = set(w2v_model.wv.index2word)
    
    
    ## Get (multitiered AND regular analysis) results of each corpus
    smart_results_related = corpus_related.similarity_analysis(True, d2v_model, w2v_model, index2word_set)
    print(smart_results_related)
    end = time.time()
    print("Took " + str(end - start) + "s to run")

