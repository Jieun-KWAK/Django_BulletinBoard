from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog
from django.utils import timezone
from .forms import BlogForm, BlogModelForm, CommentForm

# Create your views here.
def home(request):
    # 블로그 글들을 모조리 띄우는 코드
    # 아래 코드 다 가져와
    #posts = Blog.objects.all()
    # 날짜 정렬
    posts = Blog.objects.filter().order_by('-date')
    return render(request, 'index.html', {'posts':posts})

# 블로그 글 작성 html을 보여주는 함수
def new(request):
    return render(request, 'new.html')

# 블로그 글을 저장해주는 함수
def create(request):
    if(request.method == 'POST'):
        post = Blog()
        post.title = request.POST['title']
        post.body = request.POST['body']
        post.date = timezone.now()
        post.save()
    return redirect('home')  


#django form을 이용해서 입력값을 받는 함수
# GET 요청과 (=입력값을 받을 수 있는 html을 갖다 줘야함)
# POST 요청 (= 입력한 내용을 데이터베이스에 저장. form에서 입력한 내용을 처리)
# 둘 다 처리가 가능하는 점이 특징임.
def formcreate(request):
    #입력을 받을 수 있는 html을 갖다주기
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid(): #유효성 판단 _vaild()
            post = Blog()
            post.title = form.cleaned_data['title']
            post.body = form.cleaned_data['body']
            post.save()
            return redirect('home')
    else:
        form = BlogForm()
    return render(request, 'form_create.html', {'form':form})



# modelformcreate
def modelformcreate(request):
    #입력을 받을 수 있는 html을 갖다주기
    if request.method == 'POST' or request.method == 'FILES':
        form = BlogModelForm(request.POST, request.FILES)
        if form.is_valid(): #유효성 판단 _vaild()
            form.save()
            return redirect('home')
    else:
        form = BlogModelForm()
    return render(request, 'form_create.html', {'form':form})


def detail(request, blog_id):
    #blog_id 번째 블로그 글을 디비로부터 갖고와서 
    blog_detail = get_object_or_404(Blog, pk=blog_id)
    #blog_id 번째 블로그 글을 detail.html로 띄워주는 코드

    comment_form = CommentForm()

    return render(request, 'detail.html', {'blog_detail':blog_detail, 'comment_form':comment_form})
 

def create_comment(request, blog_id):
    filled_form = CommentForm(request.POST)

    if filled_form.is_valid():
        finished_form = filled_form.save(commit=False)
        finished_form.post = get_object_or_404(Blog, pk=blog_id)
        finished_form.save()
        
    return redirect('detail', blog_id)