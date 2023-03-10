from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from .forms import UserForm, AdminForm, UploadForm, EditForm, FindForm
from .models import Person, Admin
from django.db.models import Avg, Min, Max, Sum
import csv
import io



# Create your views here.

# global variables
register_flag = False  # Describes if the user is registered or not
login = 'undefined'  # Contains login-name to be shown on the admin page
register_error = False  # Throws an error if incorrect data is entered during registration
csv_error = False  # Throws an error if incorrect data was uploaded to table
find_person_flag = False  # If the data search highlights a result, this parameter is set to True
find_persons = None  # Variable that contains data from search result
redirect_path = '/app/form/'  # For HttpResponseRedirect()
not_found_message = '<h2 style="font-family: sans-serif;">Data not found</h2>'  # For HttpResponseNotFound()


# home page output
# index() also calls make_statistics() and make_result_dict()
#
# 1) make_statistics() creates statistics data
# 2) make_result_dict() creates a result_dict, which index() returns as a context attribute of the render function
def index(request):
	people = Person.objects.all()
	result_dict = make_result_dict(people)
	result_dict['statistics'] =  make_statistics(people)
	return render(request, 'persons.html', result_dict)


# creates statistics data
def make_statistics(people):
	if people:
		len_people = people.count()

		avg_age = round(tuple(Person.objects.aggregate(Avg("age")).values())[0], 2)
		min_age = tuple(Person.objects.aggregate(Min("age")).values())[0]
		max_age = tuple(Person.objects.aggregate(Max("age")).values())[0]
		sum_age = tuple(Person.objects.aggregate(Sum("age")).values())[0]

		avg_height = round(tuple(Person.objects.aggregate(Avg("height")).values())[0], 2)
		min_height = tuple(Person.objects.aggregate(Min("height")).values())[0]
		max_height = tuple(Person.objects.aggregate(Max("height")).values())[0]
		sum_height = tuple(Person.objects.aggregate(Sum("height")).values())[0]

		avg_weight = round(tuple(Person.objects.aggregate(Avg("weight")).values())[0], 2)
		min_weight = tuple(Person.objects.aggregate(Min("weight")).values())[0]
		max_weight = tuple(Person.objects.aggregate(Max("weight")).values())[0]
		sum_weight = tuple(Person.objects.aggregate(Sum("weight")).values())[0]

		statistics = {
			'len_people': len_people, 
			'avg_age': avg_age, 
			'min_age': min_age, 
			'max_age': max_age, 
			'sum_age': sum_age,

			'avg_height': avg_height, 
			'min_height': min_height, 
			'max_height': max_height, 
			'sum_height': sum_height,

			'avg_weight': avg_weight, 
			'min_weight': min_weight, 
			'max_weight': max_weight, 
			'sum_weight': sum_weight
		}
	else:
		statistics = {'len_people': 0}
	return statistics


# creates a result_dict, which index() returns as a context attribute of the render function
def make_result_dict(people):
	global register_flag
	global register_error
	global csv_error
	global find_person_flag


	result_dict = {
		'userform': UserForm(), 
		'adminform': AdminForm(), 
		'uploadform': UploadForm(), 
		'people': people, 
		'find_person_flag': False, 
		'find_persons': find_persons, 
		'findform': FindForm(), 
		'register_flag': register_flag, 
		'login': login, 
		'register_error': False, 
		'csv_error': False
	}

	if register_error:
		register_error = False
		result_dict['register_error'] = True

	if csv_error:
		csv_error = False
		result_dict['csv_error'] = True

	if find_person_flag:
		find_person_flag = False
		result_dict['find_person_flag'] = True
	
	return result_dict


# record creation
def create(request):
	if request.method == 'POST' and register_flag:
		name = request.POST.get('name')
		surname = request.POST.get('surname')
		age = request.POST.get('age')
		height = request.POST.get('height')
		weight = request.POST.get('weight')
		Person.objects.create(name=name, surname=surname, age=age, height=height, weight=weight)
		return HttpResponseRedirect(redirect_path)
	elif not register_flag:
		return HttpResponse("<h2>You dont have permission to do this</h2>")


# deleting data about one character from the database
def delete(request, id):
	if request.method == 'POST' and register_flag:
		try:
			person = Person.objects.get(id=id)
			person.delete()
			return HttpResponseRedirect(redirect_path)
		except Person.DoesNotExist:
			return HttpResponseNotFound(not_found_message)
	else:
		return HttpResponse("<h2>You dont have permission to do this</h2>")


# deleting all data from the database
def delete_all(request):
	if request.method == "POST" and register_flag:
		Person.objects.all().delete()
		return HttpResponseRedirect(redirect_path)
	else:
		return HttpResponse("<h2>You dont have permission to do this</h2>")


# edit record data
#
# this function allows you to make selective changes, that is, you can change 
# only the age of the person in the record, and the rest will remain the same
def edit(request, id):
	try:
		edit_person = Person.objects.get(id=id) 
		if request.method == "POST" and register_flag:
			
			name = request.POST.get('name')
			if name == '':
				name = edit_person.name

			surname = request.POST.get('surname')
			if surname == '':
				surname = edit_person.surname

			age = request.POST.get('age')
			if not (age != '' and age.isdigit() and 0 <= int(age) <= 120):
				age = edit_person.age

			height = request.POST.get('height')
			if not (height != '' and height.isdigit()):
				height = edit_person.height

			weight = request.POST.get('weight')
			if not (weight != '' and weight.isdigit()):
				weight = edit_person.weight

			edit_person.name = name
			edit_person.surname = surname
			edit_person.age = age
			edit_person.height = height
			edit_person.weight = weight
			edit_person.save()
			return HttpResponseRedirect(redirect_path)

		elif request.method == "GET" and register_flag:
			editform = EditForm()
			return render(request, "edit.html", {"editform": editform, 'edit_person': edit_person})

		elif not register_flag:
			return HttpResponse("<h2>You dont have permission to do this</h2>")
			
	except Person.DoesNotExist:
		return HttpResponseNotFound(not_found_message)


# unlogin
def quit(request):
	global register_flag


	if request.method == 'GET':
		register_flag = False
		return HttpResponseRedirect(redirect_path)


# login
def register(request):
	global register_flag
	global login
	global register_error


	if request.method == 'POST':
		login = request.POST.get('login')
		password = request.POST.get('password')
		try:
			Admin.objects.get(login=login, password=password)
			register_flag = True
		except Admin.DoesNotExist:
			register_error = True
		return HttpResponseRedirect(redirect_path)


# uploading a .csv file to the database
def upload(request):
	global csv_error


	if request.method == 'POST':
		csv_file = request.FILES["csv_file"]
		if not csv_file.name.endswith('.csv'):
			csv_error = True
		else:
			decoded_file = csv_file.read().decode('utf-8')
			io_string = io.StringIO(decoded_file)

			for line in csv.DictReader(io_string, delimiter=',', quotechar='|'):
				try:
					name = line.get('name', 'undefined')
					surname = line.get('surname', 'undefined')
					age = line.get('age', 'undefined')
					height = line.get('height', 'undefined')
					weight = line.get('weight', 'undefined')
					Person.objects.create(name=name, surname=surname, age=age, height=height, weight=weight)
				except Exception:
					pass
		return HttpResponseRedirect(redirect_path)


# creating an HttpResponse object with the corresponding CSV header
def make_csv_file_from_sql(data_for_exporting):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="data.csv"'

	fieldnames = ('id', 'name', 'surname', 'age', 'height', 'weight')
	writer = csv.DictWriter(response, fieldnames=fieldnames)
	writer.writeheader()

	for obj in data_for_exporting:
		writer.writerow({
			'id': obj.id, 
			'name': obj.name, 
			'surname': obj.surname, 
			'age': obj.age, 
			'height': obj.height, 
			'weight': obj.weight
		})
	return response


# the first function in the process of creating a .csv file from MAIN table to download
# returns the make_csv_file_from_sql() function, which creates a .csv file
def export_all(request):
	if request.method == 'GET':
		return make_csv_file_from_sql(Person.objects.all())


# the first function in the process of creating a .csv file from RESULT table to download
# returns the make_csv_file_from_sql() function, which creates a .csv file
def export_data_from_find_person(request):
	if request.method == 'GET':
		return make_csv_file_from_sql(find_persons)


# record search
def find_person(request):
	global find_person_flag
	global find_persons


	if request.method == 'GET':
		id = request.GET.get('id')
		if id != '' and id.isdigit():
			find_persons = Person.objects.filter(id=id)
			if find_persons:
				find_person_flag = True
			else:
				return HttpResponseNotFound(not_found_message)
		else:
			result_str = 'Person.objects'

			name = request.GET.get('name')
			if name != '':
				result_str += f'.filter(name="{name}")'

			surname = request.GET.get('surname')
			if surname != '':
				result_str += f'.filter(surname="{surname}")'

			age = request.GET.get('age')
			if age != '' and age.isdigit():
				result_str += f'.filter(age={age})'
			
			height = request.GET.get('height')
			if height != '' and height.isdigit():
				result_str += f'.filter(height={height})'

			weight = request.GET.get('weight')
			if weight != '' and weight.isdigit():
				result_str += f'.filter(weight={weight})'

			if len(result_str) > 14:
				find_persons = eval(result_str)
				if find_persons:
					find_person_flag = True
				else:
					return HttpResponseNotFound(not_found_message)
			else:
				return HttpResponseNotFound(not_found_message)
		return HttpResponseRedirect(redirect_path)