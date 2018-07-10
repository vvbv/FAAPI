import requests
import bs4
import time

import traceback, sys

class FAGet():
    base_url = 'https://www.furaffinity.net/'
    interval = 12

    def __init__(self, logger=(lambda *x: None)):
        logger('FAGet -> init')
        self.lastget = -FAGet.interval
        self.Log     = logger

    def get(self, Session, url, **params):
        self.Log(f'FAGet get -> url:{url} params:{params}')
        url = f'{FAGet.base_url.strip("/")}/{url.strip("/")}/'

        t = FAGet.interval - time.time() - self.lastget
        if t > 0:
            self.Log(f'FAGet get -> wait {t} secs')
            time.sleep(t)

        self.lastget = time.time()

        try:
            get = Session.get(url, params=params)
            self.Log(f'FAGet get -> get status:{get.ok}')

            return get if get.ok else None
        except:
            err = traceback.format_exception(*sys.exc_info())
            err = ['FAGet get -> error: '+e.strip().replace('\n', ' =') for e in err]
            self.Log(err)
            return None

    def getParse(self, Session, url, **params):
        self.Log(f'FAGet getParse -> url:{url} params:{params}')
        get = self.get(Session, url, **params)
        get = bs4.BeautifulSoup(get.text, 'lxml') if get else None

        self.Log(f'FAGet getParse -> {"success" if get else "fail"}')

        return get


    def pageFind(self, Session, url, **kwargs):
        self.Log(f'FAGet pageFind -> url:{url} kwargs:{kwargs}')
        page = self.get(Session, url)
        page = bs4.BeautifulSoup(page.text, 'lxml') if page else None

        if kwargs and page:
            find = page.find(**kwargs)
            self.Log(f'FAGet pageFind -> {len(find)} items')
            return find
        else:
            self.Log(f'FAGet pageFind -> fail')
            return False

    def pageFindAll(self, Session, url, **kwargs):
        self.Log(f'FAGet pageFindAll -> url:{url} kwargs:{kwargs}')
        page = self.get(Session, url)
        page = bs4.BeautifulSoup(page.text, 'lxml') if page else None

        if kwargs and page:
            find = page.findAll(**kwargs)
            self.Log(f'FAGet pageFindAll -> {len(find)} items')
            return find
        else:
            self.Log(f'FAGet pageFindAll -> fail')
            return False