import spacy
import random

def get_questions(paragraph: str):

    def generate_mcq_questions(question, correct_answers, other_options, num_options=3):
        options = correct_answers + other_options
        random.shuffle(options)
        mcq = {"question": question, "options": options, "correct_answers": correct_answers}
        return mcq

    def generate_random_question():
        sentence = random.choice(list(doc.sents))
        options = random.choice([token for token in sentence if not token.is_punct])
        question_text = sentence.text.replace(options.text, "*________*")
        correct_answers = [options.text]
        other_options = [token.text for token in doc if token.is_alpha and token.text != correct_answers[0]]
        num_correct_options = random.randint(1, 2)
        correct_answers.extend(random.sample(other_options, num_correct_options))
        num_other_options = min(3 - num_correct_options, len(other_options))
        other_options = random.sample(other_options, num_other_options)
        mcq = generate_mcq_questions(question_text, correct_answers, other_options)
        return mcq

    doc = nlp(paragraph)
    questions = [generate_random_question() for _ in range(5)]
    mca_questions = []
    for i, question in enumerate(questions, start=1):
        question_str = f"Q{i}: {question['question']}\n"
        options_str = ""
        for j, option in enumerate(question['options']):
            options_str += f"{chr(96+j+1)}. {option}\n"
        correct_options_formatted = " & ".join([f"({chr(97+question['options'].index(ans))})" for ans in question['correct_answers']])
        correct_options_str = f"Correct Options: {correct_options_formatted}"
        mca_question = f"{question_str}{options_str}{correct_options_str}\n"
        mca_questions.append(mca_question)
    return mca_questions

nlp = spacy.load("en_core_web_sm")
paragraph = input("Enter the Content of Paragraph: \n")
mca_questions = get_questions(paragraph)
print("\n")
for question in mca_questions:
    print(question)