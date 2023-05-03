from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
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


def show_profile(request: HttpRequest, pk: int) -> HttpResponse:
    user = get_object_or_404(User, id=pk)
    user_posts = user.posts.prefetch_related('user', 'comments', 'community')
    communities = Community.objects.prefetch_related('posts')[:5]
    recent_comments = Comment.objects.select_related('user', 'post')[:10]
    context = {
        'user': user,
        'user_posts': user_posts,
        'communities': communities,
        'recent_comments': recent_comments,
    }

    return render(request, 'users/profile.html', context)


@login_required()
def edit_profile(request: HttpRequest) -> HttpResponse:
    user = request.user
    form = CustomUserChangeForm(request.POST or None, instance=user)

    if form.is_valid():
        form.save()
        return redirect('profile', id=user.id)

    return render(request, 'users/edit_profile.html', {'form': form})


@login_required()
def delete_profile(request: HttpRequest) -> HttpResponse:
    user = request.user

    if request.method == 'POST':
        user.delete()
        return redirect('home')
    context = {'object': user}
    return render(request, 'delete.html', context)
