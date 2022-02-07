import socket
import json

# 챗봇 엔진 서버 접속 정보
host = "14.56.115.119"  # 챗봇 엔진 서버 IP 주소
port = 3306  # 챗봇 엔진 서버 통신 포트

# 클라이언트 프로그램 시작
while True:
    print("질문 : ")
    query = input()  # 질문 입력
    if query == "exit":
        exit(0)
    print("=" * 40)

    # 챗봇 엔진 서버 연결
    mySocket = socket.socket()
    mySocket.connect((host, port))

    # 챗봇 엔진 질의 요청
    json_data = {
        'Query': query,
        'BotType': "MyService"
    }
    message = json.dumps(json_data, ensure_ascii=False)
    cmd = message.encode()
    mySocket.send(message.encode())
    # 챗봇 엔진 답변 출력
    data = mySocket.recv(1024)
    ret_data = json.loads(data.decode())  # json 형태 문자열을 json 객체로 변환
    print("답변 : ")
    print(ret_data['Answer'])
    print("\n")

    # 챗봇 엔진 서버 연결 소켓 닫기
    mySocket.close()