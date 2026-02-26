# e004: Exercise - Control Flow (Collaborative Project)

## Overview

| Attribute | Value |
|-----------|-------|
| **Mode** | Hybrid (Collaborative Pair Programming) |
| **Duration** | 3-4 hours |
| **Prerequisites** | c033-c038 (Control flow, functions), d005 (Control flow demo), All Week 1 content |
| **Deliverable** | A Python quiz game application built collaboratively |

---

## The Thursday Protocol

This is a **Collaborative Project** designed to synthesize the entire week's learning. You will work in pairs using the **Driver/Navigator** pattern:

- **Driver:** Types the code, focuses on syntax and implementation details
- **Navigator:** Reviews each line, thinks about the bigger picture, suggests improvements

**Switch roles every 20-30 minutes!**

---

## Learning Objectives

By completing this exercise, you will:

- Apply conditionals, loops, and functions in a real project
- Practice pair programming techniques
- Synthesize all Week 1 Python concepts
- Work collaboratively to solve problems
- Create a complete, functional application

---

## The Scenario

You're building a **Python Quiz Game** that tests knowledge of programming concepts. The game will:

- Present multiple-choice questions
- Track user score
- Provide feedback on answers
- Display final results with a grade

---

## Setup

### Prerequisites

- Partner assigned (or work solo if necessary)
- Python 3.x installed
- Shared screen or collaborative coding tool (VS Code Live Share, repl.it, etc.)

### Getting Started

1. **Driver 1** creates a new Git repository: `<DevAInitial><DevBInitial>-python-quiz-game`
2. Clone/share the repo with your partner
3. Open `starter_code/quiz_game.py`
4. Decide who starts as Driver

---

## Data Structure

Questions are stored as a list of dictionaries:

```python
questions = [
    {
        "question": "What keyword is used to define a function in Python?",
        "options": ["A) func", "B) def", "C) function", "D) define"],
        "answer": "B",
        "explanation": "The 'def' keyword is used to define functions in Python."
    },
    # More questions...
]
```

---

## Core Tasks

### Task 1: Question Bank (Driver 1, 30 min)

Create a question bank with at least 10 questions covering Week 1 topics:

**Topics to cover:**

- Python syntax and indentation
- Data types (strings, lists, dictionaries)
- Control flow (if/else, loops)
- Functions
- Variables and operators

```python
def create_question_bank():
    """Return a list of quiz questions."""
    questions = [
        {
            "question": "Which of these is NOT a valid Python data type?",
            "options": ["A) int", "B) string", "C) array", "D) dict"],
            "answer": "C",
            "explanation": "Python uses 'list' instead of 'array'. The 'array' module exists but isn't a built-in type."
        },
        # Add 9 more questions...
    ]
    return questions
```

**Switch roles after completing the question bank!**

---

### Task 2: Core Game Functions (Driver 2, 45 min)

Implement these essential functions:

```python
def display_question(question, number):
    """
    Display a question and its options.
    
    Args:
        question: A question dictionary
        number: The question number (1-based)
    """
    pass


def get_user_answer():
    """
    Get and validate user input.
    
    Returns:
        A valid answer (A, B, C, or D) in uppercase
    """
    # Keep asking until valid input
    pass


def check_answer(question, user_answer):
    """
    Check if the user's answer is correct.
    
    Returns:
        True if correct, False otherwise
    """
    pass


def display_feedback(question, user_answer, is_correct):
    """
    Display feedback after each question.
    Show if correct/incorrect and the explanation.
    """
    pass
```

**Switch roles!**

---

### Task 3: Game Loop (Driver 1, 45 min)

Implement the main game logic:

```python
def run_quiz(questions):
    """
    Run the complete quiz game.
    
    Args:
        questions: List of question dictionaries
    
    Returns:
        Tuple of (score, total_questions)
    """
    score = 0
    total = len(questions)
    
    print("=" * 50)
    print("     WELCOME TO THE PYTHON QUIZ GAME!")
    print("=" * 50)
    print(f"\nYou will answer {total} questions.")
    print("Enter A, B, C, or D for each question.\n")
    input("Press Enter to start...")
    
    # TODO: Loop through questions
    # TODO: Display each question
    # TODO: Get user answer
    # TODO: Check answer and update score
    # TODO: Display feedback
    
    return score, total
```

**Switch roles!**

---

### Task 4: Results and Grading (Driver 2, 30 min)

```python
def calculate_grade(score, total):
    """
    Calculate letter grade based on percentage.
    
    90-100%: A
    80-89%:  B
    70-79%:  C
    60-69%:  D
    Below 60%: F
    
    Returns:
        Letter grade as string
    """
    pass


def display_results(score, total):
    """
    Display final results with grade and encouragement.
    
    Output:
    ================================================
              QUIZ COMPLETE!
    ================================================
    Score: 8/10 (80%)
    Grade: B
    
    Great job! Keep practicing!
    ================================================
    """
    pass
```

---

### Task 5: Polish and Enhancement (Both, 30 min)

Work together to add finishing touches:

1. **Input validation** - Handle unexpected input gracefully
2. **Clear screen between questions** (optional)
3. **Timer per question** (stretch goal)
4. **High score tracking** (stretch goal)

---

## Stretch Goals (Optional)

### Shuffle Questions

```python
import random
random.shuffle(questions)
```

### Category Selection

```python
categories = {
    "1": "Python Basics",
    "2": "Data Types",
    "3": "Control Flow"
}
```

### Difficulty Levels

Add a "difficulty" field to questions and let users choose.

---

## Sample Game Flow

```
==================================================
     WELCOME TO THE PYTHON QUIZ GAME!
==================================================

You will answer 10 questions.
Enter A, B, C, or D for each question.

Press Enter to start...

--------------------------------------------------
Question 1 of 10
--------------------------------------------------
What keyword is used to define a function in Python?

A) func
B) def
C) function
D) define

Your answer: B

Correct! The 'def' keyword is used to define functions in Python.

--------------------------------------------------
Question 2 of 10
--------------------------------------------------
...

==================================================
              QUIZ COMPLETE!
==================================================
Score: 8/10 (80%)
Grade: B

Great job! Keep practicing!
==================================================
```

---

## Definition of Done

- [ ] Question bank has at least 10 questions
- [ ] Questions cover multiple Week 1 topics
- [ ] Game runs without errors
- [ ] Input validation prevents crashes
- [ ] Score tracking works correctly
- [ ] Final grade displays properly
- [ ] Code is committed to shared Git repository
- [ ] Both partners contributed (check git log)

---

## Pair Programming Tips

1. **Communicate constantly** - Explain your thinking
2. **No backseat driving** - Navigator suggests, Driver decides
3. **Switch regularly** - Every 20-30 minutes
4. **Take breaks** - Step away if frustrated
5. **Celebrate wins** - Acknowledge when something works!

---

## Submission

1. Push final code to your shared Git repository
2. Include a `CONTRIBUTORS.md` noting who did what
3. Screenshot of a complete game playthrough
4. Both partners submit the repository URL
