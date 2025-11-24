import React from "react";

type Reading = {
  summary_en?: string;
  overall_story_en?: string;
  action_items_en?: string[];
  summary_ko?: string;
  overall_story_ko?: string;
  action_items_ko?: string[];
  prompt_used?: string;
};

type Props = {
  readingEn?: Reading | null;
  readingKo?: Reading | null;
};

export default function ResultView({ readingEn, readingKo }: Props) {
  if (!readingEn && !readingKo) {
    return <p style={{ color: "#6b7280" }}>Reading result will show up here.</p>;
  }

  return (
    <div style={{ display: "grid", gap: "1rem", marginTop: "1rem" }}>
      {readingEn && (
        <section style={{ padding: "1rem", border: "1px solid #e5e7eb", borderRadius: "8px" }}>
          <h3 style={{ marginTop: 0, marginBottom: "0.5rem" }}>Reading (EN)</h3>
          {readingEn.summary_en && <p><strong>Summary:</strong> {readingEn.summary_en}</p>}
          {readingEn.overall_story_en && <p><strong>Story:</strong> {readingEn.overall_story_en}</p>}
          {readingEn.action_items_en && (
            <ul>
              {readingEn.action_items_en.map((item, idx) => (
                <li key={idx}>{item}</li>
              ))}
            </ul>
          )}
        </section>
      )}
      {readingKo && (
        <section style={{ padding: "1rem", border: "1px solid #e5e7eb", borderRadius: "8px" }}>
          <h3 style={{ marginTop: 0, marginBottom: "0.5rem" }}>리딩 (KO)</h3>
          {readingKo.summary_ko && <p><strong>요약:</strong> {readingKo.summary_ko}</p>}
          {readingKo.overall_story_ko && <p><strong>이야기:</strong> {readingKo.overall_story_ko}</p>}
          {readingKo.action_items_ko && (
            <ul>
              {readingKo.action_items_ko.map((item, idx) => (
                <li key={idx}>{item}</li>
              ))}
            </ul>
          )}
        </section>
      )}
    </div>
  );
}
