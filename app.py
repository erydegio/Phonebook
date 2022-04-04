
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db" # tell where db is located (project folder)

# init db
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_name = db.Column(db.String(50), nullable=False ) 
    person_number = db.Column(db.Integer, nullable=False) 
    
    def __repr__(self):
        return f"<{self.person_name} {self.id}>" 



@app.route("/", methods=["POST", "GET"])
def index():

    if request.method == "POST":
        content_name = request.form["name"] # 'name' -> input id
        content_number = int(request.form["number"])
        new_record = Book(person_name=content_name, person_number=content_number)
        
        # if post push new contact into db
        try:
            db.session.add(new_record)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue adding a number"

    else:
        contacts = Book.query.order_by(Book.person_name).all()   
        return render_template("index.html", contacts=contacts)



@app.route("/delete/<int:id>")
def delete(id):
    person_to_delete = Book.query.get_or_404(id)

    try:  
        db.session.delete(person_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return 'There was a problem deleting that person'



@app.route("/update/<int:id>", methods=['POST', 'GET'])
def update(id):
    person = Book.query.get_or_404(id)

    if request.method == "POST":
        person.person_name = request.form['name']
        person.person_number = request.form['number']

        try:
            db.session.commit()
            return redirect("/")
        except:
            return 'There was an issue updating your contact'
    
    else:
        return render_template('update.html', person=person)




if __name__ == "__main__":
    app.run(debug=True)