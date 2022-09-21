from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from common.base.daobase import AESCharField


class AliyunDrive(models.Model):
    owner_id = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="所属用户ID")

    user_name = models.CharField(max_length=128, verbose_name="用户名")
    nick_name = models.CharField(max_length=128, verbose_name="昵称")
    user_id = models.CharField(max_length=32, verbose_name="用户ID")
    default_drive_id = models.CharField(max_length=16, verbose_name="存储ID")
    default_sbox_drive_id = models.CharField(max_length=16, verbose_name="保险箱ID")
    access_token = AESCharField(max_length=1536, verbose_name="访问token")
    refresh_token = AESCharField(max_length=512, verbose_name="刷新token")
    avatar = models.CharField(max_length=512, verbose_name="头像地址")
    expire_time = models.DateTimeField(verbose_name="过期信息", auto_now_add=True)

    used_size = models.BigIntegerField(verbose_name="已经使用空间", default=0)
    total_size = models.BigIntegerField(verbose_name="总空间大小", default=0)
    description = models.CharField(max_length=256, default='', verbose_name="备注信息", blank=True)
    enable = models.BooleanField(default=True, verbose_name="是否启用")
    private = models.BooleanField(default=True, verbose_name="是否私有，若设置为否，则该网盘可被其他用户进行上传下载")
    active = models.BooleanField(default=True, verbose_name="密钥是否可用")
    created_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = '阿里云网盘认证信息'
        verbose_name_plural = "阿里云网盘认证信息"
        unique_together = ('owner_id', 'user_id')

    def __str__(self):
        return f"所属用户:{self.owner_id}-网盘用户名:{self.user_name}-网盘昵称:{self.nick_name}-是否启用:{self.enable}"


class FileInfo(models.Model):
    # 文件下载连接实效4个小时，通过缓存进行存储
    owner_id = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="所属用户ID")
    aliyun_drive_id = models.ForeignKey(to=AliyunDrive, on_delete=models.CASCADE, verbose_name="所属阿里云盘ID")

    name = models.CharField(max_length=256, verbose_name="文件名字")
    file_id = models.CharField(max_length=64, verbose_name="文件id")
    drive_id = models.CharField(max_length=64, verbose_name="drive_id")
    created_at = models.DateTimeField(verbose_name="上传时间", auto_now_add=True)
    size = models.BigIntegerField(verbose_name="文件大小")
    content_type = models.CharField(max_length=64, verbose_name="文件类型")
    content_hash = models.CharField(max_length=64, verbose_name="content_hash")
    crc64_hash = models.CharField(max_length=64, verbose_name="crc64_hash")

    downloads = models.BigIntegerField(verbose_name="下载次数", default=0)
    description = models.CharField(max_length=256, verbose_name="备注信息", blank=True)

    class Meta:
        verbose_name = '文件信息'
        verbose_name_plural = "文件信息"

    def __str__(self):
        return f"所属用户:{self.owner_id}-文件名:{self.name}-下载次数:{self.downloads}-文件大小:{self.size}"


class ShareCode(models.Model):
    owner_id = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="所属用户ID")
    file_id = models.ManyToManyField(to=FileInfo, verbose_name="文件ID")
    short = models.CharField(max_length=16, unique=True, verbose_name="短链接", db_index=True)
    created_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    expired_time = models.DateTimeField(verbose_name="失效时间", null=True)
    password = models.CharField(max_length=16, verbose_name="访问密码", null=True, blank=True)
    description = models.CharField(max_length=256, verbose_name="备注信息", blank=True)

    class Meta:
        verbose_name = '分享信息'
        verbose_name_plural = "分享信息"

    def __str__(self):
        return f"所属用户:{self.owner_id}-短连接:{self.short}-失效时间:{self.expired_time}-分享密码:{self.password}"
