import { useNavigate, useParams } from "react-router-dom";
import { useProduct, useProductHistory, useDeactivateProduct, useRestoreProduct } from "../hooks/useProducts";
import { ProductHistory } from "../types";

const changeLabel: Record<ProductHistory["change_type"], string> = {
  update:     "Edited",
  deactivate: "Deactivated",
  restore:    "Restored",
};

const changeColor: Record<ProductHistory["change_type"], string> = {
  update:     "#2563eb",
  deactivate: "#d97706",
  restore:    "#16a34a",
};

export default function ProductDetailPage() {
  const { id = "" } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: product, isLoading, isError } = useProduct(id);
  const { data: history = [] } = useProductHistory(id);
  const deactivate = useDeactivateProduct();
  const restore = useRestoreProduct();

  if (isLoading) return <p style={msg}>Loading…</p>;
  if (isError || !product) return <p style={{ ...msg, color: "#dc2626" }}>Product not found.</p>;

  const handleToggle = async () => {
    if (product.is_active) {
      await deactivate.mutateAsync(product.id);
    } else {
      await restore.mutateAsync(product.id);
    }
  };

  return (
    <div style={container}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12 }}>
        <h2 style={title}>{product.name}</h2>
        <div style={{ display: "flex", gap: 8, alignItems: "center", flexShrink: 0 }}>
          <span style={{ ...statusBadge, background: product.is_active ? "#16a34a" : "#94a3b8" }}>
            {product.is_active ? "Active" : "Inactive"}
          </span>
          {product.is_active && (
            <button onClick={() => navigate(`/products/${id}/edit`)} style={editBtn}>
              Edit
            </button>
          )}
        </div>
      </div>
      <hr style={divider} />

      <Row label="Description" value={product.description ?? "—"} />
      <Row
        label="Price"
        value={`$${Number(product.price).toFixed(2)}`}
        valueStyle={{ fontSize: 22, color: "#2563eb", fontWeight: 700 }}
      />
      <Row label="Added" value={new Date(product.created_at).toLocaleString()} />
      {!product.is_active && product.deactivated_at && (
        <Row
          label="Deactivated"
          value={new Date(product.deactivated_at).toLocaleString()}
          valueStyle={{ color: "#d97706" }}
        />
      )}

      <button
        onClick={handleToggle}
        style={{
          ...toggleBtn,
          background: product.is_active ? "#fff" : "#16a34a",
          color: product.is_active ? "#d97706" : "#fff",
          border: product.is_active ? "1px solid #d97706" : "none",
          marginTop: 8,
          marginBottom: 24,
        }}
      >
        {product.is_active ? "Deactivate" : "Restore"}
      </button>

      {/* History */}
      <h3 style={{ margin: "0 0 8px", fontSize: 14, color: "#475569" }}>Edit History</h3>
      {history.length === 0 ? (
        <p style={{ fontSize: 13, color: "#94a3b8" }}>No changes recorded yet.</p>
      ) : (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ background: "#f8fafc" }}>
              {["Action", "Name", "Price", "By", "When"].map((h) => (
                <th key={h} style={hth}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {history.map((h) => (
              <tr key={h.id} style={{ borderBottom: "1px solid #f1f5f9" }}>
                <td style={htd}>
                  <span style={{ color: changeColor[h.change_type], fontWeight: 600, fontSize: 12 }}>
                    {changeLabel[h.change_type]}
                  </span>
                </td>
                <td style={htd}>{h.name}</td>
                <td style={htd}>${Number(h.price).toFixed(2)}</td>
                <td style={{ ...htd, color: "#64748b" }}>{h.changed_by_email}</td>
                <td style={{ ...htd, color: "#94a3b8" }}>{new Date(h.changed_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

function Row({
  label,
  value,
  valueStyle,
}: {
  label: string;
  value: string;
  valueStyle?: React.CSSProperties;
}) {
  return (
    <div style={{ marginBottom: 14 }}>
      <p style={rowLabel}>{label}</p>
      <p style={{ ...rowValue, ...valueStyle }}>{value}</p>
    </div>
  );
}

const container: React.CSSProperties = { padding: "20px", fontFamily: "inherit" };
const title: React.CSSProperties = { margin: 0, fontSize: 17, fontWeight: 700, color: "#1e293b", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis", flex: 1, marginRight: 12 };
const divider: React.CSSProperties = { border: "none", borderTop: "1px solid #e2e8f0", margin: "0 0 16px" };
const rowLabel: React.CSSProperties = { margin: 0, fontSize: 11, fontWeight: 600, color: "#94a3b8", textTransform: "uppercase", letterSpacing: "0.05em" };
const rowValue: React.CSSProperties = { margin: "3px 0 0", fontSize: 14, color: "#1e293b" };
const statusBadge: React.CSSProperties = { color: "#fff", borderRadius: 4, padding: "2px 8px", fontSize: 12, fontWeight: 600, whiteSpace: "nowrap" };
const toggleBtn: React.CSSProperties = { borderRadius: 4, padding: "6px 14px", cursor: "pointer", fontWeight: 600, fontSize: 13 };
const editBtn: React.CSSProperties = { background: "#2563eb", color: "#fff", border: "none", borderRadius: 4, padding: "4px 12px", cursor: "pointer", fontWeight: 600, fontSize: 12 };
const hth: React.CSSProperties = { padding: "7px 8px", textAlign: "left", fontSize: 11, fontWeight: 600, color: "#64748b" };
const htd: React.CSSProperties = { padding: "7px 8px", fontSize: 12 };
const msg: React.CSSProperties = { padding: 24, color: "#64748b" };
