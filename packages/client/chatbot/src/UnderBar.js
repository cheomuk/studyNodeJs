import React, { useState } from "react";
import { AiOutlineArrowUp } from "react-icons/ai";
import "./UnderBar.css";
import StopChat from "./StopChat";

function UnderBar() {
  const [doChat, setDoChat] = useState("");
  const [doChats, setDoChats] = useState([
    <div class="mb-3">
      <label for="formFile" class="form-label"></label>
      <input class="form-control" type="file" id="formFile" />
    </div>,
    <button>메시지 보내기</button>,
    <StopChat />
  ]);

  const onChange = (event) => setDoChat(event.target.value);

  const onSubmit = (event) => {
    event.preventDefault();
    if (doChat === "") {
      return;
    }

    setDoChats((currentArray) => [...currentArray, doChat]);
    setDoChat("");
  };
  return (
    <>
    <form className="textForm">
      {/* 제이쿼리..? */}
      {doChats.map((item, index) => (
        <div className="chatBox" key={index}>
          {item}
        </div>
      ))}
    </form>

      {/* 언더바 레이아웃 및 이벤트 등록 */}
      <div className="underBar">
        <form onSubmit={onSubmit}>
          <input
            className="chat"
            type="text"
            value={doChat}
            placeholder="채팅을 입력하세요"
            onChange={onChange}
          />
        </form>
        <AiOutlineArrowUp className="btnEnter" onClick={onSubmit} />
      </div>
    </>
  );
}

export default UnderBar;