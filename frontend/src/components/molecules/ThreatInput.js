import { useState } from "react";
import Card from "../atoms/Card";
import TextArea from "../atoms/TextArea";
import PrimaryButton from "../atoms/PrimaryButton";

export default function ThreatInput({ onAnalyze }) {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleAnalyze() {
    if (!text.trim()) return;

    setLoading(true);
    try {
      await onAnalyze(text);
    } finally {
      setLoading(false);
    }
  }

  return (
    <Card className="h-full">
      <div className="mb-4">
        <p className="text-xs uppercase tracking-[0.24em] text-cyan-300/80">
          Threat Intake
        </p>
        <h2 className="mt-2 text-2xl font-semibold text-white">
          Analyse a suspicious message
        </h2>
        <p className="mt-2 text-sm leading-6 text-slate-400">
          Paste the email, SMS, or chat content you want to inspect. We'll send
          it to the detection model and return a risk assessment.
        </p>
      </div>

      <TextArea
        placeholder="Paste suspicious email or message here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        disabled={loading}
      />

      <PrimaryButton
        onClick={handleAnalyze}
        disabled={loading || !text.trim()}
        className="mt-4 w-full"
      >
        {loading ? "Analysing..." : "Analyse threat"}
      </PrimaryButton>
    </Card>
  );
}
