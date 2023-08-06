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
        self.client_secret = client_secret if client_secret else os.getenv("HCP_CLIENT_SECRET")
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

    def authenticate(self):
        """Obtain bearer token"""
        auth_data = {
            "audience": self.hcp_url,
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        r = requests.post(self.auth_url, json=auth_data, timeout=self.timeout)
        if r.status_code != 200:
            print(f"Error: {r.reason}")
            sys.exit(1)
        self.bearer = r.json()
        self.set_headers()

    def set_headers(self):
        """Set the auth header for reuse"""
        self.headers = {
            "Authorization": f"Bearer {self.bearer['access_token']}"
        }

    def get_build(self, build_id=None, region=None, provider=None):
        """Get Build API call"""
        params = dict()
        params["location.region.provider"] = provider if provider else 'null'
        params["location.region.region"] = region
        url = f"{self.api_path}/{self.org_id}/projects/{self.proj_id}/builds/{build_id}"
        req = requests.get(url=url, headers=self.headers, timeout=self.timeout, params=params)
        if req.status_code != 200:
            print(f"Error: {req.status_code} {req.reason}")
            sys.exit(1)
        return req.json()

    # def delete_build
    # def update_build
    # def list_buckets
    # def create_bucket

    def get_bucket(self, bucket=None, bucket_id=None, region=None, provider=None):
        """Get Bucket API call"""
        params = dict()
        params["location.region.provider"] = provider
        params["location.region.region"] = region
        params["bucket_id"] = bucket_id
        url = f"{self.api_path}/{self.org_id}/projects/{self.proj_id}/images/{bucket}"
        req = requests.get(url=url, headers=self.headers, timeout=self.timeout, params=params)
        if req.status_code != 200:
            print(f"Error: {req.status_code} {req.reason}")
            sys.exit(1)
        return req.json()

    # def delete_bucket
    # def update_bucket
    # def list_bucket_ancestry
    # def list_channels
    # def create_channel
    # def get_channel
    # def delete_channel
    # def update_channel
    # def list_channel_history
    # def get_iteration
    # def list_iterations
    # def create_iteration
    # def create_build
    # def list_builds
    # def delete_iteration
    # def update_iteration
    # def get_registry
    # def create_registry
    # def delete_registry
    # def update_registry
