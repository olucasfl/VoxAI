// src/components/Message.jsx
import React from 'react';
import ReactMarkdown from 'react-markdown';

function Message({ sender, text }) {
  const isUser = sender === 'user';
  return (
    <div style={{ display: 'flex', justifyContent: isUser ? 'flex-end' : 'flex-start', marginBottom: '6px' }}>
      <div
        style={{
          background: isUser ? '#4caf50' : '#e0e0e0',
          color: isUser ? 'white' : 'black',
          padding: '8px 12px',
          borderRadius: '12px',
          maxWidth: '70%',
          wordBreak: 'break-word'
        }}
      >
        {isUser ? (
          text
        ) : (
          <ReactMarkdown>{text}</ReactMarkdown>
        )}
      </div>
    </div>
  );
}

export default Message;
