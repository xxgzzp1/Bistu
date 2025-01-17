#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time : 2019-04-02 10:22
# @Author : ryuchen
# @Site :
# @File : models.py
# @Desc :
# ==================================================
import uuid

from django.db import models
from django.contrib.auth.models import User

from core.definition.enums import *
from contrib.education.models import Thesis
from contrib.colleges.models import Academy, Major, Research, Class


class Education(models.Model):
    """
    学习经历模型
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, verbose_name="唯一标识ID")
    edu_begin_time = models.DateField(null=True, verbose_name="开始时间")
    edu_finish_time = models.DateField(null=True, verbose_name="结束时间")
    edu_school_name = models.CharField(max_length=128, null=True, verbose_name="学校名称")
    edu_study_major = models.CharField(max_length=128, null=True, verbose_name="专业方向")
    edu_study_field = models.CharField(max_length=128, null=True, verbose_name="研究领域")

    def __str__(self):
        return "学校：{0}  专业：{1}".format(self.edu_school_name, self.edu_study_major)

    class Meta:
        db_table = 'education'
        verbose_name = "学习经历"
        verbose_name_plural = verbose_name
        default_permissions = ()
        permissions = [
            ("can_insert_education", "新增学习经历"),
            ("can_delete_education", "删除学习经历"),
            ("can_update_education", "修改学习经历"),
            ("can_search_education", "查询学习经历")
        ]


class Tutor(models.Model):
    """
    导师模型
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, verbose_name="唯一标识ID")
    tut_user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='tut_user', verbose_name="账户信息")
    tut_name = models.CharField(max_length=64, null=True, verbose_name="导师名称")
    tut_avatar = models.ImageField(upload_to="teachers", default='default.png', null=True, verbose_name="教师图片")
    tut_birth_day = models.DateField(max_length=128, null=True, verbose_name="出生日期")
    tut_entry_day = models.DateField(max_length=128, null=True, verbose_name="入职日期")
    tut_telephone = models.IntegerField(null=True, verbose_name="电话号码")
    tut_number = models.IntegerField(null=True, verbose_name="导师工号")
    tut_cardID = models.CharField(max_length=128, null=True, verbose_name="身份证号")
    tut_gender = models.CharField(max_length=64, null=True, choices=GenderChoice, verbose_name="性别")
    tut_title = models.CharField(max_length=64, null=True, choices=TitleChoice, verbose_name="职称")
    tut_political = models.CharField(max_length=64, null=True, choices=PoliticalChoice, verbose_name="政治面貌")
    tut_degree = models.CharField(max_length=64, null=True, choices=DegreeChoice, verbose_name="学位")
    tut_education = models.ForeignKey(Education, null=True, on_delete=models.CASCADE, related_name='tut_education',
                                      verbose_name="学历")
    tut_academy = models.ForeignKey(Academy, null=True, on_delete=models.CASCADE, related_name='tut_academy',
                                    verbose_name="所属学院")

    def get_gender(self):
        return GenderType[self.tut_gender].value
    get_gender.short_description = '性别'

    def get_title(self):
        return TitleType[self.tut_title].value
    get_gender.short_description = '职称'

    def get_degree(self):
        return DegreeType[self.tut_degree].value
    get_degree.short_description = '学历'

    def get_political(self):
        return PoliticalType[self.tut_political].value
    get_political.short_description = '政治面貌'

    def __str__(self):
        return "工号：{0}  姓名：{1}".format(self.tut_number, self.tut_name)

    class Meta:
        db_table = 'teacher'
        verbose_name = "导师"
        verbose_name_plural = verbose_name
        default_permissions = ()
        permissions = [
            ("can_insert_tutor", "新增导师"),
            ("can_delete_tutor", "删除导师"),
            ("can_update_tutor", "修改导师"),
            ("can_search_tutor", "查询导师")
        ]
        ordering = ['tut_number']


class Student(models.Model):
    """
    学生模型
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, verbose_name="唯一标识ID")
    stu_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stu_user", null=True, verbose_name="账户信息")
    stu_name = models.CharField(max_length=64, null=True, verbose_name="姓名")
    stu_number = models.IntegerField(null=True, verbose_name="学号")
    stu_avatar = models.ImageField(upload_to="students", default="default.png", null=True, verbose_name="学生照片")
    stu_gender = models.CharField(max_length=64, null=True, choices=GenderChoice, verbose_name="性别")
    stu_telephone = models.IntegerField(null=True, verbose_name="电话")
    stu_card_type = models.CharField(max_length=128, null=True, default="身份证", verbose_name="身份证件类型")
    stu_cardID = models.CharField(max_length=128, null=True, verbose_name="身份证号")
    stu_candidate_number = models.CharField(max_length=128, null=True, verbose_name="考生号")
    stu_birth_day = models.DateField(max_length=64, null=True, verbose_name="出生日期")
    stu_nation = models.CharField(max_length=64, null=True, default="汉", verbose_name="民族")
    stu_source = models.CharField(max_length=128, null=True, verbose_name="生源地")
    stu_is_village = models.BooleanField(default=False, null=True, verbose_name="是否农村学生")
    stu_political = models.CharField(max_length=64, null=True, choices=PoliticalChoice, verbose_name="政治面貌")
    stu_type = models.CharField(max_length=128, null=True, choices=StudentCategoryChoice, verbose_name="学生类型")
    stu_learn_type = models.CharField(max_length=64, null=True, choices=StudentLearnChoice, verbose_name='学习形式')
    stu_learn_status = models.CharField(max_length=64, null=True, choices=DegreeChoice, verbose_name='学习阶段')
    stu_grade = models.CharField(max_length=64, null=True, default='1', verbose_name='年级')
    stu_system = models.IntegerField(null=True, default=3, verbose_name='学制')
    stu_entrance_time = models.DateField(max_length=32, null=True, verbose_name='入学日期')
    stu_graduation_time = models.DateField(max_length=32, null=True, verbose_name='毕业日期')
    stu_cultivating_mode = models.CharField(max_length=128, choices=CultivatingModeChoice, null=True, verbose_name='培养方式')
    stu_enrollment_category = models.CharField(max_length=64, null=True, choices=EnrollmentCategoryChoice, default='E1', verbose_name='录取类别')
    stu_nationality = models.CharField(max_length=128, null=True, verbose_name='国籍', default='中国')
    stu_special_program = models.CharField(max_length=128, null=True, choices=SpecialProgramChoice, default='S1', verbose_name='专项计划')
    stu_is_regular_income = models.BooleanField(default=False, verbose_name='是否有固定收入')
    stu_is_tuition_fees = models.BooleanField(default=False, verbose_name='是否欠缴学费')
    stu_is_archives = models.BooleanField(default=False, verbose_name='档案是否转到学校')
    stu_is_exemption = models.BooleanField(default=False, verbose_name="是否推免生")
    stu_is_adjust = models.BooleanField(default=False, verbose_name="是否调剂")
    stu_is_volunteer = models.BooleanField(default=True, verbose_name="是否第一志愿")
    stu_is_superb = models.BooleanField(default=False, verbose_name="是否优秀毕业生")
    stu_is_delay = models.BooleanField(default=False, verbose_name="是否延期（中期考核）")
    stu_delay_reason = models.CharField(max_length=255, null=True, verbose_name="中期考核延期原因")
    stu_mid_check = models.CharField(max_length=64, null=True, choices=MidCheckChoice, verbose_name="中期考核结果")
    stu_status = models.CharField(max_length=64, null=True, choices=StudentStatusChoice, default='S1', verbose_name="在学状态")
    stu_gain_diploma = models.BooleanField(null=True, default=False, verbose_name="学位证")
    stu_gain_cert = models.BooleanField(null=True, default=False, verbose_name="毕业证")
    stu_tutor = models.ForeignKey(Tutor, null=True, related_name='stu_tutor', on_delete=models.SET_NULL, verbose_name="指导老师")
    stu_class = models.ForeignKey(Class, null=True, related_name='stu_class', on_delete=models.SET_NULL, verbose_name="所属班级")
    stu_major = models.ForeignKey(Major, null=True, related_name='stu_major', on_delete=models.SET_NULL, verbose_name="所属专业")
    stu_academy = models.ForeignKey(Academy, null=True, related_name='stu_academy', on_delete=models.SET_NULL, verbose_name='所属学院')
    stu_research = models.ForeignKey(Research, null=True, related_name='stu_research', on_delete=models.SET_NULL, verbose_name="科研方向")
    stu_thesis = models.ForeignKey(Thesis, null=True, related_name='stu_thesis', on_delete=models.SET_NULL, verbose_name="毕业论文")

    def get_gender(self):
        return GenderType[self.stu_gender].value
    get_gender.short_description = '性别'

    def get_political(self):
        return PoliticalType[self.stu_political].value
    get_political.short_description = '政治面貌'

    def get_stu_type(self):
        return StudentCategoryType[self.stu_type].value
    get_stu_type.short_description = '学生类型'

    def get_stu_learn_type(self):
        return StudentLearnType[self.stu_learn_type].value
    get_stu_learn_type.short_description = '学习形式'

    def get_stu_learn_status(self):
        return DegreeType[self.stu_learn_status].value
    get_stu_learn_status.short_description = '学习阶段'

    def get_stu_cultivating_mode(self):
        return CultivatingModeType[self.stu_cultivating_mode].value
    get_stu_cultivating_mode.short_description = '培养方式'

    def get_stu_enrollment_category(self):
        return EnrollmentCategoryType[self.stu_enrollment_category].value
    get_stu_enrollment_category.short_description = '录取类别'

    def get_stu_special_program(self):
        return SpecialProgramType[self.stu_special_program].value
    get_stu_special_program.short_description = '专项计划'

    def get_stu_mid_check(self):
        return MidCheckType[self.stu_mid_check].value
    get_stu_mid_check.short_description = '中期考核结果'

    def get_stu_status(self):
        return StudentStatusType[self.stu_status].value
    get_stu_status.short_description = '在学状态'

    def __str__(self):
        return "学生编号：{0}  学生姓名：{1}".format(self.stu_number, self.stu_name)

    class Meta:
        db_table = 'student'
        verbose_name = "学生"
        verbose_name_plural = verbose_name
        default_permissions = ()
        permissions = [
            ("can_insert_student", "新增学生"),
            ("can_delete_student", "删除学生"),
            ("can_update_student", "修改学生"),
            ("can_search_student", "查询学生")
        ]


class MidCheckReport(models.Model):
    """
    中期考核统计模型
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, verbose_name="唯一标识ID")
    time = models.DateField(null=False, default='2019', verbose_name="年份")
    schedule_count = models.IntegerField(null=False, default=0, verbose_name="按期考核人数")
    pass_count = models.IntegerField(null=False, default=0, verbose_name="延期考核人数")
    pass_proportion = models.IntegerField(null=False, default=0, verbose_name="延期考核比例")
    delay_count = models.IntegerField(null=False, default=0, verbose_name="延期考核人数")
    delay_proportion = models.IntegerField(null=False, default=0, verbose_name="延期考核比例")
    track_count = models.IntegerField(null=False, default=0, verbose_name="被跟踪人数")
    track_proportion = models.IntegerField(null=False, default=0, verbose_name="被跟踪比例")
    fail_count = models.IntegerField(null=False, default=0, verbose_name="不合格人数")
    fail_proportion = models.IntegerField(null=False, default=0, verbose_name="不合格比例")

    class Meta:
        db_table = 'mid_check_report'
        verbose_name = "中期考核统计"
        verbose_name_plural = verbose_name
        default_permissions = ()
        permissions = [
            ("can_insert_mid_check_report", "新增中期考核统计"),
            ("can_delete_mid_check_report", "删除中期考核统计"),
            ("can_update_mid_check_report", "修改中期考核统计"),
            ("can_search_mid_check_report", "查询中期考核统计")
        ]
