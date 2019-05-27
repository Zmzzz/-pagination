from django.shortcuts import render,HttpResponse
from  rest_framework.views import APIView
from  rest_framework import serializers
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from api.models import *
from  api import models
from rest_framework.viewsets import GenericViewSet
from api.return_msg import TokenReturnMsg
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

# 分页功能
from  rest_framework.pagination import PageNumberPagination,LimitOffsetPagination

# 第一种继承PageNumberPagination或者LimitOffsetPagination
class MyPagePagination(PageNumberPagination):
    # 定义每一页显示的数据个数
    page_size = 2
    # 定义查询参数  ?page=1&size=2
    page_size_query_param = 'size'
    # 关于页码  ?page=1 想用p就写p
    page_query_param = 'p'
    # 最大返回数据的个数
    max_page_size = 5

class course(ViewSetMixin,APIView):
    # 查看所有的课程
    def list(self,*args,**kwargs):
        try:
            course_list=models.Course.objects.all()
            page=MyPagePagination()
            current_page_obj=page.paginate_queryset(course_list,self.request)
            ret=CourseModelSerializers(current_page_obj,many=True)
            return  Response(ret.data)
        except Exception as e:
            pass
    # 查看所有课程的详细信息
    def retrieve(self,*args,**kwargs):
        course_id=kwargs.get('pk')
        courseDetail=CourseDetail.objects.filter(course_id=course_id).first()
        ret=CourseDetailModelSerializers(courseDetail)
        return Response(ret.data)

# from  rest_framework import  mixins
#
# class course(mixins.ListModelMixin,mixins.RetrieveModelMixin,GenericViewSet):
#         queryset = models.Course.objects.all()
#         serializer_class = CourseModelSerializers
#

import  uuid
class login(APIView):
    def post(self,request,*args,**kwargs):
        """ 
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        ret = TokenReturnMsg()
        try:
            username=request.data.get('username')
            pwd=request.data.get('password')
            user=models.Userinfo.objects.filter(username=username,pwd=pwd).first()
            if  not user:
                ret.code=1001
                ret.error='账号或者密码错误'
                return Response(ret.dict)
            token=str(uuid.uuid1())
            models.Token.objects.update_or_create(user=user,defaults={'token':token})
            ret.token=token
            ret.username=username
            return  Response(ret.dict)
        except Exception as e:
            ret.code=1002
            ret.error='数据库连接错误'
            return  Response(ret.dict)


from  api.auth import LuffuAtuh
class mrio(APIView):
    authentication_classes = [LuffuAtuh]
    def get(self,request,*args,**kwargs):
        print(request.user)
        print(request.auth)
        return Response('微职业信息')
