from django.db import models

# Create your models here.
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django_countries.fields import CountryField
from django.utils.text import slugify
from django.utils import timezone
import uuid

class SlugUUIDMixin(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    class Meta:
        abstract = True

    def generate_unique_slug(self, base_value, model_cls):
        base_slug = slugify(base_value)
        slug = base_slug
        counter = 1
        while model_cls.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug
    
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Interests(SlugUUIDMixin, TimeStampedModel):
    name=models.CharField(max_length=255, null=False ,blank=False)
    class Meta:
        verbose_name = ("Interest")
        verbose_name_plural = ("Interests")

    def save(self, *args, **kwargs):
        if not self.pk or Interests.objects.get(pk=self.pk).name != self.name:
            self.slug = self.generate_unique_slug(self.name, Interests)
        super().save(*args, **kwargs)
    def __str__(self): return str(self.name)    


class ContactUS(SlugUUIDMixin, TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)    
    full_name = models.CharField(max_length=255, null=False ,blank=False)
    email = models.EmailField()
    phone = models.CharField(max_length=20, null=False ,blank=False)
    company_name = models.CharField(max_length=100)
    comment = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="total price")
    file = models.FileField(upload_to='chatcontactus/files/', null=True, blank=True)
    interests=models.ForeignKey(Interests, on_delete=models.CASCADE, null=False ,blank=False)
    class Meta:
        verbose_name = ("ContactUS")
        verbose_name_plural = ("ContactUS")

    def save(self, *args, **kwargs):
        if not self.pk or ContactUS.objects.get(pk=self.pk).full_name != self.full_name:
            self.slug = self.generate_unique_slug(self.full_name, ContactUS)
        super().save(*args, **kwargs)
    def __str__(self): return str(self.full_name)
         
class ChatContactUS(SlugUUIDMixin, TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)    
    full_name = models.CharField(max_length=255, null=False ,blank=False)
    email = models.EmailField()
    phone = models.CharField(max_length=20, null=False ,blank=False)
    company_name = models.CharField(max_length=100)
    comment = models.TextField()
    session = models.CharField(max_length=255, null=False ,blank=False)
    link= models.URLField(verbose_name=("link"), null=True, blank=True)

    class Meta:
        verbose_name = ("Chat ContactUS")
        verbose_name_plural = ("Chat ContactUS")

    def save(self, *args, **kwargs):
        if not self.pk or ChatContactUS.objects.get(pk=self.pk).full_name != self.full_name:
            self.slug = self.generate_unique_slug(self.full_name, ChatContactUS)
        super().save(*args, **kwargs)
    def __str__(self): return str(self.full_name)


class NewsLetter(SlugUUIDMixin, TimeStampedModel):
    email=models.EmailField(max_length=254,verbose_name='email',unique=True,null=False, blank=False)
    class Meta:
        verbose_name = ("NewsLetter")
        verbose_name_plural = ("NewsLetters")

    def save(self, *args, **kwargs):
        if not self.pk or NewsLetter.objects.get(pk=self.pk).email != self.email:
            self.slug = self.generate_unique_slug(self.email, NewsLetter)
        super().save(*args, **kwargs)
    def __str__(self): return str(self.email)    

