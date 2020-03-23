from flask import Flask, request, jsonify
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import urllib

ERROR_MESSAGE = '네트워크 접속에 문제가 발생하였습니다. 잠시 후 다시 시도해주세요.'


app = Flask(__name__)


@app.route('/ask_dust', methods=['POST'])

def ask_dust():
    ERROR_MESSAGE="네트워크에 오류가 생겼습니다. 잠시 후에 접속해주세요."
    req = request.get_json()
    location=req["action"]["detailParams"]["sys_location"]["value"]
    enc_location=urllib.parse.quote(location+'미세먼지')
    el=str(enc_location)
    url='https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query='
    url=url+el

    req=Request(url)
    page=urlopen(req)
    html=page.read()
    soup=BeautifulSoup(html,'html.parser')
    table1=soup.find('div', class_='state_info')
    table2=table1.find('em',class_='main_figure').text  

    fine_dust=int(table2)
    if len(location)<=0: answer =ERROR_MESSAGE
    elif(fine_dust<=30): 
         answer='현재 '+location+' 미세먼지 농도는 '+table2+'로 좋음! 입니다'
    elif(fine_dust<=80):
        answer='현재 '+location+' 미세먼지 농도는 '+table2+'로 보통! 입니다'
    elif(fine_dust<=150):
        answer='현재 '+location+' 미세먼지 농도는 '+table2+'로 나쁨! 입니다'
    elif(fine_dust>150):
        answer= '현재 '+location+' 미세먼지 농도는 '+table2+'로 매우나쁨! 입니다'
    res={
        "version": "2.0",
        "template":{
            "outputs":[
                {
                    "simpleText":{
                        "text":answer
                    }                
                }
              ]
           }
        }
    return jsonify(res)



if __name__=='__main__':
    app.run(host='0.0.0.0',port= 5000, threaded=True)
    