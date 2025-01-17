#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time : 2019-04-02 20:11 
# @Author : libin
# @Site :  
# @File : views.py
# @Desc : 
# ==================================================
from rest_framework import serializers
from apps.accounts.serializers import UserSerializers
from contrib.colleges.models import Major, Academy, Research, Class
from contrib.colleges.models import ReformResults, Reform


class ClassSerializers(serializers.ModelSerializer):
    """ 科研方向 """

    class Meta:
        model = Class
        fields = '__all__'


class ResearchSerializers(serializers.ModelSerializer):
    """ 科研方向 """

    class Meta:
        model = Research
        fields = '__all__'


class MajorSerializers(serializers.ModelSerializer):
    """ 学科专业 """
    maj_research = ResearchSerializers(many=True)
    student_count = serializers.SerializerMethodField(read_only=True)

    def get_student_count(self, major):
        return major.stu_major.count()

    class Meta:
        model = Major
        fields = ('uuid', 'maj_name', 'maj_code', 'maj_type', 'maj_first', 'maj_second',
                  'maj_setup_time', 'maj_degree', 'maj_research', 'student_count')

    def to_representation(self, instance):
        instance.maj_type = instance.get_maj_type_display()
        instance.maj_degree = instance.get_maj_degree_display()
        data = super(MajorSerializers, self).to_representation(instance)
        return data


class ReformSerializers(serializers.ModelSerializer):
    """ 研究生教育改革成果记录 """

    class Meta:
        model = Reform
        fields = '__all__'


class ReformResultsSerializers(serializers.ModelSerializer):
    """ 研究生教育改革成果统计 """

    class Meta:
        model = ReformResults
        fields = '__all__'


class AcademySerializer(serializers.ModelSerializer):
    """ 学院 """
    aca_majors = MajorSerializers(many=True)
    aca_user = UserSerializers(many=False)
    student_count = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_student_count(academy):
        return academy.stu_academy.count()

    class Meta:
        model = Academy
        fields = ('uuid', 'aca_avatar', 'aca_nickname', 'aca_cname', 'aca_ename', 'aca_code', 'aca_phone', 'aca_fax',
                  'aca_href', 'aca_brief', 'aca_user', 'aca_majors', 'student_count')
