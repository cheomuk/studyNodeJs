import threading
import json

from deep.config.DatabaseConfig import *
from deep.Database import Database
from BotServer import BotServer
from deep.Preprocess import Preprocess
from deep.models.intent.IntentModel import IntentModel
from deep.models.ner.NerModel import NerModel
from deep.FindAnswer import FindAnswer

# 전처리 객체 생성
p = Preprocess(word2index_dic='../train_tools/dict/chatbot_dict.bin',
               userdic='../user_dic.tsv')

# 의도 파악 모델
intent = IntentModel(model_name='../models/intent/intent_model.h5', prep=p)

# 개체명 인식 모델
ner = NerModel(model_name='../models/ner/ner_model.h5', prep=p)


def to_client(conn, addr, params):
    db = params['db']
    try:
        db.connect()  # DB 연결

        # 데이터 수신
        read = conn.recv(1024)  # 수신 데이터가 있을 때까지 블로킹
        print("===========================")
        print("Connection from: %s" % str(addr))

        if read is None or not read:
            # 클라이언트 연결이 끊어지거나 오류가 있는 경우
            print("클라이언트 연결 끊어짐")
            exit(0)  # 스레드 강제 종료

        # json 데이터로 변환
        recv_json_data = json.loads(read.decode())
        print("데이터 수신 : ", recv_json_data)
        query = recv_json_data['Query']

        # 의도 파악
        intent_predict = intent.predict_class(query)
        intent_name = intent.labels[intent_predict]

        # 개체명 파악
        ner_predicts = ner.predict(query)
        ner_tags = ner.predict_tags(query)

        # 답변 검색
        try:
            f = FindAnswer(db)
            answer_text, answer_image = f.search(intent_name, ner_tags)
            answer = f.tag_to_word(ner_predicts, answer_text)

        except Exception as e:
            answer = "죄송해요 무슨 말인지 모르겠어요. 조금 더 공부할게요."
            answer_image = None

        send_json_data_str = {
            "Query": query,
            "Answer": answer,
            "AnswerImageUrl": answer_image,
            "Intent": intent_name,
            "NER": str(ner_predicts)
        }
        message = json.dumps(send_json_data_str)  # json 객체를 전송 가능한 문자열로 변환
        conn.send(message.encode())  # 응답 전송

    except Exception as ex:
        print(ex)

    finally:
        if db is not None:  # db 연결 끊기
            db.close()
        conn.close()


if __name__ == '__main__':
    # 질문/답변 학습 db 연결 객체 생성
    db = Database(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db_name=DB_NAME
    )
    print("DB 접속")

    # 봇 서버 동작
    port = 5000
    listen = 100
    bot = BotServer(port, listen)
    bot.create_sock()
    print("bot start")

    while True:
        conn, addr = bot.ready_for_client()
        params = {
            "db": db
        }

        client = threading.Thread(target=to_client, args=(
            conn,  # 클라이언트 연결 소켓
            addr,  # 클라이언트 연결 주소 정보
            params  # 스레드 함수 파라미터
        ))
        client.start()  # 스레드 시작