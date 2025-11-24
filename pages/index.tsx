import Link from "next/link";
import Head from "next/head";

export default function Home() {
  return (
    <>
      <Head>
        <title>Lenormand LLM Reader</title>
      </Head>
      <main style={{ fontFamily: "Inter, sans-serif", margin: "2rem auto", maxWidth: "720px" }}>
        <header style={{ marginBottom: "1.5rem" }}>
          <h1>Lenormand LLM Reader</h1>
          <p>Prototype Next.js UI for FastAPI-powered Lenormand readings.</p>
        </header>
        <section style={{ display: "grid", gap: "1rem" }}>
          <div style={{ padding: "1rem", border: "1px solid #e5e7eb", borderRadius: "8px" }}>
            <h2>Get a Reading</h2>
            <p>Provide your question, category, and choose a spread.</p>
            <Link href="/reading" style={{ color: "#2563eb" }}>
              Go to reading page ->
            </Link>
          </div>
          <div style={{ padding: "1rem", border: "1px solid #e5e7eb", borderRadius: "8px" }}>
            <h2>API</h2>
            <p>Backend endpoint: <code>POST /api/reading</code></p>
          </div>
        </section>
      </main>
    </>
  );
}
