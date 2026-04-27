import React, { useEffect, useMemo, useState } from "react";
import { Bar, BarChart, Cell, Pie, PieChart, Tooltip, XAxis, YAxis } from "recharts";
import { fetchHistory, fetchMetrics, predictThreat } from "../api";

const COLORS = ["#e74c3c", "#f39c12", "#9b59b6", "#3498db", "#2ecc71", "#1abc9c"];

function Dashboard({ user, onLogout }) {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [metrics, setMetrics] = useState(null);

  const loadHistory = async () => {
    const { data } = await fetchHistory();
    setHistory(data);
  };

  useEffect(() => {
    fetchMetrics().then((res) => setMetrics(res.data)).catch(() => setMetrics(null));
    loadHistory();
  }, []);

  const onPredict = async () => {
    if (!text.trim()) return;
    const { data } = await predictThreat({ text, username: user });
    setResult(data);
    setText("");
    loadHistory();
  };

  const threatDistribution = useMemo(() => {
    const counts = {};
    history.forEach((item) => {
      counts[item.prediction] = (counts[item.prediction] || 0) + 1;
    });
    return Object.keys(counts).map((key) => ({ name: key, value: counts[key] }));
  }, [history]);

  const accuracyData = useMemo(() => {
    if (!metrics?.all_metrics) return [];
    return Object.entries(metrics.all_metrics).map(([name, value]) => ({
      model: name,
      accuracy: Number((value.accuracy * 100).toFixed(2)),
    }));
  }, [metrics]);

  return (
    <div className="dashboard">
      <div className="toolbar">
        <p>Logged in as: {user}</p>
        <button onClick={onLogout}>Logout</button>
      </div>

      <div className="card">
        <h2>Threat Detection Module</h2>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste email, log, or report text..."
          rows={5}
        />
        <button onClick={onPredict}>Analyze Threat</button>
        {result && (
          <div className={`result ${result.is_malicious ? "bad" : "safe"}`}>
            <p>Prediction: {result.prediction}</p>
            <p>Confidence: {(result.confidence * 100).toFixed(2)}%</p>
          </div>
        )}
      </div>

      <div className="chart-grid">
        <div className="card">
          <h3>Threat Distribution</h3>
          <PieChart width={300} height={250}>
            <Pie data={threatDistribution} dataKey="value" nameKey="name" outerRadius={90} label>
              {threatDistribution.map((entry, index) => (
                <Cell key={entry.name} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </div>
        <div className="card">
          <h3>Model Accuracy Comparison</h3>
          <BarChart width={350} height={250} data={accuracyData}>
            <XAxis dataKey="model" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="accuracy" fill="#3498db" />
          </BarChart>
        </div>
      </div>

      <div className="card">
        <h3>Evaluation Metrics</h3>
        {!metrics ? (
          <p>No metrics available. Train model first.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Model</th>
                <th>Accuracy</th>
                <th>Precision</th>
                <th>Recall</th>
                <th>F1-score</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(metrics.all_metrics).map(([name, value]) => (
                <tr key={name}>
                  <td>{name}</td>
                  <td>{(value.accuracy * 100).toFixed(2)}%</td>
                  <td>{(value.precision * 100).toFixed(2)}%</td>
                  <td>{(value.recall * 100).toFixed(2)}%</td>
                  <td>{(value.f1_score * 100).toFixed(2)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <div className="card">
        <h3>Prediction History</h3>
        <table>
          <thead>
            <tr>
              <th>Time</th>
              <th>Input</th>
              <th>Prediction</th>
              <th>Confidence</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {history.map((item) => {
              const malicious = item.prediction !== "normal";
              return (
                <tr key={item.id}>
                  <td>{item.created_at}</td>
                  <td>{item.input_text.slice(0, 80)}...</td>
                  <td>{item.prediction}</td>
                  <td>{(item.confidence * 100).toFixed(2)}%</td>
                  <td>
                    <span className={malicious ? "chip bad" : "chip safe"}>
                      {malicious ? "Malicious" : "Safe"}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Dashboard;
