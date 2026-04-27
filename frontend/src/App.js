import React, { useState } from "react";
import Dashboard from "./components/Dashboard";
import Login from "./components/Login";

function App() {
  const [user, setUser] = useState(null);

  return (
    <div className="app-shell">
      <h1>AI-Based Cybersecurity Threat Intelligence System</h1>
      {!user ? <Login onLogin={setUser} /> : <Dashboard user={user} onLogout={() => setUser(null)} />}
    </div>
  );
}

export default App;
