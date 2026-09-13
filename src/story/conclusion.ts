import { byYear, occupancy } from "../data/model";

/**
 * The story's closing summary: shown in the last chapter and read as the final
 * narration step. It states the measured change, then leaves the explanations
 * open. Figures come from the data; each reported detail is an approved claim
 * (Cranston Inquiry evidence on boat length, NCA seizures of 8 m boats used for
 * 50–60 people, the reported Portsmouth crossing).
 */
export function conclusion() {
  const first = Math.round(occupancy(byYear(2018)));
  const latest = Math.round(occupancy(byYear(2025)));
  return {
    known: `Each arriving boat now carries far more people: about ${first} in 2018 and about ${latest} in 2025.`,
    openQuestions:
      "Is that bigger boats, fuller boats, or both? Reports describe boats of 8 to 10 metres, and boats of about 8 metres carrying 50 to 60 people. Could boats go further, or leave from new places? One longer crossing, to Portsmouth, has been reported, but it is too soon to say whether it is part of a pattern.",
    invitation:
      "Change the assumptions in the scenarios, and check each figure against its source.",
    question: "What if boat numbers, occupancy or launch areas changed?",
  };
}
