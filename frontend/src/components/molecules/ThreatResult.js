import Card from "../atoms/Card";
import StatCard from "../atoms/StatCard";

function formatConfidence(value) {
  if (typeof value !== "number") return "-";
  if (value > 1) return `${value.toFixed(2)}%`;
  return `${(value * 100).toFixed(1)}%`;
}

export default function ThreatResult({ result }) {
  const riskTone = {
    High: "text-rose-300",
    Medium: "text-amber-300",
    Low: "text-emerald-300",
  };

  const accent = result ? riskTone[result.risk_level] || "text-slate-100" : "";

  return (
    <Card className="mt-6">
      <div className="mb-4 flex items-start justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-[0.24em] text-cyan-300/80">
            Detection Output
          </p>
          <h2 className="mt-2 text-2xl font-semibold text-white">
            Analysis result
          </h2>
        </div>
        {result ? (
          <span
            className={`rounded-full border border-white/10 px-3 py-1 text-sm font-semibold ${accent}`}
          >
            {result.risk_level} risk
          </span>
        ) : null}
      </div>

      {!result ? (
        <div className="rounded-2xl border border-dashed border-white/10 bg-white/5 p-6 text-sm text-slate-400">
          Run an analysis to see the model prediction, confidence score, and
          risk level here.
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-3">
          <StatCard
            label="Threat"
            value={result.prediction}
            tone="text-white"
          />
          <StatCard
            label="Confidence"
            value={formatConfidence(result.confidence)}
            tone="text-white"
          />
          <StatCard label="Risk" value={result.risk_level} tone={accent} />
        </div>
      )}
    </Card>
  );
}
