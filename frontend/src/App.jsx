// import { useState } from "react";
import { useState, useRef } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [report, setReport] = useState(null);
  const fileInputRef = useRef(null);
  const [overlayImage, setOverlayImage] = useState(null);
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
      setOverlayImage(`http://127.0.0.1:8000/${response.data.overlay_image}`);
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

  const resetSession = () => {
      setFile(null);
      setReport(null);
      setOverlayImage(null);
      setQuestion("");
      setChatAnswer("");
      fileInputRef.current.value = "";
    };

  return (
    <div className="container">
      <h1>DermaSense AI</h1>
      <button className="reset-button" onClick={resetSession}>
        Reset Session
      </button>
      <p className="subtitle">
        Multimodal AI system for skin hyperpigmentation analysis and educational conversation.
      </p>

      <div className="card">
        <h2>1. Upload Skin Image</h2>
        <input 
          type="file" 
          accept="image/*"
          ref={fileInputRef} 
          onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={uploadImage}>{loading ? "Analysing..." : "Analyse Image"}</button>
      </div>

      {report && (
        <div className="card">
          <h2>2. AI Generated NLG Report</h2>
          <p><strong>Prediction:</strong> {report.prediction}</p>
          <p><strong>Confidence:</strong> {report.confidence}%</p>
          {overlayImage && (
            <div>
              <h3>Explainability Overlay</h3>
              <img src={overlayImage} alt="Explainability overlay" className="overlay-image" />
            </div>
          )}
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