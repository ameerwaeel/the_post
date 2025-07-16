from django.db import models

# Create your models here.
from django.db import models
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django_countries.fields import CountryField
from django.utils.text import slugify
from django.utils import timezone
import uuid

from django.db import models
from django.utils.text import slugify
from django.utils import timezone
import uuid


# models.py - Final Version
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify
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

    # title = CKEditor5Field( config_name='default',related_name='projects')
class OurWorks(SlugUUIDMixin, TimeStampedModel):
    name=CKEditor5Field( config_name='default',verbose_name='name')
    description=CKEditor5Field( config_name='default',verbose_name='description')
    rightcolor=models.CharField( max_length=50,verbose_name='right color')
    leftcolor=models.CharField( max_length=50,verbose_name='left color')
    link = models.URLField(verbose_name='link')
    main_img=models.ImageField(upload_to='main_img/',null=False, blank=False,verbose_name='main img')
    right_img=models.ImageField(upload_to='right_img/',null=False, blank=False,verbose_name='right img')
    left_img=models.ImageField(upload_to='left_img/',null=False, blank=False,verbose_name='left img')
    def save(self, *args, **kwargs):
        if not self.pk or OurWorks.objects.get(pk=self.pk).name != self.name:
            self.slug = self.generate_unique_slug(self.name, OurWorks)
        super().save(*args, **kwargs)
    def __str__(self): return str(self.name)
    class Meta:
        verbose_name = ("OurWork")
        verbose_name_plural = ("OurWorks")



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

class WhoWeAre(SlugUUIDMixin, TimeStampedModel):
    name=CKEditor5Field( config_name='default',verbose_name='name')
    position=CKEditor5Field( config_name='default',verbose_name='position')
    whoimg=models.ImageField(upload_to='who_img/',null=False, blank=False,verbose_name='who img')

    class Meta:
        verbose_name = ("WhoWeAre")
        verbose_name_plural = ("WhoWeAre")

    def save(self, *args, **kwargs):
        if not self.pk or WhoWeAre.objects.get(pk=self.pk).name != self.name:
            self.slug = self.generate_unique_slug(self.name, WhoWeAre)
        super().save(*args, **kwargs)
    def __str__(self): return str(self.name)
    

class Logo(SlugUUIDMixin, TimeStampedModel):
    name=CKEditor5Field( config_name='default',verbose_name='name')
    link = models.URLField(verbose_name='link')
    logoimg=models.ImageField(upload_to='logo_img/',null=False, blank=False,verbose_name='logo img')

    class Meta:
        verbose_name = ("Logo")
        verbose_name_plural = ("Logos")

    def save(self, *args, **kwargs):
        if not self.pk or Logo.objects.get(pk=self.pk).name != self.name:
            self.slug = self.generate_unique_slug(self.name, Logo)
        super().save(*args, **kwargs)
    def __str__(self): return str(self.name)

class Projects(SlugUUIDMixin, TimeStampedModel):
    name=CKEditor5Field( config_name='default',verbose_name='name')
    description=CKEditor5Field( config_name='default',verbose_name='description')
    # link = models.URLField(verbose_name='link')
    main_img=models.ImageField(upload_to='main_img/',verbose_name='main img',null=False, blank=False)
    logo=models.ImageField(upload_to='right_img/',null=False, blank=False,verbose_name='logo img')
    problem_defination=CKEditor5Field( config_name='default',verbose_name='problem defination')
    our_solution=models.ManyToManyField("OurSolution", verbose_name=("our solution"),related_name='projects')
    imges=models.ManyToManyField("Imgs",verbose_name=("imgs"), related_name='projects')
    our_results=models.ManyToManyField("OurResults", verbose_name=("our results"),related_name='projects')
    link = models.URLField(verbose_name=("link"), null=True, blank=True)
    class Meta:
        verbose_name = ("Project")
        verbose_name_plural = ("Projects")

    def save(self, *args, **kwargs):
        if not self.pk or Projects.objects.get(pk=self.pk).name != self.name:
            self.slug = self.generate_unique_slug(self.name, Projects)
        super().save(*args, **kwargs)
    def __str__(self): return str(self.name)

class OurSolution(SlugUUIDMixin, TimeStampedModel):
    # Project=models.ForeignKey("Projects", verbose_name=("Project"), on_delete=models.CASCADE)
    text=CKEditor5Field( config_name='default',verbose_name='text')
    answer=CKEditor5Field( config_name='default',verbose_name='answer')
    class Meta:
        verbose_name = ("Our Solution")
        verbose_name_plural = ("Our Solutions")
    def save(self, *args, **kwargs):
        if not self.pk or OurSolution.objects.get(pk=self.pk).text != self.text:
            self.slug = self.generate_unique_slug(self.text, OurSolution)
        super().save(*args, **kwargs)
    def __str__(self): return str(self.text)


class OurResults(SlugUUIDMixin, TimeStampedModel):
    before_img=models.ImageField(upload_to='before_img/',verbose_name='before img',null=False, blank=False)
    after_img=models.ImageField(upload_to='after_img/',verbose_name='after img',null=False, blank=False)
    after_description=CKEditor5Field( config_name='default',verbose_name='after description')
    before_descrition=CKEditor5Field( config_name='default',verbose_name='before descrition')
    # project=models.ForeignKey("Projects", verbose_name=("Project"), on_delete=models.CASCADE)
    class Meta:
        verbose_name = ("Our Result")
        verbose_name_plural = ("Our Results")

    def save(self, *args, **kwargs):
        if not self.pk or OurResults.objects.get(pk=self.pk).after_description != self.after_description:
            self.slug = self.generate_unique_slug(self.after_description, OurResults)
        super().save(*args, **kwargs)
    def __str__(self): return str(self.after_description)
    
class Imgs(SlugUUIDMixin, TimeStampedModel):
    # project=models.ForeignKey("Projects", verbose_name=("Project"), on_delete=models.CASCADE)
    img=models.ImageField(upload_to='image/',verbose_name='img',null=False, blank=False)
    title=CKEditor5Field( config_name='default',verbose_name='title')
    description=CKEditor5Field( config_name='default',verbose_name='description')
    class Meta:
        verbose_name = ("Imge")
        verbose_name_plural = ("Imges")

    def save(self, *args, **kwargs):
        if not self.pk or Imgs.objects.get(pk=self.pk).title != self.title:
            self.slug = self.generate_unique_slug(self.title, Imgs)
        super().save(*args, **kwargs)
    def __str__(self): return str(self.title)