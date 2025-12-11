from django.shortcuts import get_object_or_404, redirect, render

from student_info.models import Student

from django.db.models import Q

# Create your views here.

def home(request):
    
    return render(request, 'index.html')

def add_student(request):
    if request.method == "POST":
        Student.objects.create(
        name = request.POST.get('name'),
        email = request.POST.get('email'),
        image = request.FILES.get('image')
    )
        return redirect('show_student')
     
    return render(request, 'student/add_student.html')




def show_student(request):
    
    query = request.GET.get('q')
    
    data = Student.objects.all()
    
    if query:
        data = Student.objects.filter(
            Q(name__icontains = query)|
            Q(email__icontains = query)
            )
    
    
    # Order
    order = request.GET.get('order')
    
    if order == 'asc':
        data = Student.objects.order_by('name')
        
    elif order == 'desc':
        data = Student.objects.order_by('-name')
        
        
    context = {
        "students": data
    }
    
    return render(request, 'student/show_student.html', context)

def edit_student(request, id):
    data = get_object_or_404(Student, id=id)
    
    context = {
        "student": data, 
    }
    
    if request.method == "POST":
        data.name = request.POST.get('name')
        data.email = request.POST.get('email')
        
        user_img = request.FILES.get('image')
        
        if user_img:
            data.image =  user_img
            
        data.save()
        return redirect('show_student')    
    
    
    return render(request, 'student/edit_student.html',context )
