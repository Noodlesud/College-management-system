from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    if request.user.role == 'admin':
        return redirect('admin_dashboard')
    elif request.user.role == 'teacher':
        return redirect('teacher_dashboard')
    elif request.user.role == 'student':
        return redirect('student_dashboard')
    elif request.user.role == 'registrar':
        return redirect('registrar_dashboard')
    elif request.user.role == 'department_head':
        return redirect('department_head_dashboard')
    else:
        # Handle the case where the role is not recognized
        return redirect('home')  # or return a 404, or show an error page
 # or return a 404, or show an error page
