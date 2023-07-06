from django.db import models

# Create your models here.

class Region(models.Model):
    region = models.CharField(max_length=264)
    def __str__(self):
        return self.region    
    
class State(models.Model):
    state = models.CharField(max_length=264)
    region = models.ForeignKey(Region ,on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.state

class Zone(models.Model):
    zone = models.CharField(max_length=264)
    state = models.ForeignKey(State,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.zone
    
class District(models.Model):
    district = models.CharField(max_length=264)
    zone = models.ForeignKey(Zone,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.district    
