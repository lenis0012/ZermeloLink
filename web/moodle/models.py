from django.db import models

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=64)
    pub_date = models.DateTimeField('date added')

    def __unicode__(self):
        return unicode(self.name)

class Cohort(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.name)

class Teacher(models.Model):
    code = models.CharField(max_length=64)
    first_name = models.CharField(max_length=128)
    middle_name = models.CharField(max_length=128, default='')
    last_name = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    subjects = models.ManyToManyField(Subject)

    def __unicode__(self):
        return unicode(self.code)
