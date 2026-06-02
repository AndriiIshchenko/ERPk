import { useState } from "react";
import Modal from "../components/Modal";
import {
  useCreateProduct,
  useDeactivateProduct,
  useProducts,
  useRestoreProduct,
  useUpdateProduct,
} from "../hooks/useProducts";
import { Product } from "../types";

const POPUP = "width=700,height=420,resizable=yes,scrollbars=yes";

export default function ProductsPage() {
  const [tab, setTab] = useState<"active" | "inactive">("active");
  const { data: products = [], isLoading } = useProducts(tab === "inactive");
  const createMutation = useCreateProduct();
  const updateMutation = useUpdateProduct();
  const deactivateMutation = useDeactivateProduct();
  const restoreMutation = useRestoreProduct();

  const [search, setSearch] = useState("");
  const [showCreate, setShowCreate] = useState(false);
  const [editing, setEditing] = useState<Product | null>(null);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [price, setPrice] = useState("");

  const filtered = products
    .filter((p) => (tab === "active" ? p.is_active : !p.is_active))
    .filter((p) => p.name.toLowerCase().includes(search.toLowerCase()));

  const resetForm = () => { setName(""); setDescription(""); setPrice(""); };

  const openEdit = (p: Product) => {
    setEditing(p);
    setName(p.name);
    setDescription(p.description ?? "");
    setPrice(String(p.price));
  };

  const openDetail = (p: Product) => {
    window.open(`/products/${p.id}`, `product_${p.id}`, POPUP);
  };

  const submitCreate = async () => {
    await createMutation.mutateAsync({ name, description: description || undefined, price: parseFloat(price) });
    setShowCreate(false);
    resetForm();
  };

  const submitEdit = async () => {
    if (!editing) return;
    await updateMutation.mutateAsync({ id: editing.id, payload: { name, description: description || undefined, price: parseFloat(price) } });
    setEditing(null);
    resetForm();
  };

  if (isLoading) return <p>Loading…</p>;

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
        <h2>Products</h2>
        <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
          <div style={tabGroup}>
            {(["active", "inactive"] as const).map((t) => (
              <button
                key={t}
                onClick={() => setTab(t)}
                style={{ ...tabBtn, ...(tab === t ? tabBtnActive : {}) }}
              >
                {t === "active" ? "Active" : "Inactive"}
              </button>
            ))}
          </div>
          <button onClick={() => setShowCreate(true)} style={primaryBtn}>+ New Product</button>
        </div>
      </div>

      <input
        placeholder="Search by name…"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        style={{ ...input, width: "100%", marginBottom: 12, boxSizing: "border-box" }}
      />

      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ background: "#f1f5f9" }}>
            {["Name", "Description", "Price", "Actions"].map((h) => (
              <th key={h} style={th}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {filtered.length === 0 && (
            <tr>
              <td colSpan={4} style={{ ...td, color: "#94a3b8", textAlign: "center" }}>
                No products match "{search}"
              </td>
            </tr>
          )}
          {filtered.map((p) => (
            <tr
              key={p.id}
              style={{ borderBottom: "1px solid #e2e8f0", cursor: "pointer" }}
              onClick={() => openDetail(p)}
            >
              <td style={td}>{p.name}</td>
              <td style={{ ...td, color: "#64748b" }}>{p.description ?? "—"}</td>
              <td style={td}>${Number(p.price).toFixed(2)}</td>
              <td style={td} onClick={(e) => e.stopPropagation()}>
                {p.is_active ? (
                  <>
                    <button onClick={() => openEdit(p)} style={actionBtn}>Edit</button>
                    <button
                      onClick={() => deactivateMutation.mutate(p.id)}
                      style={{ ...actionBtn, color: "#d97706" }}
                    >
                      Deactivate
                    </button>
                  </>
                ) : (
                  <button
                    onClick={() => restoreMutation.mutate(p.id)}
                    style={{ ...actionBtn, color: "#16a34a" }}
                  >
                    Restore
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {(showCreate || editing) && (
        <Modal
          title={editing ? "Edit Product" : "New Product"}
          onClose={() => { setShowCreate(false); setEditing(null); resetForm(); }}
        >
          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            <input placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} style={input} />
            <input placeholder="Description" value={description} onChange={(e) => setDescription(e.target.value)} style={input} />
            <input placeholder="Price" type="number" step="0.01" value={price} onChange={(e) => setPrice(e.target.value)} style={input} />
            <button onClick={editing ? submitEdit : submitCreate} style={primaryBtn}>
              {editing ? "Save" : "Create"}
            </button>
          </div>
        </Modal>
      )}
    </div>
  );
}

const tabGroup: React.CSSProperties = { display: "flex", border: "1px solid #e2e8f0", borderRadius: 4, overflow: "hidden" };
const tabBtn: React.CSSProperties = { background: "#fff", color: "#64748b", border: "none", padding: "6px 16px", cursor: "pointer", fontSize: 13, fontWeight: 600 };
const tabBtnActive: React.CSSProperties = { background: "#2563eb", color: "#fff" };
const primaryBtn: React.CSSProperties = { background: "#2563eb", color: "#fff", border: "none", borderRadius: 4, padding: "8px 16px", cursor: "pointer", fontWeight: 600 };
const actionBtn: React.CSSProperties = { background: "none", border: "none", cursor: "pointer", marginRight: 8, fontSize: 13 };
const th: React.CSSProperties = { padding: "10px 12px", textAlign: "left", fontSize: 13, fontWeight: 600 };
const td: React.CSSProperties = { padding: "10px 12px", fontSize: 14 };
const input: React.CSSProperties = { padding: "8px 10px", border: "1px solid #cbd5e1", borderRadius: 4, fontSize: 14 };
