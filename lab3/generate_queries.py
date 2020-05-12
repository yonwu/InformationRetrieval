import string
import xml.etree.ElementTree as ET
from itertools import islice


def take(n, iterable):
    # "Return first n items of the iterable as a list"
    return list(islice(iterable, n))


def get_config_from_file(file):
    with open(file, "r") as infile:
        sents = infile.read().split("\n\n")
        if sents[-1] == "":
            sents = sents[:-1]
    query_config = {}
    for sent in sents:
        lines = sent.split("\n")
        for line in lines:
            if line.startswith('<TOPNO>'):
                topic = line.strip('<TOPNO>').strip('</TOPNO>')
            if line.startswith('<TITLE>'):
                title = line.strip('<TITLE>').strip('</TITLE>').translate(str.maketrans('', '', string.punctuation))
                title = '#combine(' + title + ')'
        query_config[topic] = title

    return query_config


def create_query_tree(key, value):
    newtree = ET.Element('query')
    number_element = ET.SubElement(newtree, 'number')
    number_element.text = key
    text_element = ET.SubElement(newtree, 'text')
    text_element.text = value
    return newtree


def update_xml(file, topic_configs):
    query_xml = ET.parse(file)
    root = query_xml.getroot()
    # clean old queries
    for query in root.findall('query'):
        root.remove(query)
    # update with new queries
    for topic_config in topic_configs[::-1]:
        query_element = create_query_tree(topic_config[0], topic_config[1])
        root.insert(1, query_element)
    query_xml.write(file, encoding='utf-8')


if __name__ == "__main__":
    file = 'MedTopics.txt'
    all_query_config = get_config_from_file(file)
    fifty_topic_config = take(50, all_query_config.items())

    update_xml('my_queries_origin.xml', fifty_topic_config)
    update_xml('my_queries_composed.xml', fifty_topic_config)
