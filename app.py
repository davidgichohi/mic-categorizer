from flask import Flask, render_template_string, request

app = Flask(__name__)

# Updated rules using inclusive range logic save in JSON file
rules_dict = {
    'Amikacin': [
        {'min': 0.0, 'max': 16.0, 'category': 'Susceptible'},
        {'min': 16.1, 'max': 63.9, 'category': 'Intermediate'},
        {'min': 64.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Ciprofloxacin': [
        {'min': 0.0, 'max': 1.0, 'category': 'Susceptible'},
        {'min': 1.1, 'max': 3.9, 'category': 'Intermediate'},
        {'min': 4.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Meropenem': [
        {'min': 0.0, 'max': 4.0, 'category': 'Susceptible'},
        {'min': 4.1, 'max': 15.9, 'category': 'Intermediate'},
        {'min': 14.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Ceftriaxone': [
        {'min': 0.0, 'max': 8.0, 'category': 'Susceptible'},
        {'min': 16.0, 'max': 32.0, 'category': 'Intermediate'},
        {'min': 64, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Ampicillin': [
        {'min': 0.0, 'max': 0.5, 'category': 'Susceptible'},
        {'min': 0.6, 'max': 1.9, 'category': 'Intermediate'},
        {'min': 2.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Meropenem vaborbactam': [
        {'min': 0.0, 'max': 2.0, 'category': 'Susceptible'},
        {'min': 2.1, 'max': 7.9, 'category': 'Intermediate'},
        {'min': 8.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Cefpodoxime': [
        {'min': 0.0, 'max': 2.0, 'category': 'Susceptible'},
        {'min': 2.1, 'max': 7.9, 'category': 'Intermediate'},
        {'min': 8.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Ceftibuten': [
        {'min': 0.0, 'max': 8.0, 'category': 'Susceptible'},
        {'min': 8.1, 'max': 31.9, 'category': 'Intermediate'},
        {'min': 32.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Ceftibuten avibactam': [
        {'min': 0.0, 'max': 9999.9, 'category': 'Unknown'}
    ],
    'Tebipenem': [
        {'min': 0.0, 'max': 9999.9, 'category': 'Unknown'},
    ],
    'Ticarcillin-Clavulanate': [
        {'min': 0.0, 'max': 8.0, 'category': 'Susceptible'},
        {'min': 8.1, 'max': 32.9, 'category': 'Intermediate'},
        {'min': 64.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Cefiderecol': [
        {'min': 0.0, 'max': 1.0, 'category': 'Susceptible'},
        {'min': 1.1, 'max': 9999.9, 'category': 'Unknown'}
    ],
    'Chloramphenicol': [
        {'min': 0.0, 'max': 8.0, 'category': 'Susceptible'},
        {'min': 8.1, 'max': 15.9, 'category': 'Intermediate'},
        {'min': 16.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Ampicillin sulbactam': [
        {'min': 0.0, 'max': 8.0, 'category': 'Susceptible'},
        {'min': 8.1, 'max': 15.9, 'category': 'Intermediate'},
        {'min': 16.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Aztreonam': [
        {'min': 0.0, 'max': 4.0, 'category': 'Susceptible'},
        {'min': 4.1, 'max': 7.9, 'category': 'Intermediate'},
        {'min': 8.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Aztreonam avibactam': [
        {'min': 0.0, 'max': 4.0, 'category': 'Susceptible'},
        {'min': 4.1, 'max': 7.9, 'category': 'Intermediate'},
        {'min': 8.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Cefixime': [
        {'min': 0.0, 'max': 1.0, 'category': 'Susceptible'},
        {'min': 1.1, 'max': 1.9, 'category': 'Intermediate'},
        {'min': 4.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Ceftaroline': [
        {'min': 0.0, 'max': 0.5, 'category': 'Susceptible'},
        {'min': 0.6, 'max': 1.9, 'category': 'Intermediate'},
        {'min': 2.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Ceftaroline avibactam': [
        {'min': 0.0, 'max': 9999.9, 'category': 'Unknown'},
    ],
    'Ceftazidime avibactam': [
        {'min': 0.0, 'max': 8.0, 'category': 'Susceptible'},
        {'min': 8.1, 'max': 31.9, 'category': 'Intermediate'},
        {'min': 32.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Azithromycin': [
        {'min': 0.0, 'max': 2.0, 'category': 'Susceptible'},
        {'min': 2.1, 'max': 7.9, 'category': 'Intermediate'},
        {'min': 8.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Cefepime': [
        {'min': 0.0, 'max': 8.0, 'category': 'Susceptible'},
        {'min': 8.1, 'max': 31.9, 'category': 'Intermediate'},
        {'min': 32.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Cefoxitin': [
        {'min': 0.0, 'max': 8.0, 'category': 'Susceptible'},
        {'min': 8.1, 'max': 31.9, 'category': 'Intermediate'},
        {'min': 32.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Ceftazidime': [
        {'min': 0.0, 'max': 8.0, 'category': 'Susceptible'},
        {'min': 8.1, 'max': 31.9, 'category': 'Intermediate'},
        {'min': 32.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Erythromycin': [
        {'min': 0.0, 'max': 0.5, 'category': 'Susceptible'},
        {'min': 0.6, 'max': 3.9, 'category': 'Intermediate'},
        {'min': 4.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Vancomycin': [
        {'min': 0.0, 'max': 4.0, 'category': 'Susceptible'},
        {'min': 8.0, 'max': 16.0, 'category': 'Intermediate'},
        {'min': 16.1, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Tetracycline': [
        {'min': 0.0, 'max': 4.0, 'category': 'Susceptible'},
        {'min': 4.1, 'max': 16.0, 'category': 'Intermediate'},
        {'min': 16.1, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Levofloxacin': [
        {'min': 0.0, 'max': 2.0, 'category': 'Susceptible'},
        {'min': 2.1, 'max': 7.9, 'category': 'Intermediate'},
        {'min': 8.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Clarithromycin': [
        {'min': 0.0, 'max': 8.0, 'category': 'Susceptible'},
        {'min': 8.1, 'max': 31.9, 'category': 'Intermediate'},
        {'min': 32.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Clindamycin': [
        {'min': 0.0, 'max': 2.0, 'category': 'Susceptible'},
        {'min': 2.1, 'max': 7.9, 'category': 'Intermediate'},
        {'min': 8.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Imipenem': [
        {'min': 0.0, 'max': 0.12, 'category': 'Susceptible'},
        {'min': 0.13, 'max': 15.9, 'category': 'Unknown'}
       
    ],
    'Linezolid': [
        {'min': 0.0, 'max': 2.0, 'category': 'Susceptible'},
        {'min': 2.1, 'max': 7.9, 'category': 'Intermediate'},
        {'min': 8.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Metronidazole': [
        {'min': 0.0, 'max': 9999.9, 'category': 'Unknown'}
    ],
    'Minocycline': [
        {'min': 0.0, 'max': 4.0, 'category': 'Susceptible'},
        {'min': 4.1, 'max': 15.9, 'category': 'Intermediate'},
        {'min': 16.1, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Penicillin': [
        {'min': 0.0, 'max': 8.0, 'category': 'Susceptible'},
        {'min': 8.1, 'max': 15.9, 'category': 'Unknown'},
        {'min': 16.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Piperacillin tazobactam': [
        {'min': 0.0, 'max': 9999.9, 'category': 'Unknown'}
    ],
    'Tigecycline': [
        {'min': 0.0, 'max': 9999.9, 'category': 'Unknown'}
    ],
    'Colistin': [
        {'min': 0.0, 'max': 9999.9, 'category': 'Unknown'}
    ],
    'Daptomycin': [
        {'min': 0.0, 'max': 2.0, 'category': 'Susceptible'},
        {'min': 2.1, 'max': 7.9, 'category': 'Intermediate'},
        {'min': 8.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Doripenem': [
        {'min': 0.0, 'max': 1.0, 'category': 'Susceptible'},
        {'min': 1.0, 'max': 9999.9, 'category': 'Unknown'}
    ],
    'Ertapenem': [
        {'min': 0.0, 'max': 1.0, 'category': 'Susceptible'},
        {'min': 1.0, 'max': 9999.9, 'category': 'Unknown'}
    ],
    'Gatifloxacin': [
        {'min': 0.0, 'max': 2.0, 'category': 'Susceptible'},
        {'min': 2.1, 'max': 7.9, 'category': 'Intermediate'},
        {'min': 8.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Gentamicin': [
        {'min': 0.0, 'max': 4.0, 'category': 'Susceptible'},
        {'min': 4.1, 'max': 7.9, 'category': 'Unknown'},
        {'min': 8.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Moxifloxacin': [
        {'min': 0.0, 'max': 0.5, 'category': 'Susceptible'},
        {'min': 0.6, 'max': 1.9, 'category': 'Unknown'},
        {'min': 2.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Oxacillin': [
        {'min': 0.0, 'max': 0.5, 'category': 'Susceptible'},
        {'min': 0.6, 'max': 0.9, 'category': 'Unknown'},
        {'min': 1.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Quinupristin dalfopristin': [
        {'min': 0.0, 'max': 1.0, 'category': 'Susceptible'},
        {'min': 1.1, 'max': 9999.9, 'category': 'Unknown'}
    ],
    'Sulbactam': [
        {'min': 0.0, 'max': 9999.9, 'category': 'Unknown'}
    ],
    'Teicoplanin': [
        {'min': 0.0, 'max': 8.0, 'category': 'Susceptible'},
        {'min': 8.1, 'max': 31.9, 'category': 'Intermediate'},
        {'min': 32.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Trimethoprim sulfa': [
        {'min': 0.0, 'max': 2.0, 'category': 'Susceptible'},
        {'min': 2.1, 'max': 3.9, 'category': 'Unknown'},
        {'min': 4.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Ceftolozane tazobactam': [
        {'min': 0.0, 'max': 9999.9, 'category': 'Unknown'}
    ],
    'Cefoperazone sulbactam': [
        {'min': 0.0, 'max': 16.0, 'category': 'Susceptible'},
        {'min': 16.1, 'max': 63.9, 'category': 'Intermediate'},
        {'min': 64.0, 'max': 9999.9, 'category': 'Resistant'}
    ],
    'Amoxycillin clavulanate': [
        {'min': 0.0, 'max': 8.0, 'category': 'Susceptible'},
        {'min': 8.1, 'max': 31.9, 'category': 'Intermediate'},
        {'min': 32.0, 'max': 9999.9, 'category': 'Resistant'}
    ]
}

# Color mapping
category_colors = {
    'Susceptible': 'green',
    'Intermediate': 'orange',
    'Resistant': 'red',
    'No matching category found.': 'gray',
    'Invalid MIC value. Please enter a numeric value.': 'gray'
}

# HTML Template
html_template = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MIC Categorizer</title>
  <style>
    body {
      background: #f0f4f8;
      font-family: Arial, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }
    .form-container {
      background: white;
      padding: 30px;
      border-radius: 10px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      width: 400px;
    }
    h2 {
      text-align: center;
      color: #333;
    }
    label {
      display: block;
      margin-top: 15px;
      font-weight: bold;
    }
    select, input[type="text"] {
      width: 100%;
      padding: 10px;
      margin-top: 5px;
      border-radius: 5px;
      border: 1px solid #ccc;
    }
    input[type="submit"] {
      margin-top: 20px;
      width: 100%;
      padding: 10px;
      background-color: #007bff;
      border: none;
      color: white;
      font-weight: bold;
      border-radius: 5px;
      cursor: pointer;
    }
    input[type="submit"]:hover {
      background-color: #0056b3;
    }
    .result {
      margin-top: 20px;
      text-align: center;
      font-size: 1.2em;
    }
  </style>
</head>
<body>
  <div class="form-container">
    <h2>Antibiotic MIC Categorizer</h2>
    <form method="POST">
      <label for="antibiotic">Select Antibiotic:</label>
      <select name="antibiotic">
        {% for ab in antibiotics %}
          <option value="{{ ab }}" {% if ab == selected_antibiotic %}selected{% endif %}>{{ ab }}</option>
        {% endfor %}
      </select>

      <label for="mic">Enter MIC value:</label>
      <input type="text" name="mic" value="{{ mic_input or '' }}">

      <input type="submit" value="Categorize">
    </form>

    {% if result %}
      <div class="result" style="color: {{ color }};">Result: {{ result }}</div>
    {% endif %}
  </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    mic_input = None
    selected_antibiotic = 'Amikacin'
    color = 'black'

    if request.method == 'POST':
        selected_antibiotic = request.form['antibiotic']
        mic_input = request.form['mic']
        try:
            mic_value = float(mic_input)
            rules = rules_dict.get(selected_antibiotic, [])
            for rule in rules:
                if rule['min'] <= mic_value <= rule['max']:
                    result = rule['category']
                    break
            if result is None:
                result = "No matching category found."
        except ValueError:
            result = "Invalid MIC value. Please enter a numeric value."

        color = category_colors.get(result, 'black')

    return render_template_string(
        html_template,
        antibiotics=rules_dict.keys(),
        result=result,
        mic_input=mic_input,
        selected_antibiotic=selected_antibiotic,
        color=color
    )

if __name__ == '__main__':
    app.run(debug=True)
