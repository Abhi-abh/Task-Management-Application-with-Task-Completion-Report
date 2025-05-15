from django.shortcuts import render,HttpResponse,get_object_or_404
from .models import Task,Customer
from .form import insert_form
from .form1 import TaskForm
from django.contrib.auth import authenticate, login as auth_login,logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import re
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from .serializers1 import TaskReportSerializer
from .serializer2 import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework import viewsets

# Create your views here.



def signup(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password1')
        address=request.POST.get('address')
        phone=request.POST.get('phone')

        password_pattern = re.compile(r'^(?=.*[A-Z])(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$')

        if User.objects.filter(username=uname).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')
        if not password_pattern.match(password):
            messages.error(request, 'Password must be at least 8 characters long, ''include an uppercase letter, and a special character.')
            return redirect('signup')
        else:

            my_user=User.objects.create_user(uname,email,password)
            my_user.save()
            customer=Customer.objects.create(
                user=my_user,
                name=uname,
                phone=phone,
                address=address
            )
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    return render(request,'signup.html')

def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            auth_login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Username or Password is incorrect!!!")
            return redirect('login')
    return render(request,'login.html')

def login1(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff or user.is_superuser:  # Allow only staff or admin users
                auth_login(request, user)
                return redirect('home1')
            else:
                messages.error(request, "Access restricted to admin or staff users only!")
                return redirect('login1')
        else:
            messages.error(request, "Username or Password is incorrect!")
            return redirect('login1')
    return render(request, 'login1.html')

@login_required(login_url='login')
def home(request):
    user=request.user
    customer=user.customer_profile
    dict_insert = {
        'insert' : Task.objects.filter(owner=customer) 
    }
    return render(request,"home.html",dict_insert)

@login_required(login_url='login1')
def home1(request):
    dict_insert = {
        'insert' : Task.objects.all()
    }
    return render(request,"home1.html",dict_insert)


@login_required(login_url='login1')
def Addtask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'home1.html', {'product': Task.objects.all()})
    else:
        form = TaskForm()

    return render(request, 'Addtask.html', {'form': form})


@login_required(login_url='login')
def edit(request, id):
    user = request.user
    customer = user.customer_profile

    # Ensure the task belongs to the current user
    task_to_edit = get_object_or_404(Task, pk=id, owner=customer)

    if request.method == 'POST':
        form = insert_form(request.POST, instance=task_to_edit)
        if form.is_valid():
            form.save()  # Save the form, not the instance directly
            tasks = Task.objects.filter(owner=customer)
            return render(request, 'home.html', {'insert': tasks})
    else:
        form = insert_form(instance=task_to_edit)

    return render(request, 'edit.html', {'form': form})

@login_required(login_url='login')
def views_page(request,id):
   task = get_object_or_404(Task, pk=id)  # Fetch student details
   return render(request, 'views.html', {'task': task})

def loggout(request):
    logout(request)
    return redirect('login')


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        tokens = get_tokens_for_user(user)

        return Response({
            "user": UserSerializer(user).data,
            "tokens": tokens,
        }, status=status.HTTP_201_CREATED)
        

        
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            tokens = get_tokens_for_user(user)
            return Response({
                "user": UserSerializer(user).data,
                "tokens": tokens,
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({"error": "No refresh token provided"}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(str(refresh_token))
            token.blacklist()
            return Response({"message": "Successfully logged out!"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": f"Hello, {request.user.username}!"})

class TokenRefreshView(APIView):
        def post(self, request):
            try:
                refresh_token = request.data.get('refresh')
                token = RefreshToken(refresh_token)
                new_access_token = str(token.access_token)
                return Response({"access": new_access_token}, status=status.HTTP_200_OK)
            except TokenError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
class UserTasksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # Using Django User directly
        tasks = Task.objects.filter(owner=user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateTaskStatusView(APIView):
   
    permission_classes = [IsAuthenticated]
    def put(self, request, id):
        user = request.user
        task = get_object_or_404(Task, pk=id, owner=user)

        # Extract fields from request.data
        status_update = request.data.get('status')
        completion_report = request.data.get('completion_report')
        worked_hours = request.data.get('worked_hours')

        # Validate that if status is 'Completed', report and hours must be provided
        if status_update == 'Completed':
            if not completion_report or not worked_hours:
                return Response(
                    {"error": "Completion Report and Worked Hours are required when marking task as Completed."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            task.status = status_update
            task.completion_report = completion_report
            task.worked_hours = worked_hours
        else:
            # If not completed, only update status
            task.status = status_update
            

        task.save()
        return Response({"message": "Task updated successfully."}, status=status.HTTP_200_OK)


class TaskReportView(APIView):
   
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        user = request.user
        if not (user.is_staff or user.is_superuser):
            return Response({"error": "You do not have permission to view this report."}, status=status.HTTP_403_FORBIDDEN)

        task = get_object_or_404(Task, pk=id)


        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
            