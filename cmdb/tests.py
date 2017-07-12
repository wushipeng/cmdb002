# from django.test import TestCase
#
# # Create your tests here.
# import django
# django.setup()
# from xlwt import *
# from cmdb import models
# import cmdb_server
# import os
# import io
# # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cmdb_server.settings")# project_name 项目名称
#
#
# def expoort():
#     list_obj = models.Asset._meta.get_fields()
#     list_data = models.Asset.objects.all().values()
#     if list_obj:
#         ws = Workbook(encoding="utf-8")
#         w = ws.add_sheet("这是第一页")
#         for i,j in zip(range(len(list_obj)),list_obj):
#             # print(i,j.__dict__["_verbose_name"])
#             w.write(0, i, j.__dict__["_verbose_name"])
#
#         excel_row = 1
#         for obj_d in list_data :
#
#             for i,obj in zip(range(len(list_obj)),list_obj):
#
#                 row = obj.__dict__["name"]
#
#                 w.write(excel_row, i, obj_d[row])
#             excel_row += 1
#         sio = io.StringIO()
#         ws.save(sio)
#         sio.seek(0)
#         response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
#         response['Content-Disposition'] = 'attachment; filename=test.xls'
#         response.write(sio.getvalue())
#         return response
#     else
#         return
# expoort()