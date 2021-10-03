'''
Created on 
Course work: 
@author: vedha, ajesh
Source:
    
'''

# Import necessary modules
from jina import Document, DocumentArray


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


def startpy():
    docs = prep_docs(input_file="prs.txt",num_size = -1, shuffle=True)


if __name__ == '__main__':
    startpy()