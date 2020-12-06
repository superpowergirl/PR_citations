import json
import pandas as pd
from glob import glob

paper_doi_list =[]
paper_title_list = []
paper_title_format_list =[]

path_name = 'aps-dataset-metadata-2019'
for f_name in glob(path_name+'/PRA/*/*.json'):
    with open(f_name) as f:
        data = json.load(f)
        paper_doi = data.get('id')
        paper_title = data.get('title').get('value')
        paper_doi_list.append(paper_doi)
        paper_title_type= data.get('title').get('format')
        paper_title_list.append(paper_title)
        paper_title_format_list.append(paper_title_type)
d = {'paper_doi':paper_doi_list, 'paper_title':paper_title_list,
     'paper_title_type':paper_title_format_list}
df_paper_title = pd.DataFrame(d)