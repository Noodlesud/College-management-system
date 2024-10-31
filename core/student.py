from django.shortcuts import render

def grade_student_view(request):
    students = [
        {'id': 1, 'name': 'John Doe'},
        {'id': 2, 'name': 'Jane Smith'},
        {'id': 3, 'name': 'Alice Johnson'},
        {'id': 4, 'name': 'Michael Brown'},
        {'id': 5, 'name': 'Emily Davis'},
        {'id': 6, 'name': 'David Wilson'},
        {'id': 7, 'name': 'Sophia Martinez'},
        {'id': 8, 'name': 'Chris Lee'},
        {'id': 9, 'name': 'Jessica Taylor'},
        {'id': 10, 'name': 'James Anderson'},
        {'id': 11, 'name': 'Olivia Thomas'},
        {'id': 12, 'name': 'Benjamin Scott'},
        {'id': 13, 'name': 'Emma Harris'},
        {'id': 14, 'name': 'Alexander Lewis'},
        {'id': 15, 'name': 'Charlotte Walker'}
    ]

    context = {'students': students}
    return render(request, 'techer_dashboard.html', context)
