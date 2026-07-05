export default function Card({ children, className = "" }) {
  return (
    <div
      className={`rounded-[1.75rem] border border-white/10 bg-slate-950/70 p-5 shadow-2xl shadow-slate-950/30 backdrop-blur-xl ${className}`}
    >
      {children}
    </div>
  );
}
