import React from "react";

type SpreadOption = {
  value: string;
  label: string;
  cards: number;
  description: string;
};

type Props = {
  value: string;
  onChange: (value: string) => void;
};

const options: SpreadOption[] = [
  { value: "past_present_future", label: "Past-Present-Future (3)", cards: 3, description: "Quick timeline" },
  { value: "situation_obstacle_advice", label: "Situation-Obstacle-Advice (3)", cards: 3, description: "Decision helper" },
  { value: "nine_box", label: "3x3 Box (9)", cards: 9, description: "Deep situational view" },
  { value: "grand_tableau_8x4_plus4", label: "Grand Tableau (36)", cards: 36, description: "Full overview" },
];

export default function SpreadSelector({ value, onChange }: Props) {
  return (
    <label style={{ display: "block", marginBottom: "1rem" }}>
      <span style={{ display: "block", marginBottom: "0.25rem", fontWeight: 600 }}>Spread Type</span>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        style={{ width: "100%", padding: "0.5rem", borderRadius: "6px", border: "1px solid #d1d5db" }}
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label} - {option.description}
          </option>
        ))}
      </select>
    </label>
  );
}
