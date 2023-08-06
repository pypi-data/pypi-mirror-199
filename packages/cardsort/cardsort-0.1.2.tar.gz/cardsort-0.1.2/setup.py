# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cardsort']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.7.1,<4.0.0',
 'numpy>=1.24.2,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'scipy>=1.10.1,<2.0.0']

setup_kwargs = {
    'name': 'cardsort',
    'version': '0.1.2',
    'description': 'Analyse cardsorting data',
    'long_description': '# Cardsort analysis\n\nA package that helps UX researchers quickly analyse data from cardsorting exercises.\n\n__More precisely, it helps you to:__\n* Create dendrograms\n* Extract user-generated category-labels\n* Using data exports from [kardsort.com](https://kardsort.com/)\n\n## Table of Contents\n\n- [Documentation](#documentation)\n- [Quick start](#quick-start)\n  - [Installation](#installation)\n  - [Usage](#usage)\n  - [Accepted data](#accepted-data)\n- [Contributing](#contributing)\n- [License](#license)\n- [Credits](#credits)\n\n## Documentation\n[cardsort.readthedocs.io](https://cardsort.readthedocs.io)\n\n## Quick start\n### Installation\n\n```bash\n$ pip install cardsort\n```\n\n### Usage\n\n`cardsort` can be used to create dendrograms and extract user-generated category-labels:\n\n```python\nfrom cardsort import analysis\nimport pandas as pd\n\npath = "example-data.csv" # data with columns: card_id, card_label, category_id, category_label, user_id\ndf = pd.read_csv(path) \n\n# create a dendrogram that summarized user-generated clusters\nanalysis.create_dendrogram(df)\n```\n\n__Output__\n\n![Dendrogram plot generated from example data](https://github.com/katoss/cardsort/blob/main/docs/dendrogram.png?raw=true)\n\n```python\n# learn which category labels users gave to clusters\ncards = [\'Banana\', \'Apple\']\nanalysis.get_cluster_labels(df, cards)\n```\n__Output__\n\n[\'Healthy snacks\', \'Snacks\', \'Fruits\', \'Food\']\n\n\n### Accepted data\n* This package works with data exports from [kardsort.com](https://kardsort.com/) (Export format \'Casolysis Data (.csv) - Recommended\')\n* This data equals the following structure: ```card_id, card_label, category_id, category_label, user_id```\n\nSee the [documentation](https://cardsort.readthedocs.io) for details.\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`cardsort` was created by Katharina Kloppenborg and is licensed under the terms of the MIT license.\n\n## Credits\n\n`cardsort` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Katharina Kloppenborg',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
