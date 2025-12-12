from django.shortcuts import render

def home(request):
    """Home page"""
    return render(request, 'frontend/home.html')

def clinics_list(request):
    """List of all clinics"""
    return render(request, 'frontend/clinics_list.html')

def clinic_detail(request, pk):
    """Detail page for a specific clinic"""
    return render(request, 'frontend/clinic_detail.html', {'clinic_id': pk})

def doctors_list(request):
    """List of all doctors"""
    return render(request, 'frontend/doctors_list.html')

def doctor_detail(request, pk):
    """Detail page for a specific doctor"""
    return render(request, 'frontend/doctor_detail.html', {'doctor_id': pk})

def services_list(request):
    """List of all services"""
    return render(request, 'frontend/services_list.html')

def appointments_list(request):
    """User's appointments"""
    return render(request, 'frontend/appointments_list.html')

def appointment_create(request):
    """Create new appointment"""
    return render(request, 'frontend/appointment_create.html')

def profile(request):
    """User profile"""
    return render(request, 'frontend/profile.html')

def login_page(request):
    """Login page"""
    return render(request, 'frontend/login.html')

def register_page(request):
    """Registration page"""
    return render(request, 'frontend/register.html')

def about(request):
    """About us page"""
    return render(request, 'frontend/about.html')

def favorites(request):
    """Favorite doctors page"""
    return render(request, 'frontend/favorites.html')
