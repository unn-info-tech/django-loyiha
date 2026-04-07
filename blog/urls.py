from django.urls import path
from django.conf.urls.static import static
from saytim import settings
from . import views

urlpatterns = [
    path('', views.bosh_sahifa, name='bosh_sahifa'),
    path('biz-haqimizda/', views.biz_haqimizda, name='biz_haqimizda'),
    path('aloqa/', views.aloqa, name='aloqa'),
    path('portfolio/', views.portfolio, name='portfolio'),
    
    # DIQQAT: Aniq manzillar (static) har doim dinamik manzillardan (<str>, <int>) YUQORIDA bo'lishi kerak!
    path('profil/tahrirlash/', views.profil_tahrirlash, name='profil_tahrirlash'),
    
    # Bu qator endi pastda turibdi, shuning uchun 'tahrirlash' so'zi bu yerga kelmaydi
    path('profil/<str:username>/', views.profil, name='profil'),
    
    path('post/<int:post_id>/', views.post_batafsil, name='post_batafsil'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'), 
    
    path('ommabop/', views.ommabop_postlar, name='ommabop'),
    
    path('post/<int:post_id>/tahrirlash/', views.post_tahrirlash, name='post_tahrirlash'),
    path('post/<int:post_id>/ochirish/', views.post_ochirish, name='post_ochirish'),
    
    path('royxatdan-otish/', views.royxatdan_otish, name='royxatdan_otish'),
    path('kirish/', views.kirish, name='kirish'),
    path('chiqish/', views.chiqish, name='chiqish'),
    
    path('yangi/', views.post_yaratish, name='post_yaratish'),
    
    path('qidiruv/', views.qidiruv, name='qidiruv'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)