"""Redmine API Client

A class that provides common access processing to Redmine's REST API.
"""

import os
from typing import Any, Dict, Optional, Union

import requests


class RedmineAPIClient:
    """Redmine API Client

    Attributes:
        base_url (str): Base URL of the Redmine server
        api_key (str): Redmine API key
    """

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        """Initialization

        Args:
            base_url (str, optional): Base URL of the Redmine server
            api_key (str, optional): Redmine API key
        """
        self.base_url = base_url or os.environ.get("REDMINE_URL")
        self.api_key = api_key or os.environ.get("REDMINE_ADMIN_API_KEY")
        if not self.base_url or not self.api_key:
            raise ValueError("Redmine URL or API key is not set.")

    def _headers(self) -> Dict[str, str]:
        """Generate headers for API requests

        Returns:
            dict: Header information
        """
        return {"X-Redmine-API-Key": self.api_key}

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        """Send an API request

        Args:
            method (str): HTTP method
            endpoint (str): Endpoint path (e.g., '/projects.json')
            params (dict, optional): Query parameters
            data (dict or str, optional): POST/PUT data
            json (dict, optional): JSON data
            headers (dict, optional): Additional headers

        Returns:
            requests.Response: Response object

        Raises:
            requests.HTTPError: When an HTTP error occurs
        """
        url = self.base_url.rstrip("/") + endpoint
        req_headers = self._headers()
        if headers:
            req_headers.update(headers)
        resp = requests.request(
            method=method,
            url=url,
            params=params,
            data=data,
            json=json,
            headers=req_headers,
        )
        resp.raise_for_status()
        return resp

    def get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """GET request

        Args:
            endpoint (str): Endpoint path
            params (dict, optional): Query parameters
            headers (dict, optional): Additional headers

        Returns:
            requests.Response: Response
        """
        return self._request("GET", endpoint, params=params, headers=headers)

    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        """POST request

        Args:
            endpoint (str): Endpoint path
            data (dict, optional): Form data
            json (dict, optional): JSON data
            headers (dict, optional): Additional headers

        Returns:
            requests.Response: Response
        """
        return self._request("POST", endpoint, data=data, json=json, headers=headers)

    def put(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        """PUT request

        Args:
            endpoint (str): Endpoint path
            data (dict, optional): Form data
            json (dict, optional): JSON data
            headers (dict, optional): Additional headers

        Returns:
            requests.Response: Response
        """
        return self._request("PUT", endpoint, data=data, json=json, headers=headers)

    def delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """DELETE request

        Args:
            endpoint (str): Endpoint path
            headers (dict, optional): Additional headers

        Returns:
            requests.Response: Response
        """
        return self._request("DELETE", endpoint, headers=headers)

    def patch(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        """PATCH request

        Args:
            endpoint (str): Endpoint path
            data (dict, optional): Form data
            json (dict, optional): JSON data
            headers (dict, optional): Additional headers

        Returns:
            requests.Response: Response
        """
        return self._request("PATCH", endpoint, data=data, json=json, headers=headers)
