from GoogleNews import GoogleNews
from newspaper import Article,Config
import newspaper
import pandas as pd
import numpy as np
import nltk
def getGoogleNewsLink(start,end,counts, keystring):
    '''
    start: start date
    end: last date
    counts: how many pages you want to turn
    keystring: "nasdaq AND eur  1"
    '''
    googlenews=GoogleNews(start=start,end=end)
    googlenews.search(keystring)
    for i in range(0,counts):
        googlenews.getpage(i)
        result=googlenews.result() 
       
    return pd.DataFrame(result)

def getGoogleNewsArticle(gnews):
    '''
    The input file should be the output of getGoogleNewsLink
    '''
    


    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

    config = Config()
    config.browser_user_agent = user_agent
    config.request_timeout = 10
   
    nltk.download('punkt')
    for n in gnews.index:
        article = Article(gnews.loc[n,'link'],config=config)
        try: 
          article.download()
          article.parse()
          article.nlp()
          gnews.loc[n,"Title"]=article.title
          gnews.loc[n,"Article"]=article.text
          gnews.loc[n,"Summary"]=article.summary
        except newspaper.article.ArticleException:
            pass
    return gnews