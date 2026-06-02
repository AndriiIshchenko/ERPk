interface Props {
  label: string;
  variant: "draft" | "pending" | "paid" | "cancelled";
}

const colors: Record<Props["variant"], string> = {
  draft:     "#64748b",
  pending:   "#d97706",
  paid:      "#16a34a",
  cancelled: "#dc2626",
};

const labels: Record<Props["variant"], string> = {
  draft:     "Draft",
  pending:   "Pending Payment",
  paid:      "Paid",
  cancelled: "Cancelled",
};

export default function Badge({ variant }: Omit<Props, "label">) {
  return (
    <span
      style={{
        background: colors[variant],
        color: "#fff",
        borderRadius: 4,
        padding: "2px 8px",
        fontSize: 12,
        fontWeight: 600,
        whiteSpace: "nowrap",
      }}
    >
      {labels[variant]}
    </span>
  );
}
