import requests

def get_data(url):
    '''
    功能：访问 url 的网页，获取网页内容并返回
    参数：
        url ：目标网页的 url
    返回：目标网页的 html 内容
    '''

    # 用'cookie'模拟登录网页解决跳转登录的问题！
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'cookie': '''_zap=5af1d8c0-fbdc-4de4-9e41-190de568d21d; _xsrf=c5479e9c-866a-494e-8d8d-f0707d5043e4; d_c0="ANDRQfB1eBGPTqmQ4kihicWKnJywGW7C9XA=|1592921756"; _ga=GA1.2.504778147.1592921761; q_c1=0618fdc555614340b32cc006ab8c0bd5|1603953744000|1594393532000; tst=h; tshl=; l_n_c=1; n_c=1; l_cap_id="NDgyOTZjNjU3M2NjNGZlZDhhOGM2NzhhYTE1ZTQ5MTM=|1605869815|f102f844358d7fcbd027d752cc6897255d8751a5"; r_cap_id="Zjk5YmMzZWM0NDJlNGNmNGIwMmEzOTlmNjRlOWYwOTc=|1605869815|10efa7ebaf58e63b10e1ef8b30cbebf40ce4d087"; cap_id="NjlkMWQ4MDUzN2Q2NDdiM2E0ZTc2ZDhkMDkwZGM2NmM=|1605869815|bfc0053415e365ecb67ad47c6272257560cfa39e"; capsion_ticket="2|1:0|10:1606099385|14:capsion_ticket|44:OTk4MmZhN2VlYWEyNGI3OGFmNDY3MzI1ZTRkYTJlODk=|b39521c0526b959f6964dc6c47b646409370f92fb43ef5ab6792937191f4fa3a"; z_c0="2|1:0|10:1606099420|4:z_c0|92:Mi4xbU1JZENBQUFBQUFBME5GQjhIVjRFU2NBQUFDRUFsVk4yNjdpWHdCbXM2UGc4MlAxUzFxX0QwaHdUUi15RElWZll3|9c175b53eb2dfdf1cc5ee06872173ba70321f8bb374b22cdd3a1f63b21e02ddd"; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1606130777,1606204953,1606291121,1606296289; SESSIONID=gDuL8VLDyRV7NgEzg1aWKtsIUxCWuDYz7OTdnl1zges; JOID=W14QCkMjKaeRd5rzMCOntg6qO3EtS27e3E7DvHhbdPKqOPy5SewMFM55lvw9oCmxMIYyeYbaQQbJdFTxXCdVsgY=; osd=VFgcAEwsL6ubeJX1PCmouQimMX4iTWLU00HFsHJUe_SmMvO2T-AGG8F_mvYyry-9Ook9f4rQTgnPeF7-UyFZuAk=; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1606298315; KLBRSID=81978cf28cf03c58e07f705c156aa833|1606298316|1606296280'''
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text

    except requests.HTTPError as e:
        print(e)
        print("HTTPError")
    except requests.RequestException as e:
        print(e)
    except:
        print("Unknown Error !")