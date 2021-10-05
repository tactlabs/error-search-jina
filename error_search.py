'''
Created on 
Course work: 
@author: vedha, ajesh, jaabir
Source:
    
'''

# Import necessary modules

from jina import Document, DocumentArray
from jina import Flow
import random
import os




def prep_docs(input_file = "prs.txt", num_size = -1, shuffle = True):
    docs = DocumentArray()
    error = []
    print(f"Processing {input_file}")


    with open("prs.txt", "r") as my_file:
      content = my_file.read()
      content_list = content.strip().split(f"{'-' * 111}/")
    

    if shuffle:
        random.shuffle(content_list)
    
    num_size = len(content_list) if num_size == -1 else num_size

    for error in content_list:
        doctext = error.replace('\n',' ').strip()
        if len(doctext) > 10:
          doc = Document(text=doctext)
          sol = None
          if 'sol:' in doctext:
            sol = doctext.split('sol:')[-1].strip()
          doc.tags['solution'] = sol
          docs.extend([doc])

    return docs[:num_size]


def indexing( docs ):
    
    model = "sentence-transformers/paraphrase-distilroberta-base-v1" # Any model from Huggingface
    
    # global flow

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

    os.system('rm -rf workspace')
    with flow:
        flow.index(
            inputs=docs,
        )


    return flow


def search_results(flow, query):

    query_doc = Document(text = query)
    print(query_doc)
    
    with flow:
        response = flow.search(inputs=query_doc, return_results=True)

    matches = response[0].docs[0].matches
    
    data = [
        {
            "error_text" : doc.text,
            "solution" : doc.tags['solution']
        } for doc in matches
    ]

    return data



