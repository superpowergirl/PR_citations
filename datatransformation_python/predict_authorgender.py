from genderize import Genderize
import json
#print(Genderize().get(['James', 'Eva', 'Thunderhorse']))

path_name = 'aps-dataset-metadata-2019'
f_name = path_name + '/PRA/4/PhysRevA.4.1.json'
with open(f_name) as f:
    data = json.load(f)
    if 'authors' in data:
        author_temp = data.get('authors')
        paper_author_fname = [x['firstname'] for x in author_temp if x['type'] == 'Person']
        print(Genderize().get(paper_author_fname))