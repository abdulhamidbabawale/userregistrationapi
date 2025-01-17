from django.urls import path
from .views import RegisterView,ChangePasswordView,UpdateProfileView,UserProfileView

urlpatterns =[
    path('register/',RegisterView.as_view(),name='reg'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
        path('profile/update/', UpdateProfileView.as_view(), name='profile-update'),
         path('profile/', UserProfileView.as_view(), name='user-profile'),
]
