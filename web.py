from flask import Flask
from flask import render_template
from flask import request
from flask_cors import CORS
from es_client.es_client import elasticsearch_client
from flask import jsonify
import json
from flask import url_for

app = Flask(__name__)
CORS(app, supports_credentials=True)
url = 'http://gz.ccs.log.oa.com/elasticsearch'
headers = {'Cookie': 'x-host-key-ngn=16d4c8fb4cc-36f92e726b257cac0b689d52b7c2142716fa92d1; x-host-key-front=16d4c8fb6aa-7e2b83a3fbbc422bab1897338cfaa7c5e4a3a464; TCOA_TICKET=875F50A675EEF0617CAE2C4080C742B60E113683B9AAAB7AC7272109A795E357C514E53D2FEEBB22C6AD65C8F41FB908D3EEA31B4BB06DD46FEE51AB0EF862365F1D9C70B2F81493E2E1DF1D59F10097F14322DD2838A92A5C2A89FD018289522D719416F8D4E656EDC4CE16214936A4329F1BBD0DB01EBCB3EBDE62170E657F7DCE32BD31A76A8546242056C810768A7839B873CBBCE74306130DEC59CCCA7303E7471140B1ECC8; TCOA=B4sx5AmwL8; RIO_TCOA_TICKET=tof:875F50A675EEF0612625A9379AAEC522175368EDF1FCC9083C0DDEE500C278DFEE7220DE5AD66C213F3F98294A49E1FD8565746F470CA92F2E5479E52AEA543CB860732F7FBA17E0D08A6E2118046F22040A58D09386E647941ADA7438F763E9EF269AD7968B1FC86807990D695FEDBE8C650C26CAFF2ACB348876929B02143DA7403132D6DFA74B79FB9C9317A1D5B5A0E7A45C8035F67A566069D528D31D3976FFC3ABFBA1BAE28706280389679340B8670E05A4C446E83E84B0F9EEA9188B552B0AC84C878CBD'}

client = elasticsearch_client(url, headers)


@app.route('/', methods=["GET"])
def get():
    return app.send_static_file('index.html')


@app.route('/', methods=["POST"])
def post():
    data = request.json
    print('data:', data)
    res = client.search_ccs(appId=data['appid'], clusterId=data['clusterid'], kind=data['kind'], namespace=data['namespace'],
                            source=data['source'], fromtime=data['fromtime'], totime=data['totime'], reason=data['reason'], size=50)
    #print('res:', res)
    if 'code' in res:
        return jsonify(res), 600
    return jsonify(res)


if __name__ == '__main__':
    app.run(port=8080)
