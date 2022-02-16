#Wordle clone made by lightflix

from flask import Flask, request, render_template, session, redirect, url_for
import re
import random
import uuid
import datetime

app = Flask(__name__)
app.secret_key = "m1lktrUckjUsT4rr1v"
app.permanent_session_lifetime = datetime.timedelta(days=365)

@app.errorhandler(405)
def method_not_allowed(e):
    return render_template("wordleui.html", round_list=session['guess_list'], state=session['state'], status=0)

#open guess list 
with open("guess_list.txt","r") as feed:
    allowed_guesses = feed.read().splitlines()

#open answer list 
with open("answer_list.txt","r") as feed:
    answer_list = feed.read().splitlines()

def checkValidity(word):
    if word in allowed_guesses:
        # print("ITS IS A REAL WORD")
        return True
    return False

def getMatchScores(guess, answer):

    round_score = []

    guess_dissect = list(guess)
    answer_dissect = list(answer.rstrip())

    # print("guess dissect is: ",guess_dissect," and answer dissect is: ",answer_dissect)
 
    for guess_char, answer_char in zip(guess_dissect, answer_dissect):
        # print("inside the compare loop")
        if guess_char == answer_char:
        #score is 2
            round_score.append((guess_char,2))

        elif guess_char in answer_dissect:
        #score is 1
            round_score.append((guess_char,1))

        else:
        #score is 0
            round_score.append((guess_char,0))
    
    #return list of tuples containing score values for each letter
    return round_score


@app.route('/')
def begin():

    try:
        gameover = session['gameover']
    except:

        session['id'] = str(uuid.uuid4())[:10]
        session['state'] = 0
        session['guess_list'] = []
        session['guess_list_raw'] = []
        session['answer'] = random.choice(answer_list)
        print("INFO: "+session['id']+" started new game, Word: "+session['answer'])
        session['gameover'] = False
        return render_template("wordleui.html", state=session['state'], status=0)

    else:
        if not gameover:
            print("INFO: "+session['id']+" tried to start over without finishing, Word: "+session['answer'])
            return render_template("wordleui.html", round_list=session['guess_list'], state=session['state'],status=0)

    session['state'] = 0
    session['guess_list'] = []
    session['guess_list_raw'] = []
    session['answer'] = random.choice(answer_list)
    print("INFO: "+session['id']+" started new game, Word: "+session['answer']) 
    session['gameover'] = False
    return render_template("wordleui.html", state=session['state'], status=0)


@app.route('/guess', methods=['POST'])
def guess():

    if(session['state'] >= 0 and session['state'] <= 5 and not session['gameover']):

        #if state within bounds
        try:
            guess = request.form.get("guess").lower()
            
        except Exception as e:
            
            print("Bad input received - resetting")
            return redirect(url_for('/'))

        # print("Guess is "+guess)

        print("INFO: "+session['id']+" made guess: "+str(guess.encode("utf8","ignore")), "Answer: "+session['answer'])

        
        if not (re.match("^[a-z]*$", guess) and checkValidity(guess) and guess not in session['guess_list_raw']):
            #if input is bad

            #INSERT BETTER CODE HERE. THIS CLEARS THE WHOLE STATE.
            return render_template("wordleui.html", round_list=session['guess_list'], state=session['state'], status=0, invalid=1)

        else:
            session['guess_list_raw'].append(guess)
            session['guess_list'].append(getMatchScores(guess, session['answer']))
            session['state'] += 1
            
            print("INFO: "+session['id']+", State: "+str(session['state'])+" Game over: "+str(session['gameover']))

            if guess == session['answer']:
                session['gameover'] = True

                return render_template("wordleui.html", round_list=session['guess_list'], status=1)


            if(session['state'] >= 6):
                session['gameover'] = True
                return render_template("wordleui.html", round_list=session['guess_list'], state=session['state'], answer=session['answer'], status=0)

            return render_template("wordleui.html", round_list=session['guess_list'], state=session['state'],status=0)
    else:

        session['gameover'] = True
        session['state'] = 6
        return render_template("wordleui.html", round_list=session['guess_list'], state=session['state'], answer=session['answer'], status=0)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)