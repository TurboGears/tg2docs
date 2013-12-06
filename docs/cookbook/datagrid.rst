.. _datagrid-quickstart:

DataGrid Tutorial
=====================================

DataGrid is a quick way to present data in tabular form.

The columns to put inside the table are specified with the *fields* constructor argument in a list.
Each entry of the list can be an accessor (attribute name or function), a tuple (title, accessor) or a ``tw2.forms.datagrid.Column`` instance.

Preparing Application
-----------------------

This tutorial will show an addressbook with a set of people each with a name, surname and phone number.
Model used will be::

	from sqlalchemy import Table, ForeignKey, Column
	from sqlalchemy.types import Unicode, Integer, DateTime

	class Person(DeclarativeBase):
	    __tablename__ = 'person'

	    uid = Column(Integer, autoincrement=True, primary_key=True)
	    name = Column(Unicode(255))
	    surname = Column(Unicode(255))
	    phone = Column(Unicode(64))

and we will populate with this data::

        for i in [['John', 'Doe', '3413122314'],
                  ['Lucas', 'Darkstone', '378321322'],
                  ['Dorian', 'Gray', '31337433'],
                  ['Whatever', 'Person', '3294432321'],
                  ['Aaliyah', 'Byron', '676763432'],
                  ['Caesar', 'Ezra', '9943243243'],
                  ['Fahd', 'Gwyneth', '322313232'],
                  ['Last', 'Guy', '23132321']]:
            DBSession.add(Person(name=i[0], surname=i[1], phone=i[2]))

Basic DataGrid
----------------

With a model and some data set up, we can now start declaring our DataGrid and the fields it has to show::

	from tw2.forms import DataGrid

	addressbook_grid = DataGrid(fields=[
	    ('Name', 'name'),
	    ('Surname', 'surname'),
	    ('Phone', 'phone')
	])

After declaring the grid itself we will need to fetch the data to show inside the grid from our controller.
For this example we will do it inside the RootController.index method::

    @expose('dgridt.templates.index')
    def index(self):
        data = DBSession.query(Person)
        return dict(page='index', grid=addressbook_grid, data=data)

Now the grid can be displayed in the template like this:

.. highlight:: html+genshi

Template code necessary to show the grid in ``templates/index.html``::

	<div>${grid.display(value=data)}</div>


Paginating DataGrid
----------------------

Now that the grid can be displayed next probable improvement would be to paginate it.
Displaying 10 results is fine, but when results start to grow it might cause performance problems and make results harder to view. 

.. highlight:: python

The same things explained in the :ref:`pagination-quickstart` tutorial apply here. 
First of all it is needed to adapt the controller method to support pagination::

    from tg.decorators import paginate

    @expose('dgridt.templates.index')
    @paginate("data", items_per_page=3)
    def index(self):
        data = DBSession.query(Person)
        return dict(page='index', grid=addressbook_grid, data=data)

If you run the application now you will see only 3 results as they get paginated three by three and we are still missing a way to change page.
What is needed now is a way to switch pages and this can be easilly done as the paginate decorator adds to the template context a *paginators* variable
where all the paginators currently available are gathered. Rendering the "data" paginator somewhere inside the template is simply enough to have
a working pagination for our datagrid.

.. highlight:: html+genshi

Template in ``templates/index.html`` would become::

	<div>${grid.display(value=data)}</div>
	<div>${tmpl_context.paginators.data.pager()}</div>

Now the page should render with both the datagrid and the pages under the grid itself, making possible to switch between the pages.

Sorting Columns
--------------------

DataGrid itself does not provide a way to implement columns sorting, but it can be easilly achieved by inheriting
from ``tw2.forms.datagrid.Column`` to add a link that can provide sorting.

.. highlight:: python

First of all we need to declare or SortableColumn class that will return the link with the sorting request as the title for our DataGrid::

	from sqlalchemy import asc, desc
	from tw2.forms.datagrid import Column
	import genshi

	class SortableColumn(Column):
	    def __init__(self, title, name):
		super(SortableColumn, self).__init__(name)
		self._title_ = title
	   
	    def set_title(self, title):
		self._title_ = title

	    def get_title(self):
		current_ordering = request.GET.get('ordercol')
		if current_ordering and current_ordering[1:] == self.name:
		    current_ordering = '-' if current_ordering[0] == '+' else '+'
		else:
		    current_ordering = '+'
		current_ordering += self.name

		new_params = dict(request.GET)
		new_params['ordercol'] = current_ordering

		new_url = url(request.path_url, params=new_params)
		return genshi.Markup('<a href="%(page_url)s">%(title)s</a>' % dict(page_url=new_url, title=self._title_))

	    title = property(get_title, set_title)

It is also needed to tell to the DataGrid that it has to use the SortableColumn for its fields::

	addressbook_grid = DataGrid(fields=[
	    SortableColumn('Name', 'name'),
	    SortableColumn('Surname', 'surname'),
	    SortableColumn('Phone', 'phone')
	])

Now if we reload the page we should see the clickable links inside the headers of the table, but if we click one the application
will crash because of an unexpected argument. We are now passing the *ordercol* argument to our constructor to tell it
for which column we want the data to be ordered and with which ordering.

To handle the new parameter the controller must be modified to accept it and perform the ordering::

	@expose('dgridt.templates.index')
	@paginate("data", items_per_page=3)
	def index(self, *args, **kw):
	    data = DBSession.query(Person)
	    ordering = kw.get('ordercol')
	    if ordering and ordering[0] == '+':
	        data = data.order_by(asc(ordering[1:]))
	    elif ordering and ordering[0] == '-':
	        data = data.order_by(desc(ordering[1:]))
	    return dict(page='index', grid=addressbook_grid, data=data)

Now the ordering should work and clicking two times on a column should invert the ordering.

Edit Column Button
--------------------

DataGrid also permits to pass functions in the *fields* parameter to build the row content. This makes possible for example to add
and *Actions* column where to put an edit button to edit the entry on the row. 

To perform this it is just required to add another field with the name and the function that will return the edit link.
In this example addressbook_grid would become::

	addressbook_grid = DataGrid(fields=[
	    SortableColumn('Name', 'name'),
	    SortableColumn('Surname', 'surname'),
	    SortableColumn('Phone', 'phone'),
	    ('Action', lambda obj:genshi.Markup('<a href="%s">Edit</a>' % url('/edit', params=dict(item_id=obj.uid))))
	])


