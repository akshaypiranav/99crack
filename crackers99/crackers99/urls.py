
from django.contrib import admin
from django.urls import path
from APP import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('contact',views.contact,name='contact'),
    path('adminn',views.adminn,name='adminn'),
    path('addCategory',views.addCategory,name='addCategory'),
    path('addProduct',views.addProduct,name='addProduct'),
    path('deleteCategory/<int:id>', views.deleteCategory, name='deleteCategory'),
    path('deleteProduct/<int:id>', views.deleteProduct, name='deleteProduct'),
    path('updateCategory/<int:id>', views.updateCategory, name='updateCategory'),
    path('updateProduct/<int:id>', views.updateProduct, name='updateProduct'),
    path('submit-order/', views.submit_order, name='submit_order'),

    
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)