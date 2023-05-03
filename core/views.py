from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from .models import Community, Post, Comment
from .forms import CommentForm


# Community Views

class CommunityCreate(LoginRequiredMixin, CreateView):
    redirect_field_name = 'next'

    model = Community
    fields = ['name', 'description']
    template_name = 'core/community_form.html'

    success_url = reverse_lazy('home')


def communities_page(request):
    query = request.GET.get('q', '')
    communities = Community.objects.filter(name__icontains=query)

    context = {'communities': communities}
    return render(request, 'core/communities_page.html', context)


# Post Views

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['community', 'title', 'body']
    template_name = 'core/post_form.html'
    success_url = reverse_lazy('home')

    redirect_field_name = 'next'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def show_post(request, id):
    post = get_object_or_404(Post, id=id)
    post_top_level_comments = post.get_comments().select_related('user')
    post_comments_num = post.comments.count()

    # We allow users to comment on this post
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.parent = None
            new_comment.save()
            return redirect(post.get_absolute_url()+'#comment-'+str(new_comment.id))

    context = {
        'post': post,
        'post_comments_num': post_comments_num,
        'comment_form': comment_form,
        'post_top_level_comments': post_top_level_comments,
        }

    return render(request, 'core/post_detail.html', context)


class PostEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'body']

    template_name = 'core/post_form.html'

    redirect_field_name = 'next'

    def get_success_url(self):
        return reverse('post', args=[self.object.id])

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user


@login_required()
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)

    if request.user != post.user:
        raise PermissionDenied()

    if request.method == 'POST':
        post.delete()
        return redirect('home')

    context = {'object': post}
    return render(request, 'delete.html', context)


# Comment Views

@login_required()
def reply_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            post_id = request.POST.get('post')
            post = Post.objects.get(id=post_id)
            parent_id = request.POST.get('parent')
            parent = Comment.objects.get(id=parent_id)
            user = request.user
            reply = form.save(commit=False)

            reply.post = post
            reply.parent = parent
            reply.user = user
            reply.save()

            return redirect(post.get_absolute_url()+'#comment-'+str(reply.id))



@login_required()
def delete_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    post = comment.post

    if request.user != comment.user:
        raise PermissionDenied()

    if request.method == 'POST':
        comment.delete()
        return redirect('post', post.id)

    context = {'object': comment}
    return render(request, 'delete.html', context)


# Common Views

def home_page(request):
    query = request.GET.get('q', '')
    page_number = request.GET.get('page', 1)
    number_of_posts = Post.objects.count()
    posts = Post.objects.filter(
        Q(community__name__icontains=query) |
        Q(title__icontains=query) |
        Q(body__icontains=query)
    ).prefetch_related('user', 'community', 'comments')

    paginator = Paginator(posts, per_page=10)

    try:
        page_object = paginator.get_page(page_number)
    # If page is not integer return 1st page
    except PageNotAnInteger:
        page_object = paginator.get_page(1)
    # If page is out of range return last page
    except EmptyPage:
        page_object = paginator.get_page(paginator.num_pages)

    communities = Community.objects.prefetch_related('posts')[:5]
    community_comments = Comment.objects.filter(
        Q(post__community__name__icontains=query)
    ).select_related('user', 'post')[:10]

    context = {
        'page_obj': page_object,
        'number_of_posts': number_of_posts,
        'communities': communities,
        'community_comments': community_comments,
        'query': query,
        }

    return render(request, 'home.html', context)
