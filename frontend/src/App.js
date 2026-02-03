import { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleProcess = async () => {
    if (!file) return alert("Please upload an audio file");

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setData(null);

    const res = await fetch("http://127.0.0.1:8000/process", {
      method: "POST",
      body: formData
    });

    const result = await res.json();
    setData(result);
    setLoading(false);
  };

  return (
    <div className="app">
      {/* HEADER */}
      <header className="header">
        <h1>InsightMeet</h1>
        <p>AI-powered Meeting Intelligence</p>
      </header>

      {/* UPLOAD CARD */}
      <div className="card">
        <h3>Upload Meeting Audio</h3>
        <input
          type="file"
          accept=".mp3,.wav"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button onClick={handleProcess} disabled={loading}>
          {loading ? "Processing..." : "🚀 Process Meeting"}
        </button>
      </div>

      {/* LOADING */}
      {loading && (
        <div className="status">
          ⏳ Processing meeting… this may take a minute
        </div>
      )}

      {/* RESULTS */}
      {data && (
        <>
          <div className="card">
            <h3>📝 Meeting Summary</h3>
            <p>{data.summary}</p>
          </div>

          <div className="card">
            <h3>⭐ Key Insights</h3>
            <ul>
              {data.impact_points.map((item, idx) => (
                <li key={idx}>
                  <b>{item.score}</b> – {item.sentence}
                </li>
              ))}
            </ul>
          </div>

          <div className="card">
            <h3>📄 Full Transcript</h3>
            <textarea
              rows="10"
              value={data.transcript}
              readOnly
            />
          </div>

          <div className="card actions">
            <a
              href="http://127.0.0.1:8000/download-mom"
              target="_blank"
              rel="noreferrer"
            >
              ⬇️ Download MOM PDF
            </a>
          </div>
        </>
      )}
    </div>
  );
}

export default App;
