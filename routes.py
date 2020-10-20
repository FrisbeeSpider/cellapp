from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from app import app, db
from models import User, Cell, Favcell, Item
from flask import render_template, request, url_for, redirect, flash

#This defines the form for adding new cells
class CellForm(FlaskForm):
  cellname = StringField(label = "Cell Name:", validators=[DataRequired()])
  cellgroup = StringField(label = "Cell Group:", validators=[DataRequired()])
  submit = SubmitField("Add Cell")

#This defines the form for adding new profiles
class ProfileForm(FlaskForm):
  username = StringField(label = "Username:", validators=[DataRequired()])
  submit = SubmitField("Add Profile")


#This function checks to see if a cell already exists before it gets added
def exists(item, favcell):
  """Return a boolean
    True if favcell contains item. False otherwise.
    """
  for i in favcell: 
    if i.cell_id == item.cell_id:
       return True
  return False

#This page lists all the user profiles and lets you add new ones
@app.route('/profiles', methods=["GET", "POST"])
def profiles():
    form = ProfileForm()
    if request.method == 'POST':
      new_favcell = Favcell(id = len(Favcell.query.all()) + 1) #A new Favcell object needs to be made to tie with the new User object
      new_profile = User(username = form.username.data, favcell_id = new_favcell.id)
      db.session.add(new_favcell)
      db.session.add(new_profile)
      db.session.commit()
    else:
      flash(form.errors)
    current_users = User.query.all() 
    return render_template('users.html', current_users = current_users, form = form)

#This is the route for individual profiles
@app.route('/profile/<int:user_id>')
def profile(user_id):
   user = User.query.filter_by(id = user_id).first_or_404(description = "No such user found.")
   cells = Cell.query.all()
   my_favcell = Favcell.query.get(user.favcell_id)
   return render_template('profile.html', user = user, cells = cells, my_favcell = my_favcell)

#this function is for adding new cells to the favorites list (favcell)
@app.route('/add_item/<int:user_id>/<int:cell_id>/<int:favcell_id>')
def add_item(user_id, cell_id, favcell_id):
   new_item = Item(cell_id = cell_id, favcell_id = favcell_id)
   user = User.query.filter_by(id = user_id).first_or_404(description = "No such user found.")
   my_favcell = Favcell.query.filter_by(id = user.favcell_id).first()
   if not exists(new_item, my_favcell.items):
      cell = Cell.query.get(cell_id)
      cell.n = cell.n + 1
      db.session.add(new_item)
      db.session.commit()
   return redirect(url_for('profile', user_id = user_id))

#This removes a cell from the favorites list (favcell)
@app.route('/remove_item/<int:user_id>/<int:item_id>')
def remove_item(user_id, item_id):
   cell_to_remove = Item.query.get(item_id)
   cell = Cell.query.get(cell_to_remove.cell_id)
   cell.n = cell.n - 1
   db.session.delete(cell_to_remove)
   db.session.commit()
   return redirect(url_for('profile', user_id = user_id))
   
#This is the dashboard route where you can add new cells to the library
@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
  form = CellForm()
  if request.method == 'POST':
    new_cell = Cell(cellname = form.cellname.data, cellgroup = form.cellgroup.data, n = 0)
    db.session.add(new_cell)
    db.session.commit()
  else:
        flash(form.errors)
  unpopular_cells = Cell.query.order_by(Cell.n)
  cells = Cell.query.all()
  return render_template('dashboard.html', cells = cells, unpopular_cells = unpopular_cells, form = form)