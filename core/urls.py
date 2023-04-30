from django.urls import path
from . import views

urlpatterns = [
    path('create-community/', views.CommunityCreate.as_view(), name='create-community'),
    path('communities/', views.communities_page, name='communities'),

    path('create-post/', views.PostCreate.as_view(), name='create-post'),
    path('<int:id>/', views.show_post, name='post'),
    path('edit-post/<int:pk>/', views.PostEdit.as_view(), name='edit-post'),
    path('delete-post/<int:id>', views.delete_post, name='delete-post'),

    path('comment/reply/', views.reply_comment, name='reply'),
    path('delete-comment/<int:id>', views.delete_comment, name='delete-comment'),
]
