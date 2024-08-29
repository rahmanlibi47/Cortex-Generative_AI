import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isBotTyping, setIsBotTyping] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    setMessages([...messages, { text: input, type: "user" }]);
    setInput("");

    setIsBotTyping(true);

    try {
      const response = await axios.post(
        "http://localhost:5000/api/get-response",
        { user_input: input }
      );
      const botResponse = response.data.response;

      setMessages([
        ...messages,
        { text: input, type: "user" },
        { text: botResponse, type: "bot" },
      ]);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setIsBotTyping(false);
    }
  };

  return (
    <div className="App">
      <div className="chat-window">
        <div className="messages">
          {messages.map((msg, index) => (
            <div key={index} className={msg.type}>
              {msg.text}
            </div>
          ))}
          {isBotTyping && (
            <div className="bot-typing">Chatbot is typing...</div>
          )}
        </div>
        <form onSubmit={handleSubmit} className="message-form">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message..."
          />
          <button type="submit">Send</button>
        </form>
      </div>
    </div>
  );
}

export default App;
