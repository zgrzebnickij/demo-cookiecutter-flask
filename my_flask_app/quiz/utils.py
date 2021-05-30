import requests
import copy
import random
from flask import current_app

def get_questions_from_API():
    res = requests.get('https://opentdb.com/api.php?amount=5')
    if res.status_code == 200:
        questions = res.json()
        for question in questions['results']:
            current_app.logger.info(question)
            question['answers'] = copy.deepcopy(question['incorrect_answers'])
            question['answers'].append(question['correct_answer'])
            random.shuffle(question['answers'])
            del question['incorrect_answers']
        return questions
    res.raise_for_status()