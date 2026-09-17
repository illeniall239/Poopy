export type Direction = "up" | "down" | "left" | "right";

export type Command =
  | { type: "move"; direction: Direction; steps: number }
  | { type: "say"; message: string }
  | { type: "quit" };

export type ParseError = { type: "error"; message: string };

export function parseCommand(input: string): Command | ParseError {
  throw new Error("Not implemented");
}
