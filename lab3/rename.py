import os
import shutil


def rename(root_dir):
    for parent, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            special_start = 'utf-8\'\''
            if filename.startswith(special_start):
                print("before renaming: ", filename)
                os.rename(os.path.join(parent, filename), os.path.join(parent, filename.strip(special_start)))


if __name__ == "__main__":
    root_dir = '/Users/yonwu/NLP_Evolution_with_Code/NLP_with_Classification_and_Vector_Space/Word_Embeddings'
    rename(root_dir)
