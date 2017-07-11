from django import forms
from cmdb import models
from django.core.exceptions import ValidationError


class AssetForm(forms.Form):
    """对资产表的字段进行验证"""
    hostname = forms.CharField(required=True, error_messages={"required": "主机名不能为空"}, max_length=20)
    ip = forms.GenericIPAddressField(required=True, error_messages={"required": "IP地址不能为空", "invalid": "格式错误"})
    cpu_mode = forms.CharField(required=False, max_length=32)
    platform = forms.CharField(required=False, max_length=32)
    memory = forms.CharField(required=False, max_length=16)

    def clean_ip(self):
        """ip单独验证"""

        result = models.Asset.objects.filter(ip=self.cleaned_data["ip"])
        if result:
            raise ValidationError(message="IP地址已经存在", code="ip")

        else:
            return self.cleaned_data["ip"]

    def clean_hostname(self):
        """主机名验证"""

        result = models.Asset.objects.filter(hostname=self.cleaned_data["hostname"])
        if result:
            raise ValidationError(message="主机名已经存在", code="hostname")

        else:
            return self.cleaned_data["hostname"]


class AssetEditForm(forms.Form):
    """对资产表的字段进行验证"""
    id = forms.IntegerField(required=True)
    hostname = forms.CharField(required=True, error_messages={"required": "主机名不能为空"}, max_length=20)
    ip = forms.GenericIPAddressField(required=True, error_messages={"required": "IP地址不能为空", "invalid": "格式错误"})
    cpu_mode = forms.CharField(required=False, max_length=32)
    platform = forms.CharField(required=False, max_length=32)
    memory = forms.CharField(required=False, max_length=16)

    def clean_ip(self):
        """ip单独验证"""

        result = models.Asset.objects.exclude(id=self.cleaned_data["id"]).filter(ip=self.cleaned_data["ip"])
        if result:
            raise ValidationError(message="IP地址已经存在", code="ip")

        else:
            return self.cleaned_data["ip"]

    def clean_hostname(self):
        """主机名验证"""
        result = models.Asset.objects.exclude(id=self.cleaned_data["id"]).filter(hostname=self.cleaned_data["hostname"])
        if result:
            raise ValidationError(message="主机名已经存在", code="hostname")

        else:
            return self.cleaned_data["hostname"]
