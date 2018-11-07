from django.db import models

# Create your models here.
# class Category(models.Model):
#     cate_name = models.CharField(max_length=200)


class News(models.Model):
    title = models.CharField(u'标题', max_length=200)
    content = models.TextField(u'内容')
    is_publish = models.CharField(u'是否发布', max_length=2)
    category = models.CharField(u'分类', max_length=20)
    create_dt = models.DateTimeField('发表时间', auto_now_add=True, editable=True)

    def __str__(self):
        return self.title

    def to_json_dict(self):
        return {u'title': self.title, u'content': self.content, u'create_dt': self.create_dt.strftime('%Y-%m-%d %H:%M:%S')}


class Member(models.Model):
    name = models.CharField(u'用户名', max_length=50, unique=True)
    passwd = models.CharField(u'密码', max_length=50)
    active = models.CharField(u'是否激活', max_length=2)
    create_dt = models.DateTimeField(u'创建时间', auto_now_add=True, editable=True)

    def __str__(self):
        return self.name

    def to_json_dict(self):
        return {u'name': self.name, u'active': self.active, u'create_dt': self.create_dt.strftime('%Y-%m-%d %H:%M:%S')}