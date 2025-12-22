from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from .views import HomepageView, AboutUsView, search_view, CategoryListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomepageView.as_view(), name='homepage'),
    path('about-us/', AboutUsView.as_view(), name='about_us'),
    path('search/', search_view, name='search'),
    path('accounts/', include('allauth.urls')),
    path('profile/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('categories/', CategoryListView.as_view(), name='categories_list'),
    path('admin-dashboard/', include('dashboard.urls')),
    path('complaints/', include('complaints.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
