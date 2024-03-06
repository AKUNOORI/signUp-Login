# myapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from .models import Patient, Doctor
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        # Handle signup form submission
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        address_line1 = request.POST.get('address_line1')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        
        # Check if passwords match
        if password != confirm_password:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
        
        # Create user
        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        
        # Create Patient or Doctor object based on user type
        try:
            if request.POST.get('user_type') == 'patient':
                patient = Patient.objects.create(user=user, address_line1=address_line1, city=city, state=state, pincode=pincode)
                patient.save()
            elif request.POST.get('user_type') == 'doctor':
                doctor = Doctor.objects.create(user=user, address_line1=address_line1, city=city, state=state, pincode=pincode)
                doctor.save()
        except IntegrityError as e:
            return render(request, 'signup.html', {'error': 'Error creating Doctor object: ' + str(e)})
        
        
        # Redirect to login page
        return redirect('login')
    else:
        # Render signup form
        return render(request, 'signup.html')

# @csrf_exempt  
# def upload_profile_picture(request):
#     if request.method == 'POST':
#         profile_picture = request.FILES.get('profile_picture')
#         if profile_picture:
#             doctor = Doctor.objects.get(user=request.user)  # Assuming you're using authentication
#             doctor.profile_picture = profile_picture
#             doctor.save()
#             return redirect('profile')  # Redirect to profile page after successful upload
#     return render(request, 'signup.html')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        # Handle login form submission
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Login user
            auth_login(request, user)
            # Redirect to respective dashboard
            if hasattr(user, 'patient'):
                return redirect('patient_dashboard')
            elif hasattr(user, 'doctor'):
                return redirect('doctor_dashboard')
        else:
            # Invalid login
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    
        # Render login form
    return render(request, 'login.html')

@csrf_exempt
def patient_dashboard(request):
    # Get patient details
    patient = request.user.patient
    return render(request, 'patient_dashboard.html', {'patient': patient})

@csrf_exempt
def doctor_dashboard(request):
    # Get doctor details
    doctor = request.user.doctor
    return render(request, 'doctor_dashboard.html', {'doctor': doctor})
