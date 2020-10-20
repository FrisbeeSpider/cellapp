from app import app, db

#Each user has a username, and a cellgroup_id foreign key referring to the user's favorite cell list (favcell)
class User(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(50), index = True, unique = True) 
  favcell_id = db.Column(db.Integer, db.ForeignKey('favcell.id'))
  
  #how the class gets represented as a string
  def __repr__(self):
        return "{}".format(self.username)


#Each cell has a name, a group it belongs to, and an integer for how many favcell lists it's been added to
class Cell(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  cellname = db.Column(db.String(50), index = True, unique = True)
  cellgroup = db.Column(db.String(50), index = True, unique = False) 
  n = db.Column(db.Integer, index = False, unique = False)
  
  def __repr__(self):
        return "{}: a type of {}".format(self.cellname, self.cellgroup)
    

#Each Item has a foreign key for a Cell and for a favorite cell list (Favcell) so it can tie cells to the list
class Item(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  cell_id = db.Column(db.Integer, db.ForeignKey('cell.id'))
  favcell_id = db.Column(db.Integer, db.ForeignKey('favcell.id'))

  def __repr__(self):
        cell = Cell.query.get(self.cell_id)
        return "{}: a type of {}".format(cell.cellname, cell.cellgroup) 
  

#The list of favorite cells, it gets tied to the Items    
class Favcell(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  items = db.relationship('Item', backref='favcell', lazy = 'dynamic')

#this creates the database file using all these classes to generate the tables
db.create_all()