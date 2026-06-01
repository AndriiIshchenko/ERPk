import { useParams, useNavigate } from "react-router-dom";
import Badge from "../components/Badge";
import { useOrder } from "../hooks/useOrders";

export default function OrderDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: order, isLoading } = useOrder(id ?? "");

  if (isLoading) return <p>Loading…</p>;
  if (!order) return <p>Order not found.</p>;

  return (
    <div>
      <button
        onClick={() => navigate("/orders")}
        style={{ background: "none", border: "none", cursor: "pointer", color: "#2563eb", marginBottom: 16 }}
      >
        ← Back to Orders
      </button>

      <div style={{ display: "flex", gap: 16, alignItems: "center", marginBottom: 24 }}>
        <h2 style={{ margin: 0 }}>Order Detail</h2>
        <Badge label={order.status} variant={order.status} />
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 24 }}>
        <div style={card}>
          <p style={label}>Customer</p>
          <p style={value}>{order.customer.name}</p>
          <p style={{ ...label, marginTop: 4 }}>{order.customer.email}</p>
        </div>
        <div style={card}>
          <p style={label}>Total Amount</p>
          <p style={{ ...value, fontSize: 28 }}>${Number(order.total_amount).toFixed(2)}</p>
          <p style={{ ...label, marginTop: 4 }}>{new Date(order.created_at).toLocaleString()}</p>
        </div>
      </div>

      <h3>Items ({order.items.length})</h3>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ background: "#f1f5f9" }}>
            {["Product ID", "Price at Order"].map((h) => (
              <th key={h} style={{ padding: "10px 12px", textAlign: "left", fontSize: 13, fontWeight: 600 }}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {order.items.map((item) => (
            <tr key={item.id} style={{ borderBottom: "1px solid #e2e8f0" }}>
              <td style={{ padding: "10px 12px", fontSize: 14 }}>{item.product_id}</td>
              <td style={{ padding: "10px 12px", fontSize: 14 }}>${Number(item.price_snapshot).toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const card: React.CSSProperties = { background: "#f8fafc", border: "1px solid #e2e8f0", borderRadius: 8, padding: 16 };
const label: React.CSSProperties = { margin: 0, fontSize: 12, color: "#94a3b8", fontWeight: 600, textTransform: "uppercase" };
const value: React.CSSProperties = { margin: "4px 0 0", fontSize: 18, fontWeight: 700 };
