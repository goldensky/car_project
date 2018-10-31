from django.contrib import admin

# Register your models here.


from car_app.models import TruckModel, TruckNumber, Post

# Register your models here.

admin.site.register(Post)


class TruckModelAdmin(admin.ModelAdmin):

    fields = ['model_name', 'max_capacity', 'model_description']
	



class TruckNumberAdmin(admin.ModelAdmin):

    fields = ['bort_number',  'model_name', 'current_weight', 'truck_number_description', 'registration_date', 'current_work_start_date']
	
	
admin.site.register(TruckModel, TruckModelAdmin)
admin.site.register(TruckNumber, TruckNumberAdmin)
