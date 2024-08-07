import time
start_time = time.time()

class Question:
    def __init__(self, id, text, difficulty, topic, question_type):
        """Initialise a Question object with id, text, difficulty, topic, and question_type."""
        self.id = id
        self.text = text
        self.difficulty = difficulty
        self.topic = topic
        self.question_type = question_type

    def __repr__(self):
        """Provide a string representation of the Question object."""
        return (f"Question(ID: {self.id}, Text: {self.text}, Difficulty: {self.difficulty}, "
                f"Topic: {self.topic}, Type: {self.question_type})")


class QuestionBank:
    def __init__(self):
        """Initialise a QuestionBank with dictionaries for questions and topics."""
        self.questions = {}  # Dictionary to store questions by their ID
        self.topics = {}     # Nested dictionary to organise questions by topic

    def add_question(self, id, text, difficulty, topic, question_type):
        """Add a new question to the question bank."""
        if id in self.questions:
            print(f"Question with ID {id} already exists.")
            return

        question = Question(id, text, difficulty, topic, question_type)
        self.questions[id] = question

        if topic not in self.topics:
            self.topics[topic] = {}  # Initialise a new dictionary for this topic if it does not exist
        self.topics[topic][id] = question

        print(f"Question {id} added successfully.")

    def update_question(self, id, text=None, difficulty=None, topic=None, question_type=None):
        """Update an existing question in the question bank."""
        if id not in self.questions:
            print(f"Question with ID {id} does not exist.")
            return

        question = self.questions[id]

        if text:
            question.text = text
        if difficulty:
            question.difficulty = difficulty
        if topic and topic != question.topic:
            # Remove question from the old topic
            del self.topics[question.topic][id]
            question.topic = topic
            if topic not in self.topics:
                self.topics[topic] = {}  # Initialise a new dictionary for this topic if it does not exist
            self.topics[topic][id] = question
        if question_type:
            question.question_type = question_type

        print(f"Question {id} updated successfully.")

    def search_questions(self, difficulty=None, topic=None):
        """Search for questions based on difficulty and/or topic."""
        result = []
        if topic:
            if topic in self.topics:
                result.extend(self.topics[topic].values())
        else:
            result.extend(self.questions.values())

        if difficulty:
            result = [q for q in result if q.difficulty == difficulty]

        return result
    
    def search_question_by_id(self, target_id):
        """Perform binary search to find a question by its ID."""
        sorted_ids = sorted(self.questions.keys())  # Sort question IDs
        left, right = 0, len(sorted_ids) - 1
        
        while left <= right:
            mid = (left + right) // 2
            mid_id = sorted_ids[mid]
            
            if mid_id == target_id:
                return self.questions[target_id]
            elif mid_id < target_id:
                left = mid + 1
            else:
                right = mid - 1
        
        return None

    def delete_question(self, id):
        """Delete a question from the question bank."""
        if id not in self.questions:
            print(f"Question with ID {id} does not exist.")
            return

        question = self.questions.pop(id)
        del self.topics[question.topic][id]

        print(f"Question {id} deleted successfully.")

    def display_all_questions(self):
        """Display all questions in the question bank."""
        for id, question in self.questions.items():
            print(f"ID: {id}, Text: {question.text}, Difficulty: {question.difficulty}, Topic: {question.topic}, Type: {question.question_type}")

# Example of add, display, search by topic, update, display all and delete questions:
if __name__ == "__main__":
    qb = QuestionBank()
    qb.add_question(1, "What is the capital of the UK?", "Easy", "Geography", "Multiple Choice")
    qb.add_question(2, "Who was the first Prime Minister of the UK?", "Medium", "History", "Multiple Choice")
    qb.display_all_questions()
    print(qb.search_questions(topic="History"))
    qb.update_question(2, difficulty="Hard")
    qb.display_all_questions()
    qb.delete_question(1)
    qb.display_all_questions()

# Binary search by ID
    found_question = qb.search_question_by_id(2)
    if found_question:
        print("Found question:", found_question)
    else:
        print("Question not found.")


// print("Execution Time:  %s seconds." % (time.time() - start_time))
