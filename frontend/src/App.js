import React, { useState } from "react";
import "./style.css";

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { sender: "user", text: input };
    setMessages((m) => [...m, userMsg]);

    try {
      const response = await fetch("http://127.0.0.1:5000/autocorrect", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: input }),
      });

      if (!response.ok) throw new Error("Server error");

      const data = await response.json();
      const botMsg = { sender: "bot", text: data.corrected };

      setMessages((m) => [...m, botMsg]);
    } catch (err) {
      setMessages((m) => [
        ...m,
        { sender: "bot", text: "❌ Backend not reachable." },
      ]);
    }

    setInput("");
  };

  return (
    <div className="main-container">
      <div className="chat-header">AI Autocorrector</div>

      <div className="chat-box">
        {messages.map((m, i) => (
          <div key={i} className={`msg ${m.sender}`}>
            {m.text}
          </div>
        ))}
      </div>

      <div className="input-section">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type text to autocorrect…"
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default App;
