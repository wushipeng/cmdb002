from django.shortcuts import render, HttpResponse, render_to_response
from cmdb import models
# Create your views here.
import json
from django.template.context_processors import csrf
from cmdb.formsValidate import AssetForm, AssetEditForm
from cmdb.jsonFormat import JsonCustomEncoder
from cmdb_server import settings
import time
import paramiko
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import xlwt
import io


def index(request):
    """
    首页测试
    :param request:
    :return:
    """
    return render(request, "basic/index.html")


def page_trun(request, asset_all=models.Asset.objects.all()):
    """
    翻页
    :param request:
    :param asset_all:
    :return:
    """
    page = request.GET.get("page")
    # asset_all = models.Asset.objects.all()
    paginator = Paginator(asset_all, 2)  # 每页多少条数据

    try:
        asset_all = paginator.page(page)  # 返回 page（页数）的数据
    except PageNotAnInteger:
        asset_all = paginator.page(1)  # 第一页
    except EmptyPage:
        asset_all = paginator.page(1)  # 最后一页
    finally:
        return asset_all


def asset_info(request):
    """
    资产信息页面
    :param request:
    :return:
    """

    asset_all = page_trun(request)
    if request.method == "POST":
        indis = request.POST.get("indistinct")
        # print(indis)
        if indis:
            all_field = models.Asset._meta.get_fields()
            # field_list = []
            for field in all_field:
                dic = dict()
                dic[field.__dict__["name"]] = indis
                if field.__dict__["name"] == "id":
                    continue
                # print(field)
                asset_all = models.Asset.objects.filter(**dic)
                if asset_all:
                    break
            asset_all = page_trun(request, asset_all)
            return render(request, "asset/asset_info.html", {"asset": asset_all})
        find_condition = {}
        data_find = request.POST

        for key in data_find:
            # print(data_find[i])
            if not data_find[key] or key == "csrfmiddlewaretoken":
                continue
            find_condition[key] = data_find[key]
        print(find_condition)
        # print(bool(find_condition))
        asset_all = models.Asset.objects.filter(**find_condition)
        print(asset_all)
        if not find_condition:
            asset_all = models.Asset.objects.all()
        asset_all = page_trun(request, asset_all)
        return render(request, "asset/asset_info.html", {"asset": asset_all})

    return render(request, "asset/asset_info.html", {"asset": asset_all})


def asset_api(request):
    """入库"""
    # cpumode = request.POST.get("cpu_mode")
    if request.method == "POST":
        asset = json.loads(request.body.decode("utf-8"))
        # print(asset)
        models.Asset.objects.create(**asset)
    response = render(request, "asset/asset_api.html", {"csrftoken": csrf(request)})

    return response


def asset_add(request):
    """
    资产变更
    :param request:
    :return:
    """
    if request.method == "POST":
        # print("12123")
        # data = request.POST.dict()
        # data.pop("csrfmiddlewaretoken")
        res = {"status": True, "error": None, "data": None}
        obj = AssetForm(request.POST)
        if obj.is_valid():

            # print(obj.cleaned_data)
            models.Asset.objects.create(**obj.cleaned_data)
        else:
            # print(obj.errors.as_data())
            result = obj.errors.as_data()
            res["status"] = False
            res["error"] = json.dumps(result, cls=JsonCustomEncoder)
            # print(res["error"])
        return HttpResponse(json.dumps(res))
    return render(request, "asset/asset_add.html")


def asset_edit(request, nid):
    """
    资产修改
    :param request:
    :param nid:
    :return:
    """
    if request.method == "POST":
        res = {"status": True, "error": None, "data": None}

        obj = AssetEditForm(request.POST)
        if obj.is_valid():

            record = models.AssetRecord.objects.filter(asset_number=obj.cleaned_data["id"])
            data_old = models.Asset.objects.filter(id=obj.cleaned_data["id"]).values()[0]
            data_new = obj.cleaned_data
            c_to_us = settings.C_to_US
            now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            flag = 0
            for i in data_old:
                if data_old[i] != data_new[i]:
                    if record:
                        if flag == 0:
                            record_content = json.loads(record.values("content")[0]["content"])
                            flag = 1
                        # print(record_content)
                        record_content.append(now_time + "  " + "<font style='color:red;font-weight: bold;'>"
                                              + c_to_us[i] + "</font>" + "  " + data_old[i] + "  " +
                                              "变更为" + "  " + data_new[i])
                    else:
                        if flag == 0:
                            record_content = []
                            flag = 1

                        record_content.append(now_time + "  " + "<font style='color:red;font-weight: bold;'>"
                                              + c_to_us[i] + "</font>" + "  " + data_old[i] + "  " +
                                              "变更为" + "  " + data_new[i])

            try:
                type(record_content)
            except NameError:
                pass
            else:
                if record:

                    models.AssetRecord.objects.filter(asset_number=data_new["id"]).update(content=record_content)
                else:
                    models.AssetRecord.objects.create(asset_number=data_new["id"], content=record_content)
                models.Asset.objects.filter(id=obj.cleaned_data["id"]).update(**obj.cleaned_data)
        else:
            # print(obj.errors.as_data())
            result = obj.errors.as_data()
            res["status"] = False
            res["error"] = json.dumps(result, cls=JsonCustomEncoder)
            # print(res["error"])
        # print(res)
        return HttpResponse(json.dumps(res))
    data = models.Asset.objects.filter(id=nid).values()[0]
    return render(request, "asset/asset_edit.html", {"data": data})


def asset_delete(request, nid):
    """
    删除单项资产
    :param request:
    :param nid:
    :return:
    """
    # print(nid)
    data = {"info": ""}
    try:
        models.Asset.objects.get(id=nid).delete()
        models.AssetRecord.objects.filter(asset_number=nid).delete()
        data["info"] = "删除成功"

    except Exception:
        data["info"] = "删除失败"
    return HttpResponse(json.dumps(data))


def asset_details(request, nid):
    """
    资产详情
    :param request:
    :param nid:
    :return:
    """
    data = models.Asset.objects.filter(id=nid).values()[0]
    data_record = models.AssetRecord.objects.filter(asset_number=nid).values("content")
    if request.method == 'POST':
        data_record = data_record[0]["content"]

        return HttpResponse(data_record)
    if not data_record:
        data_record = ["没有进行过变更"]
        data_hidden = "NNNNN"  # 防止异常,占位
    else:
        data_hidden = json.loads(data_record[0]["content"])
        data_record = json.loads(data_record[0]["content"])
        if len(data_record) >= 5:
            data_record = data_record[-5:]

    return render(request, "asset/asset_details.html",
                  {"data": data, "data_record": data_record, "data_hidden": data_hidden})


def asset_update():
    """
    资产更新
    :return:
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='192.168.8.140', port=22)
    ssh.exec_command("python3.5 /XXX/XXXX/cleint.py")  # 标准输入、标准输出、标准错误
    # 关闭连接
    ssh.close()


def page_not_found(request):
    """404页面"""

    return render_to_response("basic/404NotFound.html")


def export_excel(request):
    """导出数据到excel表"""
    list_obj = models.Asset._meta.get_fields()
    list_data = models.Asset.objects.all().values()
    if list_obj:
        ws = xlwt.Workbook()
        w = ws.add_sheet("这是第一页")
        for i, j in zip(range(len(list_obj)), list_obj):
            # print(i,j.__dict__["_verbose_name"])
            w.write(0, i, j.__dict__["_verbose_name"])
        excel_row = 1
        for obj_d in list_data:
            for i, obj in zip(range(len(list_obj)), list_obj):
                row = obj.__dict__["name"]
                w.write(excel_row, i, obj_d[row])
            excel_row += 1
        sio = io.BytesIO()
        # print(sio)
        ws.save(sio)
        sio.seek(0)
        response = HttpResponse(sio.getvalue(), content_type='application/octet- stream')
        response['Content-Disposition'] = 'attachment; filename=test.xls'
        response.write(sio.getvalue())
        return response
    else:
        return HttpResponse("没有数据")
