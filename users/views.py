from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignupForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfessionalRegistrationForm



from django.http import JsonResponse

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Redirect after login
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})


@login_required
def professional_registration(request):
    profile = None  # Default to None, meaning no automatic profile creation

    if request.method == 'POST':
        form = ProfessionalRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  # Assign the logged-in user
            profile.save()
            messages.success(request, 'Your request to become a professional has been submitted for approval.')
            return redirect('dashboard')
    else:
        form = ProfessionalRegistrationForm()

    return render(request, 'users/mentor-reg.html', {'form': form})
from .models import CustomUser  # Import your CustomUser model

'''@login_required
def user_management(request):
    if not request.user.is_superuser:
        messages.error(request, "Unauthorized access!")
        return redirect('dashboard')

    users = CustomUser.objects.filter(is_superuser=False, is_professional=False)  # Regular Users
    professionals = CustomUser.objects.filter(is_professional=True)  # Approved Professionals
    admins = CustomUser.objects.filter(is_superuser=True)  # Admins

    return render(request, 'users/user_management.html', {
        'users': users,
        'professionals': professionals,
        'admins': admins
    })'''

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser  # ✅ Import CustomUser

@login_required
#def delete_user(request, user_id):
 #   user = get_object_or_404(CustomUser, id=user_id)  # ✅ Get user by ID
  #  if request.user.is_superuser:  # ✅ Allow only superusers to delete
   #     user.delete()
    #    messages.success(request, "User deleted successfully!")
    #else:
     #   messages.error(request, "You are not authorized to delete users.")
    #return redirect('user_management')  # ✅ Redirect back to user list

#def remove_professional_status(request, user_id):
 #   user = get_object_or_404(CustomUser, id=user_id)
    
  #  if hasattr(user, 'professionalprofile'):
   #     user.professionalprofile.delete()  # Remove ProfessionalProfile
    #    user.is_professional = False  # Reset the flag
     #   user.save(update_fields=['is_professional'])
      #  messages.success(request, f"{user.username} is no longer a professional.")
    #else:
     #   messages.error(request, "This user is not a professional.")
    
    #return redirect('user_management')

@login_required
def user_management(request):
    if not request.user.is_superuser:
        messages.error(request, "Unauthorized access!")
        return redirect('dashboard')

    users = CustomUser.objects.filter(is_superuser=False, is_professional=False)  # Regular Users
    professionals = CustomUser.objects.filter(is_professional=True)  # Approved Professionals
    admins = CustomUser.objects.filter(is_superuser=True)  # Admins

    return render(request, 'users/user_management.html', {
        'users': users,
        'professionals': professionals,
        'admins': admins
    })

@login_required
def delete_user(request, user_id):
    if not request.user.is_superuser:
        return JsonResponse({'error': "Unauthorized action!"}, status=403)

    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return JsonResponse({'success': "User deleted successfully!"})

@login_required
def remove_professional_status(request, user_id):
    if not request.user.is_superuser:
        return JsonResponse({'error': "Unauthorized action!"}, status=403)

    user = get_object_or_404(CustomUser, id=user_id)
    
    if hasattr(user, 'professionalprofile'):
        user.professionalprofile.delete()
        user.is_professional = False
        user.save(update_fields=['is_professional'])
        return JsonResponse({'success': f"{user.username} is no longer a professional!"})
    
    return JsonResponse({'error': "This user is not a professional."}, status=400)
