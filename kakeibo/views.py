from django.shortcuts import render
from django.db import models

# Create your views here.
from django.views import generic
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Category, Kakeibo
from . forms import KakeiboForm,CategoryForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm


class KakeiboListView(ListView):
    model = Kakeibo
    template_name = 'kakeibo/kakeibo_list.html'

    def queryset(self):
        return Kakeibo.objects.all()
    

class KakeiboCreateView(CreateView):
    #利用するモデルを指定
    model = Kakeibo
    #利用するフォームクラス名を指定
    form_class = KakeiboForm
    #登録処理が正常終了した場合の遷移先を指定
    success_url = reverse_lazy('kakeibo:create_done')

def create_done(request):
       #登録処理が正常終了した場合に呼ばれるテンプレートを指定
   return render(request, 'kakeibo/create_done.html')


class KakeiboUpdateView(UpdateView):
   #利用するモデルを指定
   model = Kakeibo
   #利用するフォームクラス名を指定
   form_class = KakeiboForm
   #登録処理が正常終了した場合の遷移先を指定
   success_url = reverse_lazy('kakeibo:update_done')

def update_done(request):
    #更新処理が正常終了した場合に呼ばれるテンプレートを指定
    return render(request, 'kakeibo/update_done.html')


class KakeiboDeleteView(DeleteView):
    #利用するモデルを指定
    model = Kakeibo
    #削除処理が正常終了した場合の遷移先を指定
    success_url = reverse_lazy('kakeibo:delete_done')

def delete_done(request):
    return render(request, 'kakeibo/delete_done.html')


class CategoryCreateView(CreateView):
    #利用するモデルを指定
    model = Category
    #利用するフォームクラス名を指定
    form_class = CategoryForm
    #登録処理が正常終了した場合の遷移先を指定
    success_url = reverse_lazy('kakeibo:category_create_done')

def category_create_done(request):
       #登録処理が正常終了した場合に呼ばれるテンプレートを指定
   return render(request, 'kakeibo/category_create_done.html')


def show_circle_grahp(request):   
    #全データ取得
    kakeibo_data = Kakeibo.objects.all()
    
    #すべての金額の合計を求める
    total = 0
    for item in  kakeibo_data:
        total += item.money

    category_list =[]
    #全カテゴリ名をテーブルから取得する。
    category_data = Category.objects.all()
    #ループ処理でカテゴリ名のリストを作成する。
    for item in category_data:
        category_list.append(item.category_name)
    #つづいてカテゴリ毎の合計金額を求める
    category_dict = {}
    for i,item in enumerate(category_list):
        category_total = Kakeibo.objects.filter(category__category_name=category_list[i])\
        .aggregate(sum=models.Sum('money'))['sum']
        if category_total != None:
            ratio = int((category_total / total) *100)
            category_dict[item] = ratio
        else:
            ratio = 0
            category_dict[item] = ratio
        
    return render(request, 'kakeibo/kakeibo_circle.html',{
        'category_dict': category_dict,
         } )

