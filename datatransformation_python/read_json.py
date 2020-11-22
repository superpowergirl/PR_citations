import json
import pandas as pd
from glob import glob

paper_doi_list =[]
paper_date_list = []
paper_author_list=[]
paper_title_list=[]
paper_affiliation_list=[]
path_name = 'aps-dataset-metadata-2019'
for f_name in glob(path_name+'/*/*/*.json'):
    with open(f_name) as f:
        data = json.load(f)
        paper_doi = data.get('id')
        paper_publishdate = data.get('date')
        paper_title = data.get('title').get('value')
        author_temp = data.get('authors')
        paper_author = [x['name'] for x in author_temp]
        paper_affiliation = data.get('affiliations')
        paper_doi_list.append(paper_doi)
        paper_date_list.append(paper_publishdate)
        paper_author_list.append(paper_author)
        paper_title_list.append(paper_title)
        paper_affiliation_list.append(paper_affiliation)

d = {'paper_doi':paper_doi_list, 'paper_pub_date':paper_date_list, 'paper_authors':paper_author_list,
     'paper_title':paper_title_list, 'paper_affiliations':paper_affiliation_list}
df_paper_metadata = pd.DataFrame(d)