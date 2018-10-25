from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PassportForm


def booking(request):
    return render(request, 'booking.html', {'title': 'booking'})


@login_required
def profile(request):
    if request.method == 'POST':
        # import pdb;
        # pdb.set_trace();
        form = PassportForm(request.POST, request.FILES)
        if form.is_valid():
            passport = request.FILES['passport']
            user = request.user
            user.profile.passport = passport
            user.save()
    else:
        form = PassportForm()
    return render(request, 'profile.html', {'title': request.user.get_username(), 'form': form})


@login_required()
def delete_passport(request):
    if request.method == 'POST':
        request.user.profile.passport.delete()
    return redirect('profile')
