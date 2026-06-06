from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///C:\\Janvi\\coding\\Flask_Intro\\url_db.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Url(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(500), nullable=False)
    short_url = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"{self.sno} - {self.long_url}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form.get('long_url')
        all_urls = db.session.execute(db.select(Url.short_url)).scalars().all()
        short_url = shortening_logic(long_url, all_urls)
        new_url = Url(long_url = long_url, short_url=short_url)
        db.session.add(new_url)
        db.session.commit()
        
    all_urls = db.session.execute(db.select(Url.short_url)).scalars().all()
    print(all_urls)
    url_variable = Url.query.all()
    return render_template('index.html', url_template_variable=url_variable)

def shortening_logic(long_url : str, all_urls) -> str:
    number = str(random.randint(1000,9999))
    print(number)
    found = True
    while found:
        found = False
        for url in all_urls:
            if url == number:
                found = True
                number = str(random.randint(1000,9999))
                break
    return number

@app.route('/<short_url>')
def expand_url(short_url):
    print(short_url)
    link = Url.query.filter_by(short_url=short_url).first_or_404()
    print(link) 
    return redirect(link.long_url)
    


# @app.route('/short_url')
# def new():
#     return 'this is new page'

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
