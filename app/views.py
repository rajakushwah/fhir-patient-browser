from django.shortcuts import render , get_object_or_404
from operator import itemgetter
import requests
import json
import adal

# oauth 2.0 --FHIR SERVER AUTHORIZATION
# TOKEN=''
# def auth():
#     TENANT_ID = '4ac32c75-8316-44c4-925a-c3bec0b6f4ef'
#     CLIENT = '41bc3a0a-2574-406a-833b-eec8f0fc0458'
#     KEY = '~~l_CEnOv0h2a574ud8f-dh2~sr0Qdn_m~'
#     authority_url = 'https://login.microsoftonline.com/' + TENANT_ID
#     context = adal.AuthenticationContext(authority_url)
#     global token
#     token = context.acquire_token_with_client_credentials(
#         resource='https://demoonfhir.azurehealthcareapis.com',
#         client_id=CLIENT,
#         client_secret=KEY)
#     TOKEN=token["accessToken"]
#     return TOKEN


#Function to extract patient data based on id,all patients
pid=""
TOKEN=""
def home(request):
    TENANT_ID = '4ac32c75-8316-44c4-925a-c3bec0b6f4ef'
    CLIENT = '41bc3a0a-2574-406a-833b-eec8f0fc0458'
    KEY = '~~l_CEnOv0h2a574ud8f-dh2~sr0Qdn_m~'
    authority_url = 'https://login.microsoftonline.com/' + TENANT_ID
    context = adal.AuthenticationContext(authority_url)
    global token
    token = context.acquire_token_with_client_credentials(
        resource='https://demoonfhir.azurehealthcareapis.com',
        client_id=CLIENT,
        client_secret=KEY)
    global TOKEN
    TOKEN = token["accessToken"]

    # all patients
    if request.method == "POST":
        lst = []
        global pid
        pid = request.POST.get('ID', '')
        url = "https://demoonfhir.azurehealthcareapis.com/Patient/{}".format(pid)
        newHeaders = {'Content-type': 'application/json',"Authorization": "Bearer %s" %TOKEN}
        response = requests.get(url, headers=newHeaders,verify=False)
        data = response.json()
        if response.ok:
            l = []
            resourceType = data['resourceType']
            id = data['id']

            try:
                birth = data['birthDate']
            except:
                birth = "No data available"

            try:
                gender = data['gender']
            except:
                gender = "No data available"

            try:
                name = data['name'][0]['family']
            except:
                name = "No data available"

            try:
                address = data['address'][0]['city']
            except:
                address = "No data available"

            json = data

            l.append(resourceType)
            l.append(id)
            l.append(birth)
            l.append(gender)
            l.append(name)
            l.append(address)
            lst.append(l)
        param = {'param': lst,"id":pid}
        return render(request, 'app/home.html', param)

    elif request.method == 'GET':
        url = "https://demoonfhir.azurehealthcareapis.com/Patient"
        newHeaders = {'Content-type': 'application/json', "Authorization": "Bearer %s" %TOKEN}
        response = requests.get(url, headers=newHeaders, verify=False)
        lst = []
        # next_pge_url = response.json()['link'][0].get('url')
        if response.ok:
            data = response.json()
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
        # param = {'param':lst,'pager':next_pge_url}
        param = {'param': lst}
        return render(request, 'app/home.html', param)

def observation(request):
    lst = []
    id = pid
    if id is None:
        obsparam = {'obsparam': "No patient id found"}
        return render(request, 'app/home.html', obsparam)
    else:
        url = "https://demoonfhir.azurehealthcareapis.com/Observation?patient={}".format(id)
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
                    # effectiveDateTime = all_data['resource']['effectiveDateTime']
                    # l.append(effectiveDateTime)
                    # print(resourceType, id, reference, display, value, category, effectiveDateTime)

                    lst.append(l)
        obsparam = {'obsparam': lst}
        return render(request, 'app/home.html', obsparam)

def encounter(request):
    lst = []
    if pid is None:
        obsparam = {'obsparam': "No patient id found"}
        return render(request, 'app/home.html', obsparam)
    else:
        url = "https://demoonfhir.azurehealthcareapis.com/Encounter?patient={}".format(pid)
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
        encounter_param = {'encounter_param': lst}
        return render(request, 'app/home.html', encounter_param)

# def url(request):
#     if request.method == "POST":
#         input = request.POST.get('URL', '')
#         url = ""
#         newHeaders = {'Content-type': 'application/json',"Authorization": "Bearer %s" %TOKEN}
#         response = requests.get(url, headers=newHeaders,verify=False)
#         data = response.json()
#         json_formated_url = json.dumps(data, sort_keys=True, indent=4)
#         param = {'param': json_formated_url,"url":input}
#         return render(request, 'app/jsondata.html', param)

def jsonviewPatient(request,id):
    id = str(id)
    url = "https://demoonfhir.azurehealthcareapis.com/Patient/{}".format(id)
    newHeaders = {'Content-type': 'application/json', "Authorization": "Bearer %s" % TOKEN}
    response = requests.get(url, headers=newHeaders,verify=False)
    if response.ok:
        json_data = response.json()
        json_formatted_patient= json.dumps(json_data, indent=2 ,sort_keys=True)
    param = {'param':json_formatted_patient}
    return render(request,'app/jsondata.html',param)

def jsonviewObservation(request):
    id = str(pid)
    url = "https://demoonfhir.azurehealthcareapis.com/Observation?patient={}".format(id)
    newHeaders = {'Content-type': 'application/json', "Authorization": "Bearer %s" % TOKEN}
    response = requests.get(url, headers=newHeaders,verify=False)
    if response.ok:
        json_data = response.json()
        json_formated_observation=json.dumps(json_data, sort_keys=True, indent=2)
    param = {'param':json_formated_observation}
    return render(request,'app/jsondata.html',param)

def jsonviewEncounter(request):
    id = str(pid)
    url = "https://demoonfhir.azurehealthcareapis.com/Encounter?patient={}".format(id)
    newHeaders = {'Content-type': 'application/json', "Authorization": "Bearer %s" % TOKEN}
    response = requests.get(url, headers=newHeaders,verify=False)
    if response.ok:
        json_data = response.json()
        json_formated_encounter=json.dumps(json_data, sort_keys=True, indent=4)
    param = {'param':json_formated_encounter}
    return render(request,'app/jsondata.html',param)

# def nextPage(request,id):
#     id = str(id)
#     url = "https://demoonfhir.azurehealthcareapis.com/Patient={}".format(id)
#     newHeaders = {'Content-type': 'application/json', "Authorization": "Bearer %s" % TOKEN}
#     response = requests.get(url, headers=newHeaders,verify=False)
#     next_pge_url = response.json()['link'][1].get('url')
#     new_url=next_pge_url
#     header = {'Content-type': 'application/json', "Authorization": "Bearer %s" % TOKEN}
#     nextPageResponse = requests.get(new_url, headers=header)
#     lst = []
#     if nextPageResponse.ok:
#         data = nextPageResponse.json()
#         entry = data['entry']
#         for all_data in entry:
#             l = []
#             resourceType = all_data['resource']['resourceType']
#             l.append(resourceType)
#
#             id = all_data['resource']['id']
#             l.append(id)
#
#             try:
#                 birth = all_data['resource']['birthDate']
#             except:
#                 birth = "No data available"
#             l.append(birth)
#
#             try:
#                 gender = all_data['resource']['gender']
#             except:
#                 gender = "No data available"
#             l.append(gender)
#
#             try:
#                 name = all_data['resource']['name'][0]['family']
#             except:
#                 name = "No data available"
#             l.append(name)
#
#             try:
#                 address = all_data['resource']['address'][0]['city']
#             except:
#                 address = "No data available"
#             l.append(address)
#
#             lst.append(l)
#     param = {'param': lst}
#     return render(request, 'app/home.html', param)

def error_404_view(request,exception):
    return render(request,'app/404.html')