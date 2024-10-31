from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import User,Teacher
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from .forms import StudentCreationForm
from .models import Student, Department,Course,Enrollment,Assessment_holding,Assessment_edit,Student_Result  # Import the Department model
from django.contrib import messages 
from .models import Assignment,Department_head,Teacher
from django.db.models import Q
from json import loads, dumps
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.views.decorators.http import require_POST, require_http_methods
from django.template.loader import render_to_string

def home(request):
    return render(request, 'login.html')

def blog(request):
   # teachers = Teacher.objects.all()
   # courses = Course.objects.all()

    return render(request, 'blog.html') #{ 'Teachers': teachers, 'Courses': courses})
# @login_required
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            print(user.role)
            if user.role == "student":
                return redirect('student_dashboard')
            elif user.role == "teacher":
                return redirect('teacher/teacher_dashboard')
            elif user.role == "registrar":
                return redirect('registrar_dashboard')
            elif user.role == "department_head":
                return redirect('Dep_head/department_head_dashboard')
            else:
                return redirect('index')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def logout(request):

    return render(request, 'login.html')

@login_required
def student_dashboard(request):
    student = get_object_or_404(Student, id_number=request.user.username)

    return render(request, 'student/student_dashboard.html',{'student': student})

from django.shortcuts import get_object_or_404, render
from .models import Student, Course, Student_Result

def courses_view(request):
    # Fetch the student
    student = get_object_or_404(Student, id_number=request.user.username)
    
    # Get the department of the student
    department_name = student.department
    
    # Fetch all courses for the student's department, ordered by year and semester
    courses = Course.objects.filter(department=department_name).order_by('year', 'semester')
    
    # Fetch all Student_Result entries where student_id matches the logged-in student's username
    # and course_code matches the courses in the student's department
    student_results = Student_Result.objects.filter(
        student_id=request.user.username,
        course_code__in=courses.values_list('code', flat=True)
    )
    
    # Prepare context with the courses and results
    context = {
        'courses': courses,
        'student': student,
        'student_results': student_results,
    }
    
    return render(request, 'student/courses_view.html', context)

from django.shortcuts import get_object_or_404, render
from .models import Student, Enrollment, Course, Student_Result

def student_current_course(request):
    # Fetch the student
    student = get_object_or_404(Student, id_number=request.user.username)
    
    # Fetch all enrollments for the student
    enrollments = Enrollment.objects.filter(student_id=request.user.username)
    
    # Extract course codes from enrollments
    enrolled_course_codes = enrollments.values_list('course_code', flat=True)
    
    # Fetch courses corresponding to the enrolled course codes
    courses = Course.objects.filter(code__in=enrolled_course_codes)
    
    # Fetch all Student_Result entries where student_id matches the logged-in student's username
    # and course_code matches the enrolled courses
    student_results = Student_Result.objects.filter(
        student_id=request.user.username,
        course_code__in=enrolled_course_codes
    )
    
    context = {
        'student': student,
        'courses': courses,
        'student_results': student_results,
    }
    
    return render(request, 'student/current_course.html', context)


def add_student_view(request):
    if request.method == "POST":
        id_number = request.POST.get('id_number')
        email = request.POST.get('email')

        # Check if the student ID number already exists
        if Student.objects.filter(id_number=id_number).exists():
            return JsonResponse({'status': 'error', 'message': "A student with this ID number already exists."})

        # Check if the email already exists
        if Student.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'message': "An account with this email address already exists."})
            # If user exists, do not create a Teacher object

        # If user does not exist, create a new User object
        
        
        # Proceed to create the student if no duplicates are found
        Student.objects.create(
            role='Student',
            first_name=request.POST.get('first-name'),
            last_name=request.POST.get('last-name'),
            id_number=id_number,
            registration_date=request.POST.get('registration-date'),
            department_id=request.POST.get('department'),
            gender=request.POST.get('gender'),
            date_of_birth=f"{request.POST.get('year')}-{request.POST.get('month')}-{request.POST.get('day')}",
            email=email,
            mobile_number=request.POST.get('mobile'),
            city=request.POST.get('city'),
            country=request.POST.get('country'),
            year='0',
            semester='0',
            student_class='-',
            gpa='0.0',
        )
        user = User.objects.create(
            username=id_number,  # Use id_number as username
            role='student',  # Assign role as 'teacher'
        )
        user.set_password("123456")  # Set default password
        user.save()

        return JsonResponse({'status': 'success', 'message': "Student added successfully!"})

    department = Department.objects.all()
    return render(request, 'registral/add_student.html', {'department': department})
    if request.method == "POST":
        id_number = request.POST.get('id_number')
        if Student.objects.filter(id_number=id_number).exists():
            messages.error(request, "A student with this ID number already exists.")
            return redirect('add_student_view')  # Redirect to the view name instead of the template path
        
        # Proceed to create the student if no duplicate is found
        Student.objects.create(
            role='Student',
            first_name=request.POST.get('first-name'),
            last_name=request.POST.get('last-name'),
            id_number=id_number,
            registration_date=request.POST.get('registration-date'),
            department_id=request.POST.get('department'),
            gender=request.POST.get('gender'),
            date_of_birth=f"{request.POST.get('year')}-{request.POST.get('month')}-{request.POST.get('day')}",
            email=request.POST.get('email'),
            mobile_number=request.POST.get('mobile'),
            city=request.POST.get('city'),
            country=request.POST.get('country'),
            year='0',
            semester='0',
            student_class='-',
            gpa='0.0',
        )
        messages.success(request, "Student added successfully!")

        return redirect('add_student_view')  # Redirect to the view name instead of the template path
    
    department = Department.objects.all()

    return render(request, 'registral/add_student.html', {'department': department})

def enrollment(request, student_id, course_code):
    try:
        # Attempt to create the enrollment
        Enrollment.objects.create(
            student_id=student_id,
            course_code=course_code,
        )
        return JsonResponse({'status': 'success', 'message': 'Student added successfully!'})

    except IntegrityError:
        # Handle the case where the unique constraint is violated
        return JsonResponse({'status': 'error', 'message': 'Student is already enrolled in this course'}, status=400)

    except Exception as e:
        # Handle other potential errors
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def search_students(request):
    query = request.GET.get('query', '')
    if query:
        students = Student.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(id_number__icontains=query)
        )

        results = [
            {
                'id_number': student.id_number,
                'first_name': student.first_name,
                'last_name': student.last_name,
               
            }
            for student in students
        ]
    else:
        results = []

    return JsonResponse(results, safe=False)


from django.shortcuts import get_object_or_404, render
from .models import Student, Enrollment, Course

def current_course(request, student_id):
    # Fetch the student
    student = get_object_or_404(Student, id_number=student_id)
    
    # Fetch all enrollments for the student
    enrollments = Enrollment.objects.filter(student_id=student_id)
    
    # Extract course codes from enrollments
    enrolled_course_codes = enrollments.values_list('course_code', flat=True)
    
    # Fetch courses corresponding to the enrolled course codes
    courses = Course.objects.filter(code__in=enrolled_course_codes)
    
    context = {
        'student': student,
        'courses': courses,
    }
    
    return render(request, 'registral/current_course.html', context)

def register_new_student(request):
    students = Student.objects.all()
    return render(request, 'registral/register_new_student.html', {'students': students})

def course_registration(request):
    students = Student.objects.all()
    return render(request, 'registral/course_registration.html', {'students': students})



from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string

def course_detail(request, id_number, year, semester):
    student = get_object_or_404(Student, id_number=id_number)
    enrollments = Enrollment.objects.filter(student_id=id_number)

    # Filter courses for the specified year and semester
    filtered_courses = Course.objects.filter(
        department=student.department,
        year=year,
        semester=semester
    )

    # Set of enrolled course codes
    enrolled_courses = {enrollment.course_code for enrollment in enrollments}

    context = {
        'student': student,
        'filtered_courses': filtered_courses,
        'enrolled_courses': enrolled_courses,
    }

    # Check if the request is an AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('registral/course_table.html', context)
        return JsonResponse({'html': html})

    return render(request, 'registral/course_add.html', context)

def course_filter(request, department, year, semester):
    # Fetch courses based on department, year, and semester
    filtered_courses = Course.objects.filter(
        department__name=department, 
        year=year, 
        semester=semester
    )

    # Return only the table rows for the filtered courses
    return render(request, 'registral/course_table.html', {'filtered_courses': filtered_courses})

def student_detail(request, id_number):
    student = get_object_or_404(Student, id_number=id_number)
    return render(request, 'registral/student_detail.html', {
        'student': student,
    })

def update_student(request, id_number):
    student = get_object_or_404(Student, id_number=id_number)
    if request.method == 'POST':
        student.year = request.POST.get('year')
        student.semester = request.POST.get('semester')
        student.student_class = request.POST.get('class')
        student.save()
        return redirect('student_detail', id_number=student.id_number)
    return render(request, 'registral/student_detail.html', {
        'student': student,
    })

def course_information(request):
    return render(request, 'course_information.html')
def course_assign_view(request):
     teachers = Teacher.objects.filter(user.role=='teacher')
    # Fetch the user with the role 'teacher'
     return render(request, 'department_head_dashboard.html', {'teachers': teachers})
     
@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')



@login_required

def registrar_dashboard(request):
    return render(request, 'registral/registrar_dashboard.html')  # Correct path to the template

##################### department head
@login_required
def department_head_dashboard(request):
    department = get_object_or_404(Department_head, id_number=request.user.username)

    return render(request, 'Dep_head/department_head_dashboard.html',{'department': department})

def assignment(request, id_number, course_code,assigned_class):
    try:
        # Attempt to create the assignment
        Assignment.objects.create(
            teacher_id=id_number,
            course_code=course_code,
            assigned_class=assigned_class
        )
        return JsonResponse({'status': 'success', 'message': 'teacher assigned successfully!'})

    except IntegrityError:
        # Handle the case where the unique constraint is violated
        return JsonResponse({'status': 'error', 'message': 'teacher is already assigned in this course'}, status=400)

    except Exception as e:
        # Handle other potential errors
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def search_teachers(request):
    query = request.GET.get('query', '')
    if query:
        teachers = Teacher.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(id_number__icontains=query)
        )

        results = [
            {
                'id_number': teacher.id_number,
                'first_name': teacher.first_name,
                'last_name': teacher.last_name,
               
            }
            for teacher in teachers
        ]
    else:
        results = []

    return JsonResponse(results, safe=False)

def teacher_current_course(request, teacher_id):
    # Fetch the teacher
    teacher = get_object_or_404(Teacher, id_number=teacher_id)
    department = get_object_or_404(Department_head, id_number=request.user.username)
    teachers = Teacher.objects.filter(department=department.department)

    # Fetch all assignments for the teacher
    assignments = Assignment.objects.filter(teacher_id=teacher_id)
    
    # Extract course codes from assignments
    assigned_course_codes = assignments.values_list('course_code', flat=True)
    
    # Fetch courses corresponding to the enrolled course codes
    courses = Course.objects.filter(code__in=assigned_course_codes)  # Corrected field name
    
    context = {
        'teacher': teacher,
        'courses': courses,
        'department' : department,
        'teachers':teachers,
    }
    html = render_to_string('Dep_head/assigned_course_show.html', {'courses': courses})
    
    return JsonResponse({'html': html})

@require_http_methods(["GET"])
def search_courses(request):
    query = request.GET.get('q', '')
    year = request.GET.get('year', '')
    semester = request.GET.get('semester', '')

    courses = Course.objects.all()

    if query:
        courses = courses.filter(Q(name__icontains=query) | Q(code__icontains=query))
    if year:
        courses = courses.filter(year=year)
    if semester:
        courses = courses.filter(semester=semester)

    courses_data = [
        {
            'code': course.code,
            'name': course.name,
            'year': course.get_year_display(),
            'semester': course.get_semester_display(),
        }
        for course in courses
    ]

    return JsonResponse({'courses': courses_data})

def assigned_course_detail(request, id_number, year, semester):
    teacher = get_object_or_404(Teacher, id_number=id_number)
    assignments = Assignment.objects.filter(teacher_id=id_number)

    # Filter courses for the specified year and semester
    ass_filtered_courses = Course.objects.filter(
        department=teacher.department,
        year=year,
        semester=semester
    )

    # Set of assigned course codes
    assigned_courses = {assignment.course_code for assignment in assignments}
   
    context = {
        'teacher': teacher,
        'ass_filtered_courses':ass_filtered_courses,  # Corrected variable name
        'assigned_courses': assigned_courses,
    }

    # Check if the request is an AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('Dep_head/assigned_course_show.html', context)
        return JsonResponse({'html': html})

    return render(request, 'Dep_head/course_assign.html', context)

def assignment_course_filter(request, department, year, semester):
    # Fetch courses based on department, year, and semester
    ass_filtered_courses = Course.objects.filter(   
        department__name=department, 
        year=year, 
        semester=semester
    )

    # Return only the table rows for the filtered courses
    return render(request, 'Dep_head/assigned_course_show.html', {'ass_filtered_courses':ass_filtered_courses})

def teachers_list(request):
    department = get_object_or_404(Department_head, id_number=request.user.username)
    teachers = Teacher.objects.filter(department=department.department)

    context={
    'department' : department,
    'teachers':teachers,
    }
    return render(request, 'Dep_head/assign_course.html', context)

def approval_teachers_list(request):
    department = get_object_or_404(Department_head, id_number=request.user.username)

    # Filter assignments with status 'uneditable'
    approval = Assignment.objects.filter(status='uneditable')

    # Extract teacher IDs from the assignments
    teacher_ids = approval.values_list('teacher_id', flat=True)

    # Get teacher objects based on the extracted teacher IDs
    teachers = Teacher.objects.filter(id_number__in=teacher_ids)

    context = {
        'approval': approval,
        'department': department,
        'teachers': teachers,
    }
    
    return render(request, 'Dep_head/Approve_result.html', context)


def assigning_courses(request, id_number,year ,semester):
    department = get_object_or_404(Department_head, id_number=request.user.username)
    teacher = get_object_or_404(Teacher, id_number=id_number)

    enrollments = Assignment.objects.all()

    assignments = Assignment.objects.filter(teacher_id=id_number)
    
    # Extract course codes from assignments
    assigned_course_codes = assignments.values_list('course_code', flat=True)
    courses = Course.objects.filter(code__in=assigned_course_codes)  # Corrected field name

    # Filter courses for the specified year and semester
    filtered_courses = Course.objects.filter(
        department=department.department,
        year=year,
        semester=semester
    )

    # Set of enrolled course codes
    enrolled_courses = {enrollment.course_code for enrollment in enrollments}

    context = {
        'courses': courses,
        'department' : department,
        'assignments':assignments,
        'teacher': teacher,
        'filtered_courses': filtered_courses,
        'enrolled_courses': enrolled_courses,
    }

    # Check if the request is an AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('Dep_head/course_table.html', context)
        return JsonResponse({'html': html})

    return render(request, 'Dep_head/assigning_courses.html', context)

def remove_assigned(request, teacher_id, course_code):
    if request.method == 'DELETE':
        try:
            # Fetch the assignment by teacher_id and course_code
            assignment = Assignment.objects.get(teacher_id=teacher_id, course_code=course_code)
            assignment.delete()  # Delete the found assignment
            return JsonResponse({'message': 'Course successfully removed.'})
        except Assignment.DoesNotExist:
            return JsonResponse({'message': 'Assignment not found.'}, status=404)
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=400)
@login_required
def register_student(request):
    if request.method == 'POST':
        #GET THE JSON DATA
        print(loads(request.body))
        data = loads(request.body)
        User.objects.create_user(username=data.get('username'), password=data.get('password'), role='student')
        return redirect('registrar_dashboard')
    else:
        form = StudentCreationForm()
    return render(request, 'register_student.html')

####################Teacher
@login_required
def teacher_dashboard(request):
    teacher = get_object_or_404(Teacher, id_number=request.user.username)

    # Retrieve choices from the Student model
    classes = Student.CLASS_CHOICES
    years = Student.STUDENT_YEAR_CHOICES
    semesters = Student.STUDENT_SEMESTER_CHOICES  # Define semester options here or fetch from a model if dynamic

    # Default filter values
    student_class = request.GET.get('class', None)
    year = request.GET.get('year', None)
    semester = request.GET.get('semester', None)

    students = Student.objects.none()
    print(f"Filter values - Class: {student_class}, Year: {year}, Semester: {semester}")

    if student_class or year or semester:
        students = Student.objects.all()
    # Filter students based on class, year, and semester
        if student_class:
            students = students.filter(student_class=student_class)
        if year:
            students = students.filter(year=year)
        if semester:
            students = students.filter(semester=semester)

    return render(request, 'teacher/teacher_dashboard.html', {
        'teacher': teacher,
        'students': students,
        'classes': classes,
        'years': years,
        'semesters': semesters,
        'selected_class': student_class,
        'selected_year': year,
        'selected_semester': semester,
    })

from django.forms import formset_factory

 # Adjust the import to match your model structure
def add_assessment(request):
    teacher = Teacher.objects.get(id_number=request.user.username)
    assignments = Assignment.objects.filter(teacher_id=teacher.id_number)
    assigned_course_codes = assignments.values_list('course_code', flat=True)
    courses = Course.objects.filter(code__in=assigned_course_codes)  # Corrected field name


    
    return render(request, 'teacher/assign_course.html', { 'courses': courses,'teacher':teacher,'assignments':assignments})

def get_assigned_class(request):
    course_code = request.GET.get('course_code')
    
    # Retrieve assigned classes for the selected course from the Assignment model
    if course_code:
        assigned_classes = Assignment.objects.filter(course_code=course_code).values_list('assigned_class', flat=True)
        return JsonResponse({'assigned_classes': list(assigned_classes)})
    
    return JsonResponse({'assigned_classes': []})


def add_assessments(request):
    if request.method == 'POST':
        course_code = request.POST.get('course')
        assigned_class = request.POST.get('assigned_class')
        formatted_assessments = request.POST.get('formatted_assessments')
        teacher = request.user.username


        if course_code and assigned_class and formatted_assessments:
            try:
                # Retrieve the course instance (assuming course code is unique)
                course = Course.objects.get(code=course_code)

                # Check if an assessment already exists for the teacher, course, and assigned class
                
                Assessment_holding.objects.update_or_create(
                teacher=teacher,
                course_code=course_code,
                assigned_class=assigned_class,
                defaults={
                    'assessment_data': formatted_assessments,
                    }
                )
                    # Create and save the new assessment entry
                   # Assessment_holding.objects.create(
                   #     teacher=teacher,
                   #     course_code=course_code,
                   #     assigned_class=assigned_class,
                   #     assessment_data=formatted_assessments  # Remove any extra whitespace
                    #)
                    # Success message
                messages.success(request, "Assessments added successfully!")

            except Course.DoesNotExist:
                messages.error(request, "Course not found.")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")

        else:
            messages.error(request, "All fields are required.")

    # Handle GET request or form display
    teacher = Teacher.objects.get(id_number=request.user.username)
    assignments = Assignment.objects.filter(teacher_id=teacher.id_number)
    assigned_course_codes = assignments.values_list('course_code', flat=True)
    courses = Course.objects.filter(code__in=assigned_course_codes)  # Corrected field name

    context = {
        'courses': courses,
        'teacher': teacher  # Default or based on some logic
    }
    return render(request, 'teacher/assign_course.html', context)

def gett_assigned_class(request):
    course_code = request.GET.get('course_code')
    
    # Retrieve assigned classes for the selected course from the Assignment model
    if course_code:
        assigned_classes = Assignment.objects.filter(course_code=course_code).values_list('assigned_class', flat=True)
        assessment=Assessment_holding.object.filter(assigned_class=assigned_classes, course_code=course_code)
    return render(request, 'teacher/assign_course.html', {'assessment':assessment})
    
    return JsonResponse({'assigned_classes': []})
def delete_all_assessments(request):
    if request.method == 'POST':
        try:
            Assessment_edit.objects.all().delete()
            messages.success(request, "All assessments have been deleted successfully.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    teacher = Teacher.objects.get(id_number=request.user.username)
    assignments = Assignment.objects.filter(teacher_id=teacher.id_number)
    assigned_course_codes = assignments.values_list('course_code', flat=True)
    courses = Course.objects.filter(code__in=assigned_course_codes)  # Corrected field name
    
    context = {
        'courses': courses,
        'teacher': teacher  # Default or based on some logic
    }
    return render(request, 'teacher/assign_course.html', context)


from django.http import JsonResponse
from .models import Assessment_holding

from django.http import JsonResponse
from .models import Assessment_holding,Assessment_result

def get_assessments_by_course_and_class(request):
    course_code = request.GET.get('course_code')
    assigned_class = request.GET.get('assigned_class')
    teacher = request.user.username

    try:
        # Fetch assessment details
        assessment = Assessment_holding.objects.get(course_code=course_code, assigned_class=assigned_class)
        students = Enrollment.objects.filter(course_code=course_code).values('student_id')
        assignment = Assignment.objects.get(teacher_id=request.user.username, assigned_class=assigned_class, course_code=course_code)
        status = assignment.status

        student_data = []
        for student in students:
            student_instance = Student.objects.get(id_number=student['student_id'])
            student_data.append({
                'id_number': student_instance.id_number,
                'name': f"{student_instance.first_name} {student_instance.last_name}",
                'department': {'name': student_instance.department.name},
                'assessment_marks': []  # Initialize an empty list for marks
            })

        # Fetch assessment results for each student
        assessment_results = Assessment_result.objects.filter(
            course_code=course_code, assigned_class=assigned_class, teacher_id=teacher
        )

        # Prepare assessment marks for each student
        for student in student_data:
            result_entry = assessment_results.filter(student_id=student['id_number']).first()
            if result_entry:
                # Split assessment string into individual assessments
                assessments = result_entry.assessment.split(';')
                student['assessment_marks'] = assessments  # Store assessments in the student data

        # Split the assessment data into an array
        assessment_data_array = assessment.assessment_data.split(';')

        data = {
            'status':status,
            'assessment_data': assessment_data_array,  # Send as an array
            'course_code': assessment.course_code,
            'assigned_class': assessment.assigned_class,
            'teacher': assessment.teacher,
            'students': student_data,
        }
        return JsonResponse({'assessment': data})
    except Assessment_holding.DoesNotExist:
        return JsonResponse({'error': 'No assessment found for the selected course and class.'})

def assessments_add(request):
    teacher = Teacher.objects.get(id_number=request.user.username)
    assignments = Assignment.objects.filter(teacher_id=teacher.id_number)
    assigned_course_codes = assignments.values_list('course_code', flat=True)
    courses = Course.objects.filter(code__in=assigned_course_codes)  # Corrected field name

    context = {
        'courses': courses,
        'teacher': teacher  # Default or based on some logic
    }
    return render(request, 'teacher/assigned_course_show.html', context)
# Each assessment is like "assessment-1:50=40"
                # assessment_name, value = assessment.split('=')
                #value = int(value)  # Convert mark value to an integer

                # You may want to split the assessment name to extract details
               # assessment_title, max_score = assessment_name.split(':')
               # max_score = int(max_score)
from django.http import JsonResponse
from .models import Assessment_result  # Adjust the import according to your project structure
import json

from django.http import JsonResponse
import json
from .models import Assessment_result  # Ensure your model is correctly imported

def save_assessments(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse the JSON body
            assessments = data.get('assessments')
            saved_data = []  # List to store saved assessments

            for assessment_data in assessments:
                student_id = assessment_data.get('student_id')
                formatted_assessments = assessment_data.get('assessments')
                result = assessment_data.get('result')
                course_code = data.get('course_code')
                assigned_class = data.get('assigned_class')

                # Debugging information
                print("Processing Assessment Result:")
                print(f"Student ID: {student_id}")
                print(f"Teacher ID: {request.user.username}")
                print(f"Course: {course_code}")
                print(f"Assigned Class: {assigned_class}")
                print(f"Assessments: {formatted_assessments}")
                print(f"Result: {result}")

                if not (student_id and formatted_assessments and course_code and assigned_class):
                    print("Missing data; skipping this entry.")
                    continue  # Skip this entry if any required data is missing

                # Check if the assessment result already exists
                assessment_result, created = Assessment_result.objects.update_or_create(
                    student_id=student_id,
                    teacher_id=request.user.username,
                    course_code=course_code,
                    assigned_class=assigned_class,
                    defaults={
                        'assessment': formatted_assessments,
                        'result': result
                    }
                )
                
                if created:
                    print(f"Created new assessment for Student ID: {student_id}.")
                else:
                    print(f"Updated existing assessment for Student ID: {student_id}.")

                # Append the saved assessment data to the list
                saved_data.append({
                    'student_id': student_id,
                    'teacher_id': request.user.username,
                    'course': course_code,
                    'assigned_class': assigned_class,
                    'assessment': formatted_assessments,
                    'result': result
                })

            # Format the saved_data as a string
            saved_data_string = "\n".join([f"Student ID: {item['student_id']}, Teacher ID: {item['teacher_id']}, Course: {item['course']}, Assigned Class: {item['assigned_class']}, Assessment: {item['assessment']}, Result: {item['result']}" for item in saved_data])

            return JsonResponse({
                'status': 'success',
                'message': 'Assessments saved successfully!',
                'saved_data': saved_data_string
            })
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



def assessment_results_list(request):
    # Retrieve all assessment results from the database
    assessment_results = Assessment_result.objects.all()
    teacher = Teacher.objects.get(id_number=request.user.username)
    status = Assignment.objects.filter(teacher_id=request.user.username).values('status')

    # Pass the data to the template
    return render(request, 'teacher/current_course.html', {'assessment_results': assessment_results,'teacher':teacher,'status':status})
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def update_assignment_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        teacher=request.user.username
        course_code = data.get('course_code')
        assigned_class = data.get('assigned_class')
        status = data.get('status')

        # Update the status in your Assignment table here
        try:
            # Assuming you have an Assignment model with these fields
            Assignment.objects.filter(course_code=course_code,teacher_id=teacher, assigned_class=assigned_class).update(status=status)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

from django.http import JsonResponse
from .models import Assessment_edit
import json

def request_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        teacher = request.user.username
        course_code = data.get('course_code')
        assigned_class = data.get('assigned_class')

        try:
            # Check if the request already exists
            existing_request = Assessment_edit.objects.filter(
                course_code=course_code,
                teacher_id=teacher,
                assigned_class=assigned_class,
                request_status='edit_request'  # Ensure to check for the same status
            ).exists()

            if existing_request:
                return JsonResponse({'status': 'error', 'message': 'Request already exists'})

            # If no existing request, create a new one
            Assessment_edit.objects.create(
                course_code=course_code,
                teacher_id=teacher,
                assigned_class=assigned_class,
                request_status='edit_request',
            )

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
def get_assessments_approval(request):
    course_code = request.GET.get('course_code')
    assigned_class = request.GET.get('assigned_class')
    teacher_id = request.GET.get('teacher_id')

    try:
        # Fetch assessment details
        assessment = Assessment_holding.objects.get(course_code=course_code, assigned_class=assigned_class)
        students = Enrollment.objects.filter(course_code=course_code).values('student_id')
        assignment = Assignment.objects.get(teacher_id=teacher_id, assigned_class=assigned_class, course_code=course_code)
        status = assignment.status
        
        # Check if edit request exists and set approval status
        try:
            edit_approval = Assessment_edit.objects.get(course_code=course_code, teacher_id=teacher_id, assigned_class=assigned_class)
            edit_approval_status = edit_approval.request_status
        except Assessment_edit.DoesNotExist:
            edit_approval_status = 'no_edit_request'  # Set to 'no_edit_request' if not found

        student_data = []
        for student in students:
            student_instance = Student.objects.get(id_number=student['student_id'])
            student_data.append({
                'id_number': student_instance.id_number,
                'name': f"{student_instance.first_name} {student_instance.last_name}",
                'department': {'name': student_instance.department.name},
                'assessment_marks': []  # Initialize an empty list for marks
            })

        # Fetch assessment results for each student
        assessment_results = Assessment_result.objects.filter(
            course_code=course_code, assigned_class=assigned_class, teacher_id=teacher_id
        )

        # Prepare assessment marks for each student
        for student in student_data:
            result_entry = assessment_results.filter(student_id=student['id_number']).first()
            if result_entry:
                # Split assessment string into individual assessments
                assessments = result_entry.assessment.split(';')
                student['assessment_marks'] = assessments  # Store assessments in the student data

        # Split the assessment data into an array
        assessment_data_array = assessment.assessment_data.split(';')

        data = {
            'edit_approval_status': edit_approval_status,  # Send edit approval status
            'status': status,
            'assessment_data': assessment_data_array,  # Send as an array
            'course_code': assessment.course_code,
            'assigned_class': assessment.assigned_class,
            'teacher': assessment.teacher,
            'students': student_data,
        }
        return JsonResponse({'assessment': data})

    except Assessment_holding.DoesNotExist:
        return JsonResponse({'error': 'No assessment found for the selected course and class.'})



@csrf_exempt  # Use this if you're not using CSRF tokens; otherwise, remove this line.
def update_edit_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            teacher = data.get('teacher_id')
            course_code = data.get('course_code')
            assigned_class = data.get('assigned_class')
            status = data.get('status')

            # Delete the existing Assessment_edit object, if it exists
            Assessment_edit.objects.filter(course_code=course_code, teacher_id=teacher, assigned_class=assigned_class).delete()

            # Update the status in the Assignment table
            Assignment.objects.filter(course_code=course_code, teacher_id=teacher, assigned_class=assigned_class).update(status=status)

            return JsonResponse({'status': 'success'})
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def grade_approval(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse the JSON body
            assessments = data.get('assessments')
            saved_data = []  # List to store saved assessments

            for assessment_data in assessments:
                student_id = assessment_data.get('student_id')
                formatted_assessments = assessment_data.get('assessments')
                result = assessment_data.get('result')
                course_code = data.get('course_code')
                assigned_class = data.get('assigned_class')

                # Debugging information
                print("Processing Assessment Result:")
                print(f"Student ID: {student_id}")
                print(f"Course: {course_code}")
                print(f"Assigned Class: {assigned_class}")
                print(f"Assessments: {formatted_assessments}")
                print(f"Result: {result}")

                if not (student_id and formatted_assessments and course_code and assigned_class):
                    print("Missing data; skipping this entry.")
                    continue  # Skip this entry if any required data is missing

                # Check if the assessment result already exists
                assessment_result, created = Student_Result.objects.update_or_create(
                    student_id=student_id,
                    course_code=course_code,
                    assigned_class=assigned_class,
                    defaults={
                        'assessment': formatted_assessments,
                        'result': result
                    }
                )


                created = Student_Result.objects.update_or_create(
                    student_id=student_id,
                    course_code=course_code,
                    assigned_class=assigned_class,
                    assessment= formatted_assessments,
                    result= result
                    
                )
                
                if created:
                    print(f"Created new assessment for Student ID: {student_id}.")
                else:
                    print(f"Updated existing assessment for Student ID: {student_id}.")

                # Append the saved assessment data to the list
                saved_data.append({
                    'student_id': student_id,
                    'teacher_id': request.user.username,
                    'course': course_code,
                    'assigned_class': assigned_class,
                    'assessment': formatted_assessments,
                    'result': result
                })

            # Format the saved_data as a string
            saved_data_string = "\n".join([f"Student ID: {item['student_id']}, Teacher ID: {item['teacher_id']}, Course: {item['course']}, Assigned Class: {item['assigned_class']}, Assessment: {item['assessment']}, Result: {item['result']}" for item in saved_data])

            return JsonResponse({
                'status': 'success',
                'message': 'Assessments saved successfully!',
                'saved_data': saved_data_string
            })
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


