from setuptools import setup, find_packages

setup(
    name='facebook_page_scrape_test1',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'geopy',
        'pandas',
        'selenium'

    ],
)