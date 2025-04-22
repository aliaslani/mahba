from django.db import models
from django.contrib.auth.models import User, AbstractUser
from accounts.constants import GENDER_CHOICES


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر')
#     phone_number = models.CharField(max_length=11, verbose_name='تلفن')
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='جنسیت')
#     birthdate = models.DateField('تاریخ تولد', null=True, blank=True)

#     class Meta:
#         verbose_name = 'پروفایل'
#         verbose_name_plural = 'پروفایل'

#     def __str__(self):
#         return self.user.username


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=11, verbose_name='تلفن')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='جنسیت')
    birthdate = models.DateField('تاریخ تولد', null=True, blank=True)
    profile_picture = models.ImageField('عکس پروفایل', upload_to='profile_pictures', default='profile_pictures/default.jpg')
    
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربر'

    def __str__(self):
        return self.username