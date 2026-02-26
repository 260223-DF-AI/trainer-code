# quiz_game.py - Python Quiz Game
# Starter code for e004-exercise-control-flow (Collaborative Project)

"""
Python Quiz Game
----------------
A multiple-choice quiz game that tests Python knowledge.

This is a collaborative project - use pair programming!
- Driver: Types the code
- Navigator: Reviews and guides

Switch roles every 20-30 minutes!
"""

# =============================================================================
# TODO: Task 1 - Question Bank (Driver 1)
# =============================================================================

def create_question_bank():
    """
    Return a list of quiz questions.
    
    Each question is a dictionary with:
    - question: The question text
    - options: List of 4 options (A, B, C, D)
    - answer: Correct answer letter
    - explanation: Why this answer is correct
    
    Add at least 10 questions covering Week 1 topics.
    """
    questions = [
        {
            "question": "What keyword is used to define a function in Python?",
            "options": ["A) func", "B) def", "C) function", "D) define"],
            "answer": "B",
            "explanation": "The 'def' keyword is used to define functions in Python."
        },
        # TODO: Add 9 more questions covering:
        # - Python syntax and indentation
        # - Data types (strings, lists, dictionaries)
        # - Control flow (if/else, loops)
        # - Functions and parameters
        # - Variables and operators
    ]
    return questions


# =============================================================================
# TODO: Task 2 - Core Game Functions (Driver 2)
# =============================================================================

def display_question(question, number, total):
    """
    Display a question and its options.
    
    Args:
        question: A question dictionary
        number: The current question number (1-based)
        total: Total number of questions
    
    Output format:
    --------------------------------------------------
    Question 1 of 10
    --------------------------------------------------
    [question text]
    
    A) option A
    B) option B
    C) option C
    D) option D
    """
    # TODO: Implement this function
    pass


def get_user_answer():
    """
    Get and validate user input.
    
    Keep prompting until the user enters a valid answer (A, B, C, or D).
    Accept both uppercase and lowercase input.
    
    Returns:
        A valid answer in uppercase (A, B, C, or D)
    """
    # TODO: Implement input validation loop
    pass


def check_answer(question, user_answer):
    """
    Check if the user's answer is correct.
    
    Args:
        question: The question dictionary
        user_answer: The user's answer (uppercase letter)
    
    Returns:
        True if correct, False otherwise
    """
    # TODO: Compare user_answer with question["answer"]
    pass


def display_feedback(question, user_answer, is_correct):
    """
    Display feedback after answering a question.
    
    If correct: Print "Correct!" with green styling (or just text)
    If incorrect: Print "Incorrect. The answer was X."
    Always show the explanation.
    """
    # TODO: Display appropriate feedback based on is_correct
    pass


# =============================================================================
# TODO: Task 3 - Game Loop (Driver 1)
# =============================================================================

def run_quiz(questions):
    """
    Run the complete quiz game.
    
    1. Display welcome message
    2. Loop through all questions
    3. For each question:
       - Display the question
       - Get user answer
       - Check if correct
       - Display feedback
       - Update score
    4. Return final score
    
    Args:
        questions: List of question dictionaries
    
    Returns:
        Tuple of (score, total_questions)
    """
    score = 0
    total = len(questions)
    
    # Welcome message
    print("=" * 50)
    print("     WELCOME TO THE PYTHON QUIZ GAME!")
    print("=" * 50)
    print(f"\nYou will answer {total} questions.")
    print("Enter A, B, C, or D for each question.\n")
    input("Press Enter to start...")
    
    # TODO: Implement the game loop
    # Hint: Use a for loop with enumerate
    
    return score, total


# =============================================================================
# TODO: Task 4 - Results and Grading (Driver 2)
# =============================================================================

def calculate_grade(score, total):
    """
    Calculate letter grade based on percentage.
    
    Grading scale:
    - 90-100%: A
    - 80-89%:  B
    - 70-79%:  C
    - 60-69%:  D
    - Below 60%: F
    
    Args:
        score: Number of correct answers
        total: Total number of questions
    
    Returns:
        Letter grade as string
    """
    # TODO: Calculate percentage and return grade
    pass


def display_results(score, total):
    """
    Display final results with grade and encouragement.
    
    Include:
    - Score (e.g., 8/10)
    - Percentage
    - Letter grade
    - Encouraging message based on performance
    """
    # TODO: Calculate percentage and grade
    # TODO: Display formatted results
    # TODO: Add encouragement message
    pass


# =============================================================================
# Main Program
# =============================================================================

def main():
    """Main entry point for the quiz game."""
    # Create question bank
    questions = create_question_bank()
    
    # Run the quiz
    score, total = run_quiz(questions)
    
    # Display results
    display_results(score, total)
    
    # Ask to play again
    play_again = input("\nWould you like to play again? (yes/no): ")
    if play_again.lower() in ["yes", "y"]:
        main()
    else:
        print("\nThanks for playing! Goodbye!")


if __name__ == "__main__":
    main()
