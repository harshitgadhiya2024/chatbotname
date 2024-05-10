from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
from flask_cors import CORS
import json
import os, requests
import google.generativeai as genai

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = "bhjdbgsjfmbsfjk"
secure_type = 'http'

genai.configure(api_key="AIzaSyDcZfwycmbQwUY5XaAJQueDHD7gua_0_qU")

def write_to_file(data, filename):
  """Writes a multiline string to a file.

  Args:
    data: The multiline string to write to the file.
    filename: The name of the file to write to.
  """
  with open(filename, 'w', encoding="utf-8") as f:
    f.write(data)


def get_gemini_text_response(prompt):
    try:
        model = genai.GenerativeModel('models/gemini-1.0-pro-latest')
        response = model.generate_content(prompt)
        response.resolve()
        response_text = response.text
        print(f"response fetched successfully with only prompt....")
        return response_text

    except Exception as e:
        print(f"Error in get_gemini_text_response: {e}")


@app.route('/convert_data_minify', methods=["POST", "GET"])
def convert_data_minify():
    try:
        if request.method=="POST":
            data = json.loads(request.data)
            input_code_text = data.get("row_data", "")
            response = requests.post('https://www.toptal.com/developers/javascript-minifier/api/raw', data=dict(input=input_code_text)).text

            filename = "chatbot.min.js"
            write_to_file(response, filename)

            return send_file(filename, as_attachment=True)
        else:
            return {"status": 401, "message": "Methods not allowed.."}

    except Exception as e:
        print(e)

@app.route('/get_answer', methods=["POST", "GET"])
def get_answer():
    try:
        if request.method=="POST":
            data = json.loads(request.data)
            content = data.get("content", "")
            question = data.get("question", "")
            prompt = f'Please provide a human-like answer based on the given content. Please note when question answer not provide in given content then only provide simple contact us response, without mentioning that you are an AI or an agent. Keep the answer concise, like a response from a chatbot and please Note when question as give me list then provide answer as like list. content="{content}" and question="{question}"'
            response = get_gemini_text_response(prompt)
            return {"response": response}
        else:
            return {"status": 401, "message": "Methods not allowed.."}

    except Exception as e:
        print(e)


if __name__=="__main__":
    app.run()
