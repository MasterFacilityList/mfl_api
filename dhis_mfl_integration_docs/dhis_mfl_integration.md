# DHIS2 - KMHFL Integration v0.1 <img style="width: 80px; margin-top: -20px; margin-bottom: -10px" src="assets/dhis-mfl.png" width="80"/>

## Contents
- [DHIS2 - KMHFL Integration v0.1](#dhis2---kmhfl-integration-v01)
  * [DHIS2](#dhis2)
  * [MFL API](#mfl-api)
    + [Disclaimer!](#disclaimer-)
    + [I. Lets get the source code](#i-lets-get-the-source-code)
      - [NB* _The source code is already updated with the integration modules. We'll be going through the sections of the original code that was edited to effect the integration_.](#nb---the-source-code-is-already-updated-with-the-integration-modules-we-ll-be-going-through-the-sections-of-the-original-code-that-was-edited-to-effect-the-integration-)
    + [II. Setting up the database](#ii-setting-up-the-database)
    + [III. What has changed in the source code?](#iii-what-has-changed-in-the-source-code-)
      - [a. Some bit of introduction and ground breaking](#a-some-bit-of-introduction-and-ground-breaking)
      - [b. New facility push](#b-new-facility-push)
      - [c. Organisation group assignment to new facility](#c-organisation-group-assignment-to-new-facility)
      - [d. Facility update push](#d-facility-update-push)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

## DHIS2
- Not much needs to be done on this side. All you need to know is how to use the [dhis2 Web API v2.26](https://docs.dhis2.org/2.26/en/developer/html/dhis2_developer_manual_full.html#webapi "dhis2 Web API"). This will enable you to understand and maybe improve on the code that we shall see later im the MFL API section.
- You might also need **super user** credentials to __*dhis2*__ so that you can update the ones we have, if need be.
- Lastly, :smile:, If you decide to use the [dhis2 OAuth2 protocol](https://docs.dhis2.org/2.26/en/developer/html/dhis2_developer_manual_full.html#webapi_oauth2 "dhis2 OAuth2 Authentication Protocol") make sure you have created an **OAuth2 Client** in __*dhis2*__ and take note of the **Client ID** and **Client Secret**, you know, for the various *grant_types* to obtain your *OAuth2 Tokens*.

## MFL API
>### Disclaimer!
>- This doc/tutorial assumes that one has the knowledge to **correctly setup** and **run** the **MFL API**. Reference to [MFL API Docs](http://mfl-api-docs.readthedocs.io/en/latest/02_developer_install.html "MFL API Developer Installation") is advised, if need be.
- We might have a bit of work to do here :sweat_smile:. But no worries, we'll go step by step. I got your back :thumbsup:.

### I. Lets get the source code
- You should be in a python virtual environment through this whole tutorial. You can set it up real quick. Check out [virtualenv](https://virtualenv.pypa.io/en/stable/installation/ "Virtualenv Installation"). I also advise using python's [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/ "Virtualenvwrapper Installation") together with the virtual environment. It will save you a great deal.
- Hopefully, our git repository is still active; go to uonafya [mfl_api](https://github.com/uonafya/mfl_api "uonafya MFL API Git Repository") git repository and either download a zipped version of the repository or clone it over in the terminal via `:bash-$ git clone https://github.com/uonafya/mfl_api.git`.
- I believe everything went on as expected. You should now be having a folder called `mfl_api`, that's if you didn't provide an output folder name for `git clone`. Don't worry if the cloning takes a long time. The repository is around `167MB`.
- Next, check the branch that you are currently on. You can do this by `:bash-$ git branch`. You'll get an output such as:
```bash
bash-$ git branch
       develop
       mapping_models
     * master
       workforce17
```
Taking note of the `*`, we know that we are currently at branch `master`. We need to switch to `mapping-models`. To do so, run: `:bash-$ git checkout mapping-models`. You can `:bash-$ git branch` again just to confirm that the switching was successful. As a precautionary measure, kindly run: `:bash-$ git pull`. This makes sure you have all necessary resources in that branch.
- Now, we have the source code all set up.
#### NB* _The source code is already updated with the integration modules. We'll be going through the sections of the original code that was edited to effect the integration_.
- Ok, since we have that clarified, we can continue to the database setup.

### II. Setting up the database
- Assuming you are familiar with Django and the MVC framework's migrations, you might notice that the migrations are included in the repository. This is not a good practice but when we got the source code, they were being included in the repository. We'll correct the issue soon.
- Next, you should be having a `.bak` or `.sql` backup of the mfl database. It's name should have a `integration_v0.1` somewhere within it's name. This has the general structure of the schema together with setup data and possibly some data already pre-loaded. Hopefully you successfully imported this and is now in a database called `mfl`.
- Now, `cd` into the project folder. make sure your virtual environment is active and that you have all the packages necessary. To verify this, once in the project folder, do 
```bash
:bash-$(mfl_api_venv) pip install -r requirements.txt
```
- Ok. Then as a precaution, run
```bash
:bash-$(mfl_api_venv) python manage.py makemigrations --fake
```
then 
```bash
:bash-$(mfl_api_venv) python manage.py migrate --fake
```
These are just to make sure that all the required tables are created and that your project is in sync with the database. Its really important.
- For the mapping part, kindly refer to the [dhis2-kmhfl Integration Mapping](http://git.com "DHIS2 - KMHFL Integration Mapping").
- With that, our back-end is all set. Finally. Let's jump straight into the code! :smile:

### III. What has changed in the source code?
- There are tonnes of things that have been added. I will briefly take you through them. Just to give you an overview of what has been done.
- Let's get right to it.
- Oh. Before we dive deeper, here is the project structure:
```bash
mfl_api/
.
├── ...
├── common
│   ├── ...
│   ├── models
│   │   ├── base.py
│   │   ├── base.pyc
│   │   ├── __init__.py
│   │   ├── __init__.pyc
│   │   ├── model_declarations.py
│   │   └── model_declarations.pyc
│   └── ...
├── ...
├── facilities
│   ├── ...
│   ├── models
│   │   ├── facility_models.py
│   │   ├── facility_models.pyc
│   │   ├── __init__.py
│   │   └── __init__.pyc
│   └── ...
├── mapping_scripts
│   ├── assign_dhis_groups.py
│   ├── conn.py
│   ├── conn.pyc
│   ├── copy_admin_units.py
│   ├── copy_proposed_org_unit_groups.py
│   ├── get_org_unit_id.py
│   ├── get_proposed_org_unit_groups_id.py
│   ├── ignored_2.json
│   ├── ignored.json
│   ├── __init__.py
│   ├── issues.txt
│   ├── logs.txt
│   ├── mfl.xlsx
│   ├── removing_space.py
│   ├── r.txt
│   └── test_comparison.py
└── ...

156 directories, 1136 files
# Reducted due to the size of the dir tree. Focuses on the important files and directories
```
#### a. Some bit of introduction and ground breaking
- Most of the core integration logic is located in a `class` called `DhisAuth(ApiAuthentication)` in `$PROJECT_DIR(mfl_api)/facilities/facility_models.py`
- It's implementation is outlined below. Take note of its member functions since I will be referring to them as we explore other classes and functions.

**Main integration class**

```python
#! $DIR/facility_models.py
# Line ~1279
...
@encoding.python_2_unicode_compatible
class DhisAuth(ApiAuthentication):

    '''
    Authenticates to DHIS via OAuth2.
    Handles All API related functions
    '''

    # Additional model fields
    oauth2_token_variable_name = models.CharField(max_length=255, 
                                 default="api_oauth2_token", 
                                 null=False, 
                                 blank=False)
    type = models.CharField(max_length=255, default="DHIS2")
    session_store = SessionStore(session_key="dhis2_api_12904rs")

    # @set_interval annotation definition. Enables creation of jobs using functions
    def set_interval(interval, times=-1):
        # This will be the actual decorator,
        # with fixed interval and times parameter
        def outer_wrap(function):
            # This will be the function to be
            # called
            def wrap(*args, **kwargs):
                stop = threading.Event()

                # This is another function to be executed
                # in a different thread to simulate setInterval
                def inner_wrap():
                    i = 0
                    while i != times and not stop.isSet():
                        stop.wait(interval)
                        function(*args, **kwargs)
                        i += 1

                t = threading.Timer(0, inner_wrap)
                t.daemon = True
                t.start()
                return stop

            return wrap

        return outer_wrap

    @set_interval(300.0)
    def refresh_oauth2_token(self):
        r = requests.post(
            self.server+"uaa/oauth/token",
            headers={
                "Authorization": "Basic " + base64.b64encode(self.client_id + ":" + self.client_secret),
                "Accept": "application/json"
            },
            params={
                "grant_type": "refresh_token",
                "refresh_token": json.loads(self.session_store[self.oauth2_token_variable_name].replace("u", "")
                    .replace("'", '"'))["refresh_token"]
            }
        )

        response = str(r.json())
        # print("Response @ refresh_oauth2 ", response)
        self.session_store[self.oauth2_token_variable_name] = response
        self.session_store.save()

    def get_oauth2_token(self):
        r = requests.post(
            self.server+"uaa/oauth/token",
            headers={
                "Authorization": "Basic "+base64.b64encode(self.client_id+":"+self.client_secret),
                "Accept": "application/json"
            },
            params={
                "grant_type": "password",
                "username": self.username,
                "password": self.password
            }
        )

        response = str(r.json())
        # print("Response @ get_oauth2 ", response, r.url, r.status_code)
        self.session_store[self.oauth2_token_variable_name] = response
        self.session_store.save()
        self.refresh_oauth2_token()

    def get_org_unit_id(self, code):
        r = requests.get(
            self.server + "api/organisationUnits.json",
            headers={
                "Authorization": "Bearer " +
                                 json.loads(self.session_store[self.oauth2_token_variable_name].replace("u", "")
                                            .replace("'", '"'))["access_token"],
                "Authorization": "Basic " + base64.b64encode(self.username + ":" + self.password),
                "Accept": "application/json"
            },
            params={
                "filter": "code:eq:"+str(code),
                "fields": "[id]",
                "paging": "false"
            }
        )
        print("Get Org Unit ID Response", r.json(), str(code))
        if len(r.json()["organisationUnits"]) is 1:
            return r.json()["organisationUnits"][0]["id"]
        else:
            raise ValidationError(
                {
                    "Error!": ["Unable to resolve exact organisation unit of the facility to be updated in DHIS2. "
                               "Most probably, the corresponding MFL code for the facility does not exist in DHIS2"]
                }
            )

    def get_org_unit(self, org_unit_id):
        r = requests.get(
            self.server + "api/organisationUnits/"+org_unit_id,
            headers={
                # "Authorization": "Bearer " +
                #                  json.loads(self.session_store[self.oauth2_token_variable_name].replace("u", "")
                #                             .replace("'", '"'))["access_token"],
                "Authorization": "Basic "+base64.b64encode(self.username+":"+self.password),
                "Accept": "application/json"
            }
        )
        print("Get Org Unit Response", r.url, r.status_code)
        if str(r.status_code) == "200":
            return r.json()
        else:
            raise ValidationError(
                {
                    "Error!": ["Unable to get corresponding facility in DHIS2"]
                }
            )

    def get_parent_id(self, facility_name):
        r = requests.get(
            self.server+"api/organisationUnits.json",
            headers={
                # "Authorization": "Bearer " + json.loads(self.session_store[self.oauth2_token_variable_name].replace("u", "")
                #     .replace("'", '"'))["access_token"],
                "Authorization": "Basic " + base64.b64encode(self.username + ":" + self.password),
                "Accept": "application/json"
            },
            params={
                "query": facility_name,
                "fields": "[id,name]",
                "filter": "level:in:[4]",
                "paging": "false"
            }
        )
        print(r.status_code, r.url)
        dhis2_facility_name = r.json()["organisationUnits"][0]["name"].lower()
        facility_name = str(facility_name)+ " Ward"
        facility_name = facility_name.lower()
        print("1", dhis2_facility_name, "2", facility_name, len(r.json()["organisationUnits"]))

        if len(r.json()["organisationUnits"]) is 1:
            if dhis2_facility_name == facility_name:
                return r.json()["organisationUnits"][0]["id"]
        else:
            raise ValidationError(
                {
                    "Error!": ["Unable to resolve exact parent of the new facility in DHIS2"]
                }
            )

    def push_facility_to_dhis2(self, new_facility_payload):
        r = requests.post(
            self.server+"api/organisationUnits",
            headers={
                # "Authorization": "Bearer " + json.loads(self.session_store[self.oauth2_token_variable_name].replace("u", "")
                #                                         .replace("'", '"'))["access_token"],
                "Authorization": "Basic " + base64.b64encode(self.username + ":" + self.password),
                "Accept": "application/json"
            },
            json=new_facility_payload
        )

        print("Create Facility Response", r.url, r.status_code, r.json())

        if r.json()["status"] != "OK":
            raise ValidationError(
                {
                    "Error!": ["An error occurred while pushing facility to DHIS2. This is may be caused by the "
                               "existence of an organisation unit with as similar name as to the one you are creating. "
                               "Or some specific information like geo-coordinates are not unique"]
                }
            )

    def push_facility_updates_to_dhis2(self, org_unit_id, facility_updates_payload):
        r = requests.put(
            self.server + "api/organisationUnits/"+org_unit_id,
            headers={
                # "Authorization": "Bearer " +
                #                  json.loads(self.session_store[self.oauth2_token_variable_name].replace("u", "")
                #                             .replace("'", '"'))["access_token"],
                "Authorization": "Basic " + base64.b64encode(self.username + ":" + self.password),
                "Accept": "application/json"
            },
            json=facility_updates_payload
        )

        print("Update Facility Response", r.url, r.status_code, r.json(), "Status", r.json()["status"])

        if r.json()["status"] != "OK":
            raise ValidationError(
                {
                    "Error!": ["Unable to push facility updates to DHIS2"]
                }
            )

    def add_org_unit_to_group(self, org_unit_group_id, org_unit_id):

        r_get_group = requests.get(
            self.server+"api/organisationUnitGroups/"+org_unit_group_id,
            headers={
                "Authorization": "Basic " + base64.b64encode(self.username + ":" + self.password),
                "Accept": "application/json"
            },
            params={
                "fields": "[*]"
            }
        )

        organisation_group = r_get_group.json()
        print(organisation_group)
        organisation_group["organisationUnits"].append({"id":org_unit_id})

        r = requests.put(
            self.server+"api/organisationUnitGroups/"+org_unit_group_id,
            headers={
                "Authorization": "Basic " + base64.b64encode(self.username + ":" + self.password),
                "Accept": "application/json"
            },
            json=organisation_group
        )

        if str(r.status_code) != "200":
            raise ValidationError(
                {
                    "Error!": ["Failed to assign organisation group to the facility being processed"]
                }
            )
        else:
            print ("Successfully Assigned Group")

    def format_coordinates(self, str_coordinates):
        coordinates_str_list = str_coordinates.split(" ")
        return str([float(coordinates_str_list[0]), float(coordinates_str_list[1])])

    def __str__(self):
        return "{}: {}".format("Dhis Auth - ", self.username)

...
```

- I know. A lot to take in. But I had to put it there. Just as a reference guide so that whenever I say `def add_org_unit_to_group(self)` (meaning, function add_org_unit_to_group(self) in DhisAuth class), we are on the same page.

**Authentication**

- As mentioned earlier, the integration relies heavily on the DHIS2 Web API. So, for authentication, we created a table. `common_apiauthentication`.
- `common_apiauthentication` Table.
```sql
mfl=# \d common_apiauthentication
                                    Table "public.common_apiauthentication"
    Column     |          Type          |                               Modifiers                               
---------------+------------------------+-----------------------------------------------------------------------
 id            | integer                | not null default nextval('common_apiauthentication_id_seq'::regclass)
 username      | character varying(255) | not null
 password      | character varying(255) | not null
 client_id     | character varying(255) | not null
 client_secret | character varying(255) | not null
 server        | character varying(255) | not null
 session_key   | character varying(255) | not null
Indexes:
    "common_apiauthentication_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "facilities_dhisauth" CONSTRAINT "D45ec29ca05d27761a7ce71acd14107e" FOREIGN KEY (apiauthentication_ptr_id) REFERENCES common_apiauthentication(id) DEFERRABLE INITIALLY DEFERRED
```
- This table contains the necessary credentials and details to make both `Basic` and `OAuth2` authentication using the DHIS2 Web API. We have both implementations but currently using basic auth. The OAuth2 is included. But commented out.

- You can find this in `$PROJECT_DIR(mfl_api)/facilities/facility_models.py`
```python
#! $DIR/facility_models.py
...
# Line ~1359
r = requests.get(
            self.server + "api/organisationUnits.json",
            headers={
                "Authorization": "Bearer " + json.loads(
                  self.session_store[self.oauth2_token_variable_name].replace("u", "")
                  .replace("'", '"'))["access_token"],

                # OR
                
                "Authorization": "Basic " + base64.b64encode(self.username + ":" + self.password),
                "Accept": "application/json"
            },
            params={
                "filter": "code:eq:"+str(code),
                "fields": "[id]",
                "paging": "false"
            }
        )
...
```

**OAuth 2 Token Refresh**
- When using OAuth 2, there is an aspect of the `token expiry` where an access you were given by the API has a certain period to live. To deal with this, we have put in place a function that refreshes this token and automatically updates the `access token` field in the database with the newly received token.
- You can find this in `$PROJECT_DIR(mfl_api)/facilities/facility_models.py`
```python
#! $DIR/facility_models.py
# Lne ~1319

@set_interval(30.0)
def Dhis2Auth.refresh_oauth2_token(self)
```

#### b. New facility push
- I know. What's a new facility push. Well, once a new facility is added into MFL, it is usually given a status `Pending Approval`. Now, once this facility is approved, the integration we've made enables MFL to create this new facility in DHIS2 automatically, as a new Organisation Unit.
- To achieve this, we use the function:
```python
#! $DIR/facility_models.py
# Line ~1438
...
def push_facility_to_dhis2(self, new_facility_payload):
    ...
...
```
- As outlined, the function expects a json payload containing the new facility's details. A sample is as shown below:
##### New facility push json payload
```json
{  
   code:"14180",
   name:"10 Engineer VCT",
   shortName:"10 Engineer VCT",
   displayName:"10 Engineer VCT",
   displayShortName:"10 Engineer VCT",
   openingDate:"1970-01-01T00:00:00.000",
   coordinates:"[37.094,-0.00133]",
   parent:{  
      id:"DpYpJ6E1vRc"
   },
   access:{  
      read:true,
      update:true,
      externalize:true,
      delete:true,
      write:true,
      manage:true
   },
   children:[],
   translations:[],
   ancestors:[  
      {  
         id:"HfVjCurKxh2"
      },
      ...
   ],
   organisationUnitGroups:[  
      {  
         id:"ZwPu4GoLJtA"
      },
      ...
   ],
   userGroupAccesses:[],
   attributeValues:[],
   users:[],
   userAccesses:[],
   dataSets:[  
      {  
         id:"obUj8fCPghC"
      },
      ...
   ],
   legendSets:[],
   programs:[  
      {  
         id:"j6EGTLAIMQ3"
      },
      ...
   ]
}
```

#### c. Organisation group assignment to new facility
- Once the new facility has been pushed (created) to *dhis2*, we need to add it to its respective organisation unit group(s). Refer to the [Mapping Docs](http://not-a-real-link/repo.git "Mapping Documentation") for the how various organisation unit groups from *dhis2* have been mapped and referenced in *MFL*.
- To do this, 
    * we have to know which organisation unit groups the new facility belongs. This can easily be done through `querying the local MFL database`.
    * next, using the mapping tables, `retrieve` the mapped organisation unit groups `dhis2 uids`. Then, make the function call below. This will return the **uid** of the just pushed facility:
    ##### get facility uid
    ```python
    #! $DIR/facility_models.py
    # Line ~1358
    ...
    def get_org_unit_id(self, code):
    ...
    ```
    This function expects the mfl_code of the facility in subject.
    <br />
    <br />
    * once the uids are obtained, you need to make the following function call, providing the **Organisation unit group uid** and **Organisation unit (Facility) uid** respectively.

    ```python
    #! $DIR/facility_models.py
    # Line ~1483
    ...
    def add_org_unit_to_group(self, org_unit_group_id, org_unit_id):
    ...
    ```

#### d. Facility update push
- Yes, once the updates made to a facility are approved, the changes are replicated on *dhis2* automatically.
- To effect this, make the function calls below. The second one `def push_facility_updates_to_dhis2()` takes the uid organisation unit to be updated together with the facility update payload. In json. Recall the [payload for new facility push](#new-facility-push-json-payload)? well, this one is identical to it. The the [organisation unit uid](#get-facility-uid) can be gotten using the first function call below. We've covered this before too.

```python
#! $DIR/facility_models.py
# Line ~1358
...
def get_org_unit_id(self, code):
    ...
...

#! $DIR/facility_models.py
# Line ~1461
...
def push_facility_updates_to_dhis2(self, org_unit_id, facility_updates_payload):
    ...
...
```

<small><i>Integration walk-through by <a href='http://derekprince.bitbucket.io/'>Workforce 17</a>, <a href='https://healthit.uonbi.ac.ke/'>Health IT</a> <a href='http://uonbi.ac.ke/'>(University of Nairobi)</a></i></small>

<a href='http://uonbi.ac.ke/' target='_blank'><img style="width: 80px; margin-top: -20px; margin-bottom: -10px" src="assets/UoN-Logo.png" width="80" /></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href='https://healthit.uonbi.ac.ke/' target='_blank'><img style="width: 100px; margin-top: -15px; margin-bottom: -15px" src="assets/uonafya.png" width="100"/></a>
