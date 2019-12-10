"""
A setuptools based setup module.
"""

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

opts = dict(name='CSE583project-Group9',
            version='1.0.0',
            description='Give movie recommendations based on needs',
            long_description=long_description,
            url='https://github.com/xiashuhan/CSE583project-Group9',
            license=open('LICENSE').read(),
            author='Sizhe Chen, Yandi Jin, Miaoran Li, Shuhan Xia, Jing Xu',
            packages=find_packages(),
            install_requires=['ast', 'collections', 'dash',
                              'dash_bootstrap_components',
                              'dash_core_components',
                              'dash_html_components', 'http',
                              'json', 'nltk', 'numpy', 'pandas',
                              'pickle', 'sklearn', 'surprise'],
            package_data={'movie_recommendations': ['movies-dataset/*.*',
                                                    'movies-dataset/source/*.*']}
            )

if __name__ == '__main__':
    setup(**opts)
