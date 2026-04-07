from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Post, Izoh, Like, Profil
from .forms import PostForma, RoyxatdanOtishForma, IzohForma, FoydalanuvchiYangilashForma, ProfilYangilashForma
from django.contrib.auth import login, logout, authenticate

def bosh_sahifa(request):
    postlar = Post.objects.filter(nashr_etilgan=True).order_by('-yaratilgan_sana')
    context = {'postlar': postlar}
    return render(request, 'blog/bosh.html', context)

def biz_haqimizda(request):
    return render(request, 'blog/biz_haqimizda.html')

def aloqa(request):
    return render(request, 'blog/aloqa.html')

def portfolio(request):
    return render(request, 'blog/portfolio.html')

def ommabop_postlar(request):
    postlar = Post.objects.filter(nashr_etilgan=True).order_by('-korildi')[:5]
    context = {'postlar': postlar}
    return render(request, 'blog/ommabop.html', context)

def post_batafsil(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Ko'rishlar sonini oshirish
    post.korildi += 1
    post.save(update_fields=['korildi'])

    # Like holatini tekshirish
    user_liked = False
    if request.user.is_authenticated:
        user_liked = Like.objects.filter(post=post, user=request.user).exists()

    # Izoh qo'shish logikasi
    if request.method == 'POST':
        if request.user.is_authenticated:
            forma = IzohForma(request.POST)
            if forma.is_valid():
                izoh = forma.save(commit=False)
                izoh.post = post
                izoh.muallif = request.user
                izoh.save()
                messages.success(request, "✅ Izoh qoldirildi!")
                return redirect('post_batafsil', post_id=post.id)
        else:
            messages.error(request, "❌ Izoh qoldirish uchun tizimga kiring.")

    izohlar = post.izohlar.all().order_by('-yaratilgan_sana')

    context = {
        'post': post,
        'izohlar': izohlar,
        'user_liked': user_liked,
    }
    return render(request, 'blog/post_batafsil.html', context)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like_obj, created = Like.objects.get_or_create(post=post, user=request.user)
    
    if not created:
        like_obj.delete()
        messages.info(request, "Like olib tashlandi")
    else:
        messages.success(request, "👍 Post yoqti!")
        
    return redirect('post_batafsil', post_id=post.id)

# Bitta aniq 'profil' funksiyasi
def profil(request, username):
    foydalanuvchi = get_object_or_404(User, username=username)
    postlar = Post.objects.filter(muallif=foydalanuvchi, nashr_etilgan=True).order_by('-yaratilgan_sana')

    context = {
        'profil_egasi': foydalanuvchi,
        'postlar': postlar,
        'postlar_soni': postlar.count()
    }
    return render(request, 'blog/profil.html', context)

def qidiruv(request):
    soz = request.GET.get('q', '')
    postlar = Post.objects.filter(
        Q(sarlavha__icontains=soz) | Q(matn__icontains=soz),
        nashr_etilgan=True
    )

    return render(request, 'blog/qidiruv.html', {
        'postlar': postlar,
        'soz': soz
    })

@login_required
def post_yaratish(request):
    if request.method == 'POST':
        forma = PostForma(request.POST, request.FILES)
        if forma.is_valid():
            post = forma.save(commit=False)
            post.muallif = request.user
            post.save()
            messages.success(request, '✅ Post yaratildi!')
            return redirect('bosh_sahifa')
    else:
        forma = PostForma()
    return render(request, 'blog/post_yaratish.html', {'forma': forma})

@login_required
def post_tahrirlash(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.muallif != request.user:
        messages.error(request, '❌ Siz faqat o\'z postingizni tahrirlashingiz mumkin!')
        return redirect('post_batafsil', post_id=post.id)

    if request.method == 'POST':
        forma = PostForma(request.POST, instance=post)
        if forma.is_valid():
            forma.save()
            messages.success(request, '✅ Post yangilandi!')
            return redirect('post_batafsil', post_id=post.id)
    else:
        forma = PostForma(instance=post)

    context = {'forma': forma, 'post': post}
    return render(request, 'blog/post_tahrirlash.html', context)

@login_required
def post_ochirish(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        messages.success(request, '✅ Post o\'chirildi!')
        return redirect('bosh_sahifa')
    return render(request, 'blog/post_ochirish.html', {'post': post})

def royxatdan_otish(request):
    if request.method == 'POST':
        forma = RoyxatdanOtishForma(request.POST)
        if forma.is_valid():
            user = forma.save()
            login(request, user)
            messages.success(request, f'✅ Xush kelibsiz, {user.username}!')
            return redirect('bosh_sahifa')
    else:
        forma = RoyxatdanOtishForma()
    return render(request, 'blog/royxatdan_otish.html', {'forma': forma})

def kirish(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'✅ Xush kelibsiz, {user.username}!')
            return redirect('bosh_sahifa')
        else:
            messages.error(request, '❌ Noto\'g\'ri foydalanuvchi nomi yoki parol!')
    return render(request, 'blog/kirish.html')

def chiqish(request):
    logout(request)
    messages.info(request, '👋 Xayr! Tez orada qaytib kelasiz!')
    return redirect('bosh_sahifa')

@login_required
def profil_tahrirlash(request):
    # 1. PROFIL MAVJUDLIGINI TEKSHIRISH VA YARATISH (Xavfsizlik)
    try:
        profil_obj = request.user.profil
    except Profil.DoesNotExist:
        # Agar profil yo'q bo'lsa, yangisini yaratamiz
        profil_obj = Profil.objects.create(foydalanuvchi=request.user)

    if request.method == 'POST':
        f_forma = FoydalanuvchiYangilashForma(request.POST, instance=request.user)
        p_forma = ProfilYangilashForma(request.POST, request.FILES, instance=profil_obj)

        if f_forma.is_valid() and p_forma.is_valid():
            f_forma.save()
            p_forma.save()
            messages.success(request, '✅ Profilingiz yangilandi!')
            return redirect('profil', username=request.user.username)
    else:
        f_forma = FoydalanuvchiYangilashForma(instance=request.user)
        p_forma = ProfilYangilashForma(instance=profil_obj)

    context = {
        'f_forma': f_forma,
        'p_forma': p_forma
    }
    return render(request, 'blog/profil_tahrirlash.html', context)