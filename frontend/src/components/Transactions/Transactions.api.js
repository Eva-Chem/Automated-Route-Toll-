import api from "../../services/api";

export const getTransactions = async () => {
  const response = await api.get("/api/tolls-history");
  const records = response?.data?.data || [];

  return records.map((t) => ({
    id: t.id || t.checkout_request_id,
    amount: t.amount ?? 0,
    status: t.status || "UNKNOWN",
    zone_name: t.zone_name || "",
    phone: t["phone number"] || t.phone || "",
    ref: t.mpesa_receipt_number || t.checkout_request_id || t.id || "",
    created_at: t.created_at,
  }));
};
