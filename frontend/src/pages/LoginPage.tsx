import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login, register } from "../api/auth";

export default function LoginPage() {
  const navigate = useNavigate();
  const [tab, setTab] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const submit = async () => {
    setError("");
    try {
      const fn = tab === "login" ? login : register;
      const { access_token } = await fn(email, password);
      localStorage.setItem("token", access_token);
      navigate("/customers");
    } catch {
      setError("Invalid credentials or email already taken.");
    }
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        background: "#f1f5f9",
      }}
    >
      <div
        style={{
          background: "#fff",
          padding: 32,
          borderRadius: 8,
          width: 340,
          boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
        }}
      >
        <div style={{ display: "flex", gap: 8, marginBottom: 24 }}>
          {(["login", "register"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              style={{
                flex: 1,
                padding: "8px 0",
                background: tab === t ? "#2563eb" : "#e2e8f0",
                color: tab === t ? "#fff" : "#64748b",
                border: "none",
                borderRadius: 4,
                cursor: "pointer",
                fontWeight: 600,
                textTransform: "capitalize",
              }}
            >
              {t}
            </button>
          ))}
        </div>
        <input
          placeholder="Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={inputStyle}
        />
        <input
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={inputStyle}
        />
        {error && <p style={{ color: "#dc2626", fontSize: 13 }}>{error}</p>}
        <button onClick={submit} style={btnStyle}>
          {tab === "login" ? "Sign in" : "Create account"}
        </button>
      </div>
    </div>
  );
}

const inputStyle: React.CSSProperties = {
  width: "100%",
  padding: "8px 10px",
  marginBottom: 12,
  border: "1px solid #cbd5e1",
  borderRadius: 4,
  fontSize: 14,
  boxSizing: "border-box",
};

const btnStyle: React.CSSProperties = {
  width: "100%",
  padding: "10px 0",
  background: "#2563eb",
  color: "#fff",
  border: "none",
  borderRadius: 4,
  cursor: "pointer",
  fontWeight: 600,
  fontSize: 15,
};
