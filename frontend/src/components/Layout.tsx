import { NavLink, Outlet, useNavigate } from "react-router-dom";

export default function Layout() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <nav
        style={{
          width: 200,
          background: "#1e293b",
          color: "#fff",
          display: "flex",
          flexDirection: "column",
          padding: 16,
          gap: 8,
        }}
      >
        <h1 style={{ fontSize: 18, marginBottom: 16 }}>ERPk</h1>
        {[
          { to: "/customers", label: "Customers" },
          { to: "/products", label: "Products" },
          { to: "/orders", label: "Orders" },
        ].map(({ to, label }) => (
          <NavLink
            key={to}
            to={to}
            style={({ isActive }) => ({
              color: isActive ? "#60a5fa" : "#cbd5e1",
              textDecoration: "none",
              padding: "6px 8px",
              borderRadius: 4,
              background: isActive ? "#334155" : "transparent",
            })}
          >
            {label}
          </NavLink>
        ))}
        <button
          onClick={logout}
          style={{
            marginTop: "auto",
            background: "none",
            border: "1px solid #475569",
            color: "#94a3b8",
            padding: "6px 8px",
            borderRadius: 4,
            cursor: "pointer",
          }}
        >
          Logout
        </button>
      </nav>
      <main style={{ flex: 1, padding: 24, overflowY: "auto" }}>
        <Outlet />
      </main>
    </div>
  );
}
