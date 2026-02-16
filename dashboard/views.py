from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Post, CalculationLog, Lead
from django.db.models import Sum


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


    context = {
        'total_posts': total_posts,
        'posts_growth': posts_growth,
        'total_views': total_views,
        'total_calcs': total_calcs,
        'calcs_growth': calcs_growth,
        'total_leads': total_leads,
        'leads_growth': leads_growth,
    }

    return render(request, 'dashboard/index.html')

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    session_key = f'viewed_post_{post.id}'

    if not request.session.get(session_key):
        post.views_count += 1
        post.save()

        request.session[session_key] = True
        request.session.set_expiry(86400)

    return render(request, 'blog/post_detail.html', {'post': post})