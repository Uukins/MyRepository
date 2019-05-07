from django.shortcuts import get_object_or_404,render
from django.core.paginator import Paginator
from django.db.models import Count
from .models import Blog,BlogType
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import read_statistics_once_read
from read_statistics.utils import get_seven_days_read_data,get_today_hot_data,get_yesterday_hot_data,get_7_days_hot_bogs,get_30_days_hot_bogs
from django.core.cache import cache
from mysite.forms import LoginForm


def get_blog_list_common_data(request,blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.EAHC_PAGE_BLOGS_NUMBER)
    page_num = request.GET.get('page', 1)  # 获取页面参数（GET请求）
    page_of_blogs = paginator.get_page(page_num)
    currentr_page_num = page_of_blogs.number  # 获取当前页码
    # 获取当前页码前后两页的范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 获取博客分类的对应博客数量
    '''blog_types = BlogType.objects.all()
    blog_types_list = []
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        blog_types_list.append(blog_type)
        '''

    #获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')

    blog_dates_dict={}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                            created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date]=blog_count


    context = {}
    context['page_range'] = page_range
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates'] = blog_dates_dict
    return context

def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request,blogs_all_list)

    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates,read_nums = get_seven_days_read_data(blog_content_type)

    #获取7天热门博客的缓存数据
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = get_7_days_hot_bogs()
        cache.set('hot_blogs_for_7_days',hot_blogs_for_7_days,3600)

    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['hot_blogs_for_7_days'] = get_7_days_hot_bogs()
    context['hot_blogs_for_30_days'] = get_30_days_hot_bogs()
    return render(request,'blog/blog_list.html',context)

def blogs_with_type(request,blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request,blogs_all_list)

    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))

    return render(request,'blog/blogs_with_type.html',context)

def blogs_with_date(request,year,month):
    blogs_all_list = Blog.objects.filter(created_time__year=year,created_time__month=month)
    context = get_blog_list_common_data(request,blogs_all_list)
    context['blogs_with_date'] = '%s年%s月'%(year,month)
    return render(request,'blog/blogs_with_date.html',context)

def blog_detail(request,blog_pk):
    blog =get_object_or_404(Blog,pk = blog_pk)
    read_cookie_key = read_statistics_once_read(request,blog)

    context={}
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog
    context['login_form']=LoginForm()
    response = render(request,'blog/blog_detail.html',context) #响应
    response.set_cookie(read_cookie_key,'true') # 阅读cookie标记
    return response

def hot_blogs_number(request):
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
    return render(request,'blog/blog_list.html',context)
