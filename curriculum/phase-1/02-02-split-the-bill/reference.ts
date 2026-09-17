// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export type Split = { shareCents: number; peopleWithExtraCent: number };

export function splitBill(totalDollars: number, people: number): Split {
  const totalCents = Math.round(totalDollars * 100);
  return { shareCents: Math.floor(totalCents / people), peopleWithExtraCent: totalCents % people };
}
