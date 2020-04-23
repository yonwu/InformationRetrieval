import argparse
from xml.etree.ElementTree import parse, Element
import subprocess


def modify_index_xml(file, corpus):
    index_file = parse(file)
    root = index_file.getroot()
    corpus_tree = root.find('corpus')
    path = corpus_tree.find('path')
    path.text = corpus
    index_file.write(file)


def modify_query_topic_xml(file, topic):
    index_file = parse(file)
    root = index_file.getroot()
    query_tree = root.find('query')
    number = query_tree.find('number')
    number.text = topic
    index_file.write(file)


def modify_query_command_xml(file, query):
    index_file = parse(file)
    root = index_file.getroot()
    query_tree = root.find('query')
    command = query_tree.find('text')
    command.text = query
    index_file.write(file)


if __name__ == "__main__":

    query_file = parse('my_queries.xml')

    parser = argparse.ArgumentParser(description='interact with indri.')

    parser.add_argument('-corpus', required=False, type=str, help='create indexing')

    parser.add_argument('-topic', required=False, type=str, help='create indexing')

    parser.add_argument('-query', required=False, type=str, help='queries ')

    parser.add_argument('-eval', action='store_true')

    args = parser.parse_args()

    if args.corpus:
        corpus = args.corpus
        file = 'my_index_parameters.xml'
        modify_index_xml(file, corpus)
        command = "IndriBuildIndex my_index_parameters.xml"
        subprocess.call(command, shell=True)

    if args.topic:
        topic = args.topic
        file = 'my_queries.xml'
        modify_query_topic_xml(file, topic)

    if args.query:
        query = args.query
        file = 'my_queries.xml'
        modify_query_command_xml(file, query)
        command = "IndriRunQuery my_queries.xml > my_run1_rankings.trec"
        subprocess.call(command, shell=True)

    if args.eval:
        command = "trec_eval -q -m official assessments/assessments2004/qrels_EN my_run1_rankings.trec"
        subprocess.call(command, shell=True)




