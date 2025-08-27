from django.urls import path
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh

from users.views import RegisterAPIView, UserRetrieveAPIView, UserUpdateAPIView, UserDestroyAPIView, \
    UserChangePasswordAPIView

# JWT Urls
urlpatterns = [
    path('token/', token_obtain_pair, name='token+obtain_pair'),
    path('token/refresh', token_refresh, name='token_refresh'),

]

# User Urls
urlpatterns += [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('my-account/', UserRetrieveAPIView.as_view(), name='users-details'),
    path('my-account/update/', UserUpdateAPIView.as_view(), name='users-update'),
    path('my-account/delete/', UserDestroyAPIView.as_view(), name='users-destroy'),
    path('my-account/change-password/', UserChangePasswordAPIView.as_view(), name='change-password'),
]