from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views.custom_user import*
from .views.otp import OtpViewSet
from .views.login import LoginView
from .views.service_provider_profile import ServiceProviderProfileModelView
from .views.business_owner_profile import BusinessOwnerProfileModelView
urlpatterns = [
    path('users/send_otp', OtpViewSet.as_view({'post': 'create_otp'}), name='user-send-otp'), #This is used for send Otp for the User mail 
    path('users/verify_otp', OtpViewSet.as_view({'post': 'verify_otp'}), name='user-verify-otp'),#This is used for verify Otp for the User 
    path('login', LoginView.as_view(), name='user-login'),
    path('users/create', CustomUserViewSet.as_view({'post': 'create'})),
    path('users/show', CustomUserViewSet.as_view({'get': 'show'})),
    path('users/update', CustomUserViewSet.as_view({'patch': 'update'})),
    path('users/delete', CustomUserViewSet.as_view({'delete': 'delete'})),
    path('users/index', CustomUserViewSet.as_view({'get': 'index'})),
    path('users/service_providers/create/', ServiceProviderProfileModelView.as_view({'post': 'create'})),
    path('users/service_providers/show', ServiceProviderProfileModelView.as_view({'get': 'show'})),
    path('users/service_providers/update', ServiceProviderProfileModelView.as_view({'patch': 'update'})),
    path('users/service_providers/delete', ServiceProviderProfileModelView.as_view({'patch': 'delete'})),
    path('users/service_providers/index', ServiceProviderProfileModelView.as_view({'get': 'index'})),
    path('users/business_owner/create/', BusinessOwnerProfileModelView.as_view({'post': 'create'})),
    path('users/business_owner/show', BusinessOwnerProfileModelView.as_view({'get': 'show'})),
    path('users/business_owner/update',BusinessOwnerProfileModelView .as_view({'patch': 'update'})),
    path('users/business_owner/delete', BusinessOwnerProfileModelView.as_view({'patch': 'delete'})),
    path('users/business_owner/index', BusinessOwnerProfileModelView.as_view({'get': 'index'})),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
