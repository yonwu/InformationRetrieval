import requests
from bs4 import BeautifulSoup
import json


def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


def send_request(request_url):
    print("processing url:", request_url)
    response = requests.get(url)
    return response


def get_nce_corpus(response):
    result_text = []
    response_content = response.content
    soup = BeautifulSoup(response_content, 'html5lib')
    tables_tmp = soup.find_all(class_='dialogTbl')
    if len(tables_tmp) == 0:
        divs = soup.find_all(class_="content")
        for p in divs[0].findAll('p'):
            text = p.getText().strip().replace(u'\xa0', u' ')
            contain_chinese = is_contains_chinese(text)
            if len(text) > 0 and not contain_chinese:
                text = text.replace('\t', "").split("\n")
                text = [i for i in text if i]
                result_text.append(text)

    else:
        tables = tables_tmp[0]
        for tr in tables.findAll('tr'):
            for td in tr.findAll('td'):
                co = td.getText().replace('\t', "").replace('\n', ""). \
                    replace("\xa0 ", "").replace("\xa0", "")
                if co and not str.isdigit(co):
                    result_text.append(co)

    titles = soup.find_all(class_="title")
    text_title = titles[0].h1.getText()
    text_title = [i for i in text_title.split() if not is_contains_chinese(i)]
    separator = ' '
    text_title = separator.join(text_title)
    return result_text, text_title


def build_url(English_level, pages):
    urls = []
    new_base = 'http://en-nce.xiao84.com/' + English_level + '/'
    for page in pages:
        new_url = new_base + str(page) + '.html'
        urls.append(new_url)
    return urls


if __name__ == "__main__":

    nce1_pages = range(19991, 20011, 2)
    nce2_pages = range(20136, 20147, 1)
    nce3_pages = range(20233, 20244, 1)
    nce4_pages = range(20293, 20303, 1)

    urls_nce1 = build_url(English_level="nce1", pages=nce1_pages)
    urls_nce2 = build_url(English_level="nce2", pages=nce2_pages)
    urls_nce3 = build_url(English_level="nce3", pages=nce3_pages)
    urls_nce4 = build_url(English_level="nce4", pages=nce4_pages)

    urls_dic = {"nce1": urls_nce1, "nce2": urls_nce2, "nce3": urls_nce3, "nce4": urls_nce4}

    corpus = {}
    for level, urls in urls_dic.items():
        corpus[level] = list()
        sub_dic = {}
        for url in urls:
            try:
                r = send_request(url)
                r.raise_for_status()
                content, title = get_nce_corpus(r)
                sub_dic[title] = content
                print(title)
            except:
                print("Connection Error, response code: ", r.status_code)
        corpus[level].append(sub_dic)

    with open('corpus.json', 'w') as fp:
        json.dump(corpus, fp, indent=4, ensure_ascii=False)
