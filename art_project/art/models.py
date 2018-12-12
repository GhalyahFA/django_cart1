from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import post_save

class Category(models.Model):
    category= models.CharField(max_length=150)
    slug= models.SlugField(max_length= 200, unique= True)
    description= models.TextField(default="art")

    class Meta:
        verbose_name= 'category'
        verbose_name_plural= 'categories'

    def __str__(self):
        return self.category

    def save(self, *args, **kwargs):
        self.slug= slugify(self.category)
        super(Category, self).save(*args, **kwargs)



class Product(models.Model):
    name= models.CharField(max_length= 100)
    category= models.ForeignKey(Category, on_delete= models.PROTECT, related_name='products')
    photo= models.ImageField(null=True, blank=True)
    description= models.TextField()
    price= models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        ordering=('category',)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user= models.OneToOneField(User, on_delete= models.CASCADE)
    merchandise= models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.user.username

def post_save_profile_create(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
    user_profile, created= Profile.objects.get_or_create(user=instance)

post_save.connect(post_save_profile_create, sender=User)
