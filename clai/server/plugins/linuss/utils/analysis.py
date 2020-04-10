#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#


def jaccard_analysis(article_one, article_two):
    
    """Parameters
       ----------
       Right now this function takes two strings as its parameters (article_one, article_two). In the future, it should take 
       WikiArticle instances to allow multiple sub-headers to be analyzed together. 
       
       Returns
       --------
       Jaccard Similarity Percentage."""
    
    a = set(article_one.split(" "))
    b = set(article_two.split(" "))
    comparison = a.intersection(b)
    return float(len(comparison)) / (len(a) + len(b) - len(comparison))



def cosine_analysis(article_one_frequency, article_two_frequency):

    # convert to word-vectors
    words  = list(article_one_frequency.keys() | article_two_frequency.keys())
    a_vect = [article_one_frequency.get(word, 0) for word in words]        
    b_vect = [article_two_frequency.get(word, 0) for word in words]       

    # find cosine
    len_a  = sum(av*av for av in a_vect) ** 0.5             
    len_b  = sum(bv*bv for bv in b_vect) ** 0.5             
    dot    = sum(av*bv for av,bv in zip(a_vect, b_vect))    
    cosine = dot / (len_a * len_b)
    
    # return cosine
    return cosine

def vec_cosine_analysis(a_vect, b_vect):
    # find cosine
    len_a  = sum(av*av for av in a_vect) ** 0.5             
    len_b  = sum(bv*bv for bv in b_vect) ** 0.5             
    dot    = sum(av*bv for av,bv in zip(a_vect, b_vect))    
    cosine = dot / (len_a * len_b)
    
    # return cosine
    return cosine
    



def is_over_threshold(similarity, *args):
    
    """Parameters
       ----------
       similarity (float): similarity value that will be checked against threshold.
       threshold (float): Optional paramater to provide value for threshold. Must be passed as "threshold = (value)". Default is 50.
    
       Returns
       ----------
       Boolean value. True if threshold limit is met or exceeded, else False."""
    
    if(len(args) == 1):
        threshold = args[0]
    else:
        threshold = .5
    return (similarity >= threshold)