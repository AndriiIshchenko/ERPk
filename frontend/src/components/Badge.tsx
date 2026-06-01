interface Props {
  label: string;
  variant: "vendor" | "pending" | "confirmed" | "cancelled";
}

const colors: Record<Props["variant"], string> = {
  vendor: "#2563eb",
  pending: "#d97706",
  confirmed: "#16a34a",
  cancelled: "#dc2626",
};

export default function Badge({ label, variant }: Props) {
  return (
    <span
      style={{
        background: colors[variant],
        color: "#fff",
        borderRadius: 4,
        padding: "2px 8px",
        fontSize: 12,
        fontWeight: 600,
      }}
    >
      {label}
    </span>
  );
}
