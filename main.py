import re
import random
import string

# Reflections for pronoun/perspective swapping
Reflections = {
    "i": "you",
    "me": "you",
    "my": "your",
    "mine": "yours",
    "am": "are",
    "you": "I",
    "your": "my",
    "yours": "mine",
    "are": "am",
    "we": "you",
    "us": "you",
    "our": "your",
    "ours": "yours",
    "myself": "yourself",
    "yourself": "myself",
}

def normalize(text: str) -> str:
    """Makes lowercase and removes most punctuation."""
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation.replace("'", "")))
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def reflect(text: str) -> str:
    """Swaps pronouns to reflect perspective."""
    words = text.split()
    reflected_words = [Reflections.get(w, w) for w in words]
    return " ".join(reflected_words)

def substitute_template(template: str, wildcard_text: str) -> str:
    """Replace '*' in the template with reflected wildcard text."""
    if "*" in template:
        return template.replace("*", reflect(wildcard_text))
    return template

# Safety checks for emergencies
SAFETY_PATTERNS = [
    (re.compile(r"\b((can't|cant)\s+breathe|difficulty breathing|not breathing)\b"),
     "That sounds urgent. Please seek emergency medical care right now or call your local emergency number."),
    (re.compile(r"\b(seizure|passed out|unconscious)\b"),
     "That can be urgent. Please contact emergency services or seek immediate medical care."),
    (re.compile(r"\b(chest pain|severe chest|heart racing|palpitations)\b"),
     "If this is happening now or is severe, please contact urgent/emergency medical care immediately."),
    (re.compile(r"\b(overdose|took too much|poison|swallowed pills)\b"),
     "If a child may have taken too much medication, contact Poison Control right away (in the U.S., 1-800-222-1222) or seek emergency care."),
    (re.compile(r"\b(hurt myself|suicidal|kill myself)\b"),
     "I'm really sorry you're dealing with that. If anyone is in danger right now, please call your local emergency number immediately. If you're in the U.S., you can call or text 988 for the Suicide & Crisis Lifeline."),
]

def check_safety(user_text: str) -> str | None:
    """Check for emergency situations."""
    user_text = normalize(user_text)
    for pattern, response in SAFETY_PATTERNS:
        if pattern.search(user_text):
            return response
    return None

# Conversation Rules (pattern, responses)
Rules = [
    # Opening
    (re.compile(r"\b(hello|hi|hey)\b"), [
        "Hi, I can help you if you have any questions or concerns about ADHD medications and management for your child.",
        "Hello, I can help you if you have any questions or concerns about ADHD medications and management for your child.",
        "Hey, I can help you if you have any questions or concerns about ADHD medications and management for your child.",
    ]),

    # ADHD diagnosis/evaluation
    (re.compile(r"\b(diagnosed|diagnosis|evaluation|assessed)\b"), [
        "What did the clinician say during the evaluation, and what questions do you still have?",
        "What symptoms were most important in the evaluation—attention, hyperactivity, impulsivity, or something else?",
    ]),

    # Medication in general (generic + brand names)
    (re.compile(r"\b(medications?|drugs?|medicines?|stimulants?|stims?|methylphenidate|amphetamines?|dextroamphetamine|lisdexamfetamine|nonstimulants?|atomoxetine|guanfacine|clonidine|viloxazine|adderall|ritalin|vyvanse|concerta|focalin|dexedrine|metadate|quillivant|quillchew|jornay|aptensio|daytrana|evekeo|mydayis|intuniv|kapvay|qelbree|strattera)\b"), [
        "What are you hoping medication will help with: school focus, behavior, emotional regulation?",
        "What benefits have you noticed so far, if any? And what side effects are you watching for?",
        "It can help to track timing: when was it taken, when does it seem to help, and when do problems show up. What have you observed?",
    ]),

    # Side effects
    (re.compile(r"\b(appetite|sleep(?:ing)?|mood|tics|not eating|insomnia|irritable|anxious|headache|stomach|nausea)\b"), [
        "That sounds stressful. When did you first notice those effects, and do they line up with when the medication is active?",
        "How often is this happening—daily, a few times a week, or only occasionally?",
        "What have you already tried to support it (like meal timing, bedtime routine, or adjusting the day's structure)?",
    ]),

    # School/IEP/504
    (re.compile(r"\b(teachers?|IEP|504|class(?:room)?|homework|schoolwork|(?<!after\s)school)\b"), [
        "What feedback are you hearing from school, and what do you wish they understood better?",
        "Are supports in place (like a 504 plan or classroom accommodation), or are you still exploring that?",
        "What situations at school trigger the most difficulty—transitions, seatwork, group time, or homework?",
    ]),

    # Behavior strategies/routines
    (re.compile(r"\b(routine|schedule|behavior|tantrum|meltdown|discipline|rewards?|charts?|structure)\b"), [
        "What routines are working even a little, and which parts of the day feel like chaos?",
        "For behavior supports, consistency helps. What's one moment you'd most like to improve this week?",
        "What happens when expectations are very clear and immediate—does your child respond better to short instructions and quick feedback?",
    ]),

    # Parent feelings
    (re.compile(r"\bi\s*(feel|am|'?m)\s+(.+)"), [
        "It makes sense to feel * when you're trying to help your child. What part feels most overwhelming?",
        "When you feel *, what do you most need—information, a plan, or just support?",
        "What would 'better' look like over the next two weeks?"
    ]),

    # Questions for the doctor
    (re.compile(r"\b(doctor|pediatrician|psychiatrist|appointment)\b"), [
        "If you want, we can build a short list of questions for the appointment. What are your top 2 concerns?",
        "What has your clinician suggested so far, and what are your concerns?",
        "It may help to bring a log (sleep, appetite, behavior, school notes).",
    ]),

    # "Because..."
    (re.compile(r"^because (.+)"), [
        "That makes sense. What feels like the biggest driver for you?",
        "That makes sense. When that happens, what do you usually try first?",
    ]),

    # Direct questions: "Should we...?" or "Is it safe...?"
    (re.compile(r"\b(should (we|i)|is it safe|can (i|we))\b"), [
        "I can't make medication decisions because every person is different, but I can help you think of what to ask your child's clinician. What specifically are you considering?",
        "That's a great question for the clinician. What are you worried might happen if you do that?"
    ]),

    # "My child's..." pattern (captures wildcard)
    (re.compile(r"\b(my child|my kid)'s\b(.+)"), [
        "You mentioned your child's *. When does that happen most—mornings, school time, after school, or bedtime?",
        "You mentioned your child's *. How long has this been going on?",
        "You mentioned your child's *. What tends to happen right before it starts?",
    ]),

    # "My child..." pattern (captures wildcard)
    (re.compile(r"\b(my child|my kid)\b(.+)"), [
        "You mentioned your child *. When does that happen most—mornings, school time, after school, or bedtime?",
        "You mentioned your child *. How long has this been going on?",
        "You mentioned your child *. What tends to happen right before it starts?",
    ]),

    # Fallback (matches anything)
    (re.compile(r".+"), [
        "Tell me a little more about that.",
        "What part of this feels most urgent right now?",
        "If you had to pick one, which would it be: focus, behavior, mood, or sleep?",
    ]),
]

Disclaimer = (
    "Quick note: I'm not a clinician. I can help you organize observations and questions, "
    "but medication changes should be decided with your child's prescriber."
)

def respond(user_text: str) -> str:
    """Generate a response based on user input."""
    # Check for safety concerns first
    safety = check_safety(user_text)
    if safety:
        return safety

    text = normalize(user_text)

    # Handle empty input
    if not text:
        return "Please tell me more."

    for pattern, responses in Rules:
        match = pattern.search(text)  # Using search instead of match for flexibility
        if match:
            template = random.choice(responses)
            wildcard = ""

            # Extract a wildcard if it exists
            if match.lastindex and match.lastindex > 1:
                group_content = match.group(match.lastindex)
                if group_content:
                    wildcard = group_content.strip()

            reply = substitute_template(template, wildcard)

            # Add a disclaimer occasionally (10% of the time)
            if random.random() < 0.1:
                reply = f"{reply}\n\n{Disclaimer}"

            return reply

    return "Please tell me more."

def chat():
    """Main chat loop."""
    print("Welcome! I can help with questions about ADHD medications and management.")
    print("To exit, type 'quit', 'exit', or 'bye'.\n")
    print(Disclaimer + "\n")

    while True:
        user = input("You: ").strip()
        if user.lower() in {"quit", "exit", "bye"}:
            print("Bot: Take care. If you want, we can summarize your key questions for the clinician next time.")
            break
        if user:
            print("Bot:", respond(user))

if __name__ == "__main__":
    chat()
