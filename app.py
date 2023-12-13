
from flask import Flask, render_template, request
import requests
from datetime import datetime

from constants import QUESTIONS_AND_ANSWERS, ANSWERS_NLU_API_URL




app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_answer = request.form['answer']
        current_question_num = int(request.form['question'])


        if user_answer.lower() == 'stop':
            return render_template('result.html', message="You've chosen to stop. Thank you for submitting answers")


        result = get_response_from_nlu(user_answer, current_question_num)
       

        if result == "out_of_scope":
            result = "Applogies, we did not understan your response, please answer again"
            return render_template('questions.html', question=QUESTIONS_AND_ANSWERS[current_question_num]["question"],
                                   next_question=current_question_num, result=result)


        next_question_num = current_question_num + 1
        if next_question_num >= len(QUESTIONS_AND_ANSWERS):
            return render_template('result.html', message="Congratulations! You've completed all questions.")
        else:
            return render_template('questions.html', question=QUESTIONS_AND_ANSWERS[next_question_num]["question"],
                                   next_question=next_question_num, result=result)

    return render_template('questions.html', question=QUESTIONS_AND_ANSWERS[0]["question"], next_question=0, result=None)



def get_response_from_nlu(user_answer, current_question_num):
    payload = {
            "message_data": {
                "author_id": "27833335555",
                "author_type": "OWNER",
                "contact_uuid": "e331dc93-1b9a-4db4-ad58-315d1c95f243",
                "message_direction": "inbound",
                "message_id": "ABGGJ4MzZWFfAgs-sCaxu0X72jwgbg",
                "message_body": user_answer,
                "question": QUESTIONS_AND_ANSWERS[current_question_num]["question"],
                "expected_answer": QUESTIONS_AND_ANSWERS[current_question_num]["expected_answer"],
                "message_inserted_at": datetime.now().isoformat(),
                "message_updated_at": datetime.now().isoformat()
            }
    }
    response = requests.post(ANSWERS_NLU_API_URL, json=payload)

    result = response.json().get("type", "")

    return result





if __name__ == '__main__':
    app.run(debug=True)