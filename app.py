from flask import Flask, render_template, request
from text_summary import summarizer

app = Flask(__name__)

@app.route('/')
def index(): 
    return render_template('index.html')    

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        raw_text = request.form['rawtext']
        
        # Check if text is provided
        if not raw_text.strip():
            return render_template('index.html', 
                                 error="Please enter some text to summarize.")
        
        # Get summary
        summary, original_txt, len_orig_txt, len_summary = summarizer(raw_text)
        
        return render_template('summary.html', 
                             summary=summary, 
                             original_txt=original_txt, 
                             len_orig_txt=len_orig_txt, 
                             len_summary=len_summary)
    
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0')