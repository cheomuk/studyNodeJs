import { useEffect, useState } from "react";
import { useSocket } from "socket.io-react-hook";

const getDatetime = (date) => {
  date = new Date(date);

  const time = {
    hours: date.getHours(),
    minutes: date.getMinutes(),
  };
  return `${time.hours}:${time.minutes}`;
};

/**
 * 서버 통신을 처리하는 hook입니다.
 *
 * chats - 기존 users에서 id만 추가되었습니다. { id, sender, message, date }
 *
 * error - 서버 통신 에러 메세지입니다.
 *
 * send(sender, message) - 닉네임, 메세지 전달 해주시면 됩니다. 메세지가 서버에 전송됩니다.
 * onsubmit에엣 추가
 *
 * <<<<<<< eyoung
 * onsubmit에 추가
 * =======
 * >>>>>>> main
 * 
 * remove - id 전달 해주시면 됩니다. 메세지가 서버에서 삭제됩니다.
 */
export const useChats = () => {
  const [chats, setChats] = useState([]);

  // const { socket, error } = useSocket('https://chat.pdom.me', { transports: ['websocket'] });
  const { socket, error } = useSocket('/', { transports: ['websocket'] });

  useEffect(() => {
    socket.on('send', (id, type, sender, data, time) => {
      setChats((value) => value.concat({id, isImage: type === 'image', sender, message: data, date: getDatetime(time)}));
    })

    socket.on("remove", (id) => {
      setChats((value) => value.filter((chat) => chat.id !== id));
    });
  }, [socket]);

  const send = (sender, message) => {
    socket.emit('send', 'text', sender, message);
  };

  const remove = (id) => {
    socket.emit("remove", id);
  };

  const sendImage = (sender, data) => {
    socket.emit('send', 'image', sender, data);
  };

  return { chats, error, send, remove, sendImage };
};
