from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import Group, Permission
from .models import User, College, Department, Course, Result, Student,Department_head,Teacher,Student_Result

class CustomUserAdmin(DefaultUserAdmin):
    model = User
    # Add your custom field to the list_display to make it visible on the change list page
    list_display = ('username', 'email', 'role') + DefaultUserAdmin.list_display[2:]
    
    # Add your custom field to the fieldsets to make it editable on the change form page
    fieldsets = DefaultUserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )
    
    # Add your custom field to the add_fieldsets to make it required when adding a new user
    add_fieldsets = DefaultUserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(College)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Result)
admin.site.register(Student)
admin.site.register(Department_head)
admin.site.register(Teacher)
admin.site.register(Student_Result)

