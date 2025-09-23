import React, { useState } from 'react';
import Message from './Message';
import './Chat.css'; // importa o CSS

function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const backendUrl = import.meta.env.VITE_BACKEND_URL;

  const sendMessage = async () => {
    if (!input.trim()) return;

    setMessages(prev => [...prev, { sender: 'user', text: input }]);
    const pergunta = input;
    setInput('');

    try {
      const res = await fetch(backendUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pergunta }),
      });

      const data = await res.json();
      const resposta = data.resposta || 'Sem resposta';
      setMessages(prev => [...prev, { sender: 'bot', text: resposta }]);
    } catch (err) {
      console.error(err);
      setMessages(prev => [...prev, { sender: 'bot', text: 'Erro ao se conectar ao backend.' }]);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') sendMessage();
  };

  return (
    <div className="chat-container">
      <h1>VoxAI - Chat Católica</h1>

      <div className="chat-box">
        <div className="messages">
          {messages.map((msg, idx) => <Message key={idx} sender={msg.sender} text={msg.text} />)}
        </div>
        <div className="input-container">
          <input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="Digite sua pergunta..."
          />
          <button onClick={sendMessage}>Enviar</button>
        </div>
      </div>
    </div>
  );
}

export default Chat;
