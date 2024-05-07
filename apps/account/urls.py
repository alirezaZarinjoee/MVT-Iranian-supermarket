from django.urls import path
from . import views

app_name='account'
urlpatterns = [
    path('register_view/',views.RegisterView.as_view(),name='register_view'),
    path('verify_view/',views.VerifyView.as_view(),name='verify_view'),
    path('login_view/',views.LoginView.as_view(),name='login_view'),
    path('logout_view/',views.LogoutView.as_view(),name='logout_view'),
    path('userpanel_view/',views.UserPanelView.as_view(),name='userpanel_view'),
    path('show_last_orders/',views.show_last_orders,name='show_last_orders'),
    path('changepassword_view/',views.ChangePasswordView.as_view(),name='changepassword_view'),
    path('update_profile/',views.UpdateProfileView.as_view(),name='update_profile'),
    path('GetMobileNumberForChangePassword_view/',views.GetMobileNumberForChangePasswordView.as_view(),name='GetMobileNumberForChangePassword_view'),
]
