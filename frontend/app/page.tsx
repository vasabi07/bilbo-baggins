"use client"
import React, { useState } from 'react';
import axios from 'axios';

interface Message {
  sender: 'user' | 'bot';
  text: string;
}

const ChatPage: React.FC = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!input.trim()) return;

    setMessages([...messages, { sender: 'user', text: input }]);

    try {
      const response = await axios.post('http://127.0.0.1:8000/chat', { message: input });

      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: 'bot', text: response.data.reply },
      ]);
    } catch (error) {
      console.error('Error fetching response:', error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: 'bot', text: 'Error: Unable to fetch response.' },
      ]);
    }

    setInput('');
  };

  return (
    <div className="max-w-lg mx-auto p-4">
      <div className="border border-gray-300 p-4 h-96 overflow-y-scroll bg-white rounded-lg shadow-md">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`mb-2 p-2 rounded-lg text-black ${
              message.sender === 'user' ? 'bg-blue-100 text-right' : 'bg-gray-100 text-left'
            }`}
          >
            <strong>{message.sender === 'user' ? 'You' : 'Bot'}:</strong> {message.text}
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit} className="mt-4 flex">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-grow p-2 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          className="bg-blue-500 text-white p-2 rounded-r-lg hover:bg-blue-600"
        >
          Send
        </button>
      </form>
    </div>
  );
};


export default ChatPage;