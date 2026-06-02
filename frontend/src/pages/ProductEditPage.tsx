import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useProduct, useUpdateProduct } from "../hooks/useProducts";

export default function ProductEditPage() {
  const { id = "" } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const { data: product, isLoading, isError } = useProduct(id);
  const updateMutation = useUpdateProduct();

  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [price, setPrice] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    if (product) {
      setName(product.name);
      setDescription(product.description ?? "");
      setPrice(String(product.price));
    }
  }, [product]);

  if (isLoading) return <p style={msg}>Loading…</p>;
  if (isError || !product) return <p style={{ ...msg, color: "#dc2626" }}>Product not found.</p>;

  const handleSubmit = async () => {
    setError("");
    try {
      await updateMutation.mutateAsync({
        id,
        payload: { name, description: description || undefined, price: parseFloat(price) },
      });
      navigate(`/products/${id}`);
    } catch (e: any) {
      setError(e?.response?.data?.detail ?? "Failed to save changes");
    }
  };

  return (
    <div style={container}>
      <button onClick={() => navigate(`/products/${id}`)} style={backBtn}>← Back to Product</button>
      <h2 style={title}>Edit Product</h2>

      <div style={{ display: "flex", flexDirection: "column", gap: 12, maxWidth: 480 }}>
        <label style={labelStyle}>
          Name
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            style={input}
          />
        </label>
        <label style={labelStyle}>
          Description
          <input
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            style={input}
          />
        </label>
        <label style={labelStyle}>
          Price
          <input
            type="number"
            step="0.01"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
            style={input}
          />
        </label>

        {error && <p style={{ color: "#dc2626", fontSize: 13, margin: 0 }}>{error}</p>}

        <div style={{ display: "flex", gap: 8, marginTop: 4 }}>
          <button onClick={handleSubmit} disabled={updateMutation.isPending} style={primaryBtn}>
            {updateMutation.isPending ? "Saving…" : "Save Changes"}
          </button>
          <button onClick={() => navigate(`/products/${id}`)} style={cancelBtn}>
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}

const container: React.CSSProperties = { padding: "20px", fontFamily: "inherit" };
const title: React.CSSProperties = { margin: "0 0 20px", fontSize: 17, fontWeight: 700, color: "#1e293b" };
const backBtn: React.CSSProperties = { background: "none", border: "none", cursor: "pointer", color: "#2563eb", marginBottom: 16, padding: 0, fontSize: 14 };
const labelStyle: React.CSSProperties = { display: "flex", flexDirection: "column", gap: 4, fontSize: 13, fontWeight: 600, color: "#475569" };
const input: React.CSSProperties = { padding: "8px 10px", border: "1px solid #cbd5e1", borderRadius: 4, fontSize: 14, fontWeight: 400 };
const primaryBtn: React.CSSProperties = { background: "#2563eb", color: "#fff", border: "none", borderRadius: 4, padding: "8px 16px", cursor: "pointer", fontWeight: 600 };
const cancelBtn: React.CSSProperties = { background: "#fff", color: "#64748b", border: "1px solid #cbd5e1", borderRadius: 4, padding: "8px 16px", cursor: "pointer", fontWeight: 600 };
const msg: React.CSSProperties = { padding: 24, color: "#64748b" };
