# questions.py
# A simple question bank. Each question is a dictionary with:
#   topic       - which data structure this tests
#   difficulty  - "easy", "medium", or "hard"
#   question    - the text shown to the student
#   options     - dict of answer choices
#   answer      - the key of the correct option

QUESTION_BANK = [
    # ---------- Arrays ----------
    {
        "topic": "arrays",
        "difficulty": "easy",
        "question": "What is the time complexity of accessing an element in an array by its index?",
        "options": {"A": "O(1)", "B": "O(n)", "C": "O(log n)", "D": "O(n^2)"},
        "answer": "A",
    },
    {
        "topic": "arrays",
        "difficulty": "medium",
        "question": "Why is inserting an element at the beginning of an array considered slow?",
        "options": {
            "A": "Arrays don't support insertion at all",
            "B": "All existing elements must shift to make room",
            "C": "Arrays automatically sort themselves after insertion",
            "D": "It requires converting the array to a linked list first",
        },
        "answer": "B",
    },
    {
        "topic": "arrays",
        "difficulty": "hard",
        "question": "An array has a fixed size of 10 and is completely full. What must happen to add an 11th element?",
        "options": {
            "A": "Nothing, arrays can always grow freely",
            "B": "The 1st element is automatically deleted",
            "C": "A new, larger array must be created and old elements copied over",
            "D": "The array becomes a hash table",
        },
        "answer": "C",
    },

    # ---------- Linked Lists ----------
    {
        "topic": "linked_lists",
        "difficulty": "easy",
        "question": "What does each node in a singly linked list contain?",
        "options": {
            "A": "Only data, nothing else",
            "B": "Data and a pointer/reference to the next node",
            "C": "Data and pointers to both the next and previous nodes",
            "D": "Only an index number",
        },
        "answer": "B",
    },
    {
        "topic": "linked_lists",
        "difficulty": "medium",
        "question": "Why is inserting at the front of a linked list fast (O(1)), unlike an array?",
        "options": {
            "A": "Linked lists don't actually store data",
            "B": "You just point the new node to the old head, no shifting needed",
            "C": "Linked lists are always sorted automatically",
            "D": "It isn't actually faster than an array",
        },
        "answer": "B",
    },
    {
        "topic": "linked_lists",
        "difficulty": "hard",
        "question": "What is the time complexity of accessing the 5th element in a singly linked list?",
        "options": {"A": "O(1)", "B": "O(log n)", "C": "O(n)", "D": "O(n^2)"},
        "answer": "C",
    },

    # ---------- Stacks ----------
    {
        "topic": "stacks",
        "difficulty": "easy",
        "question": "A stack follows which ordering principle?",
        "options": {
            "A": "FIFO (First In, First Out)",
            "B": "LIFO (Last In, First Out)",
            "C": "Random order",
            "D": "Sorted order",
        },
        "answer": "B",
    },
    {
        "topic": "stacks",
        "difficulty": "medium",
        "question": "Which real-world feature is a classic example of a stack in action?",
        "options": {
            "A": "A line of people waiting for a bus",
            "B": "The 'undo' button in a text editor",
            "C": "A printer queue processing jobs in order",
            "D": "A phone book sorted alphabetically",
        },
        "answer": "B",
    },
    {
        "topic": "stacks",
        "difficulty": "hard",
        "question": "What happens when you call 'pop' on an empty stack?",
        "options": {
            "A": "It returns 0 by default",
            "B": "It causes an error/exception (stack underflow)",
            "C": "It automatically adds a default element first",
            "D": "Nothing happens, the program continues silently",
        },
        "answer": "B",
    },

    # ---------- Queues ----------
    {
        "topic": "queues",
        "difficulty": "easy",
        "question": "A queue follows which ordering principle?",
        "options": {
            "A": "FIFO (First In, First Out)",
            "B": "LIFO (Last In, First Out)",
            "C": "Random order",
            "D": "Reverse insertion order",
        },
        "answer": "A",
    },
    {
        "topic": "queues",
        "difficulty": "medium",
        "question": "Which real-world scenario best matches how a queue behaves?",
        "options": {
            "A": "A stack of plates, taking from the top",
            "B": "People lining up at a ticket counter",
            "C": "Undoing your last action in an app",
            "D": "Browser back-button history",
        },
        "answer": "B",
    },
    {
        "topic": "queues",
        "difficulty": "hard",
        "question": "In a queue, which two operations are used to add and remove elements?",
        "options": {
            "A": "push and pop",
            "B": "enqueue and dequeue",
            "C": "insert and delete",
            "D": "add and subtract",
        },
        "answer": "B",
    },
]
