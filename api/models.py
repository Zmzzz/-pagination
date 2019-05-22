from django.db import models

# Create your models here.
class Course(models.Model):
    title=models.CharField(max_length=12)
    course_img=models.CharField(max_length=12)
    level_choiced=(
        (1,'初级'),
        (2,'中级'),
        (3,'高级'),
        (4,'秃顶')
    )
    level_id=models.IntegerField(choices=level_choiced)
    def __str__(self):
        return self.title

class CourseDetail(models.Model):
    why=models.CharField(max_length=200)
    course=models.OneToOneField(to='Course')
    recommended_course = models.ManyToManyField(to='Course',related_name='rc')
    def __str__(self):
        return  self.course.title

class Drectory(models.Model):
    course=models.ForeignKey(to='Course')
    name=models.CharField(max_length=12)
    def __str__(self):
        return self.name

class Userinfo(models.Model):
    username=models.CharField(max_length=12)
    pwd=models.CharField(max_length=8)

class Token(models.Model):
    user=models.OneToOneField(to='Userinfo')
    token=models.CharField(max_length=50)
