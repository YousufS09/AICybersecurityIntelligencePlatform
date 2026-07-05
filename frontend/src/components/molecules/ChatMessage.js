export default function ChatMessage({ sender, text }) {
  const isUser = sender === "user";

  return (
    <div
      className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-6 ${
        isUser
          ? "ml-auto bg-cyan-400 text-slate-950"
          : "bg-white/5 text-slate-200"
      }`}
    >
      {text}
    </div>
  );
}
