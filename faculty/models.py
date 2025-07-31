from django.db import models
from django.contrib.auth.models import User,AbstractUser
import os
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.db.models import Max
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

def validate_phone(value):
    if len(str(value)) != 10:
        raise ValidationError("Phone number must be exactly 10 digits.")
    if not str(value).isdigit():
        raise ValidationError("Phone number must contain only digits.")

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None , **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone=models.BigIntegerField(unique=True,validators=[validate_phone])
    place = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'place','phone']

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def _str_(self):
        return self.email



class Student(CustomUser):
    std_id=models.CharField(unique=True,max_length=50)
    student_name=models.CharField(max_length=100,null=True,blank=True)
    img=models.FileField(upload_to='media/Student Image',null=True,blank=True)
    options=( 
        ("Male","Male"),
        ("Female","Female"),
        ("Others","Others")
    )
    gender=models.CharField(max_length=100,choices=options,default="Male")
    age=models.PositiveIntegerField(null=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="user_addedby",default=1)
    def save(self, *args, **kwargs):
        if not self.std_id:  
            last_std_id = Student.objects.aggregate(max_id=Max('std_id'))['max_id']
            if last_std_id:
                new_id = int(last_std_id[3:]) + 1
            else:
                new_id = 1
            self.std_id = f"CQ{new_id:04d}"  
        if not self.user:
            self.user = self.request.user
        if self.pk is None or not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.std_id 
    


class StudyMaterialNotes(models.Model):
    name=models.CharField(max_length=100,null=True)
    text = models.URLField()
    user= models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='text_user')

    def __str__(self):
        return self.name

class StudyMaterialFile(models.Model):
    name=models.CharField(max_length=100,null=True)
    file = models.FileField(upload_to="media/files")
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='file_user')

    def __str__(self):
        return self.name

class Language(models.Model):
    lang = models.TextField()

    def __str__(self):
        return self.lang

class Questions(models.Model):
    question = models.TextField()
    user= models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='que_user')
    lang = models.ForeignKey(Language,on_delete=models.CASCADE,null=True)
 
    def __str__(self):
        return self.question

class Result(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='res_ans')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='res_user')
    is_correct = models.BooleanField(default=False)  # True if answer is fully correct
    score = models.IntegerField(default=0)  # Score assigned (0-5)
    feedback = models.TextField(blank=True, null=True)  # Store detailed feedback from GROQ
    attempt_time = models.DateTimeField(auto_now_add=True)  # Timestamp of attempt


class Discussion(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)

    
    def __str__(self):
        return self.title

class Comment(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.discussion.title}"

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    discussions = models.ManyToManyField(Discussion, related_name='tags')
    
    def __str__(self):
        return self.name
    
# class GameScore(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     game_type = models.CharField(max_length=20)  # 'number' or 'hangman'
#     score = models.IntegerField()
#     date_played = models.DateTimeField(auto_now_add=True)
#     won = models.BooleanField(default=False)

#     class Meta:
#         ordering = ['-date_played']