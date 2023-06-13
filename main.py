
from flask import Flask, render_template, request
import pandas as pd
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    if file:

        df = pd.read_excel(file)

        required_attributes = ['Name', 'Position', 'Salary']
        missing_attributes = [attr for attr in required_attributes if attr not in df.columns]
        if missing_attributes:
            error_message = f"Missing attributes in the Excel file: {', '.join(missing_attributes)}"
            return render_template('index.html', error=error_message)

        offer_letters = []
        for _, row in df.iterrows():
            name = row['Name']
            position = row['Position']
            salary = row['Salary']




            env = Environment(loader=FileSystemLoader('templates'), autoescape=True)
            template = env.get_template('offer_letter_templates.html')

            # Render the template with the dynamic data
            offer_letter = template.render(name=name, position=position, salary=salary)
            offer_letters.append(offer_letter)

        return render_template('offer_letters.html', offer_letters=offer_letters)

    return "<script>alert('Please Upload CSV File');window.location='/'</script>"

if __name__ == '__main__':
    app.run(debug=True)
