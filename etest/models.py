from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from datetime import datetime

class BaseModel(models.Model):
	id =              models.AutoField(primary_key=True)
	

class AppUser(BaseModel):
    user                     =  models.OneToOneField(User, on_delete=models.CASCADE, blank=True, related_name = 'app_user')
    input_user_name          =  models.CharField(max_length=255, null=False, blank=False)
    first_name               =  models.CharField(max_length=255, null=False, blank=False)
    last_name                =  models.CharField(max_length=255, null=False, blank=False)
    email                    =  models.EmailField(null=True,blank=True)
    password                 =  models.CharField(max_length=255, null=False, blank=False)

   
    def __str__(self) :
        return self.first_name + ' ' + self.last_name
    

    def save(self, *args, **kwargs):
        user = User.objects.create_user(
            username=self.input_user_name,
            email=self.email,
            password=self.password,
        )
        self.user = user
        super(AppUser, self).save(*args, **kwargs)


def upload_location_audio(instance, filename):
    current_date = datetime.today()
    file_path = 'etest/audio/{user_id}_{filename}'.format(
        user_id = instance.user.id,
        # lead_id = instance.lead.lead_display_id,
        filename = f"audio_{current_date}_2.mp3"
    )
    return file_path

class AudioData(BaseModel):
    user               = models.ForeignKey('AppUser',on_delete=models.SET_NULL, null=True, blank=True, default=1)
    audio_file         = models.FileField(upload_to=upload_location_audio)
    create_at          = models.DateField(null=False,blank=False,default= datetime.today())
