import React, { useState } from 'react';
import Message from './Message';

function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const backendUrl = 'http://127.0.0.1:8000/perguntar';

  const sendMessage = async () => {
    if (!input.trim()) return;

    // Adiciona a mensagem do usuário
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
    <div style={{
        display: 'flex',
        flexDirection: 'column',  // permite colocar o título acima do chat
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',       // ocupa toda a tela
        backgroundColor: '#f5f0e1', // tom de papel antigo
        padding: '20px',
        boxSizing: 'border-box',
    }}>
        <h1 style={{
        fontFamily: 'Georgia, serif',
        color: '#4b3b1d',         // tom marrom clássico
        marginBottom: '20px',
        textAlign: 'center',
        }}>
        VoxAI - Chat Católica
        </h1>

        <div style={{ 
        width: '500px', 
        border: '2px solid #c9b17a', // borda dourada clara
        borderRadius: '12px', 
        padding: '15px', 
        backgroundColor: '#fffaf0',   // tom de pergaminho
        boxShadow: '0 4px 15px rgba(0,0,0,0.1)'
        }}>
        <div style={{ maxHeight: '400px', overflowY: 'auto', marginBottom: '10px' }}>
            {messages.map((msg, idx) => <Message key={idx} sender={msg.sender} text={msg.text} />)}
        </div>
        <div style={{ display: 'flex' }}>
            <input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
            style={{ flex: 1, padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
            placeholder="Digite sua pergunta..."
            />
            <button
            onClick={sendMessage}
            style={{ marginLeft: '8px', padding: '8px 12px', borderRadius: '4px', cursor: 'pointer', backgroundColor: '#c9b17a', border: 'none' }}
            >
            Enviar
            </button>
        </div>
        </div>
    </div>
    );
}

export default Chat;
