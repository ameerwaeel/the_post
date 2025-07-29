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
    name=CKEditor5Field( config_name='default',verbose_name='name',null=True, blank=True)
    description=CKEditor5Field( config_name='default',verbose_name='description',null=True, blank=True)
    rightcolorfrom=models.CharField( max_length=50,verbose_name='right color from',null=True, blank=True)
    rightcolorto=models.CharField( max_length=50,verbose_name='right color to',null=True, blank=True)
    leftcolorfrom=models.CharField( max_length=50,verbose_name='left color from',null=True, blank=True)
    leftcolorto=models.CharField( max_length=50,verbose_name='left color to',null=True, blank=True)
    link = models.URLField(verbose_name='link',null=True, blank=True)
    main_img=models.ImageField(upload_to='main_img/',null=True, blank=True,verbose_name='main img')
    right_img=models.ImageField(upload_to='right_img/',null=True, blank=True,verbose_name='right img')
    left_img=models.ImageField(upload_to='left_img/',null=True, blank=True,verbose_name='left img')
    def save(self, *args, **kwargs):
        if not self.pk or OurWorks.objects.get(pk=self.pk).name != self.name:
            self.slug = self.generate_unique_slug(self.name, OurWorks)
        super().save(*args, **kwargs)
    def __str__(self): return str(self.name)
    class Meta:
        verbose_name = ("OurWork")
        verbose_name_plural = ("OurWorks")
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

class DescriptionTags(SlugUUIDMixin, TimeStampedModel):
    name=CKEditor5Field( config_name='default',verbose_name='name')
    class Meta:
        verbose_name = ("DescriptionTag")
        verbose_name_plural = ("DescriptionTags")

    def save(self, *args, **kwargs):
        if not self.pk or DescriptionTags.objects.get(pk=self.pk).name != self.name:
            self.slug = self.generate_unique_slug(self.name, DescriptionTags)
        super().save(*args, **kwargs)
    def __str__(self): return str(self.name)

class Projects(SlugUUIDMixin, TimeStampedModel):
    name=CKEditor5Field( config_name='default',verbose_name='name',null=True, blank=True)
    description=CKEditor5Field( config_name='default',verbose_name='description',null=True, blank=True)
    description_card=CKEditor5Field( config_name='default',verbose_name='description card',null=True, blank=True)    
    main_img=models.ImageField(upload_to='main_img/',verbose_name='main img',null=True, blank=True)
    logo=models.ImageField(upload_to='right_img/',null=True, blank=True,verbose_name='logo img')
    logo_card=models.ImageField(upload_to='logo_card/',null=True, blank=True,verbose_name='logo card')
    problem_defination=CKEditor5Field( config_name='default',verbose_name='problem defination',null=True,blank=True)
    our_solution=models.ManyToManyField("OurSolution", verbose_name=("our solution"),related_name='projects',blank=True)
    description_tags=models.ManyToManyField("DescriptionTags", verbose_name=("Description Tags"),related_name='projects',blank=True)
    branding=models.ManyToManyField("Branding", verbose_name=("Branding"),related_name='projects',blank=True)
    imges=models.ManyToManyField("Imgs",verbose_name=("imgs"), related_name='projects',blank=True)
    our_results=models.ManyToManyField("OurResults", verbose_name=("our results"),related_name='projects',blank=True)
    link = models.URLField(verbose_name=("link"), blank=True)
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
    before_img=models.ImageField(upload_to='before_img/',verbose_name='before img',null=True, blank=True)
    after_img=models.ImageField(upload_to='after_img/',verbose_name='after img',null=True, blank=True)
    after_description=CKEditor5Field( config_name='default',verbose_name='after description',null=True, blank=True)
    before_descrition=CKEditor5Field( config_name='default',verbose_name='before descrition',null=True, blank=True)
    # project=models.ForeignKey("Projects", verbose_name=("Project"), on_delete=models.CASCADE)
    class Meta:
        verbose_name = ("Our Result")
        verbose_name_plural = ("Our Results")

    def save(self, *args, **kwargs):
        if not self.pk or OurResults.objects.get(pk=self.pk).after_description != self.after_description:
            self.slug = self.generate_unique_slug(self.after_description, OurResults)
        super().save(*args, **kwargs)
    def __str__(self): return str(self.after_description)

class Branding(SlugUUIDMixin, TimeStampedModel):
    img=models.ImageField(upload_to='image/',verbose_name='img',null=True, blank=True)
    title=CKEditor5Field( config_name='default',verbose_name='title')
    description=CKEditor5Field( config_name='default',verbose_name='description')
    class Meta:
        verbose_name = ("Branding")
        verbose_name_plural = ("Branding")

    def save(self, *args, **kwargs):
        if not self.pk or Branding.objects.get(pk=self.pk).title != self.title:
            self.slug = self.generate_unique_slug(self.title, Branding)
        super().save(*args, **kwargs)
    def __str__(self): return str(self.title)

class DirectionSection(SlugUUIDMixin, TimeStampedModel):
    direction=CKEditor5Field( config_name='default',verbose_name='direction')
    class Meta:
        verbose_name = ("DirectionSection")
        verbose_name_plural = ("DirectionSections")

    def save(self, *args, **kwargs):
        if not self.pk or DirectionSection.objects.get(pk=self.pk).direction != self.direction:
            self.slug = self.generate_unique_slug(self.direction, DirectionSection)
        super().save(*args, **kwargs)
    def __str__(self): return str(self.direction)
class Imgs(SlugUUIDMixin, TimeStampedModel):
    # project=models.ForeignKey("Projects", verbose_name=("Project"), on_delete=models.CASCADE)
    img=models.ImageField(upload_to='image/',verbose_name='img',null=True, blank=True)
    title=CKEditor5Field( config_name='default',verbose_name='title')
    description=CKEditor5Field( config_name='default',verbose_name='description')
    direction=models.ManyToManyField("DirectionSection", verbose_name=("direction"),related_name='Imgs')
    class Meta:
        verbose_name = ("Imge")
        verbose_name_plural = ("Imges")

    def save(self, *args, **kwargs):
        if not self.pk or Imgs.objects.get(pk=self.pk).title != self.title:
            self.slug = self.generate_unique_slug(self.title, Imgs)
        super().save(*args, **kwargs)
    def __str__(self): return str(self.title)

class HomepageProjects(SlugUUIDMixin, TimeStampedModel):
    name=CKEditor5Field( config_name='default',verbose_name='name')
    description=CKEditor5Field( config_name='default',verbose_name='description')
    subdescription=CKEditor5Field( config_name='default',verbose_name='subdescription ')
    main_img=models.ImageField(upload_to='main_img/',verbose_name='main img',null=False, blank=False)
    logo=models.ImageField(upload_to='logo_img/',null=False, blank=False,verbose_name='logo img')
    link = models.URLField(verbose_name=("link"), null=True, blank=True)
    class Meta:
        verbose_name = ("Homepage Project")
        verbose_name_plural = ("Homepage Projects")

    def save(self, *args, **kwargs):
        if not self.pk or HomepageProjects.objects.get(pk=self.pk).name != self.name:
            self.slug = self.generate_unique_slug(self.name, HomepageProjects)
        super().save(*args, **kwargs)
    def __str__(self): return str(self.name)

class Counters(SlugUUIDMixin, TimeStampedModel):
    startup_numbers=models.PositiveIntegerField(verbose_name='startup_numbers')
    startup_description=CKEditor5Field( config_name='default',verbose_name='startup_description')
    strategies_numbers=models.PositiveIntegerField(verbose_name='strategies_numbers')
    strategies_description=CKEditor5Field( config_name='default',verbose_name='strategies_description')
    subscribbers_numbers=models.PositiveIntegerField(verbose_name='subscribbers_numbers')
    subscribbers_description=CKEditor5Field( config_name='default',verbose_name='subscribbers_description')

    class Meta:
        verbose_name = ("Counter")
        verbose_name_plural = ("Counters")

    def save(self, *args, **kwargs):
        if not self.pk or Counters.objects.get(pk=self.pk).startup_numbers != self.startup_numbers:
            self.slug = self.generate_unique_slug(self.startup_numbers, Counters)
        super().save(*args, **kwargs)
    def __str__(self): return str(self.startup_numbers)

class Services(SlugUUIDMixin, TimeStampedModel):
    name=CKEditor5Field( config_name='default',verbose_name='services name')

    class Meta:
        verbose_name = ("Service")
        verbose_name_plural = ("Services")

    def save(self, *args, **kwargs):
        if not self.pk or Services.objects.get(pk=self.pk).name != self.name:
            self.slug = self.generate_unique_slug(self.name, Services)
        super().save(*args, **kwargs)
    def __str__(self): return str(self.name)

