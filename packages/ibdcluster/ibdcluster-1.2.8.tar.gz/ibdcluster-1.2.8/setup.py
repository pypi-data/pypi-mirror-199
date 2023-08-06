# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['analysis', 'callbacks', 'cluster', 'factory', 'log', 'models', 'plugins']

package_data = \
{'': ['*']}

install_requires = \
['igraph>=0.10.4,<0.11.0',
 'numpy>=1.22.2,<2.0.0',
 'pandas>=1.4.0,<2.0.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'scipy>=1.8.0,<2.0.0',
 'toml>=0.10.2,<0.11.0',
 'tqdm>=4.62.3,<5.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['drive = ibdcluster.ibdcluster:app']}

setup_kwargs = {
    'name': 'ibdcluster',
    'version': '1.2.8',
    'description': 'A CLI tool to help identify ibd sharing within networks across a locus of interest at biobank scale and then test for phenotypic enrichment within these networks.',
    'long_description': '[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n# IBDCluster v1.2.1:\n\n## Documentation:\n___\nThis readme is a more technical description of the project, providing information about the class structures and relationships. More practical documentation about how to install and use the program can be found here: [IBDCluster documentation (still a work in progress)](https://jtb324.github.io/IBDCluster/) \n\n## Purpose of the project: \n___\nThis project is a cli tool that clusters shared ibd segments within biobanks around a gene of interest. These network are then analyzed to determine how many individuals within a network are affected by a phenotype of interest.\n\n## General PipeLine:\n___\n```mermaid\nflowchart LR\n    A(IBD Information) --> B(Identified Networks) --> C(Binomial test for enrichment of Phenotypes)\n```\n\n## installing:\n___\n***Cloning from github and modify permissions:***\n1. Clone the project into the appropriate directory using git clone.\n2. cd into the IBDCluster directory\n```\ncd IBDCluster\n```\n2. run the following command to set the right permissions on the IBDCluster.py file\n```\nchmod +x IBDCluster/IBDCluster.py\n```\n***Installing dependencies:***\nNext install all the necessary dependencies. The steps for this vary depending on what package manager you are using.\n\n*If using conda:*\n1. There is a environment.yml file in the main IBDCluster directory. Run the following command and it will create an environment called IBDCluster\n\n```\nconda env create -f environment.yml\n```\n\n2. You can now activate the environment by calling:\n\n```\nconda activate IBDCluster\n```\n\n*If using mamba:*\n1. This is the same as the conda section except use the command\n```\nmamba env create -f environment.yml\n```\n2. You can activate this environment using:\n```\nconda activate IBDCluster\n```\n\n*If using Poetry*\n1. The requirements for a poetry project are also in the IBDCluster directory. Ideally you need to activate some type of virtual environment first. This environment can be either a conda environment or a virtualenv. Once this environment is activated you can call:\n\n```\npoetry install\n```\n\n2. At this point all necessary dependencies should be installed.\n\n* if you wish to find more information about the project you can find the documentation here: https://python-poetry.org/\n\n***Adding IBDCluster to the users $PATH:***\nTo be able to run the IBDCluster program without having to be in the source code directory, you should add the IBDCluster.py file to your path.\n\n1. In your .bashrc file or .zshrc add the line :\n```\nexport PATH="{Path to the directory that the program was cloned into}/IBDCluster/IBDCluster:$PATH"\n```\n2. run this line:\n```\nsource .bashrc\n```\nor\n```\nsource .zshrc\n```\nThis will allow you to run the code by just typing IBDCluster.py from any directory.\n\n***Running IBDCluster***\n* You can find all the optional parameters by running:\n```\nIBDCluster.py --help\n```\n## Running the code:\n___\n*\n\n## Reporting Issues:\n___\nAll issues can be reported using the templates in the .github/ folder. There are options for bug_reports and for feature_request\n\n## Technical Details of the project:\n___\n* This part is mainly for keeping track of the directory structure.\n\n## Project Structure:\n___\n```\n├── IBDCluster\n│   ├── analysis\n│   │   ├── main.py\n│   │   ├── percentages.py\n│   ├── callbacks\n│   │   ├── check_inputs.py\n│   ├── models\n│   │   ├── cluster_class.py\n│   │   ├── indices.py\n│   │   ├── pairs.py\n│   │   ├── writers.py\n│   ├── log\n│   │   ├── logger.py\n│   ├── cluster\n│   │   ├── main.py\n│   ├── IBDCluster.py\n├── .env\n├── environment.yml\n├── .gitignore\n├── poetry.lock\n├── pyproject.toml\n├── README.md\n├── requirements.txt\n│   ├── tests\n│   │   ├── test_data\n│   │   ├── test_integration\n\n```\n## Comments about models:\n___\n* Classes for the cluster_class.py:\n\n```mermaid\nclassDiagram\n    class Cluster {\n        ibd_file: str\n        ibd_program: str\n        indices: models.FileInfo\n        count: int=0\n        ibd_df: pd.DataFrame=pd.DataFrame\n        network_id: str=1\n        inds_in_network: Set[str]=set\n        network_list: List[Network]=list\n    }\n    class Network {\n        gene_name: str\n        gene_chr: str\n        network_id: int\n        pairs: List[Pairs]=list\n        iids: Set[str]=set\n        haplotypes: Set[str]=set\n        +filter_for_seed(ibd_df: pd.DataFrame, ind_seed: List[str], indices: FileInfo, exclusion: Set[str]=None) -> pd.DataFrame\n        #determine_pairs(ibd_row: pd.Series, indices: FileInfo) -> Pairs\n        +gather_grids(dataframe: pd.DataFrame, pair_1_indx: int, pair_2_indx: int) -> Set[str]\n        +update(ibd_df: pd.DataFrame, indices: FileInfo) -> None\n    }\n    class FileInfo {\n        <<interface>>\n        id1_indx: int\n        ind1_with_phase: int\n        id2_indx: int\n        ind2_with_phase: int\n        chr_indx: int\n        str_indx: int\n        end_indx: int\n        +set_program_indices(program_name: str) -> None\n    }\n    Cluster o-- Network\n```\n\n## Entity relationships:\n___\n```mermaid\nerDiagram\n    NETWORK }|--|{ PAIRS : contains\n    NETWORK {\n        string gene_name\n        string chromosome\n        int network_id\n    }\n    NETWORK }|--|{ IIDS : contains\n    NETWORK }|--|{ HAPLOTYPES : contains\n    PAIRS {\n       string pair_1_id\n       string pair_1_phase \n       string pair_2_id\n       string pair_2_phase \n       int chromosome_number\n       int segment_start \n       int segment_end\n       float length \n       series affected_statuses \n    }\n    IIDS {\n        string Individual-ids\n    }\n    HAPLOTYPES {\n        string haplotype-phase\n    }\n```\n## Plugins: (all the plugins are classes)\n___\n**NetworkWriter**\n```mermaid\nclassDiagram\n    class NetworkWriter {\n        gene_name: str\n        chromosome: str\n        carrier_cols: List[str]\n        #_form_header() -> str\n        #_find_min_phecode(analysis_dict: Dict) -> Tuple[str, str]\n        #_form_analysis_string(analysis_dict: Dict) -> str\n        +write(**kwargs) -> None\n\n    }\n\n```\n\n## Work in Progress:\n---\n',
    'author': 'jtb324',
    'author_email': 'james.baker@vanderbilt.edu',
    'maintainer': 'jtb324',
    'maintainer_email': 'james.baker@vanderbilt.edu',
    'url': 'https://jtb324.github.io/IBDCluster/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0.0',
}


setup(**setup_kwargs)
