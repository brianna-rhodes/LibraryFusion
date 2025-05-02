from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, PaymentForm, UserNoteForm
from .models import User, Payment, UserNote
from django.contrib.auth.views import LoginView

def register(request):
    if request.user.is_authenticated:
        return redirect('books:home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('books:home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'account/register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('books:home')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('books:home')
    else:
        form = UserLoginForm()
    
    return render(request, 'account/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('account:login')

@login_required
def profile(request):
    return render(request, 'account/profile.html')

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'account/profile_edit.html'
    success_url = reverse_lazy('account:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)

@login_required
def user_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    payments = Payment.objects.filter(user=user).order_by('-payment_date')
    notes = UserNote.objects.filter(user=user).order_by('-created_at')
    
    if request.method == 'POST':
        if 'payment' in request.POST:
            payment_form = PaymentForm(request.POST)
            if payment_form.is_valid():
                payment = payment_form.save(commit=False)
                payment.user = user
                payment.processed_by = request.user
                payment.save()
                messages.success(request, 'Payment recorded successfully!')
                return redirect('account:user_profile', pk=user.pk)
        elif 'note' in request.POST:
            note_form = UserNoteForm(request.POST)
            if note_form.is_valid():
                note = note_form.save(commit=False)
                note.user = user
                note.created_by = request.user
                note.save()
                messages.success(request, 'Note added successfully!')
                return redirect('account:user_profile', pk=user.pk)
    else:
        payment_form = PaymentForm()
        note_form = UserNoteForm()
    
    context = {
        'profile_user': user,
        'payments': payments,
        'notes': notes,
        'payment_form': payment_form,
        'note_form': note_form,
    }
    return render(request, 'account/user_profile.html', context)

@login_required
def delete_note(request, pk):
    note = get_object_or_404(UserNote, pk=pk)
    if request.user.is_librarian or request.user.is_manager:
        note.delete()
        messages.success(request, 'Note deleted successfully!')
    return redirect('account:user_profile', pk=note.user.pk)

class CustomLoginView(LoginView):
    template_name = 'account/login.html'
    
    def get_success_url(self):
        user = self.request.user
        if user.role == 'MANAGER':
            return reverse_lazy('managers:dashboard')
        elif user.role == 'LIBRARIAN':
            return reverse_lazy('librarians:dashboard')
        else:
            return reverse_lazy('books:home')
