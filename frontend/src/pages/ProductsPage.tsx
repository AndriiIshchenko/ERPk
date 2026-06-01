import { useState } from "react";
import Modal from "../components/Modal";
import {
  useCreateProduct,
  useDeleteProduct,
  useProducts,
  useUpdateProduct,
} from "../hooks/useProducts";
import { Product } from "../types";

export default function ProductsPage() {
  const { data: products = [], isLoading } = useProducts();
  const createMutation = useCreateProduct();
  const updateMutation = useUpdateProduct();
  const deleteMutation = useDeleteProduct();

  const [showCreate, setShowCreate] = useState(false);
  const [editing, setEditing] = useState<Product | null>(null);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [price, setPrice] = useState("");

  const resetForm = () => { setName(""); setDescription(""); setPrice(""); };

  const openEdit = (p: Product) => {
    setEditing(p);
    setName(p.name);
    setDescription(p.description ?? "");
    setPrice(String(p.price));
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
        <button onClick={() => setShowCreate(true)} style={primaryBtn}>+ New Product</button>
      </div>

      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ background: "#f1f5f9" }}>
            {["Name", "Description", "Price", "Actions"].map((h) => (
              <th key={h} style={th}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {products.map((p) => (
            <tr key={p.id} style={{ borderBottom: "1px solid #e2e8f0" }}>
              <td style={td}>{p.name}</td>
              <td style={td}>{p.description ?? "—"}</td>
              <td style={td}>${Number(p.price).toFixed(2)}</td>
              <td style={td}>
                <button onClick={() => openEdit(p)} style={actionBtn}>Edit</button>
                <button onClick={() => deleteMutation.mutate(p.id)} style={{ ...actionBtn, color: "#dc2626" }}>Delete</button>
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

const primaryBtn: React.CSSProperties = { background: "#2563eb", color: "#fff", border: "none", borderRadius: 4, padding: "8px 16px", cursor: "pointer", fontWeight: 600 };
const actionBtn: React.CSSProperties = { background: "none", border: "none", cursor: "pointer", marginRight: 8 };
const th: React.CSSProperties = { padding: "10px 12px", textAlign: "left", fontSize: 13, fontWeight: 600 };
const td: React.CSSProperties = { padding: "10px 12px", fontSize: 14 };
const input: React.CSSProperties = { padding: "8px 10px", border: "1px solid #cbd5e1", borderRadius: 4, fontSize: 14 };
