from itertools import islice
import math
import linecache
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd


# This function read the "index.txt" file and compute the invert index accordingly
def create_inverted_index(file, lowercase=False):
    with open(file, "r") as infile:
        sents = infile.read().split("\n")
        if sents[-1] == "":
            sents = sents[:-1]
        if lowercase:
            sents = map(str.lower, sents)

    invert_index = {}
    for sent in sents:
        token = sent.split(" ")[0]
        doc_id = int(sent.split(" ")[1])
        if token not in invert_index.keys():
            invert_index[token] = set([doc_id])
        else:
            invert_index[token].update([doc_id])

    return invert_index


# This function sort the invert_index with decreasing length of posting
# It will help to find the words with longest posting
def get_sorted_dic_with_length(dictionary):
    for key, value in dictionary.items():
        dictionary[key] = len(value)

    sorted_dictionary = {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse=True)}
    return sorted_dictionary


# find the sorted word list with decreasing frequency in order to fit into algorithms of multiple intersection.
def sort_by_decreasing_frequency(dictionary, wordlist):
    value_list = list()
    for word in wordlist:
        value_list.append(len(dictionary[word]))
    zipped = list(zip(wordlist, value_list))
    res = sorted(zipped, key=lambda x: x[1], reverse=True)
    return [x[0] for x in res]


# Get total posting size
def get_total_posting_length(sorted_dic):
    return sum(sorted_dic.values())


# take n numbers of items from a iterable object, use to solve "top n" question
def take(n, iterable):
    return list(islice(iterable, n))


# Code of single query
def single_query(dictioanry, word):
    return sorted(dictioanry[word])


# Code for intersection of two posting
def intersection_post(pc1, pc2):
    intersection_result = []
    num_cmp = 0

    while len(pc1) > 0 and len(pc2) > 0:
        post1 = pc1[0]
        post2 = pc2[0]
        if post1 == post2:
            intersection_result.append(post1)
            num_cmp = num_cmp + 1
            pc2 = pc2[1:]
            pc1 = pc1[1:]
        if post1 < post2:
            num_cmp = num_cmp + 1
            pc1 = pc1[1:]
        if post1 > post2:
            num_cmp = num_cmp + 1
            pc2 = pc2[1:]

    return intersection_result, num_cmp


# optimize the intersection algorithm by adding skip, and skip size is around sqrt of posting length
def intersection_post_with_skip(pc1, pc2):
    intersection_result = []
    num_cmp = 0

    skip1 = int(math.sqrt(len(pc1)))
    skip2 = int(math.sqrt(len(pc2)))

    while len(pc1) > 0 and len(pc2) > 0 and skip1 < len(pc1) and skip2 < len(pc2):
        post1 = pc1[0]
        post2 = pc2[0]
        if post1 == post2:
            intersection_result.append(post1)
            num_cmp = num_cmp + 1
            pc2 = pc2[1:]
            pc1 = pc1[1:]
        if post1 < post2:
            num_cmp = num_cmp + 1
            if pc1[skip1] <= post2:
                num_cmp = num_cmp + 1
                pc1 = pc1[skip1:]
            else:
                pc1 = pc1[1:]
        if post1 > post2:
            num_cmp = num_cmp + 1
            if pc2[skip2] <= post1:
                num_cmp = num_cmp + 1
                pc2 = pc2[skip2:]
            else:
                pc2 = pc2[1:]

    return intersection_result, num_cmp


# intersection operation decoration by inputs of words instead of posting
def intersection(dictionary, word1, word2, skip=False):
    p1 = sorted(list(dictionary[word1]))
    p2 = sorted(list(dictionary[word2]))

    p1_copy = p1[:]
    p2_copy = p2[:]

    if skip:
        intersection_result, num_cmp = intersection_post_with_skip(p1_copy, p2_copy)
    else:
        intersection_result, num_cmp = intersection_post(p1_copy, p2_copy)

    return intersection_result, num_cmp


# Code for multiple intersection, with variable number of words input
def multi_intersection(dictionary, *words):
    words_list = list(words)

    sorted_words_list = sort_by_decreasing_frequency(dictionary, words_list)

    result = single_query(dictionary, sorted_words_list[0])

    for word in sorted_words_list[1:]:
        result = intersection_post(result, single_query(dictionary, word))[0]

    return result


# Code to find document according a list of line numbers in the movie.txt
def find_corpus(file, line_numbers):
    corpus = []
    for line_number in line_numbers:
        doc = linecache.getline(file, line_number).strip()
        corpus.append(doc.lower())
    return corpus


# Calculate tfid of each item in different documents
def get_related_tfid(corpus, vocabulary):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)
    df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names())

    df.index = doc_ids
    df.index.name = 'Document_ID'
    return df.filter(vocabulary)


# Testing and printout
if __name__ == "__main__":
    file = 'index.txt'

    movie_invert_index = create_inverted_index(file)
    sorted_invert_index = get_sorted_dic_with_length(movie_invert_index.copy())
    postings_lenth = get_total_posting_length(sorted_invert_index)
    stop_words = take(10, sorted_invert_index.keys())
    stop_words_posting_lenth = sum(take(10, sorted_invert_index.values()))

    movie_invert_index_lower = create_inverted_index(file, lowercase=True)
    sorted_invert_index_lower = get_sorted_dic_with_length(movie_invert_index_lower.copy())
    postings_lenth_lower = get_total_posting_length(sorted_invert_index_lower)
    stop_words_lower = take(10, sorted_invert_index_lower.keys())
    stop_words_posting_lenth_lower = sum(take(10, sorted_invert_index_lower.values()))
    print("\n")
    print("dictionary size before lowercasing: ", len(movie_invert_index))
    print("postings total size before lowercasing: ", postings_lenth)
    print("stop words before lowercasing", stop_words)
    print("stop words postings length", stop_words_posting_lenth)
    print("\n")
    print("dictionary size after lowercasing: ", len(movie_invert_index_lower))
    print("postings total size after lowercasing: ", postings_lenth_lower)
    print("stop words before lowercasing", stop_words_lower)
    print("stop words postings length", stop_words_posting_lenth_lower)

    print("\n")
    print("single query for word \'school\':", single_query(movie_invert_index_lower, "school"))
    print("\n")
    intersection_result1, num_cmp1 = intersection(movie_invert_index_lower, word1="school", word2="kids")
    print("intersection with query \'school\' And \'kids\' is %s , and number of comparision is %s:"
          % (intersection_result1, num_cmp1))

    intersection_result1_opt, num_cmp1_opt = intersection(movie_invert_index_lower, word1="school", word2="kids",
                                                          skip=True)
    print("with skip feature, intersection with query \'school\' And \'kids\' is %s , and number of comparision is %s:"
          % (intersection_result1_opt, num_cmp1_opt))

    doc_ids = multi_intersection(movie_invert_index_lower, "school", "kids", "really")
    print("multi intersection with query \'really\' And \'school\' And \'kids\':", doc_ids)

    print("\n")

    corpus = find_corpus("movies.txt", doc_ids)

    vocabulary = ["school", "kids", "really"]

    tfid_result = get_related_tfid(corpus, vocabulary)

    print(tfid_result)
