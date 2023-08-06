from setuptools import setup, find_packages

setup(
    name='uci_5640',
    version='0.1.7',
    description='For fun',
    author='Xuhu Wan',
    author_email='xuhu.wan@gmail.com',
    install_requires=[
        'numpy',
        'pandas',
        "TextBlob",
        "GoogleNews",
        "tweepy",
        "pyLDAvis",
        "newspaper3k",
        "wordcloud",
        "stop_words",
        "gensim",
        "nltk"
    ],
    packages=['uci_5640'],
)
