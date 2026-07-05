import ThreatInput from "../molecules/ThreatInput";
import ThreatResult from "../molecules/ThreatResult";
import SecurityAssistant from "../organisms/SecurityAssistant";

export default function DashboardTemplate({ analysis, error, onAnalyze }) {
  return (
    <div className="relative min-h-screen overflow-hidden bg-slate-950 text-slate-100">
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute left-[-8rem] top-[-6rem] h-72 w-72 rounded-full bg-cyan-500/20 blur-3xl" />
        <div className="absolute right-[-6rem] top-24 h-80 w-80 rounded-full bg-sky-400/10 blur-3xl" />
        <div className="absolute inset-x-0 bottom-[-8rem] mx-auto h-80 w-80 rounded-full bg-teal-400/10 blur-3xl" />
      </div>

      <div className="relative mx-auto flex min-h-screen w-full max-w-7xl flex-col px-4 py-6 sm:px-6 lg:px-8">
        <header className="mb-8 flex items-center justify-between gap-4 rounded-[2rem] border border-white/10 bg-white/5 px-5 py-4 shadow-2xl shadow-slate-950/30 backdrop-blur-xl">
          <div>
            <p className="text-xs uppercase tracking-[0.28em] text-cyan-300/80">
              AI Cybersecurity Intelligence
            </p>
            <h1 className="mt-2 text-2xl font-semibold text-white sm:text-3xl">
              Threat analysis workspace
            </h1>
          </div>
          <p className="max-w-sm text-right text-sm leading-6 text-slate-400">
            Phishing detection, risk assessment, and AI-assisted response in one
            focused cockpit.
          </p>
        </header>

        {error ? (
          <div className="mb-6 rounded-[1.5rem] border border-rose-400/20 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">
            {error}
          </div>
        ) : null}

        <main className="grid flex-1 gap-6 lg:grid-cols-[1.05fr_0.95fr]">
          <div className="space-y-6">
            <ThreatInput onAnalyze={onAnalyze} />
            <ThreatResult result={analysis} />
          </div>

          <SecurityAssistant context={analysis} />
        </main>
      </div>
    </div>
  );
}
