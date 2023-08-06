"""Packer Handler"""
import os
import sys
import requests

class PyPacker():
    """IOPP HCP-Packer Client"""

    def __init__(
            self,
            hcp_url='https://api.hashicorp.cloud',
            auth_url='https://auth.hashicorp.com/oauth/token',
            client_id=None,
            client_secret=None,
            org_id=None,
            proj_id=None,
            timeout=30,
        ):
        """Creates a new client instance"""
        self.client_id = client_id if client_id else os.getenv("HCP_CLIENT_ID")
        if self.client_id is None:
            print('Either provide a client ID or set HCP_CLIENT_ID')
            sys.exit(1)
        self.client_secret = client_secret if client_secret else \
            os.getenv("HCP_CLIENT_SECRET")
        if self.client_secret is None:
            print('Either provide a client secret or set HCP_CLIENT_SECRET')
            sys.exit(1)
        self.org_id = org_id if org_id else os.getenv("HCP_ORGANIZATION_ID")
        if self.org_id is None:
            print('Either provide an org ID or set HCP_ORGANIZATION_ID')
            sys.exit(1)
        self.proj_id = proj_id if proj_id else os.getenv("HCP_PROJECT_ID")
        if self.proj_id is None:
            print('Either provide a project ID or set HCP_PROJECT_ID')
            sys.exit(1)
        self.hcp_url = hcp_url
        self.auth_url = auth_url
        self.timeout = timeout
        self.bearer = None
        self.headers = None
        self.api_path = f"{self.hcp_url}/packer/2021-04-30/organizations"
        self.proj_path = f"{self.api_path}/{self.org_id}/projects/{self.proj_id}"

    def authenticate(self):
        """Obtain bearer token"""
        auth_data = {
            "audience": self.hcp_url,
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        req = requests.post(self.auth_url, json=auth_data, timeout=self.timeout)
        if req.status_code != 200:
            print(f"Error: {req.reason}")
            sys.exit(1)
        self.bearer = req.json()
        self.set_headers()

    def set_headers(self):
        """Set the auth header for reuse"""
        self.headers = {
            "Authorization": f"Bearer {self.bearer['access_token']}"
        }

    def get_build(self, build_id=None, region=None, provider=None):
        """Get Build API call"""
        params = {}
        params["location.region.provider"] = provider if provider else 'null'
        params["location.region.region"] = region if region else 'null'
        url = f"{self.proj_path}/builds/{build_id}"
        req = requests.get(url=url, headers=self.headers,\
                           timeout=self.timeout, params=params)
        if req.status_code != 200:
            print(f"Error: {req.status_code} {req.reason}")
            sys.exit(1)
        return req.json()

    def delete_build(self, build_id=None, region=None, provider=None):
        """Delete Build API call"""
        params = {}
        params["location.region.provider"] = provider if provider else 'null'
        params["location.region.region"] = region if region else 'null'
        url = f"{self.proj_path}/builds/{build_id}"
        req = requests.delete(url=url, headers=self.headers,\
                              timeout=self.timeout, params=params)
        if req.status_code != 200:
            print(f"Error: {req.status_code} {req.reason}")
            sys.exit(1)
        return req.json()

    def update_build(self):
        """Update Build API Call"""
        print("API route not implemented in this client yet")
        return ""

    def list_buckets(self):
        """List Buckets API Call"""
        print("API route not implemented in this client yet")
        return ""

    def create_bucket(self):
        """Create Bucket API Call"""
        print("API route not implemented in this client yet")
        return ""

    def get_bucket(self, bucket=None, bucket_id=None, region=None, provider=None):
        """Get Bucket API call"""
        params = {}
        params["location.region.provider"] = provider
        params["location.region.region"] = region
        params["bucket_id"] = bucket_id
        url = f"{self.proj_path}/images/{bucket}"
        req = requests.get(url=url, headers=self.headers,\
                           timeout=self.timeout, params=params)
        if req.status_code != 200:
            print(f"Error: {req.status_code} {req.reason}")
            sys.exit(1)
        return req.json()

    def delete_bucket(self):
        """Delete Bucket API Call"""
        print("API route not implemented in this client yet")
        return ""

    def update_bucket(self):
        """Update Bucket API Call"""
        print("API route not implemented in this client yet")
        return ""

    def list_bucket_ancestry(self):
        """List Bucket Ancestry API Call"""
        print("API route not implemented in this client yet")
        return ""

    def list_channels(self, bucket=None, region=None, provider=None):
        """List Channels API Call"""
        params = {}
        params["location.region.provider"] = provider
        params["location.region.region"] = region
        url = f"{self.proj_path}/images/{bucket}/channels"
        req = requests.get(url=url, headers=self.headers,\
                           timeout=self.timeout, params=params)
        if req.status_code != 200:
            print(f"Error: {req.status_code} {req.reason}")
            sys.exit(1)
        return req.json()

    def create_channel(self):
        """Create Channel API Call"""
        print("API route not implemented in this client yet")
        return ""

    def get_channel(self, bucket=None, channel=None, region=None, provider=None):
        """Get Channel API Call"""
        params = {}
        params["location.region.provider"] = provider
        params["location.region.region"] = region
        url = f"{self.proj_path}/images/{bucket}/channels/{channel}"
        req = requests.get(url=url, headers=self.headers,\
                           timeout=self.timeout, params=params)
        if req.status_code != 200:
            print(f"Error: {req.status_code} {req.reason}")
            sys.exit(1)
        return req.json()

    def delete_channel(self):
        """Delete Channel API Call"""
        print("API route not implemented in this client yet")
        return ""

    def update_channel(self):
        """Update Channel API Call"""
        print("API route not implemented in this client yet")
        return ""

    def list_channel_history(self):
        """List Channel History API Call"""
        print("API route not implemented in this client yet")
        return ""

    def get_iteration(self):
        """Get Iteration API Call"""
        print("API route not implemented in this client yet")
        return ""

    def list_iterations(self):
        """List Iterations API Call"""
        print("API route not implemented in this client yet")
        return ""

    def create_iteration(self):
        """Create Iteration API Call"""
        print("API route not implemented in this client yet")
        return ""

    def create_build(self):
        """Create Build API Call"""
        print("API route not implemented in this client yet")
        return ""

    def list_builds(self):
        """List Builds API Call"""
        print("API route not implemented in this client yet")
        return ""

    def delete_iteration(self):
        """Delete Builds API Call"""
        print("API route not implemented in this client yet")
        return ""

    def update_iteration(self):
        """Update Iteration API Call"""
        print("API route not implemented in this client yet")
        return ""

    def get_registry(self, region=None, provider=None):
        """Get Registry API Call"""
        params = {}
        params["location.region.provider"] = provider
        params["location.region.region"] = region
        url = f"{self.proj_path}/registry"
        req = requests.get(url=url, headers=self.headers,\
                           timeout=self.timeout, params=params)
        if req.status_code != 200:
            print(f"Error: {req.status_code} {req.reason}")
            sys.exit(1)
        return req.json()

    def create_registry(self):
        """Create Registry API Call"""
        print("API route not implemented in this client yet")
        return ""

    def delete_registry(self):
        """Delete Registry API Call"""
        print("API route not implemented in this client yet")
        return ""

    def update_registry(self):
        """Update Registry API Call"""
        print("API route not implemented in this client yet")
        return ""
