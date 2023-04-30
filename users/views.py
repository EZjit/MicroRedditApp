from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from core.models import Community, Comment
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


def show_profile(request, id):
    user = get_object_or_404(User, id=id)
    user_posts = user.post_set.all()
    communities = Community.objects.all()[:5]
    recent_comments = Comment.objects.all()[:10]
    context = {
        'user': user,
        'user_posts': user_posts,
        'communities': communities,
        'recent_comments': recent_comments,
    }

    return render(request, 'users/profile.html', context)


@login_required(login_url='login')
def edit_profile(request):
    user = request.user
    form = CustomUserChangeForm(request.POST or None, instance=user)

    if form.is_valid():
        form.save()
        return redirect('profile', id=user.id)

    return render(request, 'users/edit_profile.html', {'form': form})


@login_required(login_url='login')
def delete_profile(request):
    user = request.user

    if request.method == 'POST':
        user.delete()
        return redirect('home')
    context = {'object': user}
    return render(request, 'delete.html', context)
