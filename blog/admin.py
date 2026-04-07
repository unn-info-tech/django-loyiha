from django.contrib import admin
from .models import Post, Izoh, Profil

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('sarlavha', 'muallif', 'yaratilgan_sana', 'nashr_etilgan')
    list_filter = ('nashr_etilgan', 'yaratilgan_sana')
    search_fields = ('sarlavha', 'matn')
    date_hierarchy = 'yaratilgan_sana'

@admin.register(Izoh)
class IzohAdmin(admin.ModelAdmin):
    # 👇 CHANGE 'yaratilgan' to the ACTUAL field name in your model (e.g., 'yaratilgan_sana' or 'sana')
    list_display = ('post', 'muallif', 'yaratilgan_sana')  
    list_filter = ('yaratilgan_sana',)  # 👇 CHANGE here too
    search_fields = ('matn',)

@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ('foydalanuvchi', 'tugilgan_sana')
    search_fields = ('foydalanuvchi__username',)