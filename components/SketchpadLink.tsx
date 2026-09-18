"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

// On an exercise page, opens that exercise's sketchpad (Workspace listens for this event);
// anywhere else, goes to the general sketchpad page.
export const OPEN_SKETCHPAD = "poopy:open-sketchpad";

export function SketchpadLink({ compact = false }: { compact?: boolean }) {
  const path = usePathname();
  const onExercise = path.startsWith("/exercises/");
  const active = path === "/sketchpad";
  const className = compact
    ? "grid size-9 place-items-center rounded-md font-mono text-xs font-bold text-muted hover:bg-ground hover:text-ink"
    : `rounded-md px-3 py-2 text-left text-sm font-semibold transition-colors ${active ? "bg-accent-soft text-accent" : "text-muted hover:bg-ground hover:text-ink"}`;
  const label = compact ? "Sk" : "Sketchpad";

  if (onExercise) {
    return (
      <button type="button" onClick={() => window.dispatchEvent(new Event(OPEN_SKETCHPAD))} className={className} title="Sketch this exercise">
        {label}
      </button>
    );
  }
  return (
    <Link href="/sketchpad" aria-current={active ? "page" : undefined} className={className} title="Sketchpad">
      {label}
    </Link>
  );
}
