import time
import random
import json

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

    def to_dict(self):
        """Convert the Question object to a dictionary."""
        return {
            'id': self.id,
            'text': self.text,
            'difficulty': self.difficulty,
            'topic': self.topic,
            'question_type': self.question_type
        }

    @staticmethod
    def from_dict(data):
        """Create a Question object from a dictionary."""
        return Question(
            id=data['id'],
            text=data['text'],
            difficulty=data['difficulty'],
            topic=data['topic'],
            question_type=data['question_type']
        )

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

    def search_questions(self, difficulties=None, topics=None):
        """Search for questions based on multiple difficulties and/or topics."""
        result = []
        if topics:
            for topic in topics:
                if topic in self.topics:
                    result.extend(self.topics[topic].values())
        else:
            result.extend(self.questions.values())

        if difficulties:
            result = [q for q in result if q.difficulty in difficulties]

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

    def generate_random_question(self, topic=None, difficulty=None):
        """Generate a random question based on optional criteria."""
        filtered_questions = list(self.questions.values())
        if topic:
            filtered_questions = [q for q in filtered_questions if q.topic == topic]
        if difficulty:
            filtered_questions = [q for q in filtered_questions if q.difficulty == difficulty]
        if not filtered_questions:
            return None
        return random.choice(filtered_questions)

    def provide_statistics(self):
        """Provide statistics about the question bank."""
        total_questions = len(self.questions)
        topic_distribution = {topic: len(questions) for topic, questions in self.topics.items()}
        difficulty_distribution = {}
        for question in self.questions.values():
            if question.difficulty not in difficulty_distribution:
                difficulty_distribution[question.difficulty] = 0
            difficulty_distribution[question.difficulty] += 1

        return {
            'total_questions': total_questions,
            'topic_distribution': topic_distribution,
            'difficulty_distribution': difficulty_distribution
        }

    def save_to_file(self, filename):
        """Save the question bank to a file."""
        with open(filename, 'w') as file:
            json.dump({
                'questions': {id: question.to_dict() for id, question in self.questions.items()},
                'topics': {topic: {id: question.to_dict() for id, question in questions.items()} for topic, questions in self.topics.items()}
            }, file, indent=4)
        print(f"Question bank saved to {filename}.")

    def load_from_file(self, filename):
        """Load the question bank from a file."""
        with open(filename, 'r') as file:
            data = json.load(file)
            self.questions = {int(id): Question.from_dict(question) for id, question in data['questions'].items()}
            self.topics = {
                topic: {int(id): Question.from_dict(question) for id, question in questions.items()}
                for topic, questions in data['topics'].items()
            }
        print(f"Question bank loaded from {filename}.")

# Example of usage:
if __name__ == "__main__":
    qb = QuestionBank()
    qb.add_question(1, "What is the capital of the UK?", "Easy", "Geography", "Multiple Choice")
    qb.add_question(2, "Who was the first Prime Minister of the UK?", "Medium", "History", "Multiple Choice")
    qb.display_all_questions()
    print(qb.search_questions(topics=["History"]))
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

    # Random question generator
    random_question = qb.generate_random_question(topic="History")
    if random_question:
        print("Random question:", random_question)
    else:
        print("No question found.")

    # Provide statistics
    stats = qb.provide_statistics()
    print("Statistics:", stats)

    # Save and load question bank
    qb.save_to_file('question_bank.json')
    qb.load_from_file('question_bank.json')

# Print execution time
print("Execution Time:  %s seconds." % (time.time() - start_time))
