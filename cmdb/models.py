from django.db import models

# Create your models here.


class Asset(models.Model):
    """
    资产信息表
    """

    hostname = models.CharField("主机名", max_length=64, unique=True)
    ip = models.GenericIPAddressField("IP")
    cpu_mode = models.CharField("cpu", max_length=128)
    platform = models.CharField("系统信息", max_length=64)
    memory = models.CharField("内存信息", max_length=32)

    class Meta:

        verbose_name_plural = "资产信息表"

    def __str__(self):
        return self.hostname


class AssetRecord(models.Model):
    """资产修改表"""

    asset_number = models.IntegerField(null=True)
    content = models.TextField(null=True)
