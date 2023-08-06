from GoogleNews import GoogleNews
from newspaper import Article

def getGoogleNewsLink(start,end,counts, keystring):
    googlenews=GoogleNews(start=start,end=end)
    googlenews.search(keystring)
    for i in range(0,counts):
        googlenews.getpage(i)
        result=googlenews.result()
        df=pd.DataFrame(result)
    return df