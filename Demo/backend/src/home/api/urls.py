from django.urls import path
from .views import getUrl, getCR, current_user, UserList, getImg, save_user, get_user, signout_user, insert_properties, save, cosine, adz1, adz2, check_save, delete_save, show_recommend, prediction, estimate, barchart, pyramidd, getsave, show_random_recommend

urlpatterns = [
    path('get_url/', getUrl),
    path('address/<str:value>', getCR),
    path('current_user/', current_user),
    path('save_user/', save_user),
    path('get_user/', get_user),
    path('signout_user/', signout_user),
    path('users/', UserList.as_view()),
    path('img/', getImg),
    path('insert/', insert_properties),
    path('save/', save),
    path('cosine/', cosine),
    path('adz1/', adz1),
    path('adz2/', adz2),
    path('check_save/', check_save),
    path('delete_save/', delete_save),
    path('show_recommend/', show_recommend),
    path('prediction/', prediction),
    path('estimate/', estimate),
    path('barchart/', barchart),
    path('pyramid/', pyramidd),
    path('getsave/', getsave),
    path('show_random_recommend/', show_random_recommend)
]