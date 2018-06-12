import requests
import base64

url = "http://localhost:8080/api/organisationUnits/"
cred = base64.b64encode("admin:district")


def weka(payload):
    r = requests.put(
        url+payload["id"],
        headers={
            "Authorization": "Basic " + cred,
            "Accept": "application/json"
        },
        json=payload["data"]
    )
    print(r)


def sahihisha(jina):
    return str(jina).strip().replace("  ", " ").title()


r = requests.get(
        url,
        headers={
            "Authorization": "Basic "+cred,
            "Accept": "application/json"
        },
        params={
            "paging": "false",
            "level" : 4,
            "fields" : '[*]'
        }
    )


orgunits = r.json()['organisationUnits']

total = len(orgunits)
percentage_complete = 0
counter = 0
corrected = 0

for orgunit in orgunits:
    counter += 1
    percentage_complete = (float(counter) / float(total)) * 100.0

    print ("\033[0mProcessing " + orgunit['name'] + " ({}% Completed)...\n".format(str(percentage_complete)))

    original_name = orgunit["name"]
    orgunit["name"] = sahihisha(orgunit["name"])

    payload = {
        "id": orgunit["id"],
        "data": orgunit
    }

    if sahihisha(orgunit["name"]) != original_name:
        weka(payload)
        corrected += 1
        print ("\033[92mFinished Processing " + orgunit['name'] + "...\n")
    else:
        print ("\033[91mSkipped Processing " + orgunit['name'] + "...\n")


print ("\033[92mNimemaliza! Tumeweka - "+ str(corrected) +"\033[0m")
