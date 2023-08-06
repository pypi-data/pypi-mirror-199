from setuptools import setup, find_packages

setup(
    name='msba_wan',
    version='0.1.7',
    description='For fun',
    author='Xuhu Wan',
    author_email='xuhu.wan@gmail.com',
    packages=find_packages(),
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
)
