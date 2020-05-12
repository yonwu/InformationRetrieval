import subprocess
import os
import gzip
import shutil


def gunzip(file_path, output_path):
    with gzip.open(file_path, "rb") as f_in, open(output_path, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)


def create_eval_query_dict(files):
    eval_query_dict = {}
    for file in files:
        key = ''.join(i for i in file if i.isdigit())
        with open(file, "r") as infile:
            sents = infile.read().split("\n")
            if sents[-1] == "":
                sents = sents[:-1]
            eval_dict = {}
            for sent in sents:
                doc_id = sent.split('\t')[0]
                score = sent.split('\t')[1]
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


if __name__ == "__main__":
    result_test = create_query_score_dict('./eval_file')
    for value in result_test.values():
        print(value.keys())
