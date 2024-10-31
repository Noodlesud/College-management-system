from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('login/', views.user_login, name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('register-student/', views.register_student, name='register_student'),
    path('teacher/teacher_dashboard/', views.teacher_dashboard, name='teacher/teacher_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('courses_view/', views.courses_view, name='courses_view'),
    path('student_current_course/', views.student_current_course, name='student_current_course'),
    path('grade_approval/', views.grade_approval, name='grade_approval'),

    path('login/', views.logout, name='login'),


    path('registral/registrar_dashboard/', views.registrar_dashboard, name='registrar_dashboard'),
   # path('department_head_dashboard/', views.department_head_dashboard, name='department_head_dashboard'),
    path('info/', views.blog, name='info'),
    path('add-student/', views.add_student_view, name='add_student_view'),
    path('register-new-student/', views.register_new_student, name='register_new_student'),
    path('course-registration/', views.course_registration, name='course_registration'),
    path('course-information/', views.course_information, name='course_information'),
    path('search_students/', views.search_students, name='search_students'),
    path('student_detail/<str:id_number>/', views.student_detail, name='student_detail'),
    path('update_student/<str:id_number>/', views.update_student, name='update_student'),
    path('course_detail/<str:id_number>/<int:year>/<int:semester>/', views.course_detail, name='course_detail'),
   # path('course_filter/<str:department>/<int:year>/<int:semester>/', views.course_filter, name='course_filter'),
    path('enroll/<str:student_id>/<str:course_code>/', views.enrollment, name='enrollment'),
    path('current_course/<str:student_id>/', views.current_course, name='current_course'),
    #
    path('Dep_head/department_head_dashboard/', views.department_head_dashboard, name='Dep_head/department_head_dashboard'),
    path('Dep_head/assign_course/', views.teachers_list, name='assign_course'),
    path('approve-result/', views.approval_teachers_list, name='approval_teachers_list'),

    
    path('search-courses/', views.search_courses, name='search_courses'),
    path('assigning_courses/<str:id_number>/<int:year>/<int:semester>/', views.assigning_courses, name='assigning_courses'),
    path('teacher_current_course/<int:teacher_id>/', views.teacher_current_course, name='teacher_current_course'),
    path('remove_assignment/<int:teacher_id>/<str:course_code>/', views.remove_assigned, name='remove_assignment'),



    path('get_assessments_approval/', views.get_assessments_approval, name='get_assessments_approval'),

    path('Dep_head/assignings/', views.teachers_list, name='assignings'),
    path('assignment/<str:id_number>/<str:course_code>/<str:assigned_class>/', views.assignment, name='assignment'),
    path('search_teachers/', views.search_teachers, name='search_teachers'),
    path('add_assessment/', views.add_assessment, name='add_assessment'),
    path('get-assigned-class/', views.get_assigned_class, name='get_assigned_class'),
    path('add-assessments/', views.add_assessments, name='add_assessments'),
    path('delete-assessments/', views.delete_all_assessments, name='delete_all_assessments'),
    path('get-assessments/', views.get_assessments_by_course_and_class, name='get_assessments_by_course_and_class'),
    path('save-assessments/', views.save_assessments, name='save-assessments'),
    path('assessment-results/', views.assessment_results_list, name='assessment_results_list'),
    path('update-assignment-status/', views.update_assignment_status, name='update_assignment_status'),
    path('update_edit_status/', views.update_edit_status, name='update_edit_status'),

    
    path('request_status/', views.request_status, name='request_status'),
    path('assessments_add/', views.assessments_add, name='assessments_add'),
    # Add other URL patterns as needed
]
