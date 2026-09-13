function ChatBox() {
  return (
    <div className="chat-box">
      <h3>💬 AI Tutor</h3>

      <p>
        Ask EduMentor a question about your uploaded study material.
      </p>

      <input
        type="text"
        placeholder="Ask a question..."
      />

      <button>Ask EduMentor</button>
    </div>
  );
}

export default ChatBox;