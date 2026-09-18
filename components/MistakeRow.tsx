"use client";
import { useState, useTransition } from "react";
import { editMistake, removeMistake } from "@/app/actions";

export function MistakeRow({ id, text, count, source }: { id: number; text: string; count: number; source: string }) {
  const [editing, setEditing] = useState(false);
  const [value, setValue] = useState(text);
  const [pending, start] = useTransition();

  return (
    <li className="grid gap-1 rounded-md border border-line p-3">
      {editing ? (
        <form
          onSubmit={(e) => { e.preventDefault(); start(async () => { await editMistake(id, value); setEditing(false); }); }}
          className="flex gap-2"
        >
          <label htmlFor={`mistake-${id}`} className="sr-only">Mistake text</label>
          <input id={`mistake-${id}`} value={value} onChange={(e) => setValue(e.target.value)} className="field flex-1" autoFocus />
          <button type="submit" disabled={pending} className="btn btn-primary">Save</button>
          <button type="button" onClick={() => { setValue(text); setEditing(false); }} className="btn">Cancel</button>
        </form>
      ) : (
        <p className="text-[15px]">{text}</p>
      )}
      <div className="flex items-center gap-3 text-xs text-muted">
        <span className="chip bg-warn-soft text-warn">{count}×</span>
        <span>from {source}</span>
        {!editing && (
          <span className="ml-auto flex gap-3">
            <button onClick={() => setEditing(true)} className="font-semibold hover:text-ink">Edit</button>
            <button onClick={() => start(() => removeMistake(id))} disabled={pending} className="font-semibold hover:text-bad">Fixed — remove</button>
          </span>
        )}
      </div>
    </li>
  );
}
