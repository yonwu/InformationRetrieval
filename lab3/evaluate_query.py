import subprocess
import os
import gzip
import shutil
import matplotlib.pyplot as plt
import numpy as np


def gunzip(file_path, output_path):
    with gzip.open(file_path, "rb") as f_in, open(output_path, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)


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
        precision_at_k[topic] = score
    return precision_at_k


def plot_bi_precision_at_k(origin_precision_at_k, title):
    name_list = list(origin_precision_at_k.keys())
    num_list = list(origin_precision_at_k.values())
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

    plot_bi_precision_at_k(precision_at_k_origin, 'origin')
    plot_bi_precision_at_k(precision_at_k_decompounded, 'decompounded')


