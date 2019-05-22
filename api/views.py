from django.shortcuts import render,HttpResponse
from  rest_framework.views import APIView
from  rest_framework import serializers
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from api.models import *
from  api import models
from rest_framework import  generics
# Create your views here.
class CourseModelSerializers(serializers.ModelSerializer):
    level_id=serializers.CharField(source='get_level_id_display')
    class Meta:
        model=Course
        fields=['title','course_img','level_id','id']

class CourseDetailModelSerializers(serializers.ModelSerializer):
    course=serializers.CharField(source='course.title')
    recommended_course=serializers.SerializerMethodField()
    drectory=serializers.SerializerMethodField()
    class Meta:
        model=CourseDetail
        fields=['id','why','course','recommended_course','drectory']
    def get_recommended_course(self,obj):
        temp=[]
        for item in obj.recommended_course.all():
            temp.append({'id':item.id,'name':item.title})
        return temp
    def get_drectory(self,obj):
        temp=[]
        for item in  obj.course.drectory_set.all():
            temp.append({'id':item.id,'name':item.name})
        return temp

class DrectoryModelSerializers(serializers.ModelSerializer):
    class Meta:
        model=Drectory
        fields='__all__'

    class course(ViewSetMixin,APIView):
    # 查看所有的课程
    def list(self,*args,**kwargs):
        course_list=models.Course.objects.all()
        ret=CourseModelSerializers(course_list,many=True)
        return  Response(ret.data)
    # 查看所有课程的详细信息
    def retrieve(self,*args,**kwargs):
        course_id=kwargs.get('pk')
        courseDetail=CourseDetail.objects.filter(course_id=course_id).first()
        ret=CourseDetailModelSerializers(courseDetail)
        return Response(ret.data)

import  uuid
class login(APIView):
    def post(self,request,*args,**kwargs):
        ret = {'code': 1000}
        username=request.data.get('username')
        pwd=request.data.get('password')
        user=models.Userinfo.objects.filter(username=username,pwd=pwd).first()
        if  not user:
            ret['code']=1001
            ret['error']='账号或者密码错误'
        else:
            token=str(uuid.uuid1())
            models.Token.objects.update_or_create(user=user,defaults={'token':token})
            ret['token']=token
            ret['username']=username
        return  Response(ret)
from  api.auth import LuffuAtuh

class mrio(APIView):
    authentication_classes = [LuffuAtuh]
    def get(self,request,*args,**kwargs):
        print(request.user)
        print(request.auth)
        return Response('微职业信息')
