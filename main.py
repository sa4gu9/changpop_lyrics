from flask import Flask,render_template, make_response,request,redirect,url_for,jsonify
import random
import secret.option as option
import os
from gevent.pywsgi import WSGIServer
import datetime

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, 'templates')
app = Flask(__name__, template_folder=template_path)


host = ""

if option.testMode:
    host="127.0.0.1"
else:
    host="0.0.0.0"



@app.route('/lyrics', methods=['GET','POST'])
def youthyouthsheet():
    group=request.args.get("group")
    songName=request.args.get("songName")
    returnstr=""
    htmltext=""
    if group==None:
        return "잘못된 접근입니다."
    else:
        groups=[]
        with open(f"{os.path.dirname(os.path.abspath(__file__))}/group.txt","r",encoding="UTF-8") as f:
            groups=f.readlines()
            groups=[g.replace("\n","") for g in groups]
        print(group)
        if group in groups:
            if songName==None:
                #폴더내 모든파일 가져오기
                print(group)
                print(f"{os.path.dirname(os.path.abspath(__file__))}/lyrics/{group}")
                try:
                    file_list=os.listdir(f"{os.path.dirname(os.path.abspath(__file__))}/lyrics/{group}")

                    if group=="따따잇컵" or group=="건드림컵":
                        returnstr=""
                        for file_name in file_list:
                            with open(f"{os.path.dirname(os.path.abspath(__file__))}/lyrics/{group}/{file_name}","r",encoding="UTF-8") as f:
                                returnstr+=f.read()
                                returnstr+="<br>"
                        return returnstr
                except:
                    return "현재 가사 목록이 있는 월드컵이 아니거나, 존재하지 않는 창드컵입니다."

                print(file_list)
                htmltext="<table>"
                for f in file_list:
                    htmltext+=f"<tr><td><a href='lyrics?group={group}&songName={f}'>{f}</a></td></tr>"
                htmltext+="</table>"
                return htmltext
            else:
                if os.path.exists(f"{os.path.dirname(os.path.abspath(__file__))}/lyrics/{group}/{songName}"):

                    with open(f"{os.path.dirname(os.path.abspath(__file__))}/lyrics/{group}/{songName}","r",encoding="UTF-8") as f:
                        returnstr=f.read()
                        returnstr=returnstr.replace("\n","<br>")
                        return returnstr
                else:
                    return f"{group}에 수록되지 않은 노래입니다."
        else:
            return "존재하지 않는 창드컵입니다."




    return returnstr

    # else:
        


def getFileContent(htmlFileName,cpoplink=None):
    hfn = open(f"{os.path.dirname(os.path.abspath(__file__))}/templates/{htmlFileName}.html","r",encoding="UTF-8")
    content = hfn.readlines()
    hfn.close()

    if cpoplink=="lostmedia":
        content[8]="youtube-video-link<br>"
        del content[2:8]
    
    returnstr=""

    for line in content:
        returnstr+=line

    return returnstr

@app.route('/', methods=['GET','POST'])
def home():
    groups=[]
    htmltext=""

    with open(f"{os.path.dirname(os.path.abspath(__file__))}/templates/ads.html","r",encoding="UTF-8") as f:
        htmltext+=f.read()


    #파일 읽기 with로
    with open(f"{os.path.dirname(os.path.abspath(__file__))}/group.txt","r",encoding="UTF-8") as f:
        groups=f.readlines()

    htmltext+='<body><table>'

    for g in groups:
        g=g.replace("\n","")
    
        htmltext+=f"<tr><td><a href='lyrics?group={g}'>{g}</a></td></tr>"
    

    htmltext+="</table><br><br><br>가사 추가 문의 partyhost@changpop.party</body>"
    print(htmltext)
    
    return htmltext


@app.route('/ads.txt', methods=['GET','POST'])
def adstxt():
    with open(f"{os.path.dirname(os.path.abspath(__file__))}/ads.txt","r",encoding="UTF-8") as f:
        return f.read()

if __name__ == '__main__':
    # app.run(debug=True, host=host, port=option.port)
    if option.testMode:
        app.run(debug=True, host=host, port=option.port)
    else:
        # Debug/Development
        # app.run(debug=True, host="0.0.0.0", port="5000")
        # Production
        


        http_server = WSGIServer(('', option.port), app)
        http_server.serve_forever()