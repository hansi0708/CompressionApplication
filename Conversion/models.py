from django.db import models
class File_Form(models.Model):
    file = models.FileField()

# class Revenue(models.Model):
#     MonthlyFiles = models.CharField(max_length=50)
#     Month = models.CharField(max_length=50)

#     def __unicode__(self):
#         return u'%s %s' % (self.MonthlyFiles, self.Month)    

