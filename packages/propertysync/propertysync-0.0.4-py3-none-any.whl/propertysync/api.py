import requests, os

"""
This is a helper for interacting with the PropertySync API
"""

# TODO: Follow styleguide: https://google.github.io/styleguide/pyguide.html#316-naming

class ApiClient:
    def __init__(self, email=None, password=None, document_group_id=None, company_id=None):
        self.search_url = "https://api.propertysync.com/v1/search"
        self.login_url = "https://api.propertysync.com/v1/login"
        self.indexing_url = "https://api.propertysync.com/v1/indexing"
        self.trailing_slash = "" #this should get set if we change the URLs above
        self.user_agent = "PropertySync API Python Client"
        self.email = email
        self.password = password
        self.token = None
        self.company_id = company_id
        self.document_group_id = document_group_id
        self.document_group_info = None

        self.login()

    def get_document_group_name(self):
        if self.document_group_info is None:
            self.document_group_info = self.get_info()
        return self.document_group_info["name"]
    
    def get_document_group_county(self):
        if self.document_group_info is None:
            self.document_group_info = self.get_info()
        return self.document_group_info["county"]
    
    def get_document_group_state(self):
        if self.document_group_info is None:
            self.document_group_info = self.get_info()
        return self.document_group_info["state"]

    def get_plant_effective_date(self):
        if self.document_group_info is None:
            self.document_group_info = self.get_info()
        return self.document_group_info["plantEffectiveDate"]
    
    def set_document_group_id(self, document_group_id):
        # reset the document group info
        self.document_group_info = None
        self.document_group_id = document_group_id
    
    def set_company_id(self, company_id):
        self.company_id = company_id

    def get_token(self):
        return self.token
    
    def get_company_id(self):
        return self.company_id  
    
    def get_document_group_id(self):
        return self.document_group_id

    # login function
    def login(self):
        # if email is not set, check for environment variables
        if self.email is None:
            if os.environ.get("PROPERTYSYNC_API_EMAIL") is None:
                raise Exception("Email is not set")
            else:
                self.email = os.environ.get("PROPERTYSYNC_API_EMAIL")

        # if password is not set, check for environment variables
        if self.password is None:
            if os.environ.get("PROPERTYSYNC_API_PASSWORD") is None:
                raise Exception("Password is not set")
            else:
                self.password = os.environ.get("PROPERTYSYNC_API_PASSWORD")

        credentials = {"email":self.email,"password":self.password}
        
        headers = {
            "User-Agent": self.user_agent,
            "Content-Type": "application/json"
            }
        # if the token is already set, return
        if os.environ.get("PROPERTYSYNC_API_TOKEN") is not None:
            self.token = os.environ.get("PROPERTYSYNC_API_TOKEN")
            return
        
        login_request = requests.post(self.login_url,json=credentials, headers=headers)

        if login_request.status_code != 200:
            raise Exception("Login failed: "+login_request.text)

        self.token = login_request.json()["token"]
        os.environ["PROPERTYSYNC_API_TOKEN"] = self.token

    # make a call to the API
    def api_call(self, method, url, params=None, body=None, tries=1):
        # create a header with the token
        headers = {
            "User-Agent": self.user_agent,
            "Authorization": "Bearer "+self.token, 
            "Content-Type": "application/json"
        }

        if (method == "GET"):
            request = requests.get(url,params=params,headers=headers, json=body)
        elif (method == "POST"):
            request = requests.post(url,params=params,headers=headers, json=body)
        elif (method == "DELETE"):
            request = requests.delete(url,params=params,headers=headers, json=body)    
        elif (method == "PATCH"):
            request = requests.patch(url,params=params,headers=headers, json=body)             
        else:
            raise Exception("Invalid method: "+method)

        # determine if the request was successful
        if request.status_code == 200:
            return request.json()
        elif request.status_code == 401:
            # if the token is invalid, try to login again, if we receive a failure again, raise an exception
            if (tries < 2):
                tries += 1
                self.login()
                return self.api_call(method=method, url=url, params=params, tries=tries)
            else:
                raise Exception("Unauthorized   : "+request.text)
        elif request.status_code == 403:
            raise Exception("Forbidden: You do not have access to this resource")
        elif request.status_code == 500:
            raise Exception("Server Error: "+request.text)
        else:
            raise Exception("Unknown Error: "+request.text)

    # get info about the document group
    def get_info(self):
        if self.document_group_info is not None:
            return self.document_group_info
        
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}"
        return self.api_call("GET", url, None)
    
    # get a list of batches
    def get_batches(self):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/batches"
        return self.api_call("GET", url, None)

    # create a batch
    def create_batch(self, batch_name, search_id=None):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/batches"
        params = {"name":batch_name}
        if search_id is not None:
            params["searchId"] = search_id
        return self.api_call("POST", url, params)
    
    # create batch from json
    def create_batch_from_json(self, json):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/batches"
        return self.api_call("POST", url, body=json)
    
    # update batch from json
    def update_batch_from_json(self, json, batch_id):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/batches/{batch_id}"
        return self.api_call("PATCH", url, body=json)
    
    # create batch from file at URL
    def create_batch_from_url(self, url):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/batches"
        body = {
            "name":"Python CLI Batch", 
            "fileUrl":url
            }
        return self.api_call("POST", url, body=body)

    # delete a batch
    def delete_batch(self, batch_id):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/batches/{batch_id}"
        return self.api_call("DELETE", url)
    
    # get batch info
    def get_batch_info(self, batch_id):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/batches/{batch_id}"
        return self.api_call("GET", url)
    
    # get batch documents
    def get_batch(self, batch_id, filter=None):
        # filter can be "complete" or "incomplete" to filter by status
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/batches/{batch_id}"
        params = {
            "include-documents":1
        }
        if filter is not None:
            params["filter[completedFilter]"] = filter
        return self.api_call("GET", url, params=params)
    
    # save batch to search
    def save_batch_to_search(self, batch_id):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/queue-process-documents"
        params = {
            "exportTo":"propertySync",
            "batchId":batch_id
        }
        return self.api_call("GET", url, params=params)
    
    # get autocompletes
    def get_autocompletes(self, type=None, search=None):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/auto-completes"
        params = {}

        if type is not None:
            params["type"] = type
        if search is not None:
            params["search"] = search

        return self.api_call("GET", url, params=params)
    
    # delete an autocomplete
    def delete_autocomplete(self, autocomplete_id):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/auto-completes/{autocomplete_id}"
        return self.api_call("DELETE", url)
    
    # add an autocomplete
    def add_autocomplete(self, type, value):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/auto-completes"
        body = {
            "type":type,
            "value":value
        }
        return self.api_call("POST", url, body=body)
    
    # get document IDs from a search ID
    def get_document_ids_from_search(self, search_id):
        url = f"{self.search_url}/document-groups/{self.document_group_id}/searches/{search_id}/document-ids{self.trailing_slash}"
        return self.api_call("GET", url)
    
    # get JSON from a document ID
    def get_json_from_document_id(self, document_id):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/documents/{document_id}"
        return self.api_call("GET", url)
    
    # get assets from a document ID
    def get_document_assets(self, document_id):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/documents/{document_id}/assets"
        return self.api_call("GET", url)
    
    # get asset from a document ID
    def get_document_asset(self, document_id, asset_id):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/documents/{document_id}/assets/{asset_id}"
        return self.api_call("GET", url)
    
    # get versions from a document ID
    def get_document_versions(self, document_id):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/documents/{document_id}/versions"
        return self.api_call("GET", url)

    # get orders (requires a company ID)
    def get_orders(self):
        if self.company_id is None:
            raise Exception("You must set a company ID to use this method")
        url = f"{self.search_url}/document-groups/{self.document_group_id}/companies/{self.company_id}/orders{self.trailing_slash}"
        return self.api_call("GET", url)

    # close an order
    def close_order(self, order_id):
        if self.company_id is None:
            raise Exception("You must set a company ID to use this method")
        url = f"{self.search_url}/document-groups/{self.document_group_id}/companies/{self.company_id}/orders/{order_id}/close{self.trailing_slash}"
        return self.api_call("POST", url)

    # reopen an order
    def reopen_order(self, order_id):
        if self.company_id is None:
            raise Exception("You must set a company ID to use this method")
        url = f"{self.search_url}/document-groups/{self.document_group_id}/companies/{self.company_id}/orders/{order_id}/re-open{self.trailing_slash}"
        return self.api_call("POST", url)
    
    # get document group meta data
    def get_document_group_metadata(self):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/plant-info"
        return self.api_call("GET", url)
    
    # run a report
    def run_report(self, report_id, params=None):
        url = f"{self.search_url}/reports/{report_id}/run{self.trailing_slash}"
        return self.api_call("GET", url, params=params)
    
    # run a search
    def run_search(self, search_query):
        url = f"{self.search_url}/document-groups/{self.document_group_id}/searches{self.trailing_slash}"
        return self.api_call("POST", url, body=search_query)

    # run the user-activity report
    def run_user_activity_report(self, start_date, end_date, format="json"):
        params = {
            "companyId":self.company_id,
            "plantId":self.document_group_id,
            "responseType":format,
            "startDate":start_date,
            "endDate":end_date
        }
        return self.run_report("user-activity", params=params)
