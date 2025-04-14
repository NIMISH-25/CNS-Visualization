import React, { useState } from 'react';
import './App.css';

function App() {
  const [language, setLanguage] = useState('python');
  const [code, setCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [iframeUrl, setIframeUrl] = useState('');
  const [iframeLoaded, setIframeLoaded] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setIframeUrl('');
    setIframeLoaded(false);
    try {
      const response = await fetch('http://localhost:5000/api/visualize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ language, code }),
      });
      const data = await response.json();
      if (response.ok) {
        setIframeUrl(data.file_url);
      } else {
        setError(data.error);
      }
    } catch (err) {
      setError("Error connecting to server: " + err.message);
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <header className="header">
        <h1>Visualization Generator</h1>
        <p>Create stunning visualizations using Python or R</p>
      </header>
      <main className="main">
        <form onSubmit={handleSubmit} className="form">
          <div className="field">
            <label htmlFor="language">Language</label>
            <select id="language" value={language} onChange={(e) => setLanguage(e.target.value)}>
              <option value="python">Python</option>
              <option value="r">R</option>
            </select>
          </div>
          <div className="field">
            <label htmlFor="code">Your Code</label>
            <textarea
              id="code"
              rows="10"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="Enter your script here..."
            />
          </div>
          <button type="submit" className="btn" disabled={loading}>
            {loading ? <div className="loader"></div> : "Generate Visualization"}
          </button>
        </form>
        {error && <div className="error">{error}</div>}
        {iframeUrl && (
          <div className="iframeContainer">
            <h2>Your Visualization</h2>
            {!iframeLoaded && (
              <div className="iframeLoader">
                <div className="loader"></div>
              </div>
            )}
            <iframe 
              src={iframeUrl} 
              title="Visualization" 
              onLoad={() => setIframeLoaded(true)}
              style={{ display: iframeLoaded ? 'block' : 'none' }}
            />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
