# ADHD Support Chatbot (ELIZA-Style)

A command-line chatbot built in Python that provides supportive, non-clinical guidance for parents and guardians with questions about ADHD medications and day-to-day management.

This project uses classic ELIZA-style pattern matching with topic-aware prompts, pronoun reflection, and safety-focused messaging.

## Why This Project

This demonstrates practical NLP fundamentals without external frameworks:
- Regex-driven intent matching
- Rule-based dialogue design
- Pronoun/perspective reflection
- Safety-first response handling
- Randomized template responses for more natural conversation

## Features

- Topic-based response rules for ADHD diagnosis, medications, side effects, school support, and routines
- Pronoun reflection to make responses feel conversational
- Emergency keyword detection with urgent-care guidance
- Periodic non-clinical disclaimer reminders
- Clean command-line chat loop with exit commands

## Safety Scope

This chatbot is informational and supportive only.
- It does not provide diagnosis or treatment decisions
- It does not replace a licensed clinician
- In urgent or dangerous situations, it directs users to emergency resources

## Tech Stack

- Python 3.10+
- Standard library only (`re`, `random`, `string`)

## Run Locally

```bash
python main.py
```

Type `quit`, `exit`, or `bye` to end the chat.

## Example Interaction

```text
You: My child isn't eating lunch after taking medication.
Bot: That sounds stressful. When did you first notice those effects, and do they line up with when the medication is active?
```

## Project Structure

- `main.py`: Chatbot logic, safety checks, rules, and chat loop
- `README.md`: Project overview and usage instructions

## Improvement Ideas

- Add unit tests for `normalize`, `reflect`, and `respond`
- Move rules to a data file for easier maintenance
- Add structured conversation logging for analysis
- Expand safety patterns and localization

## Author

Bradley Mendel
