from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Post, CalculationLog, Lead
from django.db.models import Sum
from .forms import PostForm


def get_growth(current, previous):
    if previous == 0:
        return 100 if current > 0 else 0
    return round(((current - previous) / previous) * 100, 1)


def index(request):
    # Datas para o cálculo
    now = timezone.now()
    last_30_days = now - timedelta(days=30)
    previous_30_days = now - timedelta(days=60)

    # 1. POSTS
    total_posts = Post.objects.count()
    posts_current = Post.objects.filter(created_at__gte=last_30_days).count()
    posts_prev = Post.objects.filter(created_at__range=(previous_30_days, last_30_days)).count()
    posts_growth = get_growth(posts_current, posts_prev)

    # 2. VISUALIZAÇÕES
    total_views = Post.objects.aggregate(Sum('views_count'))['views_count__sum'] or 0
    # Nota: Para crescimento real de views dia a dia, precisaríamos de um log de Analytics. 
    # Por enquanto, manteremos fixo ou simulado.

    # 3. CÁLCULOS
    total_calcs = CalculationLog.objects.count()
    calcs_current = CalculationLog.objects.filter(created_at__gte=last_30_days).count()
    calcs_prev = CalculationLog.objects.filter(created_at__range=(previous_30_days, last_30_days)).count()
    calcs_growth = get_growth(calcs_current, calcs_prev)

    # 4. LEADS
    total_leads = Lead.objects.count()
    leads_current = Lead.objects.filter(created_at__gte=last_30_days).count()
    leads_prev = Lead.objects.filter(created_at__range=(previous_30_days, last_30_days)).count()
    leads_growth = get_growth(leads_current, leads_prev)

    views_grouth = 12.5 # Valor similado
    latest_activities = Post.objects.all().order_by('-created_at')[:5]

    chart_data = [
        {'day': 'Seg', 'value': 45},
        {'day': 'Ter', 'value': 70},
        {'day': 'Qua', 'value': 55},
        {'day': 'Qui', 'value': 150},
        {'day': 'Sex', 'value': 200},
        {'day': 'Sab', 'value': 23},
        {'day': 'Dom', 'value': 10},
    ]

    context = {
        'total_posts': total_posts,
        'posts_growth': posts_growth,
        'total_views': total_views,
        'total_calcs': total_calcs,
        'calcs_growth': calcs_growth,
        'total_leads': total_leads,
        'leads_growth': leads_growth,
        'latest_activities': latest_activities,
        'chart_data': chart_data,
    }

    return render(request, 'dashboard/index.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    session_key = f'viewed_post_{post.id}'

    if not request.session.get(session_key):
        post.views_count += 1
        post.save()

        request.session[session_key] = True
        request.session.set_expiry(86400)

    return render(request, 'blog/post_detail.html', {'post': post})


def article_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            article = form.save() # Salva direto se estiver tudo ok
            return redirect('articles_list')
    else:
        form = PostForm()

    # O return deve ficar fora do IF para responder ao GET inicial
    return render(request, 'dashboard/article_editor.html', {'form': form})

def article_edit(request, pk):
    article = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles_list')
    else:
        # Se for GET, carregamos o formulário com os dados do artigo existente
        form = PostForm(instance=article)

    # O return fora do IF garante que a página de edição abra corretamente
    return render(request, 'dashboard/article_editor.html', {'form': form, 'article': article})
    

def article_delete(request, pk):
    article = get_object_or_404(Post, pk=pk)
    article.delete()
    return redirect('articles_list')


def articles_list(request):
    articles = Post.objects.all().order_by('-created_at')

    return render(request, 'dashboard/articles_list.html', {'articles': articles})