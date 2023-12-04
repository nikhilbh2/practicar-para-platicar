from flask import Flask, request, render_template, jsonify
import random
from sentences import tense_sentences

app = Flask(__name__)

def generate_sentences(selected_tenses):
    combined_sentence = []
    for tense in selected_tenses:
        if tense in tense_sentences:
            sentence = random.choice(tense_sentences[tense])['sentence']
            combined_sentence.append(sentence)
    return " ".join(combined_sentence)

@app.route('/')
def index():
    selected_tenses = request.args.getlist('tenses')  # Get selected tenses as a list
    if not selected_tenses:
        selected_tenses = ['present']  # Default to 'present' tense if none selected
    sentence = generate_sentences(selected_tenses)

    # Return the HTML page for regular page loads
    return render_template('index.html', sentence=sentence)


@app.route('/generate_sentence', methods=['POST'])
def generate_sentence():
    selected_tenses = request.form.getlist('tenses')
    if not selected_tenses:
        print("got here")
        return jsonify({"sentence": "Please select at least one tense"})

    # Randomly select one tense from the list of selected tenses
    random_tense = random.choice(selected_tenses)

    # Retrieve a sentence based on the randomly selected tense
    sentences_for_tense = tense_sentences.get(random_tense, [])
    if not sentences_for_tense:
        return jsonify({"sentence": "No sentences available for the selected tense."})

    # Randomly select a sentence for the selected tense
    random_sentence = random.choice(sentences_for_tense)
    sentence = random_sentence.get("sentence", "")

    print(sentence)

    return jsonify({"sentence": sentence})

@app.route('/check_translation', methods=['POST'])
def check_translation():

    user_translation = request.form.get('user_translation')
    print(user_translation)

    sentence = request.form.get('sentence')

    print(sentence)

    print(request.form.get('tense'))

    user_sentence = sentence.strip().lower()  # Clean and normalize user-submitted sentence
    correct_translation = next((s['translation'] for s in tense_sentences[request.form.get('tense')] if user_sentence == s['sentence'].strip().lower()), None)


    if user_translation == correct_translation:
        result = "Correct!"
    else:
        result = "Incorrect. The correct translation is: " + correct_translation

    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)


