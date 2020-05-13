import subprocess
import os
import gzip
import shutil
import matplotlib.pyplot as plt


# function to extract single file
def gunzip(file_path, output_path):
    with gzip.open(file_path, "rb") as f_in, open(output_path, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)


# create data structure dict to store evaluation info
def create_eval_query_dict(files):
    eval_query_dict = {}
    for file in files:
        key = int(''.join(i for i in file if i.isdigit()))
        with open(file, "r") as infile:
            sents = infile.read().split("\n")
            if sents[-1] == "":
                sents = sents[:-1]
            eval_dict = {}
            for sent in sents:
                doc_id = sent.split('\t')[0]
                score = int(sent.split('\t')[1])
                if score == 0:
                    score = 0
                else:
                    score = 1
                eval_dict[doc_id] = score
        eval_query_dict[key] = eval_dict
    return eval_query_dict


# clean old text files, extract all files, generate query evaluation info dict for dir
def create_query_score_dict(rootDir):
    for dirName, subdirList, fileList in os.walk(rootDir):
        # clean old text files
        for fname in fileList:
            if fname.endswith('.txt'):
                os.unlink(os.path.join(rootDir, fname))
        # extract files
        for fname in fileList:
            if fname.endswith('.gz'):
                f = os.path.join(rootDir, fname)
                gunzip(f, f.replace('.gz', ''))
        all_text_files = list()
        for fname in fileList:
            if fname.endswith('.txt'):
                f = os.path.join(rootDir, fname)
                all_text_files.append(f)
        query_scores_dict = create_eval_query_dict(all_text_files)

    return query_scores_dict


# store query ranking in data structure dict
def get_query_ranking(file):
    with open(file, "r") as infile:
        sents = infile.read().split("\n")
        if sents[-1] == "":
            sents = sents[:-1]
        query_ranking_info = {}
        for sent in sents:
            key = int(sent.split(' ')[0])
            doc_id = sent.split(' ')[2]
            if key in query_ranking_info.keys():
                query_ranking_info[key].append(doc_id)
            else:
                query_ranking_info[key] = [doc_id]
    return query_ranking_info


# get precision at k for all queries
def get_precision_at_k(query_ranking, query_score_table, k):
    precision_at_k = {}
    for topic in query_ranking.keys():
        top_k_rank = query_ranking[topic][:k]
        score = 0
        if topic not in query_score_table.keys():
            continue
        else:
            query_score = query_score_table[topic]

        for doc in top_k_rank:
            if doc not in query_score.keys():
                continue
            else:
                score = score + query_score[doc]
        precision_at_k[topic] = score / k
    return precision_at_k


# get precision at k for one topic
def get_precision_at_k_topic(query_ranking, query_score_table, k, topic):
    query_ranking_topic = {topic: query_ranking[topic]}
    precision_at_k_topic = get_precision_at_k(query_ranking_topic, query_score_table, k)
    return precision_at_k_topic[topic]


# get everage precisioin for one topic
def get_everage_precision_topic(query_ranking, query_score_table, N, topic):
    precision_at_all = 0
    for k in range(1, N + 1):
        precision_at_k_topic = get_precision_at_k_topic(query_ranking, query_score_table, k, topic)
        precision_at_all = precision_at_all + precision_at_k_topic
    return precision_at_all / N


# get MAP for all queries
def mean_everage_precision(query_ranking, query_score_table):
    map_topics = {}
    for topic in query_ranking.keys():
        Q = sum(query_score_table[topic].values())
        total_ap = 0
        for i in range(1, Q + 1):
            ap_i = get_everage_precision_topic(query_ranking, query_score_table, i, topic)
            total_ap = total_ap + ap_i
        map_topic = total_ap / Q
        map_topics[topic] = map_topic
    return map_topics


# plot result
def plot_result(result, title):
    name_list = list(result.keys())
    num_list = list(result.values())
    plt.figure(figsize=(15, 5))
    plt.bar(range(len(num_list)), num_list, color='blue', tick_label=name_list)
    plt.title(title)
    plt.savefig(title + '.png')


if __name__ == "__main__":

    query_score_dict = create_query_score_dict('./eval_file')
    query_ranking_origin = get_query_ranking('result_origin')
    query_ranking_compose = get_query_ranking('result_compose')

    precision_at_k_origin = get_precision_at_k(query_ranking_origin, query_score_dict, 10)
    precision_at_k_decompounded = get_precision_at_k(query_ranking_compose, query_score_dict, 10)

    plot_result(precision_at_k_origin, 'precision_at_k_origin')
    plot_result(precision_at_k_decompounded, 'precision_at_k_decompounded')

    socre_of_different_k = {}
    for k in range(1, 11):
        socre_of_different_k[k] = get_precision_at_k_topic(query_ranking_origin, query_score_dict, k, 27)
    plot_result(socre_of_different_k, 'prescision_at_different_k')

    map_origin = mean_everage_precision(query_ranking_origin, query_score_dict)
    map_decompounded = mean_everage_precision(query_ranking_compose, query_score_dict)

    plot_result(map_origin, 'MAP_origin')
    plot_result(map_decompounded, 'MAP_decompounded')
