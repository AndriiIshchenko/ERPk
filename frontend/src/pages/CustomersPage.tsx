import { useState } from "react";
import Modal from "../components/Modal";
import {
  useCreateCustomer,
  useCustomers,
  useDeleteCustomer,
  useUpdateCustomer,
} from "../hooks/useCustomers";
import { Customer } from "../types";

export default function CustomersPage() {
  const { data: customers = [], isLoading } = useCustomers();
  const createMutation = useCreateCustomer();
  const updateMutation = useUpdateCustomer();
  const deleteMutation = useDeleteCustomer();

  const [showCreate, setShowCreate] = useState(false);
  const [editing, setEditing] = useState<Customer | null>(null);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");

  const resetForm = () => { setName(""); setEmail(""); setPhone(""); };

  const openEdit = (c: Customer) => {
    setEditing(c);
    setName(c.name);
    setEmail(c.email);
    setPhone(c.phone ?? "");
  };

  const submitCreate = async () => {
    await createMutation.mutateAsync({ name, email, phone: phone || undefined });
    setShowCreate(false);
    resetForm();
  };

  const submitEdit = async () => {
    if (!editing) return;
    await updateMutation.mutateAsync({
      id: editing.id,
      payload: { name, email, phone: phone || undefined },
    });
    setEditing(null);
    resetForm();
  };

  if (isLoading) return <p>Loading…</p>;

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
        <h2>Customers</h2>
        <button onClick={() => setShowCreate(true)} style={primaryBtn}>+ New Customer</button>
      </div>

      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ background: "#f1f5f9" }}>
            {["Name", "Email", "Phone", "Actions"].map((h) => (
              <th key={h} style={th}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {customers.map((c) => (
            <tr key={c.id} style={{ borderBottom: "1px solid #e2e8f0" }}>
              <td style={td}>{c.name}</td>
              <td style={td}>{c.email}</td>
              <td style={td}>{c.phone ?? "—"}</td>
              <td style={td}>
                <button onClick={() => openEdit(c)} style={actionBtn}>Edit</button>
                <button onClick={() => deleteMutation.mutate(c.id)} style={{ ...actionBtn, color: "#dc2626" }}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {(showCreate || editing) && (
        <Modal
          title={editing ? "Edit Customer" : "New Customer"}
          onClose={() => { setShowCreate(false); setEditing(null); resetForm(); }}
        >
          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            <input placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} style={input} />
            <input placeholder="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} style={input} />
            <input placeholder="Phone" value={phone} onChange={(e) => setPhone(e.target.value)} style={input} />
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
