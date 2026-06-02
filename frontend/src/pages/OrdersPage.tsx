import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Badge from "../components/Badge";
import Modal from "../components/Modal";
import { useCreateOrder, useDeleteOrder, useOrders } from "../hooks/useOrders";
import { useCustomers } from "../hooks/useCustomers";
import { Order } from "../types";

export default function OrdersPage() {
  const navigate = useNavigate();
  const { data: orders = [], isLoading } = useOrders();
  const { data: customers = [] } = useCustomers();
  const createMutation = useCreateOrder();
  const deleteMutation = useDeleteOrder();

  const [showCreate, setShowCreate] = useState(false);
  const [customerId, setCustomerId] = useState("");
  const [error, setError] = useState("");

  const submitCreate = async () => {
    setError("");
    try {
      const order = await createMutation.mutateAsync(customerId);
      setShowCreate(false);
      setCustomerId("");
      navigate(`/orders/${order.id}`);
    } catch (e: any) {
      setError(e?.response?.data?.detail ?? "Failed to create order");
    }
  };

  if (isLoading) return <p>Loading…</p>;

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
        <h2>Orders</h2>
        <button onClick={() => setShowCreate(true)} style={primaryBtn}>+ New Order</button>
      </div>

      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ background: "#f1f5f9" }}>
            {["Customer", "Status", "Total", "Items", "Created", "Actions"].map((h) => (
              <th key={h} style={th}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {orders.map((o: Order) => (
            <tr
              key={o.id}
              style={{ borderBottom: "1px solid #e2e8f0", cursor: "pointer" }}
              onClick={() => navigate(`/orders/${o.id}`)}
            >
              <td style={td}>{o.customer.name}</td>
              <td style={td}><Badge variant={o.status} /></td>
              <td style={td}>${Number(o.total_amount).toFixed(2)}</td>
              <td style={td}>{o.items.length}</td>
              <td style={td}>{new Date(o.created_at).toLocaleDateString()}</td>
              <td style={td} onClick={(e) => e.stopPropagation()}>
                <button onClick={() => deleteMutation.mutate(o.id)} style={{ ...actionBtn, color: "#dc2626" }}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {showCreate && (
        <Modal title="New Order" onClose={() => { setShowCreate(false); setCustomerId(""); setError(""); }}>
          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            <select value={customerId} onChange={(e) => setCustomerId(e.target.value)} style={input}>
              <option value="">Select customer…</option>
              {customers.map((c) => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
            {error && <p style={{ margin: 0, color: "#dc2626", fontSize: 13 }}>{error}</p>}
            <button onClick={submitCreate} style={primaryBtn} disabled={!customerId}>
              Create Order
            </button>
          </div>
        </Modal>
      )}
    </div>
  );
}

const primaryBtn: React.CSSProperties = { background: "#2563eb", color: "#fff", border: "none", borderRadius: 4, padding: "8px 16px", cursor: "pointer", fontWeight: 600 };
const actionBtn: React.CSSProperties = { background: "none", border: "none", cursor: "pointer" };
const th: React.CSSProperties = { padding: "10px 12px", textAlign: "left", fontSize: 13, fontWeight: 600 };
const td: React.CSSProperties = { padding: "10px 12px", fontSize: 14 };
const input: React.CSSProperties = { padding: "8px 10px", border: "1px solid #cbd5e1", borderRadius: 4, fontSize: 14 };
