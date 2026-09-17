import { Marked } from "marked";

// Tutor replies are model output: raw HTML in them is shown as text, never rendered.
const escapeHtml = (s: string) => s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]!);
const marked = new Marked({ async: false, gfm: true, breaks: false, renderer: { html: ({ text }) => escapeHtml(text) } });

export function Markdown({ text, className = "" }: { text: string; className?: string }) {
  return <div className={`md ${className}`} dangerouslySetInnerHTML={{ __html: marked.parse(text) as string }} />;
}
