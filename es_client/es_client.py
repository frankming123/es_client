import requests
import json
import logging

ERR_NOT_JSON = {'code': -1,
                'message': 'type of returned elasticsearch data is not json'}
ERR_NOT_200 = {'code': -2,
               'message': 'response code of elasticsearch is not 200'}
logging.basicConfig(level=logging.WARNING)


class elasticsearch_client:
    url = ''
    headers = {}

    def __init__(self, url='127.0.0.1:9200', headers={}):
        self.url = url
        self.headers = headers

    def health(self):
        url = self.url+'/_cat/health?v'
        r = requests.get(url, headers=self.headers)
        if r.status_code != 200:
            logging.warning(r.status_code)
            return r.status_code
        return r.text

    def search(self, index='', q='', size=10):
        url = self.url+'/'+index+'/_search/'
        payload = {'q': q, 'size': size, 'sort': 'lastSeenTime:desc'}

        logging.info('url: '+url)
        logging.info('payload: '+str(payload))
        r = requests.get(url, params=payload, headers=self.headers)
        if r.status_code != 200:
            logging.warning(
                'response code from elasticsearch is {}'.format(r.status_code))
            return ERR_NOT_200
        logging.info('res: '+r.text)
        if 'application/json' not in r.headers['Content-Type']:
            logging.warning('data from elasticsearch not json')
            return ERR_NOT_JSON
        return r.json()

    def search_ccs(self, appId='', clusterId='', kind='', namespace='', message='', source='', reason='', fromtime='', totime='', size=10):
        strs = []
        if appId:
            strs.append("appId:"+appId)
        if clusterId:
            strs.append("clusterId:"+clusterId)
        if kind:
            strs.append("kind:"+kind)
        if namespace:
            strs.append("namespace:"+namespace)
        if message:
            strs.append("message:"+message)
        if source:
            strs.append("source:"+source)
        if reason:
            strs.append("reason"+reason)
        if fromtime and totime:
            strs.append(
                'lastSeenTime:{{"{0}" TO "{1}"}}'.format(fromtime, totime))
        q = ' AND '.join(strs)
        return self.search(index='ccs_event_log_*', q=q, size=size)


if __name__ == '__main__':
    url = ''
    headers={}
    es = elasticsearch_client(url, headers)
    res = es.search_ccs(clusterId='cls-qv3z2icb', fromtime='2019-09-18T00:00:00.000+08:00',
                        totime='2019-09-18T23:59:59.999+08:00', size=2)
    print(json.dumps(res))
