from django.urls import path
from .views import SignUpView, edit_profile, delete_profile, show_profile

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/<int:pk>/', show_profile, name='profile'),
    path('edit-profile/', edit_profile, name='edit-profile'),
    path('delete-profile/', delete_profile, name='delete-profile'),
]
