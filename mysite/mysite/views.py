from django.shortcuts import render,redirect
from read_statistics.utils import get_seven_days_read_data,get_today_hot_data,get_yesterday_hot_data,get_7_days_hot_bogs,get_30_days_hot_bogs
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from blog.models import Blog
from django.contrib import auth
from django.urls import reverse
from .forms import LoginForm,RegForm
from django.contrib.auth.models import User



def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates,read_nums = get_seven_days_read_data(blog_content_type)

    #获取7天热门博客的缓存数据
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = get_7_days_hot_bogs()
        cache.set('hot_blogs_for_7_days',hot_blogs_for_7_days,3600)

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['hot_blogs_for_7_days'] = get_7_days_hot_bogs()
    context['hot_blogs_for_30_days'] = get_30_days_hot_bogs()
    return render(request,'home.html',context)

def login(request):
    '''username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = auth.authenticate(request, username=username, password=password)
    referer = request.META.get('HTTP_REFERER',reverse('home'))
    if user is not None:
        auth.login(request, user)
        return redirect(referer)
    else:
        return render(request,'error.html',{'message':'用户名或密码不正确'})'''
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
           user = login_form.cleaned_data['user']
           auth.login(request,user)
           return redirect(request.GET.get('from',reverse('home')))
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request,'login.html',context)

def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username,email,password)
            user.save()
            # 登录用户
            user = auth.authenticate(username=username,password=password)
            auth.login(request,user)
            return redirect(request.GET.get('from',reverse('home')))
    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)