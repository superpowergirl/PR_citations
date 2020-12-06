import json
import pandas as pd
from glob import glob
import numpy as np

paper_doi_list =[]
paper_journal_category_list=[]
paper_date_list = []
paper_author_list=[]
paper_author_count=[]
paper_length_list=[]
paper_title_list=[]
paper_affiliation_list=[]

path_name = 'aps-dataset-metadata-2019'
#for f_name in glob(path_name+'/*/*/*.json'):
for f_name in glob(path_name + '/RMP/59/RevModPhys.59.S1.json'):
    with open(f_name) as f:
        data = json.load(f)
        paper_doi = data.get('id') #journal paper doi - e.g. 10.1103/PhysRevA.4.1
        paper_journal_category = data.get('journal').get('id') #category of journal, e.g. PRA, PRB, etc.
        paper_publishdate = data.get('date') #Date paper was published
        paper_title = data.get('title').get('value') # Journal paper title
        author_af_list = [] #list of journal paper authors' affiliations
        paper_author =[] # list of journal paper authors
        if 'authors' in data:
            author_temp = data.get('authors')
            paper_author = [x['name'] for x in author_temp if x['type']=='Person']
            if 'affiliations' in data:
                paper_affiliation = data.get('affiliations')
                if any('affiliationIds' in d for d in author_temp):
                    author_af_id = [x['affiliationIds'] for x in author_temp if 'affiliationIds' in x]
                    for i in author_af_id:
                        author_ind_af_list=[]
                        for j in i:
                            author_ind_af_list.extend([x['name'] for x in paper_affiliation if x['id'] == j])
                        author_af_list.append(author_ind_af_list)
        paper_length = data.get('numPages') # length of the paper
        paper_doi_list.append(paper_doi)
        paper_date_list.append(paper_publishdate)
        paper_author_list.append(paper_author)
        paper_author_count.append(len(paper_author))
        paper_title_list.append(paper_title)
        paper_affiliation_list.append(author_af_list)
        paper_length_list.append(paper_length)
        paper_journal_category_list.append(paper_journal_category)

d = {'paper_doi':paper_doi_list, 'paper_journal_category':paper_journal_category_list,
     'paper_pub_date':paper_date_list,
     'paper_length':paper_length_list,
     'paper_authors':paper_author_list,
     'paper_authors_count':paper_author_count,
     'paper_affiliations':paper_affiliation_list,
     'paper_title':paper_title_list}
df_paper_metadata = pd.DataFrame(d)
df_new = df_paper_metadata.explode('paper_authors')

df_paper_metadata_notnull = df_paper_metadata[df_paper_metadata['paper_authors'].map(len) != 0]
df_paper_metadata_notnull = df_paper_metadata_notnull[df_paper_metadata_notnull['paper_affiliations'].map(len) != 0]
# clean empty string list from aff

# def clean_aff(df_row):
#     xx = df_row['paper_affiliations']
#     yy = [item for sublist in xx for item in sublist]
#     if '' in yy:
#         return True
#     else:
#         return False
#
# delete_flag  = df_paper_metadata_notnull.apply(clean_aff, axis=1)
# df_paper_metadata_notnull = df_paper_metadata_notnull[~delete_flag]

def get_first_aff(df_row):
    aff = list(df_row['paper_affiliations'])
    print(aff)

    for i in range(len(aff)):
        if len(aff[i])==0:
            aff[i] = 'NOAFF'
        if '' in aff[i]:
            aff[i] = 'NOAFF'
        else:
            aff[i] = aff[i][0]

    #first_aff_list = [item[0] for item in aff]

    return aff

df_paper_metadata_notnull['paper_affiliations_first'] = df_paper_metadata_notnull.apply(get_first_aff, axis=1)



def explode(df, lst_cols, fill_value=''):
    # make sure `lst_cols` is a list
    if lst_cols and not isinstance(lst_cols, list):
        lst_cols = [lst_cols]
    # all columns except `lst_cols`
    idx_cols = df.columns.difference(lst_cols)

    # calculate lengths of lists
    lens = df[lst_cols[0]].str.len()

    if (lens > 0).all():
        # ALL lists in cells aren't empty
        print("1")
        y = [np.concatenate(df[col].values) for col in lst_cols]
        print("2")
        return pd.DataFrame({
            col:np.repeat(df[col].values, df[lst_cols[0]].str.len())
            for col in idx_cols
        }).assign(**{col:np.concatenate(df[col].values) for col in lst_cols}) \
          .loc[:, df.columns]
        print("3")
    else:
        # at least one list in cells is empty
        return pd.DataFrame({
            col:np.repeat(df[col].values, df[lst_cols[0]].str.len())
            for col in idx_cols
        }).assign(**{col:np.concatenate(df[col].values) for col in lst_cols}) \
          .append(df.loc[lens==0, idx_cols]).fillna(fill_value) \
          .loc[:, df.columns]


explode_cols = ['paper_authors', 'paper_affiliations_first']


def myexplode(df_row):
    auth_list = list(df_row['paper_authors'])
    aff_list = list(df_row['paper_affiliations_first'])
    doi_list = [df_row['paper_doi']]*len(auth_list)

    tups = list(zip(auth_list, aff_list, doi_list))
    return tups


    #return res


auth_aff_dict_df = df_paper_metadata_notnull.apply(myexplode, axis = 1)
auth_aff_dict_df_exp = auth_aff_dict_df.explode()
df_auth_aff = pd.DataFrame(auth_aff_dict_df_exp.tolist())
df_auth_aff.columns = ['author_name', 'affiliation', 'doi']