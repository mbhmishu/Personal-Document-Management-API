
from django.urls import path
from . import views
app_name='account'

"""from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    )   
"""


urlpatterns = [
    #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/',views.UserLoginView.as_view(), name='login'),
    path('password-change/',views.UserPasswordChangeView.as_view(), name='password-change'),
    path('password-reset-link/',views.PasswordResetByEmailView.as_view(), name='password-reset-link'),
    path('password-reset/<uid>/<token>/',views.UserPasswordResetView.as_view(), name='password-reset'),
    path('profile-update/',views.UserProfileView.as_view(), name='profile-update'),

]
