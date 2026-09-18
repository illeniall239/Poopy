// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
export type Direction = "up" | "down" | "left" | "right";

export type Command =
  | { type: "move"; direction: Direction; steps: number }
  | { type: "say"; message: string }
  | { type: "quit" };

export type ParseError = { type: "error"; message: string };

function error(message: string): ParseError {
  return { type: "error", message };
}

function toDirection(word: string): Direction | undefined {
  const lower = word.toLowerCase();
  if (lower === "up" || lower === "down" || lower === "left" || lower === "right") return lower;
  return undefined;
}

function toSteps(word: string): number | undefined {
  for (const ch of word) {
    if (ch < "0" || ch > "9") return undefined;
  }
  const steps = Number(word);
  return steps >= 1 ? steps : undefined;
}

export function parseCommand(input: string): Command | ParseError {
  const words: string[] = [];
  for (const part of input.split(" ")) {
    if (part !== "") words.push(part);
  }
  if (words.length === 0) return error("Empty command");

  const name = words[0].toLowerCase();
  if (name === "quit") {
    return words.length === 1 ? { type: "quit" } : error("quit takes no arguments");
  }
  if (name === "say") {
    if (words.length < 2) return error("say needs a message");
    return { type: "say", message: words.slice(1).join(" ") };
  }
  if (name === "move") {
    if (words.length !== 3) return error("Usage: move <direction> <steps>");
    const direction = toDirection(words[1]);
    if (direction === undefined) return error(`Unknown direction "${words[1]}"`);
    const steps = toSteps(words[2]);
    if (steps === undefined) return error(`Steps must be a whole number of at least 1, got "${words[2]}"`);
    return { type: "move", direction, steps };
  }
  return error(`Unknown command "${words[0]}"`);
}
