import { connection } from "next/server";
import { getSetting } from "@/lib/db.ts";
import { settingsDefaults } from "@/lib/llm.ts";
import { LANGUAGES, LANGUAGE_IDS } from "@/lib/languages.ts";
import { saveSettings } from "@/app/actions.ts";

export default async function SettingsPage() {
  await connection();
  const value = (k: keyof typeof settingsDefaults) => getSetting(k, settingsDefaults[k]);
  const mode = value("providerMode");

  return (
    <main className="grid content-start gap-6 px-6 py-8 xl:px-10">
      <header className="grid gap-1">
        <p className="eyebrow">Settings</p>
        <h1 className="font-display text-4xl font-bold">Models and backups</h1>
      </header>

      <div className="grid items-start gap-6 xl:grid-cols-[minmax(0,3fr)_minmax(0,2fr)]">
        <form action={saveSettings} className="panel grid gap-6 p-6">
          <fieldset className="grid gap-3">
            <legend className="mb-3 font-display text-lg font-semibold">Which model teaches</legend>
            <div className="grid gap-3 md:grid-cols-3">
              {[
                ["auto", "Claude, then local", "Uses your Pro login through Claude Code. If Claude fails (for example the Pro usage limit), switches to Ollama."],
                ["claude", "Claude only", "Shows an error instead of switching."],
                ["ollama", "Local only", "Free and offline, but weaker at code review and follow-up questions."],
              ].map(([v, label, help]) => (
                <label key={v} className="grid content-start gap-1 rounded-md border border-line p-4 has-[:checked]:border-accent has-[:checked]:bg-accent-soft">
                  <span className="flex items-center gap-2 font-semibold">
                    <input type="radio" name="providerMode" id={`mode-${v}`} value={v} defaultChecked={mode === v} className="accent-[var(--accent)]" />
                    {label}
                  </span>
                  <span className="text-sm text-muted">{help}</span>
                </label>
              ))}
            </div>
          </fieldset>
          <fieldset className="grid gap-2">
            <legend className="mb-1 font-display text-lg font-semibold">Exercise language</legend>
            <select id="language" name="language" defaultValue={value("language")} className="field max-w-xs">
              {LANGUAGE_IDS.map((l) => <option key={l} value={l}>{LANGUAGES[l].label}</option>)}
            </select>
            <p className="text-sm text-muted">Python needs <code className="font-mono">python</code> and Java needs <code className="font-mono">javac</code>/<code className="font-mono">java</code> on your PATH (both are installed). Topics 1.9 and 1.11 teach TypeScript's type system; in other languages they use that language's nearest equivalent. You can also change this on any exercise page.</p>
          </fieldset>
          <div className="grid gap-4 md:grid-cols-3">
            <Field id="claudeModel" label="Claude model" help="An alias like sonnet or opus, or a full model name." defaultValue={value("claudeModel")} />
            <Field id="ollamaModel" label="Ollama model" help="Must already be pulled in Ollama." defaultValue={value("ollamaModel")} />
            <Field id="ollamaUrl" label="Ollama address" help="Only addresses on this computer are accepted." defaultValue={value("ollamaUrl")} />
          </div>
          <button type="submit" className="btn btn-primary justify-self-start">Save settings</button>
        </form>

        <section className="panel grid gap-3 p-6">
          <h2 className="font-display text-lg font-semibold">Back up your progress</h2>
          <p className="text-sm text-muted">
            Everything (progress, Spaced Reviews, conversations) lives in <code className="font-mono">data/poopy.db</code> on this computer only.
            Nothing backs it up automatically. Download a copy and keep it somewhere safe.
          </p>
          <a href="/api/export" className="btn justify-self-start">Export backup (JSON)</a>
        </section>
      </div>
    </main>
  );
}

function Field({ id, label, help, defaultValue }: { id: string; label: string; help: string; defaultValue: string }) {
  return (
    <div className="grid content-start gap-1">
      <label htmlFor={id} className="text-sm font-semibold">{label}</label>
      <input id={id} name={id} defaultValue={defaultValue} className="field font-mono text-sm" />
      <span className="text-xs text-muted">{help}</span>
    </div>
  );
}
