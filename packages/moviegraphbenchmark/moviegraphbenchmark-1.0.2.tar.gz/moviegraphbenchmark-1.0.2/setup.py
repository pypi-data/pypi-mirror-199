# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['moviegraphbenchmark']

package_data = \
{'': ['*']}

install_requires = \
['pandas', 'pystow', 'requests', 'tqdm']

entry_points = \
{'console_scripts': ['moviegraphbenchmark = '
                     'moviegraphbenchmark.create_graph:create_graph_data']}

setup_kwargs = {
    'name': 'moviegraphbenchmark',
    'version': '1.0.2',
    'description': 'Benchmark datasets for Entity Resolution on Knowledge Graphs containing information about movies, tv shows and persons from IMDB,TMDB and TheTVDB',
    'long_description': '# Dataset License\nDue to licensing we are not allowed to distribute the IMDB datasets (more info on their license can be found [here](https://help.imdb.com/article/imdb/general-information/can-i-use-imdb-data-in-my-software/G5JTRESSHJBBHTGX?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=3aefe545-f8d3-4562-976a-e5eb47d1bb18&pf_rd_r=2TNAA9FRS3TJWM3AEQ2X&pf_rd_s=center-1&pf_rd_t=60601&pf_rd_i=interfaces&ref_=fea_mn_lk1#))\nWhat we can do is let you build the IMDB side of the entity resolution datasets yourself. Please be aware, that the mentioned license applies to the IMDB data you produce.\n\n# Usage\nYou can simply install the package via pip:\n```bash\npip install moviegraphbenchmark\n```\nand then run\n```bash\nmoviegraphbenchmark\n```\nwhich will create the data in the default data path `~/.data/moviegraphbenchmark/data`\n\nYou can also define a specific folder if you want with\n```bash\nmoviegraphbenchmark --data-path anotherpath\n```\n\nFor ease-of-usage in your project you can also use this library for loading the data (this will create the data if it\'s not present):\n\n```python\nfrom moviegraphbenchmark import load_data\nds = load_data()\n# by default this will load `imdb-tmdb`\nprint(ds.attr_triples_1)\n\n# specify other pair and specific data path\nds = load_data(pair="imdb-tmdb",data_path="anotherpath")\n\n# the dataclass contains all the files loaded as pandas dataframes\nprint(ds.attr_triples_2)\nprint(ds.rel_triples_1)\nprint(ds.rel_triples_2)\nprint(ds.ent_links)\nfor fold in in ds.folds:\n    print(fold)\n```\n\n# Dataset structure\nThere are 3 entity resolution tasks in this repository: imdb-tmdb, imdb-tvdb, tmdb-tvdb, all contained in the `data` folder. \nThe data structure follows the structure used in [OpenEA](https://github.com/nju-websoft/OpenEA).\nEach folder contains the information of the knowledge graphs (`attr_triples_*`,`rel_triples_*`) and the gold standard of entity links (`ent_links`). The triples are labeled with `1` and `2` where e.g. for imdb-tmdb `1` refers to imdb and `2` to tmdb. The folder 721_5fold contains pre-split entity link folds with 70-20-10 ratio for testing, training, validation.\n\n# Citing\nThis dataset was first presented in this paper:\n```\n@inproceedings{EAGERKGCW2021,\n  author    = {Daniel Obraczka and\n               Jonathan Schuchart and\n               Erhard Rahm},\n  editor    = {David Chaves-Fraga and\n               Anastasia Dimou and\n               Pieter Heyvaert and\n               Freddy Priyatna and\n               Juan Sequeda},\n  title     = {Embedding-Assisted Entity Resolution for Knowledge Graphs},\n  booktitle = {Proceedings of the 2nd International Workshop on Knowledge Graph Construction co-located with 18th Extended Semantic Web Conference (ESWC 2021), Online, June 5, 2021},\n  series    = {{CEUR} Workshop Proceedings},\n  volume    = {2873},\n  publisher = {CEUR-WS.org},\n  year      = {2021},\n  url       = {http://ceur-ws.org/Vol-2873/paper8.pdf},\n}\n```\n',
    'author': 'Daniel Obraczka',
    'author_email': 'obraczka@informatik.uni-leipzig.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ScaDS/MovieGraphBenchmark',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1',
}


setup(**setup_kwargs)
