from django.urls import path
from .views import ComplaintsListView, complaint

urlpatterns = [
    path('list/', ComplaintsListView.as_view(), name='complaints'),
    path('contact-us/', complaint, name='contact')
]
