from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    publish_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="blog/posts/images/%Y/%m/%d/")
    text = RichTextField()

    class Meta:
        verbose_name = f"Статья"
        verbose_name_plural = "Статьи"
    
    def __str__(self):
        return self.title
    
    
# для блока Доставка и оплата
class Paragraph(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название',
        null=True, blank=True
    )
    text = models.TextField(
        verbose_name='Текст параграфа',
        null=True, blank=True
    )
    parent = models.ForeignKey(
        'self',
        verbose_name='Родительский параграф',
        on_delete=models.CASCADE,
        null=True, blank=True,
    )

    class Meta:
        verbose_name = 'Параграф'
        verbose_name_plural = 'Параграфы'