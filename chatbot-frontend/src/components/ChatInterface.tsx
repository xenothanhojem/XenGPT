import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './ChatInterface.css';

interface Message {
  text: string;
  isUser: boolean;
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }

  useEffect(scrollToBottom, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    const userMessage: Message = { text: inputMessage, isUser: true };
    setMessages(prevMessages => [...prevMessages, userMessage]);
    setInputMessage('');

    try {
      const result = await axios.post('http://localhost:8000/chat', { user_message: inputMessage });
      const botMessage: Message = { text: result.data.response, isUser: false };
      setMessages(prevMessages => [...prevMessages, botMessage]);
    } catch (error) {
      console.error('Error:', error);
      const errorMessage: Message = { text: 'An error occurred while processing your request.', isUser: false };
      setMessages(prevMessages => [...prevMessages, errorMessage]);
    }
  };

  const reloadVectorStore = async () => {
    try {
      const response = await axios.post('http://localhost:8000/reload_vector_store');
      alert(response.data.message);
    } catch (error) {
      console.error('Error reloading vector store:', error);
      if (axios.isAxiosError(error) && error.response) {
        alert(`Error: ${error.response.data.detail}`);
      } else {
        alert('An error occurred while reloading the vector store.');
      }
    }
  };

  return (
    <div className="chat-container">
      {/* <button onClick={reloadVectorStore} className="reload-button">Reload Vector Store</button> */}
      <div className="chat-messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.isUser ? 'user-message' : 'bot-message'}`}>
            {message.text}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <form onSubmit={handleSubmit} className="chat-input-form">
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="Type your message here"
          className="chat-input"
        />
        <button type="submit" className="chat-submit">Send</button>
      </form>
    </div>
  );
};

export default ChatInterface;
