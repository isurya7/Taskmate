from django.shortcuts import render,redirect
from django.http import HttpResponse
from todolist.models import Tasklist
from todolist.forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required  #this is a pre define function from django to preview your views only to people who are logged in into your application

# Create your views here.
def home(request):
    return render(request,"home.html")

@login_required  #this is the decorator which we have imported from the django
def todolist(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
        messages.success(request, "New task added successfully")
        return redirect('todolist')
    else:
        all_task = Tasklist.objects.filter(owner=request.user)
        paginator = Paginator(all_task, 5)
        page = request.GET.get("pg")
        all_task = paginator.get_page(page)

    return render(request, "todolist.html", {'all_task': all_task})

def contact(request):
    context={
       'welcome_text':"Hello! welcome to our contact page." 
    }
    return render(request, "contact.html",context)

def about(request):
    context={
       'welcome_text':"Hello! welcome to our about page." 
    }
    return render(request, "about.html",context)

@login_required
def delete_task(request, task_id):
    try:
        task = Tasklist.objects.get(pk=task_id)
    except Tasklist.DoesNotExist:
        messages.error(request, "Task not found.")
        return redirect('todolist')

    if task.owner == request.user:  # Assuming Tasklist has an 'owner' field
        task.delete()
        messages.success(request, "Task deleted successfully.")
    else:
        messages.error(request, "Sorry, you don't have access to that task. Please delete it from the options provided.")

    return redirect('todolist')

@login_required
def edit_task(request,task_id):
        if request.method =="POST":
             task=Tasklist.objects.get(pk=task_id)
             form=TaskForm(request.POST or None , instance=task)
             if form.is_valid():
                form.save()
             messages.success(request,("Task Edited!"))
             return redirect('todolist')

        else:    
         task_obj = Tasklist.objects.get(pk=task_id)
         return render(request,'edit.html',{'task_obj': task_obj})

@login_required
def complete_task(request, task_id):
    try:
        task = Tasklist.objects.get(pk=task_id)
    except Tasklist.DoesNotExist:
        messages.error(request, "Task not found.")
        return redirect('todolist')

    if task.owner == request.user:  # Assuming Tasklist has an 'owner' field
        task.done = False
        task.save()
        messages.success(request, "Task marked as incomplete.")
    else:
        messages.error(request, "Sorry, you don't have access to mark this task as incomplete.")

    return redirect('todolist')

@login_required
def notcomplete_task(request, task_id):
    try:
        task = Tasklist.objects.get(pk=task_id)
    except Tasklist.DoesNotExist:
        messages.error(request, "Task not found.")
        return redirect('todolist')

    if task.owner == request.user:  # Assuming Tasklist has an 'owner' field
        task.done = True
        task.save()
        messages.success(request, "Task marked as complete.")
    else:
        messages.error(request, "Sorry, you don't have access to mark this task as complete.")

    return redirect('todolist')
         
    


  