import React, { useState } from "react";

function App() {
  const [inputText, setInputText] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handlePredict = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: inputText }),
      });

      const data = await response.json();
      if (response.ok) {
        setResult(data);
        setError(null);
      } else {
        setError(data.error);
      }
    } catch (err) {
      setError("Failed to connect to backend");
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Cyber Threat Prediction</h1>
      <textarea
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        placeholder="Enter text here..."
        rows="4"
        cols="50"
      />
      <br />
      <button onClick={handlePredict}>Predict</button>

      {result && (
        <div>
          <h3>Prediction Result:</h3>
          <p><strong>Threat Type:</strong> {result.threat_type}</p>
          <p><strong>Probability:</strong> {result.probability.toFixed(2)}</p>
        </div>
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default App;
