import { FormEvent, useState } from "react";
import Head from "next/head";
import SpreadSelector from "../components/SpreadSelector";
import CardView, { CardPosition } from "../components/CardView";
import ResultView from "../components/ResultView";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export default function ReadingPage() {
  const [question, setQuestion] = useState("올해 커리어 방향은 어떻게 될까요?");
  const [category, setCategory] = useState("career");
  const [spreadType, setSpreadType] = useState("past_present_future");
  const [cards, setCards] = useState<CardPosition[]>([]);
  const [readingEn, setReadingEn] = useState<any>(null);
  const [readingKo, setReadingKo] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/api/reading`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question_ko: question,
          category,
          spread_type: spreadType,
        }),
      });
      if (!res.ok) {
        const errText = await res.text();
        throw new Error(errText || "Failed to fetch reading");
      }
      const data = await res.json();
      setCards(data.cards || []);
      setReadingEn(data.reading_en || null);
      setReadingKo(data.reading_ko || null);
    } catch (err: any) {
      console.error(err);
      setError(err.message || "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>Reading | Lenormand LLM Reader</title>
      </Head>
      <main style={{ fontFamily: "Inter, sans-serif", margin: "2rem auto", maxWidth: "900px" }}>
        <header style={{ marginBottom: "1.5rem" }}>
          <h1>Get a Lenormand Reading</h1>
          <p>Send a request to the FastAPI backend and view the drafted output.</p>
        </header>

        <form onSubmit={handleSubmit} style={{ display: "grid", gap: "1rem", marginBottom: "1.5rem" }}>
          <label style={{ display: "block" }}>
            <span style={{ display: "block", marginBottom: "0.25rem", fontWeight: 600 }}>Question (KO)</span>
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              rows={3}
              style={{ width: "100%", padding: "0.75rem", borderRadius: "8px", border: "1px solid #d1d5db" }}
              placeholder="예: 연애, 커리어, 재정 등 구체적인 질문을 입력하세요."
            />
          </label>

          <label style={{ display: "block" }}>
            <span style={{ display: "block", marginBottom: "0.25rem", fontWeight: 600 }}>Category</span>
            <input
              type="text"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              style={{ width: "100%", padding: "0.5rem", borderRadius: "6px", border: "1px solid #d1d5db" }}
              placeholder="love / career / finance / self"
            />
          </label>

          <SpreadSelector value={spreadType} onChange={setSpreadType} />

          <button
            type="submit"
            disabled={loading}
            style={{
              padding: "0.75rem 1rem",
              backgroundColor: "#2563eb",
              color: "#fff",
              border: "none",
              borderRadius: "8px",
              cursor: loading ? "not-allowed" : "pointer",
              fontWeight: 700,
            }}
          >
            {loading ? "Requesting..." : "Request Reading"}
          </button>
          {error && <p style={{ color: "#b91c1c" }}>Error: {error}</p>}
          <p style={{ color: "#6b7280", fontSize: "0.9rem" }}>
            Disclaimer: This UI and backend are prototypes. Replace the stub LLM/translation clients with real services.
          </p>
        </form>

        <section style={{ marginBottom: "1.5rem" }}>
          <h2>Cards</h2>
          <CardView cards={cards} />
        </section>

        <section>
          <h2>Results</h2>
          <ResultView readingEn={readingEn} readingKo={readingKo} />
        </section>
      </main>
    </>
  );
}
