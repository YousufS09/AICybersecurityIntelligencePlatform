import { useState } from "react";
import DashboardTemplate from "../templates/DashboardTemplate";
import { analyzeThreat } from "../../services/api";

export default function DashboardPage() {
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState("");

  async function handleAnalyze(text) {
    setError("");

    try {
      const result = await analyzeThreat(text);
      setAnalysis(result);
    } catch (err) {
      setAnalysis(null);
      setError(err instanceof Error ? err.message : "Analysis failed.");
    }
  }

  return (
    <DashboardTemplate
      analysis={analysis}
      error={error}
      onAnalyze={handleAnalyze}
    />
  );
}
