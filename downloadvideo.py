# -*- coding: utf-8 -*-

import urllib.request
import time
import json
import http.cookiejar
import re
import zlib

# 获取Cookiejar对象（存在本机的cookie消息）
cookie = http.cookiejar.CookieJar()
# 自定义opener,并将opener跟CookieJar对象绑定
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
# 安装opener,此后调用urlopen()时都会使用安装过的opener对象
urllib.request.install_opener(opener)

home_url = 'https://sv.ksmobile.net/video/index?vercode=10110178&ptvn=2&countryCode=CN&api=23&channelid=200001&mcc=460&ver=1.1.10&os=android&cl=zh&model=Redmi+Note+4'

headers = {
    'd': 'da41109aafcc53ff',
    'xd': '02%3A11%3A00%3A00%3A00%3A001114RC8227T5H75da4110555fa5999d',
    't': '1503886783202',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0; Redmi Note 4 MIUI/V8.5.5.0.MBFCNED)',
    'Host': 'sv.ksmobile.net',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'Content-Length': '96'
}

values = {
'tuid' : '00115038867817271992305821',
'token' : '',
'netst' : '1',
'mod' : '1',
'isNew' : '1',
'pid' : '7',
'page' : '2',
'posid' : '7001',
'pageSize' : '20'
}
for page in range(0,1):
    values['page']=page


    body = urllib.parse.urlencode(values)
    body = body.encode('utf-8')
    headers['Content-Length'] = len(body)
    # 初始化表单
    req = urllib.request.Request(home_url,body, headers=headers)
    result = opener.open(req)

    html_content = result.read()
    gzipped=result.headers.get('Content-Encoding')
    #gzipped = result.info().getheader('Content-Encoding')
    if gzipped:
        html_content = zlib.decompress(html_content, 16 + zlib.MAX_WBITS)
    resp = json.loads(html_content.decode('utf-8'))

    for i in range(0,20):
        time.sleep(2)
        print(resp['data']['list'][i]['feed']['nickname'])
        print(resp['data']['list'][i]['feed']['sex'])
        print(resp['data']['list'][i]['feed']['face'])
        print(resp['data']['list'][i]['feed']['shareurl'])
        print(resp['data']['list'][i]['feed']['path'])


        n = resp['data']['list'][i]['feed']['path'].rfind('/')+1
        l = len(resp['data']['list'][i]['feed']['path'])+1

        filename=resp['data']['list'][i]['feed']['path'][n:l]
        filenamedisp = filename+'.txt'

        headersmp4 = {
            'User-Agent': ' com.cmcm.shorts/1.1.10 (Linux;Android 6.0) ExoPlayerLib/2.5.1',
            'Accept - Encoding': 'identity',
            'Host': 'g.ksmobile.net',
            'Connection': 'Keep - Alive'
        }

        reqmp4 = urllib.request.Request(resp['data']['list'][i]['feed']['path'], headers=headersmp4)
        resultmp4 = opener.open(reqmp4)
        content = resultmp4.read()
        gzipped=resultmp4.headers.get('Content-Encoding')
        if gzipped:
            content = zlib.decompress(content, 16 + zlib.MAX_WBITS)
        with open(filename,'wb') as f:
            f.write(content);
        with open(filenamedisp,'wb') as fd:
            fd.write(resp['data']['list'][i]['feed']['nickname'].encode('utf-8'))
            nxt=' sex:'+resp['data']['list'][i]['feed']['sex']+' '+resp['data']['list'][i]['feed']['shareurl']
            nxt= nxt.encode('utf-8')
            fd.write(nxt);



