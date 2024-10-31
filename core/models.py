from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.db import models

# Custom User model to handle different roles
class User(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('registrar', 'Registrar'),
        ('department_head', 'Department Head'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=20, choices=ROLES)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class College(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Department(models.Model):
    name = models.CharField(max_length=100)
    college = models.ForeignKey(College, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    
class Course(models.Model):
    SEMESTER_CHOICES = [
        (1, 'Semester 1'),
        (2, 'Semester 2'),
    ]
    YEAR_CHOICES = [
        (1, 'Year 1'),
        (2, 'Year 2'),
         (3, 'Year 3'),
          (4, 'Year 4'),
           (5, 'Year 5'),
    ]
    code = models.CharField(max_length=50, primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    year = models.PositiveIntegerField(choices=YEAR_CHOICES, default=1)
    semester = models.PositiveIntegerField(choices=SEMESTER_CHOICES, default=1)
    credits = models.PositiveIntegerField(default=3)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return f"{self.code}:{self.name}"

class Department_head(models.Model):
    # Define gender choices
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    first_name = models.CharField(max_length=50, default='abebe')
    last_name = models.CharField(max_length=50, default='beso')
    id_number = models.CharField(max_length=20, unique=True, default='0012')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='male')
    email = models.EmailField(unique=True, default='department_head@email.com')
    mobile_number = models.CharField(max_length=10, default='0912345678')

    def save(self, *args, **kwargs):
        # Check if a User with the same id_number as username already exists
        if User.objects.filter(username=self.id_number).exists():
            # If user exists, do not create a Teacher object
            print("User with this ID already exists. Teacher object not created.")
            return  # Skip the creation of the Teacher object

        # If user does not exist, create a new User object
        user = User.objects.create(
            username=self.id_number,  # Use id_number as username
            role='department_head',  # Assign role as 'teacher'
        )
        user.set_password("123456")  # Set default password
        user.save()

        # Proceed to create and save the Teacher object
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.id_number})"

class Assignment(models.Model):
    CLASS_CHOICES = [
         ('-', 'freshman'),
        ('A', 'Class A'),
        ('B', 'Class B'),
        ('C', 'Class C'),
        ('D', 'Class D'),
    ]
    teacher_id = models.CharField(max_length=20)
    assigned_class = models.CharField(max_length=1, choices=CLASS_CHOICES, default='A')
    course_code = models.CharField(max_length=50)
    status = models.CharField(max_length=50,default='editable')

    date_enrolled = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('teacher_id', 'course_code')

    def __str__(self):
        return f"{self.teacher_id} - {self.course_code}"

class Student(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    
    STUDENT_YEAR_CHOICES = [
         (0, 'freshman'),
        (1, 'Year 1'),
        (2, 'Year 2'),
        (3, 'Year 3'),
        (4, 'Year 4'),
        (5, 'Year 5'),
    ]

    STUDENT_SEMESTER_CHOICES = [
        (0, 'freshman'),
        (1, 'Semester 1'),
        (2, 'Semester 2'),
    ]

    CLASS_CHOICES = [
         ('-', 'freshman'),
        ('A', 'Class A'),
        ('B', 'Class B'),
        ('C', 'Class C'),
        ('D', 'Class D'),
    ]
    role = models.CharField(max_length=50, default='Student')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    id_number = models.CharField(max_length=20, unique=True)
    registration_date = models.DateField()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=10)
    gpa = models.CharField(max_length=10,default='0.0')
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    password = models.CharField(max_length=50,default='12345678')
    year = models.IntegerField(choices=STUDENT_YEAR_CHOICES, default='0')
    semester = models.IntegerField(choices=STUDENT_SEMESTER_CHOICES, default='0')
    student_class = models.CharField(max_length=1, choices=CLASS_CHOICES, default='-')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.id_number})"
        
class Teacher(models.Model):
    # Define gender choices
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    first_name = models.CharField(max_length=50,null=True)
    last_name = models.CharField(max_length=50,null=True)
    id_number = models.CharField(max_length=20, unique=True,null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES,null=True)
    email = models.EmailField(unique=True,null=True)
    mobile_number = models.CharField(max_length=10,null=True)

    def save(self, *args, **kwargs):
        # Check if a User with the same id_number as username already exists
        if User.objects.filter(username=self.id_number).exists():
            # If user exists, do not create a Teacher object
            print("User with this ID already exists. Teacher object not created.")
            return  # Skip the creation of the Teacher object

        # If user does not exist, create a new User object
        user = User.objects.create(
            username=self.id_number,  # Use id_number as username
            role='teacher',  # Assign role as 'teacher'
        )
        user.set_password("123456")  # Set default password
        user.save()

        # Proceed to create and save the Teacher object
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.id_number})"
    
class Registrar(models.Model):
    #id = models.CharField(max_length=50, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}"


class Enrollment(models.Model):
    student_id = models.CharField(max_length=20)
    course_code = models.CharField(max_length=50)
    date_enrolled = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student_id', 'course_code')

    def __str__(self):
        return f"{self.student_id} - {self.course_code}"

class Assessment_holding(models.Model):
    teacher = models.CharField(max_length=20)
    course_code = models.CharField(max_length=50)
    assigned_class = models.CharField(max_length=50)
    assessment_data = models.CharField(max_length=255)
    date_enrolled = models.DateTimeField(auto_now_add=True)

    

    def __str__(self):
        return f"{self.course_code} - {self.teacher}"
        
class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.student.user.username} - {self.course.name}: {self.grade}"

class Assessment_result(models.Model):
    student_id = models.CharField(max_length=20)
    course_code = models.CharField(max_length=50)
    assessment=models.CharField(max_length=50)
    assigned_class=models.CharField(max_length=50)
    teacher_id=models.CharField(max_length=50)
    result=models.CharField(max_length=10,default='0')
    date_enrolled = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_id} - {self.course_code}"
class Assessment_edit(models.Model):
    course_code = models.CharField(max_length=50)
    assigned_class=models.CharField(max_length=50)
    teacher_id=models.CharField(max_length=50)
    request_status=models.CharField(max_length=10)
    date_enrolled = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_id} - {self.course_code}"

class Student_Result(models.Model):
    course_code = models.CharField(max_length=50)
    assigned_class=models.CharField(max_length=50)
    student_id=models.CharField(max_length=50)
    result=models.CharField(max_length=10)
    assessment=models.CharField(max_length=10)

    date_enrolled = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_id} - {self.course_code}"
