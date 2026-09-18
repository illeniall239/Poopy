"use client";
import dynamic from "next/dynamic";

// Client wrapper so the server page can render Excalidraw, which needs the browser.
const SketchPad = dynamic(() => import("./SketchPad"), { ssr: false, loading: () => <p className="p-6 text-sm text-muted">Loading the sketchpad…</p> });

export function GeneralSketchPad({ id, initialScene }: { id: string; initialScene: string | null }) {
  return <SketchPad exerciseId={id} initialScene={initialScene} />;
}
