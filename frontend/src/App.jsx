import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [report, setReport] = useState(null);
  const [question, setQuestion] = useState("");
  const [chatAnswer, setChatAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const uploadImage = async () => {
    if (!file) {
      alert("Please select an image first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);

    try {
      const response = await axios.post("http://127.0.0.1:8000/upload", formData);
      setReport(response.data.analysis_report);
    } catch (error) {
      alert("Image upload failed.");
      console.error(error);
    }

    setLoading(false);
  };

  const askQuestion = async () => {
    if (!question || !report) {
      alert("Please upload an image and type a question first.");
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:8000/chat", {
        question: question,
        analysis_report: report,
      });

      setChatAnswer(response.data.answer);
    } catch (error) {
      alert("Chat request failed.");
      console.error(error);
    }
  };

  return (
    <div className="container">
      <h1>DermaSense AI</h1>
      <p className="subtitle">
        Multimodal AI system for skin hyperpigmentation analysis and educational conversation.
      </p>

      <div className="card">
        <h2>1. Upload Skin Image</h2>
        <input type="file" accept="image/*" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={uploadImage}>{loading ? "Analysing..." : "Analyse Image"}</button>
      </div>

      {report && (
        <div className="card">
          <h2>2. AI Generated NLG Report</h2>
          <p><strong>Prediction:</strong> {report.prediction}</p>
          <p><strong>Confidence:</strong> {report.confidence}%</p>
          <div className="answer">
          <h3>Mistral Generated Report</h3>
          <p>{report.nlg_report}</p>
          </div>
          <p className="disclaimer">{report.disclaimer}</p>
        </div>
      )}

      {report && (
        <div className="card">
          <h2>3. Ask Follow-up Question</h2>
          <input
            type="text"
            placeholder="Example: What should I do next?"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />
          <button onClick={askQuestion}>Ask AI</button>

          {chatAnswer && (
            <div className="answer">
              <h3>AI Response</h3>
              <p>{chatAnswer}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;