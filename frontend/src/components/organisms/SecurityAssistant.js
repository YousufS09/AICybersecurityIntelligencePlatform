import { useState } from "react";
import { chatWithAssistant } from "../../services/api";
import Card from "../atoms/Card";
import TextInput from "../atoms/TextInput";
import PrimaryButton from "../atoms/PrimaryButton";
import ChatMessage from "../molecules/ChatMessage";

export default function SecurityAssistant({ context }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [typing, setTyping] = useState(false);
  const [error, setError] = useState("");

  async function sendMessage() {
    if (!input.trim() || typing || !context) return;

    const userMessage = input;
    setInput("");
    setTyping(true);
    setError("");

    setMessages((prev) => [...prev, { sender: "user", text: userMessage }]);

    try {
      const response = await chatWithAssistant({
        message: userMessage,
        ...context,
      });

      setMessages((prev) => [...prev, { sender: "bot", text: response.reply }]);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Unable to send message."
      );
    } finally {
      setTyping(false);
    }
  }

  if (!context) {
    return (
      <Card className="h-full min-h-[420px]">
        <p className="text-xs uppercase tracking-[0.24em] text-cyan-300/80">
          Security Assistant
        </p>
        <h2 className="mt-2 text-2xl font-semibold text-white">
          Ready when the threat is analysed
        </h2>
        <p className="mt-4 text-sm leading-6 text-slate-400">
          Run an analysis first. The assistant will then explain the result and
          help with mitigation, impact, and next steps.
        </p>
      </Card>
    );
  }

  return (
    <Card className="flex min-h-[520px] flex-col">
      <div className="mb-4">
        <p className="text-xs uppercase tracking-[0.24em] text-cyan-300/80">
          Security Assistant
        </p>
        <h2 className="mt-2 text-2xl font-semibold text-white">
          AI response desk
        </h2>
      </div>

      <div className="mb-4 rounded-2xl border border-white/8 bg-white/5 p-4 text-sm leading-6 text-slate-300">
        This threat was classified as{" "}
        <span className="font-semibold text-white">{context.risk_level}</span>{" "}
        risk. Ask about impact, mitigation, or what to do next.
      </div>

      <div className="flex-1 space-y-3 overflow-y-auto pr-1">
        {error ? (
          <div className="rounded-2xl border border-rose-400/20 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">
            {error}
          </div>
        ) : null}

        {messages.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-white/10 bg-white/5 p-4 text-sm text-slate-400">
            Try asking why it was flagged or what the next response should be.
          </div>
        ) : null}

        {messages.map((message, index) => (
          <ChatMessage key={`${message.sender}-${index}`} {...message} />
        ))}

        {typing ? (
          <div className="rounded-2xl bg-white/5 px-4 py-3 text-sm italic text-slate-400">
            Security assistant is typing...
          </div>
        ) : null}
      </div>

      <div className="mt-4 flex gap-3">
        <TextInput
          placeholder="Ask about this threat..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              sendMessage();
            }
          }}
          disabled={typing}
        />
        <PrimaryButton onClick={sendMessage} disabled={typing || !input.trim()}>
          Send
        </PrimaryButton>
      </div>
    </Card>
  );
}
