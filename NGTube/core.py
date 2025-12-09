"""
NGTube Core Module

This module provides the core functionality for interacting with YouTube.
"""

import requests
import re
import demjson3 as demjson

class YouTubeCore:
    """
    Core class for YouTube data extraction.

    Attributes:
        url (str): The YouTube URL.
        headers (dict): HTTP headers for requests.
    """

    def __init__(self, url: str):
        """
        Initialize the YouTubeCore with a URL.

        Args:
            url (str): The YouTube URL.
        """
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def fetch_html(self) -> str:
        """
        Fetch the HTML content from the YouTube URL.

        Returns:
            str: The HTML content.
        """
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Failed to fetch HTML: {response.status_code}")

    def extract_ytinitialdata(self, html: str) -> dict:
        """
        Extract ytInitialData from HTML.

        Args:
            html (str): The HTML content.

        Returns:
            dict: The ytInitialData JSON.
        """
        start_pattern = r'var ytInitialData\s*=\s*\{'
        start_match = re.search(start_pattern, html)

        if start_match:
            start_index = start_match.end() - 1
            brace_count = 0
            in_string = False
            escape_next = False
            end_index = start_index

            for i in range(start_index, len(html)):
                char = html[i]
                if escape_next:
                    escape_next = False
                    continue
                if char == '\\':
                    escape_next = True
                    continue
                if char == '"' and not in_string:
                    in_string = True
                elif char == '"' and in_string:
                    in_string = False
                elif not in_string:
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end_index = i
                            break

            json_str = html[start_index:end_index + 1]
            try:
                result = demjson.decode(json_str)
                if isinstance(result, dict):
                    return result
                else:
                    raise Exception("Parsed data is not a dictionary")
            except Exception as e:
                raise Exception(f"Failed to parse ytInitialData: {e}")
        else:
            raise Exception("ytInitialData not found in HTML")

    def extract_ytinitialplayerresponse(self, html: str) -> dict:
        """
        Extract ytInitialPlayerResponse from HTML.

        Args:
            html (str): The HTML content.

        Returns:
            dict: The ytInitialPlayerResponse JSON.
        """
        start_pattern = r'var ytInitialPlayerResponse\s*=\s*\{'
        start_match = re.search(start_pattern, html)

        if start_match:
            start_index = start_match.end() - 1
            brace_count = 0
            in_string = False
            escape_next = False
            end_index = start_index

            for i in range(start_index, len(html)):
                char = html[i]
                if escape_next:
                    escape_next = False
                    continue
                if char == '\\':
                    escape_next = True
                    continue
                if char == '"' and not in_string:
                    in_string = True
                elif char == '"' and in_string:
                    in_string = False
                elif not in_string:
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end_index = i
                            break

            json_str = html[start_index:end_index + 1]
            try:
                result = demjson.decode(json_str)
                if isinstance(result, dict):
                    return result
                else:
                    raise Exception("Parsed data is not a dictionary")
            except Exception as e:
                raise Exception(f"Failed to parse ytInitialPlayerResponse: {e}")
        else:
            raise Exception("ytInitialPlayerResponse not found in HTML")

    def make_api_request(self, endpoint: str, payload: dict) -> dict:
        """
        Make a POST request to YouTube's internal API.

        Args:
            endpoint (str): The API endpoint.
            payload (dict): The request payload.

        Returns:
            dict: The API response JSON.
        """
        response = requests.post(endpoint, json=payload, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed: {response.status_code}")