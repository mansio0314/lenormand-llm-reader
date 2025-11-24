import React from "react";

export type CardPosition = {
  card_id: number;
  position_key?: string | null;
  position_label_en?: string | null;
  position_label_ko?: string | null;
  row?: number | null;
  column?: number | null;
  name_en?: string | null;
  name_ko?: string | null;
  interpretation_en?: string | null;
  interpretation_ko?: string | null;
};

type Props = {
  cards: CardPosition[];
};

export default function CardView({ cards }: Props) {
  if (!cards?.length) {
    return (
      <p style={{ color: "#6b7280" }}>
        Cards will appear here after you request a reading.
      </p>
    );
  }

  return (
    <div style={{ display: "grid", gap: "0.75rem", gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))" }}>
      {cards.map((card) => (
        <div
          key={`${card.position_key}-${card.card_id}`}
          style={{
            border: "1px solid #e5e7eb",
            borderRadius: "8px",
            padding: "0.75rem",
            background: "#fff",
            boxShadow: "0 1px 2px rgba(0,0,0,0.04)",
          }}
        >
          <div style={{ fontSize: "0.85rem", color: "#6b7280" }}>
            {card.position_label_en || card.position_key} - {card.position_label_ko}
          </div>
          <div style={{ fontWeight: 700, marginTop: "0.25rem" }}>
            {card.name_en} / {card.name_ko}
          </div>
          <div style={{ fontSize: "0.9rem", marginTop: "0.35rem" }}>
            #{card.card_id} - Row {card.row} Col {card.column}
          </div>
          {card.interpretation_en && (
            <p style={{ marginTop: "0.35rem", color: "#111827" }}>{card.interpretation_en}</p>
          )}
        </div>
      ))}
    </div>
  );
}
