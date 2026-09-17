"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

export function NavLink({ href, children, match }: { href: string; children: React.ReactNode; match?: string }) {
  const path = usePathname();
  const active = href === "/" ? path === "/" : path.startsWith(match ?? href);
  return (
    <Link
      href={href}
      aria-current={active ? "page" : undefined}
      className={`rounded-md px-3 py-2 text-sm font-semibold transition-colors ${active ? "bg-accent-soft text-accent" : "text-muted hover:bg-ground hover:text-ink"}`}
    >
      {children}
    </Link>
  );
}

export function TopicLink({ href, children, className }: { href: string; children: React.ReactNode; className: string }) {
  const path = usePathname();
  const active = path === href;
  return (
    <Link href={href} aria-current={active ? "page" : undefined} className={`${className} ${active ? "bg-ground" : "hover:bg-ground"}`}>
      {children}
    </Link>
  );
}
