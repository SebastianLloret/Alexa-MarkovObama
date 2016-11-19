import requests

def build_speechlet_response(title, output, should_end_session):
    return {
        'version': "1.0",
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': output
            }
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': "I'm sorry, I didn't catch that."
            }
        },
        'shouldEndSession': should_end_session
    }

def lambda_handler(event, context):
    if event["request"]["intent"]["name"] == "GetMarkovIntent":
        if "value" not in event["request"]["intent"]["slots"]["issue"]:
            markov = requests.get('http://talk-to-obama.herokuapp.com/chat')
            markovDictionary = markov.json()
            response = markovDictionary["content"]
            return build_speechlet_response("", response, True)
        else:
            markov = requests.get('http://talk-to-obama.herokuapp.com/chat?issue=' + event["request"]["intent"]["slots"]["issue"]["value"])
            markovDictionary = markov.json()
            response = markovDictionary["prefacingText"] + markovDictionary["content"]
            return build_speechlet_response("", response, True)
