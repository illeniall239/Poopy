"use client";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

// Remembers the choice in a cookie so the server renders the right width on the next load (no flicker).
export function SidebarToggle({ collapsed }: { collapsed: boolean }) {
  const router = useRouter();

  function toggle() {
    document.cookie = `sidebar=${collapsed ? "open" : "collapsed"}; path=/; max-age=31536000; samesite=lax`;
    router.refresh();
  }

  useEffect(() => {
    // Ctrl+B (or Cmd+B) toggles, like most editors.
    const onKey = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "b" && !(e.target as HTMLElement).closest(".monaco-editor")) {
        e.preventDefault();
        toggle();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  });

  return (
    <button
      onClick={toggle}
      aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
      aria-expanded={!collapsed}
      title={`${collapsed ? "Expand" : "Collapse"} sidebar (Ctrl+B)`}
      className="hidden size-9 shrink-0 place-items-center rounded-md text-muted transition-colors hover:bg-ground hover:text-ink lg:grid"
    >
      <svg width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden>
        <rect x="2" y="3" width="14" height="12" rx="2" stroke="currentColor" strokeWidth="1.5" />
        <path d="M7 3v12" stroke="currentColor" strokeWidth="1.5" />
        <path d={collapsed ? "M10.5 7.5 12 9l-1.5 1.5" : "M12 7.5 10.5 9 12 10.5"} stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    </button>
  );
}
