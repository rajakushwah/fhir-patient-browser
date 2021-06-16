from django.shortcuts import render , get_object_or_404
from operator import itemgetter
import requests
import json
import adal
from django.http import JsonResponse
from django.core.paginator import Paginator


#Function to extract patient data based on id,all patients
pid=""
TOKEN=""
encounter_id=""
observation_id=""
url=""
Resource=""
def home(request):
    # oauth 2.0 --FHIR SERVER AUTHORIZATION
    # Opening JSON file
    f = open('app/credentials.json')
    data = json.load(f)
    TENANT_ID = data.get('TENANT_ID')
    CLIENT = data.get('CLIENT_ID')
    KEY = data.get('CLIENT_SECRET')
    authority_url = 'https://login.microsoftonline.com/' + TENANT_ID
    global Resource
    Resource=data.get('RESOURCE_ID')
    context = adal.AuthenticationContext(authority_url)
    global token
    token = context.acquire_token_with_client_credentials(
        resource=Resource,
        client_id=CLIENT,
        client_secret=KEY)
    global TOKEN
    TOKEN = token["accessToken"]

    # Get Patient by id
    if request.method == "POST":
        lst = []
        global pid
        pid = request.POST.get('ID', '')
        url = Resource+"/Patient/{}".format(pid)
        newHeaders = {'Content-type': 'application/json',"Authorization": "Bearer %s" %TOKEN}
        response = requests.get(url, headers=newHeaders,verify=False)
        data = response.json()
        if response.ok:
            l = []
            resourceType = data['resourceType']
            l.append(resourceType)

            id = data['id']
            l.append(id)

            try:
                birth = data['birthDate']
            except:
                birth = "No data available"
            l.append(birth)

            try:
                gender = data['gender']
            except:
                gender = "No data available"
            l.append(gender)

            try:
                name = data['name'][0]['family']
            except:
                name = "No data available"
            l.append(name)

            try:
                address = data['address'][0]['city']
            except:
                address = "No data available"
            l.append(address)
            lst.append(l)
        param = {'param': lst,"id":pid}
        return render(request, 'app/home.html', param)
    #all patients
    elif request.method == 'GET':
        url = Resource+"/Patient?_count=20"
        newHeaders = {'Content-type': 'application/json', "Authorization": "Bearer %s" %TOKEN}
        response = requests.get(url, headers=newHeaders, verify=False)
        data = response.json()
        lst = []
        # next_pge_url = response.json()['link'][0].get('url')
        key_to_lookup = 'entry'
        if key_to_lookup in data:
            entry = data['entry']
            for all_data in entry:
                l = []
                resourceType = all_data['resource']['resourceType']
                l.append(resourceType)

                id = all_data['resource']['id']
                l.append(id)

                try:
                    birth = all_data['resource']['birthDate']
                except:
                    birth = "No data available"
                l.append(birth)

                try:
                    gender = all_data['resource']['gender']
                except:
                    gender = "No data available"
                l.append(gender)

                try:
                    name = all_data['resource']['name'][0]['family']
                except:
                    name = "No data available"
                l.append(name)

                try:
                    address = all_data['resource']['address'][0]['city']
                except:
                    address = "No data available"
                l.append(address)

                lst.append(l)
            param = {'param':lst}
            return render(request, 'app/home.html', param)
        else:
            param = {'param': "No Data Available..!!!"}
            return render(request, 'app/error.html', param)

def observation(request):
    lst = []
    id = pid
    if id is None:
        obsparam = {'obsparam': "No patient id found"}
        return render(request, 'app/home.html', obsparam)
    else:
        url = Resource+"/Observation?patient={}".format(id)
        newHeaders = {'Content-type': 'application/json', "Authorization": "Bearer %s" %TOKEN}
        response = requests.get(url, headers=newHeaders,verify=False)
        if response.ok:
            data = response.json()
            if 'entry' not in data.keys():
                print("NO Observation available")
            else:
                entry = data['entry']
                for all_data in entry:
                    l = []
                    resourceType = all_data['resource']['resourceType']
                    l.append(resourceType)

                    id = all_data['resource']['id']
                    global observation_id
                    observation_id = id
                    l.append(id)

                    try:
                        reference = all_data['resource']['subject'].get('reference')
                    except:
                        reference = "No data available"
                    l.append(reference)

                    try:
                        display = all_data['resource']['code']['coding'][0].get('display')
                    except:
                        display = "No data available"
                    l.append(display)

                    try:
                        res = list(map(itemgetter('coding'), all_data['resource']['category']))
                        category = res[0][0]['display']
                    except:
                        category = "No data available"
                    l.append(category)

                    try:
                        v1 = all_data['resource']['valueQuantity'].get('value')
                        v2 = all_data['resource']['valueQuantity'].get('unit')
                        value = str(v1) + " " + str(v2)
                    except:
                        value = "No data available"
                    l.append(value)
                    lst.append(l)
        obsparam = {'obsparam': lst,'observation_id':observation_id}
        return render(request, 'app/home.html', obsparam)

def encounter(request):
    lst = []
    if pid is None:
        obsparam = {'obsparam': "No patient id found"}
        return render(request, 'app/home.html', obsparam)
    else:
        url = Resource+"/Encounter?patient={}".format(pid)
        newHeaders = {'Content-type': 'application/json', "Authorization": "Bearer %s" % TOKEN}
        response = requests.get(url, headers=newHeaders,verify=False)
        if response.ok:
            data = response.json()
            if 'entry' not in data.keys():
                print("NO Encounter available")
            else:
                entry = data['entry']
                for all_data in entry:
                    l = []
                    try:
                        resourceType = all_data['resource']['resourceType']
                    except:
                        resourceType = "No data available"
                    l.append(resourceType)

                    try:
                        id = all_data['resource']['id']
                        global encounter_id
                        encounter_id=id
                    except:
                        id = "No data available"
                    l.append(id)

                    try:
                        priority = all_data['resource']['priority']['coding'][0]['display']
                    except:
                        priority = "No data available"
                    l.append(priority)

                    try:
                        reason = list(map(itemgetter('coding'), all_data['resource']['reasonCode']))
                        reasonCode = reason[0][0]['display']
                    except:
                        reasonCode = "No data available"
                    l.append(reasonCode)

                    try:
                        admitSource = all_data['resource']['hospitalization']['admitSource']['coding'][0]['display']
                    except:
                        admitSource = "No data available"
                    l.append(admitSource)

                    try:
                        serviceProvider = all_data['resource']['serviceProvider'].get('reference')
                    except:
                        serviceProvider = "No data available"
                    l.append(serviceProvider)

                    lst.append(l)
        encounter_param = {'encounter_param': lst,'encounter_id':encounter_id}
        return render(request, 'app/home.html', encounter_param)

def jsonviewPatient(request,id):
    id = str(id)
    url = Resource+"/Patient/{}".format(id)
    newHeaders = {'Content-type': 'application/json', "Authorization": "Bearer %s" % TOKEN}
    response = requests.get(url, headers=newHeaders,verify=False)
    if response.ok:
        json_data = response.json()
        # json_formatted_patient= json.dumps(json_data, sort_keys = True, indent = 4)
    # param = {'param':json_formatted_patient}
    return JsonResponse(json_data,content_type='application/json')

def jsonviewObservation(request,id):
    id = str(id)
    url = Resource+"/Observation/{}".format(id)
    newHeaders = {'Content-type': 'application/json', "Authorization": "Bearer %s" % TOKEN}
    response = requests.get(url, headers=newHeaders,verify=False)
    if response.ok:
        json_data = response.json()
    #     json_formated_observation=json.dumps(json_data, sort_keys = True, indent = 4)
    # param = {'param':json_formated_observation}
    # return render(request,'app/jsondata.html',param)
    return JsonResponse(json_data,content_type='application/json')

def jsonviewEncounter(request,id):
    id = str(id)
    url = Resource+"/Encounter/{}".format(id)
    newHeaders = {'Content-type': 'application/json', "Authorization": "Bearer %s" % TOKEN}
    response = requests.get(url, headers=newHeaders,verify=False)
    if response.ok:
        json_data = response.json()
    #     json_formated_encounter=json.dumps(json_data, sort_keys = True, indent = 4)
    # param = {'param':json_formated_encounter}
    # return render(request,'app/jsondata.html',param)
    return JsonResponse(json_data,content_type='application/json')

def url(request):
    if request.method == "POST":
        json_data=''
        url = request.POST.get('URL', '')
        newHeaders = {'Content-type': 'application/json',"Authorization": "Bearer %s" %TOKEN}
        response = requests.get(Resource+"/"+url, headers=newHeaders,verify=False)
        if response.ok:
            json_data = response.json()
    return JsonResponse(json_data,content_type='application/json',safe=False)

def error_404_view(request,exception):
    return render(request,'app/404.html')
