'''
Created on 
Course work: 
@author: vedha, ajesh
Source:
    
'''

# Import necessary modules
from flask.wrappers import Request
from jina import Document, DocumentArray
from jina import Flow
from flask import Flask, render_template


app = Flask(__name__)


def preprocess():

    delim = '---------------------------------------------------------------------------------------------------------------'
    length = len(delim)

    delim = f"{'-' * 111}/"

    my_file = open("prs.txt", "r")
    content = my_file.read()
    content_list = content.strip().split(f"{'-' * 111}/")
    my_file.close()

    for i in range(len(content_list)):
        if 'sol:' in content_list[i]:
            ind = i
            break

    samp = content_list[ind].replace('\n', ' ').strip()

    samp.split('sol:')[-1].strip()


def prep_docs(input_file, num_size = -1, shuffle=True):
    docs = DocumentArray()
    error = []
    print(f"Processing {input_file}")


    with open("prs.txt", "r") as my_file:
      content = my_file.read()
      content_list = content.strip().split(f"{'-' * 111}/")
    

    if shuffle:
        import random
        # random_seed = 0

        # random.seed(random_seed)
        random.shuffle(content_list)
    
    num_size = len(content_list) if num_size == -1 else num_size

    for error in content_list:
        doctext = error.replace('\n',' ').strip()
        if len(doctext) > 99:
          doc = Document(text=doctext)
          sol = None
          # if 'sol:' in doctext:
          #   sol = doctext.split('sol:')[-1].strip()
          # doc.tags['solution'] = sol
          docs.extend([doc])

    return docs[:num_size]

def somethings_going_on_here(docs):

    for i in docs:
        if len(i.text) == 0:
            print(len(i.text))

    model = "sentence-transformers/paraphrase-distilroberta-base-v1" # Any model from Huggingface

    flow = (
        Flow()
        .add(
            name="error_text_encoder",
            uses="jinahub://TransformerTorchEncoder",
            uses_with={"pretrained_model_name_or_path": model},
        )
        .add(
            name="error_text_indexer",
            uses='jinahub://SimpleIndexer',
        )
    )

    with flow:
        flow.index(
            inputs=docs,
        )

    docs[0].text

    query_doc = Document(text='nbformat.reader.NotJSONError: Notebook does not appear to be JSON')

    with flow:
        response = flow.search(inputs=query_doc, return_results=True)

    matches = response[0].docs[0].matches


    for ind, i in enumerate(matches):
        print(f' error number : {ind} '.center(60,'='))
        print(i.text)
        print()

    
    

   
@app.route('/', methods=['GET'])
def startpy():
    
    # docs = prep_docs(input_file = "prs.txt", num_size = -1, shuffle = True)
    # somethings_going_on_here(docs)

    return render_template('index.html')


   
@app.route('/', methods=['POST'])
def post_search_results():
    
    # docs = prep_docs(input_file = "prs.txt", num_size = -1, shuffle = True)
    # somethings_going_on_here(docs)

    
    data = [
        {
            "location" : "sample text",
            "text" : "target query"
        },
        {
            "location" : "sample text",
            "text" : "target query"
        },
        {
            "location" : "sample text",
            "text" : "target query"
        }
    ]

    return render_template('index.html', result = data)


if __name__ == '__main__':

    # preprocess()
    app.run(host="0.0.0.0", port="5555", debug = True)