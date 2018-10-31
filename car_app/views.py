from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render_to_response

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from car_app.models import TruckModel, TruckNumber, Post
from car_app.forms import TruckModelForm, TruckNumberForm, PostForm

from django.utils import timezone
from django.db.models import Max, Avg, FloatField, Count, F 

from django.views.generic.base import View


    
    
#output_field=FloatField()

def update_overload():
    overloads = TruckNumber.objects.select_related('model_name').annotate(
	    overload_100_1 = (F('current_weight') - F('model_name_id__max_capacity')   ) * 100 / F('model_name_id__max_capacity'), 
	    ).values()
    print('overloads = ')
    for item in overloads:
    
        #print(item)
        #print('----', item['id'], item['overload_100_1'])
        
        
        truck_instance = get_object_or_404(TruckNumber, pk=item['id'])
        #print('truck_instance = ', truck_instance)
        #print('truck_instance[overload] = ', truck_instance.overload)
        
        #print("item['overload_100_1'] = ", item['overload_100_1'])
        
        if truck_instance.overload == 0:
            truck_instance.overload = item['overload_100_1']
            truck_instance.save()
        
        
        #print()
	
	
    return overloads










def index(request, truck_model_select="all"):
	print('======', request.GET)
	
	print('===================      ', len(request.GET))
	
	'''
	if request.GET['truck_model_select'] == '1':
		requested_numbers = TruckNumber.objects.filter(model_name=1)
		print('r = ', requested_numbers)
	'''
	
	
	try:
		

		all_truck_models = TruckModel.objects.all()
		all_truck_numbers = TruckNumber.objects.all()
		requested_numbers = TruckNumber.objects.all()
	except (KeyError, MultiValueDictKeyError) as key_error:
		print('%%%%%%%%%%%%%%%%%%%%%%%%%')
	
	
	

		
	if len(request.GET) == 0:
	    print('NOT  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
	    print()
	    print()
	    print()
	    print('NOT  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
	    
	    requested_numbers = TruckNumber.objects.all()
	    
	   
	    
	elif request.GET['truck_model_select'] == 'all':
	    print('ALL')
	    requested_numbers = TruckNumber.objects.all()
	    

	else:
	
		try:
			model_id = request.GET['truck_model_select']
			print('model_id = ', model_id, type(model_id))
			model_id_int = int(model_id)
			requested_numbers = TruckNumber.objects.filter(model_name=model_id_int)
			
		except (KeyError, UnboundLocalError)  as err:
			print('\n\n\n\n\n       index')
			print('KeyError from index.html', err)
			
			
		except (MultiValueDictKeyError, django.utils.datastructures.MultiValueDictKeyError) as multy_error:
			print('\n\n\n\n\n')
			requested_numbers = TruckNumber.objects.all()
		
			
			
			
			print('#######################  requested_numbers = ', requested_numbers)
	
	print('requested_numbers = ', requested_numbers)
	print()
	print()
			


	current_moment_overloads = update_overload()
	
	amount_numbers = len(requested_numbers)
		
	context = {'all_truck_models': all_truck_models,
		#'all_truck_numbers': all_truck_numbers, 
		'requested_numbers': requested_numbers, 
		'amount_numbers': amount_numbers,
		}
	
	
	
	print('LEN + + + ', len(requested_numbers))
	
	
	return render(request, 'car_app/index.html', context)






def search(request):
	all_truck_models = TruckModel.objects.all()
	all_truck_numbers = TruckNumber.objects.all()
	requested_numbers = TruckNumber.objects.all()
		
	if not request.GET:
	    print('NOT')
	    requested_numbers = TruckNumber.objects.all()
	    
	elif request.GET['truck_model_select'] == 'all':
	    print('ALL')
	    requested_numbers = TruckNumber.objects.all()

	else:
	
		try:
			model_id = request.GET['truck_model_select']
			print('model_id = ', model_id, type(model_id))
		except (KeyError, UnboundLocalError)  as err:
			
			print('KeyError from index.html', err)
			requested_numbers = TruckNumber.objects.filter(model_name=model_id)
	
	print('requested_numbers = ', requested_numbers)
	print()
	print()

	current_moment_overloads = update_overload()
		
	context = {'all_truck_models': all_truck_models,
		'all_truck_numbers': all_truck_numbers, 
		'requested_numbers': requested_numbers, 
		#'numbers_count': numbers_count, 
		#'models_count': models_count, 
		#'over': over,
		#'overload': overload,
		#'all_models': all_models,
		}

	


	return render(request, 'car_app/search.html', context)











    


# Models

def models(request):
	all_models = TruckModel.objects.all()
	paginator = Paginator(all_models, 2) 
	page = request.GET.get('page')
	try:
	    models = paginator.page(page)
	except PageNotAnInteger:
	    models = paginator.page(1)
	except EmptyPage:
	    models = paginator.page(paginator.num_pages)
		
	context = {'models': models}	
	return render(request, 'car_app/models.html', {'models': models})


def model_detail(request, pk):
    model_instance = get_object_or_404(TruckModel, pk=pk)
    truck_numbers_for_this_model = model_instance.trucknumber_set.order_by('bort_number')
    print('truck_numbers_for_this_model = ', truck_numbers_for_this_model)

    context = {
        'model_instance': model_instance, 
        'truck_numbers_for_this_model': truck_numbers_for_this_model, 
        }
    return render(request, 'car_app/model_detail.html', context)




def model_new(request):
    if request.method == "POST":
        model_form = TruckModelForm(request.POST)
        if model_form.is_valid():
            model = model_form.save(commit=False)
            model.save()
            return redirect('car_app:model_detail', pk=model.pk)
    else:
        model_form = TruckModelForm()
    return render(request, 'car_app/add_model.html', {'model_form': model_form})
    
    
    

def model_edit(request, pk):
    model = get_object_or_404(TruckModel, pk=pk)
    if request.method == "POST":
        model_form = TruckModelForm(request.POST, instance=model)
        if model_form.is_valid():
            model = model_form.save(commit=False)

            model.save()
            return redirect('car_app:model_detail', pk=model.pk)
    else:
        model_form = TruckModelForm(instance=model)
    
    return render(request, 'car_app/add_model.html', {'model_form': model_form})    
    
    





# Numbers

def numbers(request):
	all_numbers = TruckNumber.objects.all()
	paginator = Paginator(all_numbers, 5) 
	page = request.GET.get('page')
	try:
	    numbers = paginator.page(page)
	except PageNotAnInteger:
	    numbers = paginator.page(1)
	except EmptyPage:
	    numbers = paginator.page(paginator.num_pages)
		
	context = {'models': numbers}	
	return render(request, 'car_app/numbers.html', {'numbers': numbers})
	
	

def number_detail(request, pk):
    print('Number pk = ', pk)
    number_instance = get_object_or_404(TruckNumber, pk=pk)
    print('number_instance = ', number_instance)

    context = {
        'number_instance': number_instance, 
        }
    return render(request, 'car_app/number_detail.html', context)    
    

def number_new(request):
    if request.method == "POST":
        number_form = TruckNumberForm(request.POST)
        if number_form.is_valid():
            number = number_form.save(commit=False)
            # overload
            print('number_new   current_weight = ', number.current_weight)
            print('model number.model_name.id = ', number.model_name.id)
            print('model max_capacity = ', number.model_name.max_capacity)
            current_truck_overload = ((number.current_weight - 
                number.model_name.max_capacity) / number.model_name.max_capacity) * 100
            print()
            print('current_truck_overload = ', current_truck_overload)
            format_current_truck_overload = float('{0:.2f}'.format(current_truck_overload))
            print('format_current_truck_overload = ', format_current_truck_overload)
            print()
            number.overload = format_current_truck_overload
            
            
            number.save()
            return redirect('car_app:number_detail', pk=number.pk)
    else:
        number_form = TruckNumberForm()
    return render(request, 'car_app/add_number.html', {'number_form': number_form})
    
       

def number_edit(request, pk):
    number = get_object_or_404(TruckNumber, pk=pk)
    if request.method == "POST":
        number_form = TruckNumberForm(request.POST, instance=number)
        if number_form.is_valid():
            number = number_form.save(commit=False)
            
            current_truck_overload = ((number.current_weight - 
                number.model_name.max_capacity) / number.model_name.max_capacity) * 100
            number.overload = float('{0:.2f}'.format(current_truck_overload))

            number.save()
            return redirect('car_app:number_detail', pk=number.pk)
    else:
        number_form = TruckNumberForm(instance=number)
    
    return render(request, 'car_app/add_number.html', {'number_form': number_form})    
    
    

# Posts
def posts(request):
	all_posts = Post.objects.order_by('-published_date')
	paginator = Paginator(all_posts, 2) 
	page = request.GET.get('page')
	try:
	    posts = paginator.page(page)
	except PageNotAnInteger:
	    posts = paginator.page(1)
	except EmptyPage:
	    posts = paginator.page(paginator.num_pages)
		
	context = {'posts': posts}	
	return render(request, 'car_app/posts.html', {'posts': posts})
	
	

	
def post_detail(request, pk):
	print('+++++++++++++++++++++++++++')
	print('Receive pk = ', pk)
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'car_app/post_detail.html', {'post': post})  

	
	

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('car_app:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'car_app/post_edit.html', {'form': form})



def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('car_app:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'car_app/post_edit.html', {'form': form})    




