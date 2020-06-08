from django.shortcuts import render
from django.views import View
from . import models
import json
from django.http import HttpResponse, JsonResponse
from dateutil.parser import parse
from django.db import connection
from django.db.utils import ProgrammingError, IntegrityError


class NationView(View):
    def put(self, request):
        print(request.body)
        req = json.loads(request.body)
        print(req)
        NationName = req.get('NationName', None)
        Area = req.get('Area', None)
        Comment = req.get('Comment', None)
        
        instance = models.Nation(NationName=NationName, Area=Area, Comment=Comment)
        instance.save()
        return JsonResponse({'status': 'success', 'msg': 'success'})
            
    def get(self, request):
        temp = models.Nation.objects.all().values()
        res = {'Nation': list(temp)}
        return JsonResponse(res)

    def delete(self, request):
        req = request.body
        result = models.Nation.objects.filter(NationName=req.decode())
        print(result)
        print(result.values())
        result.delete()
        return JsonResponse({'status': 'success', 'msg': 'success'})


class CityView(View):
    def put(self, request):
        req = json.loads(request.body)
        CityName = req.get('CityName')
        PowerTariff = req.get('PowerTariff')
        NationName = req.get('NationName')

        n = models.Nation.objects.get(NationName=NationName)
        instance = models.City(CityName=CityName, PowerTariff=PowerTariff, NationName=n)
        instance.save()

        return JsonResponse({'status': 'success', 'msg': 'success'})

    def get(self, request):
        temp = models.CityInfo.objects.all().values()
        res = {'City': list(temp)}
        return JsonResponse(res)
        

class ProviderView(View):

    def put(self, request):
        req = json.loads(request.body)
        ProviderName = req.get('ProviderName')
        NationName = req.get('NationName')
        EstablishedTime = parse(req.get('EstablishedTime'))
        Comment = req.get('Comment')
        Nation = models.Nation.objects.get(NationName=NationName)
        
        instance = models.Provider(ProviderName=ProviderName, NationName=Nation, 
                                 EstablishedTime=EstablishedTime, Comment=Comment)
        instance.save()

        return JsonResponse({'status': 'success', 'msg': 'success'})

    def get(self, request):
        temp = models.Provider.objects.all().values()
        res = {'Provider': list(temp)}
        return JsonResponse(res)

    def delete(self, request):
        print(request.body)
        req = json.loads(request.body)
        ProviderName = req.get('ProviderName')
        NationName = req.get('NationName')
        
        Nation = models.Nation.objects.get(NationName=NationName)
        Provider = models.Provider.objects.get(ProviderName=ProviderName, NationName=NationName)
        Provider.delete()

        return JsonResponse({'status': 'success', 'msg': 'success'})


class DatacenterView(View):

    def put(self, request):
        req = json.loads(request.body)
        print(req)
        DatacenterName = req['DatacenterName']
        DatacenterCapacity = req['DatacenterCapacity']
        DatacenterAvaliableCapacity = req['DatacenterAvaliableCapacity']
        CityName = req['CityName']
        NationName = req['NationName']
        Comment = req['Comment']

        with connection.cursor() as cursor:
            cursor.execute('exec DatacenterInfo_Insert %s,%s,%s,%s,%s,%s',
                            [DatacenterName, DatacenterCapacity, DatacenterAvaliableCapacity, 
                             CityName, NationName, Comment])
        
        return JsonResponse({'status': 'success', 'msg': 'success'})

    def get(self, request):
        temp = models.DatacenterInfo.objects.all().values()
        return JsonResponse({'Datacenter': list(temp)})

    def delete(self, request):
        req = json.loads(request.body)
        DatacenterName = req.get('DatacenterName')
        temp = models.Datacenter.objects.get(DatacenterName=DatacenterName)
        temp.delete()

        return JsonResponse({'status': 'success', 'msg': 'success'})


class Container(View):

    def put(self, request):
        req = json.loads(request.body)
        ContainerName = req.get('ContainerName')
        ContainerIP = req.get('ContainerIP')
        DatacenterName = req.get('DatacenterName')
        ProviderName = req.get('ProviderName')
        LastBootTime = parse(req.get('LastBootTime'))
        Comment = req.get('Comment')

        cursor = connection.cursor() 

        cursor.execute('exec Container_Insert  %s,%s,%s,%s,%s,%s',
                        [ContainerName, ContainerIP, DatacenterName,
                        ProviderName, LastBootTime, Comment])
        return JsonResponse({'status': 'success', 'msg': 'success'})
        
        '''
        instance = models.Container(ContainerName=ContainerName, ContainerIP=ContainerIP, 
                                    DatacenterName=DatacenterName, LastBootTime=LastBootTime, 
                                    ProviderName=ProviderName, Comment=Comment)
        
        try:
            instance.save()
        except (ProgrammingError, IntegrityError) as e:
            print(e)
            response =  JsonResponse({'status': 'success', 'msg': str(e)})
            response.status_code=400
            return response

        '''
    
    def post(self, request):
        req = json.loads(request.body)
        ContainerName = req.get('ContainerName')
        ContainerIP = req.get('ContainerIP')
        DatacenterName = req.get('DatacenterName')
        ProviderName = req.get('ProviderName')
        LastBootTime = parse(req.get('LastBootTime'))
        Comment = req.get('Comment')

        with connection.cursor() as cursor:
            cursor.execute('exec Container_Update  %s,%s,%s,%s,%s,%s',
                           [ContainerName, ContainerIP, DatacenterName,
                            ProviderName, LastBootTime, Comment])
        
        return JsonResponse({'status': 'success', 'msg': 'success'})

    def get(self, request):
        temp = models.ContainerInfo.objects.all().values()
        return JsonResponse({'Container': list(temp)})

    def delete(self, request):
        req = json.loads(request.body)
        ContainerName = req.get('ContainerName')

        with connection.cursor() as cursor:
            cursor.execute('''SET xact_abort ON
                              BEGIN TRAN Container_Cascade
                              DELETE FROM ContainerService WHERE ContainerName_id = %s
                              DELETE FROM Container WHERE ContainerName = %s
                              COMMIT TRAN Container_Cascade
                           ''', [ContainerName, ContainerName])
        
        return JsonResponse({'status': 'success', 'msg': 'success'})
        

class Service(View):

    def put(self, request):
        req = json.loads(request.body)
        ServiceName = req.get('ServiceName')
        Describe = req.get('Describe')

        instance = models.Service(ServiceName=ServiceName, Describe=Describe)
        instance.save()

        return JsonResponse({'status': 'success', 'msg': 'success'})

    def get(self, request):
        temp = models.Service.objects.all().values()
        return JsonResponse({'Service': list(temp)})

    def delete(self, request):
        req = json.loads(request.body)
        ServiceName = req.get('ServiceName')

        with connection.cursor() as cursor:
            cursor.execute('''SET xact_abort ON
                              BEGIN TRAN
                              DELETE FROM ContainerService WHERE ServiceName_id = %s
                              DELETE FROM Service WHERE ServiceName = %s
                              COMMIT TRAN
                           ''', [ServiceName, ServiceName])
        
        return JsonResponse({'status': 'success', 'msg': 'success'})

class ContainerService(View):

    def put(self, request):
        req = json.loads(request.body)

        Char = req.get('Char', None)
        if Char == "高级筛选":
            pass
        ContainerName = req.get('ContainerName')
        ServiceName = req.get('ServiceName')
        StartTime = parse(req.get('StartTime'))
        Comment = req.get('Comment')
        ContainerName = models.Container.objects.get(ContainerName=ContainerName)
        ServiceName = models.Service.objects.get(ServiceName=ServiceName)

        instance = models.ContainerService(ContainerName=ContainerName, ServiceName=ServiceName, 
                                           StartTime=StartTime, Comment=Comment)
        instance.save()

        return JsonResponse({'status': 'success', 'msg': 'success'})

    def get(self, request):
        if request.GET.get('Char') == '数据中心':
            Value = request.GET.get('Value')

            with connection.cursor() as cursor:
                cursor.execute('''select CS.ServiceName_id, S.Describe, C.ContainerName, C.CityName, C.NationName, C.DatacenterName, CS.StartTime, CS.Comment
                                  from (ContainerService CS join ContainerInfo C 
                                  on CS.ContainerName_id = C.ContainerName) join Service S
                                  on CS.ServiceName_id = S.ServiceName
                                  where C.DatacenterName = %s
                               ''', [Value])
                row = cursor.fetchall()
            
            req_list = []

            for item in row:
                serv_dict = {}

                serv_dict['ServiceComment'] = item[7]
                serv_dict['StartTime'] = item[6]
                serv_dict['ServiceName'] = item[0]
                serv_dict['Describe'] = item[1]
                serv_dict['ContainerName'] = item[2]
                serv_dict['DatacenterName'] = item[5]
                serv_dict['CityName'] = item[3]
                serv_dict['NationName'] = item[4]

                req_list.append(serv_dict)

            return JsonResponse({'ContainerService': req_list}) 
        
        elif request.GET.get('Char') is None:
            req_list = []

            temp = models.ContainerService.objects.all()
            for cs in temp:
                
                serv_dict = {}

                serv_dict['ServiceComment'] = cs.Comment 
                serv_dict['StartTime'] = cs.StartTime

                temp = models.Service.objects.get(ServiceName=cs.ServiceName_id)
                serv_dict['ServiceName'] = temp.ServiceName
                serv_dict['Describe'] = temp.Describe

                temp = models.ContainerInfo.objects.get(ContainerName=cs.ContainerName_id)
                serv_dict['ContainerName'] = temp.ContainerName
                serv_dict['DatacenterName'] = temp.DatacenterName
                serv_dict['CityName'] = temp.CityName
                serv_dict['NationName'] = temp.NationName

                req_list.append(serv_dict)
            
            return JsonResponse({'ContainerService': req_list}) 
    
    def delete(self, request):
        req = json.loads(request.body)
        Char = req.get('Char', None)

        if Char == "数据中心":
            Value = req.get('Value')
            with connection.cursor() as cursor:
                cursor.execute('''
                                SET xact_abort ON
                                BEGIN TRAN AdvanceServiceDelete
                                DELETE ContainerService
                                FROM Container JOIN ContainerService ON Container.ContainerName = ContainerService.ContainerName_id 
                                WHERE Container.DatacenterName_id = %s
                                COMMIT TRAN''', [Value])
        elif Char == "容器名称":
            Value = req.get('Value')
            with connection.cursor() as cursor:
                cursor.execute('''
                                SET xact_abort ON
                                BEGIN TRAN AdvanceServiceDelete
                                DELETE ContainerService
                                FROM Container JOIN ContainerService ON Container.ContainerName = ContainerService.ContainerName_id 
                                WHERE Container.ContainerName = %s
                                COMMIT TRAN''', [Value])
        
        elif Char is None:
            ServiceName = req.get('ServiceName')
            ContainerName = req.get('ContainerName')
            temp = models.ContainerService.objects.get(ServiceName=ServiceName, ContainerName=ContainerName)
            temp.delete()
        
        return JsonResponse({'status': 'success', 'msg': 'success'})
    

