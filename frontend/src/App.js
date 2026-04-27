import { useState } from "react";
import ReactMarkdown from "react-markdown";
import "./App.css";

export default function App() {
  const [topic, setTopic] = useState("");
  const [steps, setSteps] = useState([]);

  const startResearch = () => {
    if (!topic) return;
    setSteps([]);

    const es = new EventSource(
      `http://localhost:8000/research?topic=${encodeURIComponent(topic)}`
    );

    es.onmessage = (e) => {
      const data = JSON.parse(e.data);
      setSteps((prev) => [...prev, data]);
      if (data.step === "complete") es.close();
    };

    es.onerror = () => es.close();
  };

  const getStep = (name) =>
    steps.find((s) => s.step === name && s.status === "done");

  const format = (d) => {
    if (!d) return "";
    if (typeof d === "string") return d.replace(/\\n/g, "\n");
    if (d.text) return d.text;
    return "";
  };

  const final = getStep("complete")?.data || {};
  const critic = getStep("critic")?.data || "";

  return (
    <div className="app">

      {/* SIDEBAR */}
      <div className="sidebar">
        <h2> Pipeline</h2>
        {["Search", "Reader", "Writer", "Critic", "Complete"].map((s) => (
          <div key={s} className="step">{s}</div>
        ))}
      </div>

      {/* MAIN */}
      <div className="main">
        <h1 className="title"> Multi-Agent Research System</h1>

        <div className="inputBox">
          <input
            placeholder="Enter topic..."
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
          />
          <button onClick={startResearch}>Start</button>
        </div>

        {/* PROGRESS */}
        <div className="card">
          <h2>⚡ Live Progress</h2>

          {steps.map((s, i) => (
            <div key={i} className="progressItem fade">
              <span>{s.step.toUpperCase()}</span>
              <span className={s.status === "done" ? "done" : "running"}>
                {s.status}
              </span>
            </div>
          ))}
        </div>

        {/* FINAL REPORT */}
        {final.report && (
          <div className="card glow">
            <h2>📄 Final Report</h2>
            <ReactMarkdown>{format(final.report)}</ReactMarkdown>
          </div>
        )}
      </div>

      {/* RIGHT PANEL */}
      <div className="rightPanel">
        <h2> Critics Review</h2>

        <div className="card">
          <ReactMarkdown>{format(critic)}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
}