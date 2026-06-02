import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Badge from "../components/Badge";
import {
  useOrder,
  useAddOrderItem,
  useRemoveOrderItem,
  useConfirmOrder,
  useMarkOrderPaid,
  useCancelOrder,
} from "../hooks/useOrders";
import { useProducts } from "../hooks/useProducts";

export default function OrderDetailPage() {
  const { id = "" } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const { data: order, isLoading } = useOrder(id);
  const { data: products = [] } = useProducts(false); // active only

  const addItem = useAddOrderItem(id);
  const removeItem = useRemoveOrderItem(id);
  const confirmOrder = useConfirmOrder(id);
  const markPaid = useMarkOrderPaid(id);
  const cancelOrder = useCancelOrder(id);

  const [selectedProductId, setSelectedProductId] = useState("");
  const [actionError, setActionError] = useState("");

  if (isLoading) return <p>Loading…</p>;
  if (!order) return <p>Order not found.</p>;

  const isDraft = order.status === "draft";
  const isPendingPayment = order.status === "pending";
  const addedProductIds = new Set(order.items.map((i) => i.product_id));
  const availableProducts = products.filter((p) => !addedProductIds.has(p.id));

  const handleAddItem = async () => {
    if (!selectedProductId) return;
    setActionError("");
    try {
      await addItem.mutateAsync(selectedProductId);
      setSelectedProductId("");
    } catch (e: any) {
      setActionError(e?.response?.data?.detail ?? "Failed to add item");
    }
  };

  const handleRemoveItem = async (itemId: string) => {
    setActionError("");
    try {
      await removeItem.mutateAsync(itemId);
    } catch (e: any) {
      setActionError(e?.response?.data?.detail ?? "Failed to remove item");
    }
  };

  const handleConfirm = async () => {
    setActionError("");
    try {
      await confirmOrder.mutateAsync();
    } catch (e: any) {
      setActionError(e?.response?.data?.detail ?? "Failed to confirm order");
    }
  };

  const handleMarkPaid = async () => {
    setActionError("");
    try {
      await markPaid.mutateAsync();
    } catch (e: any) {
      setActionError(e?.response?.data?.detail ?? "Failed to mark order as paid");
    }
  };

  const handleCancel = async () => {
    setActionError("");
    try {
      await cancelOrder.mutateAsync();
    } catch (e: any) {
      setActionError(e?.response?.data?.detail ?? "Failed to cancel order");
    }
  };

  return (
    <div>
      <button onClick={() => navigate("/orders")} style={backBtn}>← Back to Orders</button>

      <div style={{ display: "flex", gap: 12, alignItems: "center", marginBottom: 24 }}>
        <h2 style={{ margin: 0 }}>Order</h2>
        <Badge variant={order.status} />
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 24 }}>
        <div style={card}>
          <p style={labelStyle}>Customer</p>
          <p style={valueStyle}>{order.customer.name}</p>
          <p style={{ ...labelStyle, marginTop: 4 }}>{order.customer.email}</p>
        </div>
        <div style={card}>
          <p style={labelStyle}>Total</p>
          <p style={{ ...valueStyle, fontSize: 28 }}>${Number(order.total_amount).toFixed(2)}</p>
          <p style={{ ...labelStyle, marginTop: 4 }}>{new Date(order.created_at).toLocaleString()}</p>
        </div>
      </div>

      {/* Items table */}
      <h3 style={{ marginBottom: 8 }}>Items ({order.items.length})</h3>
      {order.items.length === 0 ? (
        <p style={{ color: "#94a3b8", fontSize: 14 }}>No items yet. Add a product below.</p>
      ) : (
        <table style={{ width: "100%", borderCollapse: "collapse", marginBottom: 16 }}>
          <thead>
            <tr style={{ background: "#f1f5f9" }}>
              {["Product", "Price at Order", ...(isDraft ? [""] : [])].map((h, i) => (
                <th key={i} style={th}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {order.items.map((item) => (
              <tr key={item.id} style={{ borderBottom: "1px solid #e2e8f0" }}>
                <td style={td}>{item.product_name}</td>
                <td style={td}>${Number(item.price_snapshot).toFixed(2)}</td>
                {isDraft && (
                  <td style={{ ...td, textAlign: "right" }}>
                    <button
                      onClick={() => handleRemoveItem(item.id)}
                      style={{ background: "none", border: "none", cursor: "pointer", color: "#dc2626", fontSize: 13 }}
                    >
                      Remove
                    </button>
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {/* Add item row — only in draft */}
      {isDraft && (
        <div style={{ display: "flex", gap: 8, marginBottom: 24 }}>
          <select
            value={selectedProductId}
            onChange={(e) => setSelectedProductId(e.target.value)}
            style={{ ...input, flex: 1 }}
          >
            <option value="">Select product to add…</option>
            {availableProducts.map((p) => (
              <option key={p.id} value={p.id}>
                {p.name} — ${Number(p.price).toFixed(2)}
              </option>
            ))}
          </select>
          <button onClick={handleAddItem} disabled={!selectedProductId} style={primaryBtn}>
            Add
          </button>
        </div>
      )}

      {actionError && <p style={{ color: "#dc2626", fontSize: 13, marginBottom: 12 }}>{actionError}</p>}

      {/* Draft actions */}
      {isDraft && (
        <div style={{ display: "flex", gap: 8 }}>
          <button
            onClick={handleConfirm}
            disabled={order.items.length === 0}
            title={order.items.length === 0 ? "Add at least one product to confirm" : ""}
            style={{
              ...primaryBtn,
              opacity: order.items.length === 0 ? 0.45 : 1,
              cursor: order.items.length === 0 ? "not-allowed" : "pointer",
            }}
          >
            Confirm Order
          </button>
          <button onClick={handleCancel} style={cancelBtn}>
            Cancel
          </button>
        </div>
      )}

      {/* Pending payment actions */}
      {isPendingPayment && (
        <div style={{ display: "flex", gap: 8 }}>
          <button onClick={handleMarkPaid} style={{ ...primaryBtn, background: "#16a34a" }}>
            Mark as Paid
          </button>
          <button onClick={handleCancel} style={cancelBtn}>
            Cancel
          </button>
        </div>
      )}
    </div>
  );
}

const backBtn: React.CSSProperties = { background: "none", border: "none", cursor: "pointer", color: "#2563eb", marginBottom: 16, padding: 0, fontSize: 14 };
const card: React.CSSProperties = { background: "#f8fafc", border: "1px solid #e2e8f0", borderRadius: 8, padding: 16 };
const labelStyle: React.CSSProperties = { margin: 0, fontSize: 12, color: "#94a3b8", fontWeight: 600, textTransform: "uppercase" };
const valueStyle: React.CSSProperties = { margin: "4px 0 0", fontSize: 18, fontWeight: 700 };
const th: React.CSSProperties = { padding: "10px 12px", textAlign: "left", fontSize: 13, fontWeight: 600 };
const td: React.CSSProperties = { padding: "10px 12px", fontSize: 14 };
const input: React.CSSProperties = { padding: "8px 10px", border: "1px solid #cbd5e1", borderRadius: 4, fontSize: 14 };
const primaryBtn: React.CSSProperties = { background: "#2563eb", color: "#fff", border: "none", borderRadius: 4, padding: "8px 16px", cursor: "pointer", fontWeight: 600 };
const cancelBtn: React.CSSProperties = { background: "#fff", color: "#dc2626", border: "1px solid #dc2626", borderRadius: 4, padding: "8px 16px", cursor: "pointer", fontWeight: 600 };
