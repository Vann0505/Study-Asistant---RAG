import { useState, useRef, useEffect } from "react";
import "./App.css";

const API_BASE = "http://127.0.0.1:8000";

export default function App() {
  const [sessionId, setSessionId] = useState(null);
  const [fileName, setFileName] = useState("");
  const [chunkCount, setChunkCount] = useState(0);
  const [uploading, setUploading] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [lastSources, setLastSources] = useState([]);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function handleFileUpload(e) {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${API_BASE}/upload`, { method: "POST", body: formData });
      if (!res.ok) throw new Error("Upload gagal");
      const data = await res.json();
      setSessionId(data.session_id);
      setFileName(data.filename);
      setChunkCount(data.chunk_count);
      setMessages([]);
      setLastSources([]);
    } catch (err) {
      alert("Gagal upload file. Pastikan backend jalan di " + API_BASE);
    } finally {
      setUploading(false);
    }
  }

  async function handleAsk() {
    if (!input.trim() || !sessionId || loading) return;
    const question = input.trim();
    setMessages((prev) => [...prev, { role: "user", content: question }]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, question }),
      });
      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.answer, sourceCount: (data.sources || []).length },
      ]);
      setLastSources(data.sources || []);
    } catch (err) {
      setMessages((prev) => [...prev, { role: "assistant", content: "Gagal menghubungi backend.", sourceCount: 0 }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <header className="masthead">
        <div className="masthead-title">Study Assistant System</div>
        {fileName && (
          <div className="masthead-file">
            <span className="spine-label">{fileName}</span>
            <span className="stamp">{chunkCount} Potongan Terindeks</span>
          </div>
        )}
      </header>

      {!sessionId ? (
        <div className="intake">
          <p className="intake-kicker">Mulai Masukan Materi dan Siap Untuk Belajar</p>
          <h1 className="intake-headline">Materi apa hari ini?</h1>
          <p className="intake-sub">
            Terima file PDF, DOCX, atau Txt.
          </p>
          <label className={`drop-slot ${uploading ? "is-busy" : ""}`}>
            <input type="file" accept=".pdf,.docx,.txt" onChange={handleFileUpload} disabled={uploading} hidden />
            {uploading ? "Memproses dokumen…" : "Pilih berkas untuk diunggah"}
          </label>
        </div>
      ) : (
        <div className="reading-room">
          <main className="transcript">
            {messages.length === 0 && (
              <p className="transcript-empty">
                Tanyakan apa saja tentang isi dokumen ini. Sistem siap membantu
              </p>
            )}
            {messages.map((m, i) => (
              <div key={i} className={`entry entry--${m.role}`}>
                <div className="entry-label">{m.role === "user" ? "Pertanyaan" : "Jawaban"}</div>
                <div className="entry-body">
                  {m.content}
                  {m.role === "assistant" && m.sourceCount > 0 && (
                    <span className="footnote-marks">
                      {Array.from({ length: m.sourceCount }).map((_, k) => (
                        <sup key={k}>[{k + 1}]</sup>
                      ))}
                    </span>
                  )}
                </div>
              </div>
            ))}
            {loading && <div className="transcript-status">Menelusuri dokumen…</div>}
            <div ref={bottomRef} />
          </main>

          <aside className="margin-notes">
            <div className="margin-heading">Note</div>
            {lastSources.length === 0 ? (
              <p className="margin-empty">Sumber akan muncul di sini setelah kamu bertanya.</p>
            ) : (
              lastSources.map((s, i) => (
                <div key={i} className="footnote">
                  <div className="footnote-index">[{i + 1}]</div>
                  <div className="footnote-text">{s.text}</div>
                  <div className="footnote-score">Similarity {s.score.toFixed(2)}</div>
                </div>
              ))
            )}
          </aside>
        </div>
      )}

      {sessionId && (
        <div className="composer">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleAsk()}
            placeholder="Tulis pertanyaanmu di sini…"
          />
          <button onClick={handleAsk} disabled={loading || !input.trim()}>
            Kirim
          </button>
        </div>
      )}
    </div>
  );
}