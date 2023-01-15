from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from .forms import UserForm, AdminForm, UploadForm, EditForm, FindForm
from .models import Person, Admin
from django.db.models import Avg, Min, Max, Sum
import csv
import io


# Create your views here.

flag = False
login = 'undefined'
register_error = False
csv_error = False
find_person_flag = False
find_persons = None
edit_person = '1'
data = None



# вывод всей бд
def index(request):

	result_dict = make_statistics()
	return render(request, 'persons.html', result_dict)



def make_statistics():
	people = Person.objects.all()
	len_people = people.count()

	try:
		avg_age = round(tuple(Person.objects.aggregate(Avg("age")).values())[0], 2)
	except TypeError:
		avg_age = None

	min_age = tuple(Person.objects.aggregate(Min("age")).values())[0]
	max_age = tuple(Person.objects.aggregate(Max("age")).values())[0]
	sum_age = tuple(Person.objects.aggregate(Sum("age")).values())[0]
	statistics = {'len_people': len_people, 
				'avg_age': avg_age, 
				'min_age': min_age, 
				'max_age': max_age, 
				'sum_age': sum_age
				}
	return make_result_dict(people=people, statistics=statistics)



def make_result_dict(people, statistics):
	global flag
	global register_error
	global csv_error
	global find_person_flag


	result_dict = {'userform': UserForm(), 
				'adminform': AdminForm(), 
				'uploadform': UploadForm(), 
				'people': people, 
				'find_person_flag': False, 
				'find_persons': find_persons, 
				'findform': FindForm(), 
				'statistics': statistics, 
				'flag': flag, 
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



# создание
def create(request):
	if request.method == 'POST' and flag:
		name = request.POST.get('name')
		surname = request.POST.get('surname')
		age = request.POST.get('age') 
		Person.objects.create(name=name, surname=surname, age=age)
		return HttpResponseRedirect("/app/form/")

	elif not flag:
		return HttpResponse("<h2>You dont have access to do this</h2>")






	 
# удаление данных об одном персонаже из бд
def delete(request, id):
	if flag:
		try:
			person = Person.objects.get(id=id)
			person.delete()
			return HttpResponseRedirect('/app/form/')
		except Person.DoesNotExist:
			return HttpResponseNotFound("<h2>Person not found</h2>")
	elif not flag:
		return HttpResponse("<h2>You dont have access to do this</h2>")


# удаление всех данных из бд
def delete_all(request):
	if flag:
		Person.objects.all().delete()
		return HttpResponseRedirect("/app/form/")
	elif not flag:
		return HttpResponse("<h2>You dont have access to do this</h2>")




def edit(request, id):
	global edit_person


	try:
		edit_person = Person.objects.get(id=id)

 
		if request.method == "POST" and flag:

			if request.POST.get('name') != '':
				name = request.POST['name']
			else:
				name = edit_person.name
			if request.POST.get('surname') != '':
				surname = request.POST['surname']
			else:
				surname = edit_person.surname
			age = request.POST.get('age')
			if age != '' and age.isdigit() and 0 <= int(age) <= 120:
				pass
			else:
				age = edit_person.age

			edit_person.name = name
			edit_person.surname = surname
			edit_person.age = age
			edit_person.save()
			return HttpResponseRedirect("/app/form/")

		elif request.method == "GET" and flag:
			editform = EditForm()
			return render(request, "edit.html", {"editform": editform, 'edit_person': edit_person})

		elif not flag:
			return HttpResponse("<h2>You dont have access to do this</h2>")
			
	except Person.DoesNotExist:
		return HttpResponseNotFound("<h2>Person not found</h2>")



def quit(request):
	global flag


	if request.method == 'GET':
		flag = False
		return HttpResponseRedirect("/app/form/")



def register(request):
	global flag
	global login
	global register_error


	if request.method == 'POST':

		login = request.POST.get('login', 'undefined')
		password = request.POST.get('password', 'undefined')

		try:
			Admin.objects.get(login=login, password=password)
			flag = True
			return HttpResponseRedirect("/app/form/")
		except Admin.DoesNotExist:
			register_error = True
			return HttpResponseRedirect("/app/form/")



def upload(request):
	global csv_error


	if request.method == 'POST':
		csv_file = request.FILES["csv_file"]
		if not csv_file.name.endswith('.csv'):
			csv_error = True

		else:
			decoded_file = csv_file.read().decode('utf-8')
			io_string = io.StringIO(decoded_file)
			for line in csv.reader(io_string, delimiter=',', quotechar='|'):
				try:
					name = line[0]
					surname = line[1]
					age = line[2] 
					Person.objects.create(name=name, surname=surname, age=age)
				except Exception:
					pass

		return HttpResponseRedirect("/app/form/")



def make_csv_file_from_sql(data):
	# Create the HttpResponse object with the appropriate CSV header.
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="data.csv"'

	fieldnames = ['id', 'name', 'surname', 'age']
	writer = csv.DictWriter(response, fieldnames=fieldnames)
	writer.writeheader()

	for obj in data:
		writer.writerow({'id': obj.id, 'name': obj.name, 'surname': obj.surname, 'age': obj.age})

	return response




def export_all(request):

	if request.method == 'GET':
		data = Person.objects.all()
		return make_csv_file_from_sql(data)


def export_data_from_find_person(request):

	if request.method == 'GET':
		return make_csv_file_from_sql(data)



def find_person(request):
	global find_person_flag
	global find_persons
	global data


	if request.method == 'GET':

		id = request.GET.get('id')
		if id != '' and id.isdigit():
			find_persons = Person.objects.filter(id=id)
			if find_persons:
				find_person_flag = True
				data = find_persons
			else:
				return HttpResponseNotFound("<h2>Person not found</h2>")
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
			else:
				return HttpResponseNotFound("<h2>Persons not found</h2>")


			if len(result_str) > 14:
				find_persons = eval(result_str)
				if not find_persons:
					return HttpResponseNotFound("<h2>Persons not found</h2>")
				else:
					data = find_persons
					find_person_flag = True
			else:
				return HttpResponseNotFound("<h2>Persons not found</h2>")

		return HttpResponseRedirect("/app/form/")



