try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Jellyfish',
    'author': 'Eriberto Lopez',
    'url': 'https://github.com/EribertoLopez/Jellyfish', 
    'download_url': 'https://github.com/EribertoLopez/Jellyfish',
    'author_email': 'elopez3@uw.edu',
    'version': '0.0.1',
    'install_requires': ['FlowCytometryTools', 'pydent', 'pandas'],
    'packages': [],
    'scripts': [],
    'name': 'Jellyfish',
    'license': 'Copyright University of Washington'
}

setup(**config)