"""
NGTube Search Module

This module provides functionality to search YouTube and extract search results.
"""

from ..core import YouTubeCore
import requests
import json

class SearchFilters:
    """
    Predefined search filters for YouTube search.
    """
    CHANNELS = "EgIQAg%3D%3D"
    VIDEOS_TODAY = "EgIIAg%3D%3D"
    SORT_BY_DATE = "CAI%3D"

class Search:
    """
    Class to perform YouTube searches and extract results.

    Attributes:
        query (str): The search query.
        max_results (int): Maximum number of results to load.
        results (list): List of video results.
        estimated_results (int): Estimated total results.
    """

    def __init__(self, query: str, max_results: int = 50, filter: str = ""):
        """
        Initialize the Search with a query.

        Args:
            query (str): The search query.
            max_results (int): Maximum number of results to load.
            filter (str): Search filter, use SearchFilters constants or custom params string.
        """
        self.query = query
        self.max_results = max_results
        self.filter = filter
        self.params = filter if isinstance(filter, str) else (filter.value if hasattr(filter, 'value') else str(filter))
        self.results = []
        self.estimated_results = 0
        self.url = "https://www.youtube.com/youtubei/v1/search?prettyPrint=false"
        self.payload = {
            "context": {
                "client": {
                    "hl": "de",
                    "gl": "DE",
                    "remoteHost": "2001:9e8:5b95:d300:259a:3c08:df9e:b87b",
                    "deviceMake": "",
                    "deviceModel": "",
                    "visitorData": "CgtoOEhOakxyRkNFYyjNiuLJBjIKCgJERRIEEgAgF2LfAgrcAjE0LllUPVZrQmNQLWxyV0RZYTRiOW1OMVRIaktaMm1UQ1IwRUM0WEdJRW1YZXJwTDhDdDNaS1NRdXpnMVRON2pEbmg0elBUdEJtdkp1dnA2dnZwWG1CSmJRN0ZJRVg1dmVBbTJoWmwwaVR5QUZucEtrVy1kVVJyREg5RlR2RFlHdEVJQ3V5cVhwUVo3M09yS1AyN1ZYaEZUekFTV1pINHpXNmxRMW9HbjZxRVJEd1MyMWtubks5d1Z3V3lUMUN2RFg2WkJ5ckRGOHJBbWlab3BFQXdRcmJNRTljbmhJY2xwOU1GeWFqdFc2YVZNUTBtb1ZES1pLMjVTRXBSLTlxT2xpYlczU0dQc2todExJd2dDamRnNUpyeGNuWjV4Z0tKLWRJSGRYWDVaRFptSXhUdTBXQWgyWV9KeWR4QkJiR0NEX3JORGVVQzFzeWNnVUdJdnNCMHdrV1A1N2JOZw%3D%3D",
                    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 OPR/124.0.0.0,gzip(gfe)",
                    "clientName": "WEB",
                    "clientVersion": "2.20251208.06.00",
                    "osName": "Windows",
                    "osVersion": "10.0",
                    "originalUrl": f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}",
                    "platform": "DESKTOP",
                    "clientFormFactor": "UNKNOWN_FORM_FACTOR",
                    "windowWidthPoints": 1875,
                    "configInfo": {
                        "appInstallData": "CM2K4skGEIOs0BwQvKTQHBDAqtAcEL2KsAUQs5DPHBDwtNAcEMGP0BwQt-r-EhC45M4cEInorgUQibDOHBCi-88cELuu0BwQlP6wBRC9rtAcEJTyzxwQ5uDPHBCV988cEKil0BwQ5aTQHBDa984cELnZzhwQ9quwBRCNsNAcEN68zhwQxPTPHBDLstAcEJ3QsAUQla_QHBCHrM4cEMn3rwUQ0eDPHBCW288cEK7WzxwQh4PQHBDM688cEMOR0BwQ9NXOHBC72c4cEM3RsQUQmY2xBRDjuM8cEKys0BwQ94nQHBDzs4ATEIOe0BwQ8rPQHBCL988cEIzpzxwQmbnQHBCRjP8SEL22rgUQsaLQHBDmh9AcEMj3zxwQgo_PHBDartAcEIiT0BwQndfPHBCmmrAFELyzgBMQ2JbQHBCTg9AcEPyyzhwQw6rQHBDRvdAcEMzfrgUQ4M2xBRCTttAcEJSZgBMQ0-GvBRDyndAcEL2ZsAUQzrPQHBDi1K4FEIiHsAUQy9GxBRCBzc4cEI-50BwQ-b6AExDildAcKnBDQU1TVUJWTC1acS1ETGlVRW9nQzlnU3FBb1BPNWd2d3NSS0hUREtnckFRRHk3NEYtam41Z2dhZ0JxSXVfQ2FtQV9GUHpnX3VYSUlQNmlmMkQ0VVU0aVB1blFXTUVKMHZnaTdwRTU5THE0M2xIaDBIMAA%3D",
                        "coldConfigData": "CM2K4skGEOy6rQUQxIWuBRC9tq4FEOLUrgUQvYqwBRCNzLAFEJ3QsAUQz9KwBRDM9rAFEOP4sAUQr6fOHBD8ss4cEPTVzhwQ47jPHBD4xs8cENrTzxwQndfPHBCf188cEMfazxwQsODPHBDP4M8cEOXnzxwQ5-fPHBCTg9AcEIiG0BwQ5ofQHBD3idAcEM2L0BwQ_pPQHBCTldAcEOKV0BwQqpzQHBC8pNAcELSo0BwQwKrQHBDDqtAcEJ2s0BwQzqzQHBC7rtAcEL2u0BwQjbDQHBCtstAcEMuy0BwQ8LTQHBCTttAcEJm50BwQzrnQHBD7utAcEJW70BwQn73QHBCuvdAcEMW90BwaMkFDRFNSMlRTNjJmdnZfYzRCUWhDR2c2aXIzQzVyMHBDMjBtVlhEYmdVTTZOVWhsYld3IjJBQ0RTUjJSQ2tGWFFNMkFnVU5fQUpadXRpTkpwbEJzMDRJa2QwcXpYU0dUdFJqV1RyZyqYAUNBTVNiQTB0dU4yM0FxUVpseC1mVDVtU21oRDdGbzAyX2lPbkRjZ0FyQXhxTkowV3FBU2hES2dDMlJldURhc1BGVG1ac2JjZmhhUUZrWndGNGRzQno4SUFqNmNHX2RRR01zLUFCZG1rQmdPaXNnWEtTd2F3YjRjRHhnbnpBNnFJQnBSU3lubkxTZ1NTdmdiS2RZMXNCUT09",
                        "coldHashData": "CM2K4skGEhMxMTIwNzUxNjc2MDk1NDAyMzUxGM2K4skGMjJBQ0RTUjJUUzYyZnZ2X2M0QlFoQ0dnNmlyM0M1cjBwQzIwbVZYRGJnVU02TlVobGJXdzoyQUNEU1IyUkNrRlhRTTJBZ1VOX0FKWnV0aU5KcGxCczA0SWtkMHF6WFNHVHRSaldUcmdCmAFDQU1TYkEwdHVOMjNBcVFabHgtZlQ1bVNtaEQ3Rm8wMl9pT25EY2dBckF4cU5KMFdxQVNoREtnQzJSZXVEYXNQRlRtWnNiY2ZoYVFGa1p3RjRkc0J6OElBajZjR19kUUdNcy1BQmRta0JnT2lzZ1hLU3dhd2I0Y0R4Z256QTZxSUJwUlN5bm5MU2dTU3ZnYktkWTFzQlE9PQ%3D%3D",
                        "hotHashData": "CM2K4skGEhQxMzcwMTE1MjM3Mzc0MTU5MDg2NxjNiuLJBiiU5PwSKKXQ_RIonpH-EijIyv4SKLfq_hIokYz_Eii0i4ATKPeQgBMoy5GAEyiUmYATKLWbgBMo2LCAEyi8s4ATKMO2gBMosLeAEyjbt4ATKKW4gBMovrqAEyjCvYATKPm-gBMoj7-AEyj-v4ATMjJBQ0RTUjJUUzYyZnZ2X2M0QlFoQ0dnNmlyM0M1cjBwQzIwbVZYRGJnVU02TlVobGJXdzoyQUNEU1IyUkNrRlhRTTJBZ1VOX0FKWnV0aU5KcGxCczA0SWtkMHF6WFNHVHRSaldUcmdCRENBTVNMdzBXb3RmNkZhN0JCcE5Oc3hhbFJvSU55d1lWSGQzUHdnemk5Z19jcWVZTDJNMEo4NUFFc2FvVzZRNjNCdU16"
                    },
                    "screenDensityFloat": 1,
                    "userInterfaceTheme": "USER_INTERFACE_THEME_DARK",
                    "timeZone": "Europe/Berlin",
                    "browserName": "Opera",
                    "browserVersion": "124.0.0.0",
                    "acceptHeader": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "deviceExperimentId": "ChxOelU0TVRrMU5qVTBNRFE1TnpVd09UTXpOdz09EM2K4skGGM2K4skG",
                    "rolloutToken": "CKrC-PrFiJv-lAEQssHcioHCjQMY8ejh9vCwkQM%3D",
                    "screenWidthPoints": 1875,
                    "screenHeightPoints": 923,
                    "screenPixelDensity": 1,
                    "utcOffsetMinutes": 60,
                    "connectionType": "CONN_CELLULAR_4G",
                    "memoryTotalKbytes": "8000000",
                    "mainAppWebInfo": {
                        "graftUrl": f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}",
                        "pwaInstallabilityStatus": "PWA_INSTALLABILITY_STATUS_UNKNOWN",
                        "webDisplayMode": "WEB_DISPLAY_MODE_BROWSER",
                        "isWebNativeShareAvailable": True
                    },
                    "clientScreen": "ADUNIT"
                },
                "user": {
                    "lockedSafetyMode": False
                },
                "request": {
                    "useSsl": True,
                    "internalExperimentFlags": [],
                    "consistencyTokenJars": []
                },
                "clickTracking": {
                    "clickTrackingParams": "CEIQt6kLGAEiEwjFzr2Aq7GRAxXuyzsCHcHiLgLKAQRJQENQ"
                },
                "adSignalsInfo": {
                    "params": [
                        {"key": "dt", "value": "1765311820294"},
                        {"key": "flash", "value": "0"},
                        {"key": "frm", "value": "0"},
                        {"key": "u_tz", "value": "60"},
                        {"key": "u_his", "value": "4"},
                        {"key": "u_h", "value": "1080"},
                        {"key": "u_w", "value": "1920"},
                        {"key": "u_ah", "value": "1032"},
                        {"key": "u_aw", "value": "1920"},
                        {"key": "u_cd", "value": "24"},
                        {"key": "bc", "value": "31"},
                        {"key": "bih", "value": "923"},
                        {"key": "biw", "value": "1860"},
                        {"key": "brdim", "value": "-1920,0,-1920,0,1920,0,1920,1032,1875,923"},
                        {"key": "vis", "value": "1"},
                        {"key": "wgl", "value": "true"},
                        {"key": "ca_type", "value": "image"}
                    ]
                }
            },
            "query": query
        }
        if self.params:
            self.payload["params"] = self.params
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 OPR/124.0.0.0"
        }

    def perform_search(self):
        """
        Perform the search and load results.
        """
        continuation = None
        while len(self.results) < self.max_results:
            if continuation:
                self.payload["continuation"] = continuation
            response = requests.post(self.url, json=self.payload, headers=self.headers)
            if response.status_code != 200:
                break
            data = response.json()
            items, estimated, cont = self._parse_results(data)
            if not self.estimated_results:
                self.estimated_results = estimated
            self.results.extend(items)
            continuation = cont
            if not continuation:
                break

    def _parse_results(self, data):
        if not data:
            return [], 0, None
        estimated_results = int(data.get("estimatedResults", "0"))
        contents = data.get("contents", {}).get("twoColumnSearchResultsRenderer", {}).get("primaryContents", {}).get("sectionListRenderer", {}).get("contents", [])
        continuation = None
        items = []
        for item in contents:
            if "itemSectionRenderer" in item:
                for content in item["itemSectionRenderer"]["contents"]:
                    if "videoRenderer" in content:
                        video = content["videoRenderer"]
                        video_info = {
                            "type": "video",
                            "videoId": video.get("videoId"),
                            "title": video.get("title", {}).get("runs", [{}])[0].get("text"),
                            "channel": video.get("longBylineText", {}).get("runs", [{}])[0].get("text"),
                            "publishedTime": video.get("publishedTimeText", {}).get("simpleText"),
                            "length": video.get("lengthText", {}).get("simpleText"),
                            "viewCount": video.get("viewCountText", {}).get("simpleText"),
                            "thumbnail": video.get("thumbnail", {}).get("thumbnails", [{}])[0].get("url")
                        }
                        items.append(video_info)
                    elif "channelRenderer" in content:
                        channel = content["channelRenderer"]
                        channel_info = {
                            "type": "channel",
                            "channelId": channel.get("channelId"),
                            "title": channel.get("title", {}).get("simpleText"),
                            "description": " ".join([run.get("text", "") for run in channel.get("descriptionSnippet", {}).get("runs", [])]),
                            "subscriberCount": channel.get("videoCountText", {}).get("simpleText"),  # Note: This seems to be videoCount in the data
                            "thumbnail": channel.get("thumbnail", {}).get("thumbnails", [{}])[0].get("url")
                        }
                        items.append(channel_info)
            elif "continuationItemRenderer" in item:
                continuation = item["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]
        # Check for continuation in onResponseReceivedCommands
        if "onResponseReceivedCommands" in data:
            for command in data["onResponseReceivedCommands"]:
                if "appendContinuationItemsAction" in command:
                    for item in command["appendContinuationItemsAction"]["continuationItems"]:
                        if "itemSectionRenderer" in item:
                            for content in item["itemSectionRenderer"]["contents"]:
                                if "videoRenderer" in content:
                                    video = content["videoRenderer"]
                                    video_info = {
                                        "type": "video",
                                        "videoId": video.get("videoId"),
                                        "title": video.get("title", {}).get("runs", [{}])[0].get("text"),
                                        "channel": video.get("longBylineText", {}).get("runs", [{}])[0].get("text"),
                                        "publishedTime": video.get("publishedTimeText", {}).get("simpleText"),
                                        "length": video.get("lengthText", {}).get("simpleText"),
                                        "viewCount": video.get("viewCountText", {}).get("simpleText"),
                                        "thumbnail": video.get("thumbnail", {}).get("thumbnails", [{}])[0].get("url")
                                    }
                                    items.append(video_info)
                                elif "channelRenderer" in content:
                                    channel = content["channelRenderer"]
                                    channel_info = {
                                        "type": "channel",
                                        "channelId": channel.get("channelId"),
                                        "title": channel.get("title", {}).get("simpleText"),
                                        "description": " ".join([run.get("text", "") for run in channel.get("descriptionSnippet", {}).get("runs", [])]),
                                        "subscriberCount": channel.get("videoCountText", {}).get("simpleText"),
                                        "thumbnail": channel.get("thumbnail", {}).get("thumbnails", [{}])[0].get("url")
                                    }
                                    items.append(channel_info)
                        elif "continuationItemRenderer" in item:
                            continuation = item["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]
        return items, estimated_results, continuation

    def get_results(self):
        """
        Get the search results.

        Returns:
            dict: Dictionary with query, filter, params, estimated_results, loaded_items, and items list.
        """
        return {
            "query": self.query,
            "filter": self.filter,
            "params": self.params,
            "estimated_results": self.estimated_results,
            "loaded_items": len(self.results),
            "items": self.results
        }