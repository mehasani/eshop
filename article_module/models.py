from django.db import models
from django.urls import reverse

from admin_module.models import Admin
from user_module.models import User


# Create your models here.


class ArticleCategory(models.Model):
    parent = models.ForeignKey('ArticleCategory', null=True, blank=True, on_delete=models.CASCADE,
                               verbose_name='دسته بندی والد')
    title = models.CharField(max_length=200, verbose_name='عنوان')
    url_title = models.CharField(max_length=200, unique=True, verbose_name='عنوان لینک')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    def __str__(self):
        return self.title

    class Meta:
        db_table='article_category'
        verbose_name = 'دسته بندی مقاله'
        verbose_name_plural = 'دسته بندی های مقاله'


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    slug = models.SlugField(max_length=400, db_index=True, allow_unicode=True, verbose_name='عنوان در url')
    image = models.ImageField(upload_to='images/articles', null=True, blank=True, verbose_name='تصویر مقاله')
    short_description = models.TextField(verbose_name='توضیحات کوتاه')
    text = models.TextField(verbose_name='متن مقاله')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    selected_categories = models.ManyToManyField(ArticleCategory, verbose_name='دسته بندی ها')
    author = models.ForeignKey(Admin, on_delete=models.CASCADE, verbose_name='نویسنده', null=True, editable=False)
    create_date = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='تاریخ ثبت')

    def selected_categories_list(self):
        return ', '.join(category.title for category in self.selected_categories.all())

    def __str__(self):
        return self.title

    def get_jalali_create_time(self):
        return self.create_date.strftime('%H:%M')

    class Meta:
        db_table='article'
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'


class ArticleComment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='مقاله')
    parent = models.ForeignKey('ArticleComment', on_delete=models.CASCADE, null=True, blank=True, verbose_name='والد')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    text = models.TextField(verbose_name='متن نظر')
    show_comment = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')

    def __str__(self):
        return str(self.user)

    class Meta:
        db_table='article_comment'
        verbose_name = 'نظر مقاله'
        verbose_name_plural = 'نظرات مقاله'
