# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['portfolios', 'portfolios.tests']

package_data = \
{'': ['*']}

install_requires = \
['cvxpy>=1.3.1,<2.0.0',
 'numpy>=1.24.2,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'plotext>=5.2.8,<6.0.0',
 'plotly>=5.13.1,<6.0.0',
 'toml>=0.10.2,<0.11.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['markowitz = portfolios.markowitz:experiment',
                     'ptfio = portfolios.cli:app',
                     'test = portfolios.tests.test_utils:app']}

setup_kwargs = {
    'name': 'portfolios',
    'version': '0.1.0',
    'description': '',
    'long_description': "# Portfolio Optimization Experiments\n\nI've been interested in finance for a long time, but I've never had the\nopportunity to learn about it in a structured way. This idea came to me\nafter a twitter mutual mentioned that french state pensions had to be better\nin terms of revenue for middle class people compared to S&P 500. I was curious\nabout how to compare the two, and I started to learn about financial concepts\nsuch as volatility, risk, and return. I also wanted to learn about how to compare\nmetrics such as the IRR via the Sharpe ratio, and how to compare risk-free assets\nsuch as french pensions to risky assets such as S&P 500.\n\nThe experiments can be found on [GitHub](https://github.com/arnos-stuff/portfolios),\nand the results are published in sections of [my optimization book](https://optim.arnov.dev)\n(which is also open source).\n\n## Main tools (for now)\n\n- [Pandas](https://pandas.pydata.org/)\n- [Numpy](https://numpy.org/)\n- [CVXPY](https://www.cvxpy.org/)\n- [Plotly](https://plotly.com/python/)\n\n## Upcoming experiments\n\n- Model the french pension system as an asset & compare it to S&P 500\n- Estimate risk aversion from historical data\n- Calculate the tradeoff curve for the french pension system\n\n## Contributors\n\n- [Arno](https://twitter.com/arno_shae)\n- [Max](https://twitter.com/max_oikonomikos)\n",
    'author': 'arnos-stuff',
    'author_email': 'bcda0276@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
