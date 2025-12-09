"""
NGTube Channel Module

This module provides functionality to extract channel metadata and videos from YouTube channels.
"""

from typing import Union
from ..core import YouTubeCore
from .. import utils

class Channel:
    """
    Class to extract channel metadata and videos from a YouTube channel.

    Attributes:
        url (str): The YouTube channel URL.
        data (dict): The extracted channel data.
    """

    def __init__(self, url: str):
        """
        Initialize the Channel with a URL.

        Args:
            url (str): The YouTube channel URL.
        """
        self.url = url
        self.core = YouTubeCore(url)
        self.data = {}

    def extract_profile(self, max_videos: Union[int, str] = 200) -> dict:
        """
        Extract channel profile data including metadata and videos.

        Args:
            max_videos (int | str): Maximum number of videos to load. Use 'all' to load all videos.
        """
        # API URL
        api_url = "https://www.youtube.com/youtubei/v1/browse"

        # Extract channel ID from URL
        channel_id = self._extract_channel_id()

        # Payload for Featured Tab
        payload_featured = self._get_payload_featured(channel_id)

        # Make API request for featured data
        try:
            data_featured = self.core.make_api_request(api_url, payload_featured)
        except Exception as e:
            raise Exception(f"Failed to fetch featured data: {e}")

        # Extract profile data from featured
        self._extract_profile_data(data_featured)

        # Payload for Videos Tab
        payload_videos = self._get_payload_videos(channel_id)

        # Make API request for videos
        try:
            data_videos = self.core.make_api_request(api_url, payload_videos)
        except Exception as e:
            raise Exception(f"Failed to fetch videos data: {e}")

        # Extract videos
        self._extract_videos(data_videos, max_videos)

        # Extract additional profile data from videos response
        self._extract_profile_data(data_videos)

        # Extract numbers
        self._extract_numbers()

        return self.data

    def _extract_channel_id(self) -> str:
        """Extract channel ID from URL."""
        if '@' in self.url:
            username = self.url.split('@')[1].split('/')[0]
            # Map known @handles to their channel IDs
            handle_to_id = {
                'HandOfUncut': 'UCCJ-NJtqLQRxuaxHZA9q6zg'
            }
            if username in handle_to_id:
                return handle_to_id[username]
            # For unknown handles, try to use the username directly
            return username
        elif '/channel/' in self.url:
            return self.url.split('/channel/')[1].split('/')[0]
        else:
            raise ValueError("Invalid channel URL format")

    def _get_payload_featured(self, channel_id: str) -> dict:
        """Get payload for featured tab."""
        return {
            "context": {
                "client": {
                    "hl": "de",
                    "gl": "DE",
                    "remoteHost": "2001:9e8:5b95:d300:259a:3c08:df9e:b87b",
                    "deviceMake": "",
                    "deviceModel": "",
                    "visitorData": "CgtoOEhOakxyRkNFYyiczeHJBjIKCgJERRIEEgAgF2LfAgrcAjE0LllUPUwwOGlIVEVUaHhvVXhiWWF2Rlo0OFhMRms0cFBpOVIwZFFQZDM4NGpsWnltU2t3ODJ5TjFaTFFwUWNwemV2NHhiSXJIUENxU2ozSWZOczJuN1M5d01WS2E2R3ZwNjlvZWRyLVBaclRKYnZyUGU5WkNXRERkd0VFbGJod1E3akg0TWNSTnk4eERqVThvWTdXNkNOODJUZU01UnlvQThrVDNPM2g1MUhWaUNiTFdFRmhOeGxmZEZtMUZ6dFlrNENaUnZMR1Y2Z2N4cC1naDRVTnFIWUl6b3BFS2ZJX1BMQUIwbzJkeDdXLU4yWTZVVFpGcFVrMndmZkdEbjIzX1ZKYkVGaHNmTXVKT1I4RUhOVG1uZUxaNlllOTJXLVNvLVo2b3RKWXE4ZXRqYWZXTTFHOXdFUHJHVmJUaUFtZW9PUWVBZVkxU2hlaEZ5ekhMODdhQXU4cS01UQ",
                    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 OPR/124.0.0.0,gzip(gfe)",
                    "clientName": "WEB",
                    "clientVersion": "2.20251207.11.00",
                    "osName": "Windows",
                    "osVersion": "10.0",
                    "originalUrl": self.url,
                    "platform": "DESKTOP",
                    "clientFormFactor": "UNKNOWN_FORM_FACTOR",
                    "windowWidthPoints": 1875,
                    "configInfo": {
                        "appInstallData": "CJzN4ckGEJbbzxwQwKrQHBCu1s8cEImwzhwQovvPHBD8ss4cEMT0zxwQ4M2xBRC8s4ATEIv3zxwQ5ofQHBCd0LAFEL2u0BwQyPfPHBC36v4SEJTyzxwQvKTQHBDi1K4FEPKd0BwQsaLQHBC9tq4FEPKz0BwQppqwBRDm4M8cEIiHsAUQ47jPHBD2q7AFENG90BwQzdGxBRDLstAcEIKPzxwQvZmwBRDzs4ATENPhrwUQzN-uBRCRjP8SEJX3zxwQ5aTQHBCTg9AcELjkzhwQndfPHBCzkM8cEIOs0BwQudnOHBDevM4cEJT-sAUQ2vfOHBC72c4cENiW0BwQzrPQHBCJ6K4FEPC00BwQjOnPHBCZudAcEIeszhwQ2q7QHBDDqtAcEMvRsQUQg57QHBCsrNAcEPeJ0BwQj7nQHBC7rtAcEIeD0BwQlJmAExDBj9AcEIiT0BwQw5HQHBDM688cEIHNzhwQyfevBRC9irAFEJO20BwQjbDQHBCopdAcEJmNsQUQ0eDPHBD01c4cEJWv0BwQ-b6AExDildAcKnRDQU1TVVJWSy1acS1ETGlVRW9nQzlnU3FBb1BPNWd2d3NSS0hUREtnckFRRHk3NEYtam41Z2dhZ0JxSXVfQ2FtQV9GUHpnX3VYSUlQNmlmMkQ0VVU0aVB1blFXTUVKd3ZWTGN2NlJPZlM2dU41UjZkQnc9PTAA",
                        "coldConfigData": "CJzN4ckGEOy6rQUQxIWuBRC9tq4FEOLUrgUQvYqwBRCNzLAFEJ3QsAUQz9KwBRDM9rAFEOP4sAUQr6fOHBD8ss4cEPTVzhwQ47jPHBD4xs8cENrTzxwQndfPHBCf188cEMfazxwQsODPHBDP4M8cEOXnzxwQ5-fPHBCTg9AcEIiG0BwQ5ofQHBD3idAcEM2L0BwQ_pPQHBCTldAcEOKV0BwQqpzQHBC8pNAcELSo0BwQwKrQHBDDqtAcEJ2s0BwQzqzQHBC7rtAcEL2u0BwQjbDQHBCtstAcEMuy0BwQ8LTQHBCTttAcEJm50BwQzrnQHBD7utAcEJW70BwQn73QHBCuvdAcEMW90BwaMkFPakZveDBmMnVCVFhJaWxBLVpDWklyMWRLeUlOa3J3UXFKVzVUOVJhVlZfa0tVdXpBIjJBT2pGb3gzWGw2Mzk2MXhIYmhoR3cyeTBRcFk1WDNScFI5VjVfRElVaUdMVTdfOVhqUSqYAUNBTVNiQTB0dU4yM0FxUVpseC1mVDVtU21oRDdGbzAyX2lPbkRjZ0FyQXhxTkowV3FBU2hES2dDMlJldURhc1BGVG1ac2JjZmhhUUZrWndGNGRzQno4SUFqNmNHX2RRR01zLUFCZG1rQmdPaXNnWEtTd2F3YjRjRHhnbnpBNnFJQnBSU3lubkxTZ1NTdmdiS2RZMXNCUT09",
                        "coldHashData": "CJzN4ckGEhMxMTIwNzUxNjc2MDk1NDAyMzUxGJzN4ckGMjJBT2pGb3gwZjJ1QlRYSWlsQS1aQ1pJcjFkS3lJTmtyd1FxSlc1VDlSYVZWX2tLVXV6QToyQU9qRm94M1hsNjM5NjF4SGJoaEd3MnkwUXBZNVgzUnBSOVY1X0RJVWlHTFU3XzlYalFCRENBTVNMdzBXb3RmNkZhN0JCcE5Oc3hhbFJvSU55d1lWSGQzUHdnemk5Z19jcWVZTDJNMEo4NUFFc2FvVzZRNjNCdU16"
                    },
                    "screenDensityFloat": 1,
                    "userInterfaceTheme": "USER_INTERFACE_THEME_DARK",
                    "timeZone": "Europe/Berlin",
                    "browserName": "Opera",
                    "browserVersion": "124.0.0.0",
                    "acceptHeader": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "deviceExperimentId": "ChxOelU0TVRreU1qYzVNekF4TmpNM01ERTJOUT09EJzN4ckGGJzN4ckG",
                    "rolloutToken": "CKrC-PrFiJv-lAEQssHcioHCjQMY8ejh9vCwkQM=",
                    "screenWidthPoints": 1875,
                    "screenHeightPoints": 923,
                    "screenPixelDensity": 1,
                    "utcOffsetMinutes": 60,
                    "connectionType": "CONN_CELLULAR_4G",
                    "memoryTotalKbytes": "8000000",
                    "mainAppWebInfo": {
                        "graftUrl": self.url,
                        "pwaInstallabilityStatus": "PWA_INSTALLABILITY_STATUS_UNKNOWN",
                        "webDisplayMode": "WEB_DISPLAY_MODE_BROWSER",
                        "isWebNativeShareAvailable": True
                    },
                    "clientScreen": "ADUNIT"
                }
            },
            "browseId": channel_id,
            "params": "EghmZWF0dXJlZPIGBAoCMgA%3D"
        }

    def _get_payload_videos(self, channel_id: str) -> dict:
        """Get payload for videos tab."""
        return {
            "context": {
                "client": {
                    "hl": "de",
                    "gl": "DE",
                    "remoteHost": "2001:9e8:5b95:d300:259a:3c08:df9e:b87b",
                    "deviceMake": "",
                    "deviceModel": "",
                    "visitorData": "CgtoOEhOakxyRkNFYyiczeHJBjIKCgJERRIEEgAgF2LfAgrcAjE0LllUPUwwOGlIVEVUaHhvVXhiWWF2Rlo0OFhMRms0cFBpOVIwZFFQZDM4NGpsWnltU2t3ODJ5TjFaTFFwUWNwemV2NHhiSXJIUENxU2ozSWZOczJuN1M5d01WS2E2R3ZwNjlvZWRyLVBaclRKYnZyUGU5WkNXRERkd0VFbGJod1E3akg0TWNSTnk4eERqVThvWTdXNkNOODJUZU01UnlvQThrVDNPM2g1MUhWaUNiTFdFRmhOeGxmZEZtMUZ6dFlrNENaUnZMR1Y2Z2N4cC1naDRVTnFIWUl6b3BFS2ZJX1BMQUIwbzJkeDdXLU4yWTZVVFpGcFVrMndmZkdEbjIzX1ZKYkVGaHNmTXVKT1I4RUhOVG1uZUxaNlllOTJXLVNvLVo2b3RKWXE4ZXRqYWZXTTFHOXdFUHJHVmJUaUFtZW9PUWVBZVkxU2hlaEZ5ekhMODdhQXU4cS01UQ",
                    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 OPR/124.0.0.0,gzip(gfe)",
                    "clientName": "WEB",
                    "clientVersion": "2.20251207.11.00",
                    "osName": "Windows",
                    "osVersion": "10.0",
                    "originalUrl": self.url,
                    "platform": "DESKTOP",
                    "clientFormFactor": "UNKNOWN_FORM_FACTOR",
                    "windowWidthPoints": 1875,
                    "configInfo": {
                        "appInstallData": "CJzN4ckGEJbbzxwQwKrQHBCu1s8cEImwzhwQovvPHBD8ss4cEMT0zxwQ4M2xBRC8s4ATEIv3zxwQ5ofQHBCd0LAFEL2u0BwQyPfPHBC36v4SEJTyzxwQvKTQHBDi1K4FEPKd0BwQsaLQHBC9tq4FEPKz0BwQppqwBRDm4M8cEIiHsAUQ47jPHBD2q7AFENG90BwQzdGxBRDLstAcEIKPzxwQvZmwBRDzs4ATENPhrwUQzN-uBRCRjP8SEJX3zxwQ5aTQHBCTg9AcELjkzhwQndfPHBCzkM8cEIOs0BwQudnOHBDevM4cEJT-sAUQ2vfOHBC72c4cENiW0BwQzrPQHBCJ6K4FEPC00BwQjOnPHBCZudAcEIeszhwQ2q7QHBDDqtAcEMvRsQUQg57QHBCsrNAcEPeJ0BwQj7nQHBC7rtAcEIeD0BwQlJmAExDBj9AcEIiT0BwQw5HQHBDM688cEIHNzhwQyfevBRC9irAFEJO20BwQjbDQHBCopdAcEJmNsQUQ0eDPHBD01c4cEJWv0BwQ-b6AExDildAcKnRDQU1TVVJWSy1acS1ETGlVRW9nQzlnU3FBb1BPNWd2d3NSS0hUREtnckFRRHk3NEYtam41Z2dhZ0JxSXVfQ2FtQV9GUHpnX3VYSUlQNmlmMkQ0VVU0aVB1blFXTUVKd3ZWTGN2NlJPZlM2dU41UjZkQnc9PTAA",
                        "coldConfigData": "CJzN4ckGEOy6rQUQxIWuBRC9tq4FEOLUrgUQvYqwBRCNzLAFEJ3QsAUQz9KwBRDM9rAFEOP4sAUQr6fOHBD8ss4cEPTVzhwQ47jPHBD4xs8cENrTzxwQndfPHBCf188cEMfazxwQsODPHBDP4M8cEOXnzxwQ5-fPHBCTg9AcEIiG0BwQ5ofQHBD3idAcEM2L0BwQ_pPQHBCTldAcEOKV0BwQqpzQHBC8pNAcELSo0BwQwKrQHBDDqtAcEJ2s0BwQzqzQHBC7rtAcEL2u0BwQjbDQHBCtstAcEMuy0BwQ8LTQHBCTttAcEJm50BwQzrnQHBD7utAcEJW70BwQn73QHBCuvdAcEMW90BwaMkFPakZveDBmMnVCVFhJaWxBLVpDWklyMWRLeUlOa3J3UXFKVzVUOVJhVlZfa0tVdXpBIjJBT2pGb3gzWGw2Mzk2MXhIYmhoR3cyeTBRcFk1WDNScFI5VjVfRElVaUdMVTdfOVhqUSqYAUNBTVNiQTB0dU4yM0FxUVpseC1mVDVtU21oRDdGbzAyX2lPbkRjZ0FyQXhxTkowV3FBU2hES2dDMlJldURhc1BGVG1ac2JjZmhhUUZrWndGNGRzQno4SUFqNmNHX2RRR01zLUFCZG1rQmdPaXNnWEtTd2F3YjRjRHhnbnpBNnFJQnBSU3lubkxTZ1NTdmdiS2RZMXNCUT09",
                        "coldHashData": "CJzN4ckGEhMxMTIwNzUxNjc2MDk1NDAyMzUxGJzN4ckGMjJBT2pGb3gwZjJ1QlRYSWlsQS1aQ1pJcjFkS3lJTmtyd1FxSlc1VDlSYVZWX2tLVXV6QToyQU9qRm94M1hsNjM5NjF4SGJoaEd3MnkwUXBZNVgzUnBSOVY1X0RJVWlHTFU3XzlYalFCRENBTVNMdzBXb3RmNkZhN0JCcE5Oc3hhbFJvSU55d1lWSGQzUHdnemk5Z19jcWVZTDJNMEo4NUFFc2FvVzZRNjNCdU16"
                    },
                    "screenDensityFloat": 1,
                    "userInterfaceTheme": "USER_INTERFACE_THEME_DARK",
                    "timeZone": "Europe/Berlin",
                    "browserName": "Opera",
                    "browserVersion": "124.0.0.0",
                    "acceptHeader": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "deviceExperimentId": "ChxOelU0TVRreU1qYzVNekF4TmpNM01ERTJOUT09EJzN4ckGGJzN4ckG",
                    "rolloutToken": "CKrC-PrFiJv-lAEQssHcioHCjQMY8ejh9vCwkQM=",
                    "screenWidthPoints": 1875,
                    "screenHeightPoints": 923,
                    "screenPixelDensity": 1,
                    "utcOffsetMinutes": 60,
                    "connectionType": "CONN_CELLULAR_4G",
                    "memoryTotalKbytes": "8000000",
                    "mainAppWebInfo": {
                        "graftUrl": self.url,
                        "pwaInstallabilityStatus": "PWA_INSTALLABILITY_STATUS_UNKNOWN",
                        "webDisplayMode": "WEB_DISPLAY_MODE_BROWSER",
                        "isWebNativeShareAvailable": True
                    },
                    "clientScreen": "ADUNIT"
                }
            },
            "browseId": channel_id,
            "params": "EgZ2aWRlb3PyBgQKAjoA"
        }

    def _extract_profile_data(self, data: dict):
        """Extract profile data from API response."""
        def find_profile_data(obj):
            if isinstance(obj, dict):
                if 'channelMetadataRenderer' in obj:
                    cmr = obj['channelMetadataRenderer']
                    self.data['title'] = cmr.get('title', '')
                    self.data['description'] = cmr.get('description', '')
                    self.data['channelId'] = cmr.get('externalId', '')
                    self.data['channelUrl'] = cmr.get('channelUrl', '')
                    self.data['keywords'] = cmr.get('keywords', '')
                    self.data['isFamilySafe'] = cmr.get('isFamilySafe', False)
                    self.data['links'] = utils.extract_links(self.data.get('description', ''))
                    return True
                if 'subscriberCountText' in obj and 'simpleText' in obj['subscriberCountText']:
                    self.data['subscriberCountText'] = obj['subscriberCountText']['simpleText']
                if 'viewCountText' in obj and 'simpleText' in obj['viewCountText']:
                    self.data['viewCountText'] = obj['viewCountText']['simpleText']
                if 'videoCountText' in obj and 'simpleText' in obj['videoCountText']:
                    self.data['videoCountText'] = obj['videoCountText']['simpleText']
                if 'channelVideoPlayerRenderer' in obj:
                    cvpr = obj['channelVideoPlayerRenderer']
                    video = {
                        'videoId': cvpr.get('videoId'),
                        'title': cvpr.get('title', {}).get('runs', [{}])[0].get('text', ''),
                        'description': cvpr.get('description', {}).get('runs', [{}])[0].get('text', '')
                    }
                    self.data['featured_video'] = video
                # Also check for metadataRows for video count
                if 'metadataRows' in obj and isinstance(obj['metadataRows'], list):
                    for row in obj['metadataRows']:
                        if 'metadataParts' in row and isinstance(row['metadataParts'], list):
                            for part in row['metadataParts']:
                                if 'text' in part and 'content' in part['text']:
                                    content = part['text']['content']
                                    if 'Videos' in content:
                                        self.data['videoCountText'] = content
                for v in obj.values():
                    find_profile_data(v)
            elif isinstance(obj, list):
                for item in obj:
                    find_profile_data(item)

        find_profile_data(data)

    def _extract_videos(self, data: dict, max_videos: Union[int, str]):
        """Extract videos from API response with continuation."""
        api_url = "https://www.youtube.com/youtubei/v1/browse"
        data_videos_list = [data]
        loaded_videos = 0

        # Initial videos
        initial_videos = self._find_videos(data)
        loaded_videos += len(initial_videos)

        # Find continuation token
        continuation_token = self._find_continuation_token(data)

        # Load more videos
        while continuation_token and (max_videos == 'all' or (isinstance(max_videos, int) and loaded_videos < max_videos)):
            payload_continuation = {
                "context": {
                    "client": {
                        "hl": "de",
                        "gl": "DE",
                        "remoteHost": "2001:9e8:5b95:d300:259a:3c08:df9e:b87b",
                        "deviceMake": "",
                        "deviceModel": "",
                        "visitorData": "CgtoOEhOakxyRkNFYyiczeHJBjIKCgJERRIEEgAgF2LfAgrcAjE0LllUPUwwOGlIVEVUaHhvVXhiWWF2Rlo0OFhMRms0cFBpOVIwZFFQZDM4NGpsWnltU2t3ODJ5TjFaTFFwUWNwemV2NHhiSXJIUENxU2ozSWZOczJuN1M5d01WS2E2R3ZwNjlvZWRyLVBaclRKYnZyUGU5WkNXRERkd0VFbGJod1E3akg0TWNSTnk4eERqVThvWTdXNkNOODJUZU01UnlvQThrVDNPM2g1MUhWaUNiTFdFRmhOeGxmZEZtMUZ6dFlrNENaUnZMR1Y2Z2N4cC1naDRVTnFIWUl6b3BFS2ZJX1BMQUIwbzJkeDdXLU4yWTZVVFpGcFVrMndmZkdEbjIzX1ZKYkVGaHNmTXVKT1I4RUhOVG1uZUxaNlllOTJXLVNvLVo2b3RKWXE4ZXRqYWZXTTFHOXdFUHJHVmJUaUFtZW9PUWVBZVkxU2hlaEZ5ekhMODdhQXU4cS01UQ",
                        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 OPR/124.0.0.0,gzip(gfe)",
                        "clientName": "WEB",
                        "clientVersion": "2.20251207.11.00",
                        "osName": "Windows",
                        "osVersion": "10.0",
                        "originalUrl": self.url,
                        "platform": "DESKTOP",
                        "clientFormFactor": "UNKNOWN_FORM_FACTOR",
                        "windowWidthPoints": 1875,
                        "configInfo": {
                            "appInstallData": "CJzN4ckGEJbbzxwQwKrQHBCu1s8cEImwzhwQovvPHBD8ss4cEMT0zxwQ4M2xBRC8s4ATEIv3zxwQ5ofQHBCd0LAFEL2u0BwQyPfPHBC36v4SEJTyzxwQvKTQHBDi1K4FEPKd0BwQsaLQHBC9tq4FEPKz0BwQppqwBRDm4M8cEIiHsAUQ47jPHBD2q7AFENG90BwQzdGxBRDLstAcEIKPzxwQvZmwBRDzs4ATENPhrwUQzN-uBRCRjP8SEJX3zxwQ5aTQHBCTg9AcELjkzhwQndfPHBCzkM8cEIOs0BwQudnOHBDevM4cEJT-sAUQ2vfOHBC72c4cENiW0BwQzrPQHBCJ6K4FEPC00BwQjOnPHBCZudAcEIeszhwQ2q7QHBDDqtAcEMvRsQUQg57QHBCsrNAcEPeJ0BwQj7nQHBC7rtAcEIeD0BwQlJmAExDBj9AcEIiT0BwQw5HQHBDM688cEIHNzhwQyfevBRC9irAFEJO20BwQjbDQHBCopdAcEJmNsQUQ0eDPHBD01c4cEJWv0BwQ-b6AExDildAcKnRDQU1TVVJWSy1acS1ETGlVRW9nQzlnU3FBb1BPNWd2d3NSS0hUREtnckFRRHk3NEYtam41Z2dhZ0JxSXVfQ2FtQV9GUHpnX3VYSUlQNmlmMkQ0VVU0aVB1blFXTUVKd3ZWTGN2NlJPZlM2dU41UjZkQnc9PTAA",
                            "coldConfigData": "CJzN4ckGEOy6rQUQxIWuBRC9tq4FEOLUrgUQvYqwBRCNzLAFEJ3QsAUQz9KwBRDM9rAFEOP4sAUQr6fOHBD8ss4cEPTVzhwQ47jPHBD4xs8cENrTzxwQndfPHBCf188cEMfazxwQsODPHBDP4M8cEOXnzxwQ5-fPHBCTg9AcEIiG0BwQ5ofQHBD3idAcEM2L0BwQ_pPQHBCTldAcEOKV0BwQqpzQHBC8pNAcELSo0BwQwKrQHBDDqtAcEJ2s0BwQzqzQHBC7rtAcEL2u0BwQjbDQHBCtstAcEMuy0BwQ8LTQHBCTttAcEJm50BwQzrnQHBD7utAcEJW70BwQn73QHBCuvdAcEMW90BwaMkFPakZveDBmMnVCVFhJaWxBLVpDWklyMWRLeUlOa3J3UXFKVzVUOVJhVlZfa0tVdXpBIjJBT2pGb3gzWGw2Mzk2MXhIYmhoR3cyeTBRcFk1WDNScFI5VjVfRElVaUdMVTdfOVhqUSqYAUNBTVNiQTB0dU4yM0FxUVpseC1mVDVtU21oRDdGbzAyX2lPbkRjZ0FyQXhxTkowV3FBU2hES2dDMlJldURhc1BGVG1ac2JjZmhhUUZrWndGNGRzQno4SUFqNmNHX2RRR01zLUFCZG1rQmdPaXNnWEtTd2F3YjRjRHhnbnpBNnFJQnBSU3lubkxTZ1NTdmdiS2RZMXNCUT09",
                            "coldHashData": "CJzN4ckGEhMxMTIwNzUxNjc2MDk1NDAyMzUxGJzN4ckGMjJBT2pGb3gwZjJ1QlRYSWlsQS1aQ1pJcjFkS3lJTmtyd1FxSlc1VDlSYVZWX2tLVXV6QToyQU9qRm94M1hsNjM5NjF4SGJoaEd3MnkwUXBZNVgzUnBSOVY1X0RJVWlHTFU3XzlYalFCRENBTVNMdzBXb3RmNkZhN0JCcE5Oc3hhbFJvSU55d1lWSGQzUHdnemk5Z19jcWVZTDJNMEo4NUFFc2FvVzZRNjNCdU16"
                        },
                        "screenDensityFloat": 1,
                        "userInterfaceTheme": "USER_INTERFACE_THEME_DARK",
                        "timeZone": "Europe/Berlin",
                        "browserName": "Opera",
                        "browserVersion": "124.0.0.0",
                        "acceptHeader": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                        "deviceExperimentId": "ChxOelU0TVRreU1qYzVNekF4TmpNM01ERTJOUT09EJzN4ckGGJzN4ckG",
                        "rolloutToken": "CKrC-PrFiJv-lAEQssHcioHCjQMY8ejh9vCwkQM=",
                        "screenWidthPoints": 1875,
                        "screenHeightPoints": 923,
                        "screenPixelDensity": 1,
                        "utcOffsetMinutes": 60,
                        "connectionType": "CONN_CELLULAR_4G",
                        "memoryTotalKbytes": "8000000",
                        "mainAppWebInfo": {
                            "graftUrl": self.url,
                            "pwaInstallabilityStatus": "PWA_INSTALLABILITY_STATUS_UNKNOWN",
                            "webDisplayMode": "WEB_DISPLAY_MODE_BROWSER",
                            "isWebNativeShareAvailable": True
                        },
                        "clientScreen": "ADUNIT"
                    }
                },
                "continuation": continuation_token
            }

            try:
                data_cont = self.core.make_api_request(api_url, payload_continuation)
                data_videos_list.append(data_cont)
                new_videos = len(self._find_videos(data_cont))
                loaded_videos += new_videos
                if new_videos == 0:
                    break
                continuation_token = self._find_continuation_token(data_cont)
            except Exception:
                break

        # Collect all videos
        all_videos = []
        for data in data_videos_list:
            all_videos.extend(self._find_videos(data))

        # Limit videos if max_videos is not 'all'
        if max_videos != 'all' and isinstance(max_videos, int):
            all_videos = all_videos[:max_videos]

        self.data['videos'] = all_videos
        self.data['loaded_videos_count'] = len(all_videos)

    def _find_videos(self, obj):
        """Find videos in the data structure."""
        videos = []
        if isinstance(obj, dict):
            # Initial videos
            if 'richGridRenderer' in obj and 'contents' in obj['richGridRenderer']:
                for item in obj['richGridRenderer']['contents']:
                    if 'richItemRenderer' in item and 'content' in item['richItemRenderer']:
                        content = item['richItemRenderer']['content']
                        if 'videoRenderer' in content:
                            vr = content['videoRenderer']
                            video = {
                                'videoId': vr.get('videoId'),
                                'title': vr.get('title', {}).get('runs', [{}])[0].get('text', ''),
                                'publishedTimeText': vr.get('publishedTimeText', {}).get('simpleText', ''),
                                'viewCountText': vr.get('viewCountText', {}).get('simpleText', ''),
                                'lengthText': vr.get('lengthText', {}).get('simpleText', ''),
                                'thumbnails': vr.get('thumbnail', {}).get('thumbnails', [])
                            }
                            videos.append(video)
                        elif 'gridVideoRenderer' in content:
                            gvr = content['gridVideoRenderer']
                            video = {
                                'videoId': gvr.get('videoId'),
                                'title': gvr.get('title', {}).get('simpleText', ''),
                                'publishedTimeText': gvr.get('publishedTimeText', {}).get('simpleText', ''),
                                'viewCountText': gvr.get('viewCountText', {}).get('simpleText', ''),
                                'lengthText': gvr.get('thumbnailOverlays', [{}])[0].get('thumbnailOverlayTimeStatusRenderer', {}).get('text', {}).get('simpleText', ''),
                                'thumbnails': gvr.get('thumbnail', {}).get('thumbnails', [])
                            }
                            videos.append(video)
            # Continuation videos
            if 'onResponseReceivedActions' in obj:
                for action in obj['onResponseReceivedActions']:
                    if 'appendContinuationItemsAction' in action:
                        for item in action['appendContinuationItemsAction']['continuationItems']:
                            if 'richItemRenderer' in item and 'content' in item['richItemRenderer']:
                                content = item['richItemRenderer']['content']
                                if 'videoRenderer' in content:
                                    vr = content['videoRenderer']
                                    video = {
                                        'videoId': vr.get('videoId'),
                                        'title': vr.get('title', {}).get('runs', [{}])[0].get('text', ''),
                                        'publishedTimeText': vr.get('publishedTimeText', {}).get('simpleText', ''),
                                        'viewCountText': vr.get('viewCountText', {}).get('simpleText', ''),
                                        'lengthText': vr.get('lengthText', {}).get('simpleText', ''),
                                        'thumbnails': vr.get('thumbnail', {}).get('thumbnails', [])
                                    }
                                    videos.append(video)
                                elif 'gridVideoRenderer' in content:
                                    gvr = content['gridVideoRenderer']
                                    video = {
                                        'videoId': gvr.get('videoId'),
                                        'title': gvr.get('title', {}).get('simpleText', ''),
                                        'publishedTimeText': gvr.get('publishedTimeText', {}).get('simpleText', ''),
                                        'viewCountText': gvr.get('viewCountText', {}).get('simpleText', ''),
                                        'lengthText': gvr.get('thumbnailOverlays', [{}])[0].get('thumbnailOverlayTimeStatusRenderer', {}).get('text', {}).get('simpleText', ''),
                                        'thumbnails': gvr.get('thumbnail', {}).get('thumbnails', [])
                                    }
                                    videos.append(video)
            for v in obj.values():
                videos.extend(self._find_videos(v))
        elif isinstance(obj, list):
            for item in obj:
                videos.extend(self._find_videos(item))
        return videos

    def _find_continuation_token(self, obj):
        """Find continuation token in the data structure."""
        if isinstance(obj, dict):
            # Initial structure
            if 'continuationItemRenderer' in obj:
                cir = obj['continuationItemRenderer']
                if 'continuationEndpoint' in cir:
                    endpoint = cir['continuationEndpoint']
                    if isinstance(endpoint, dict) and 'continuationCommand' in endpoint:
                        cmd = endpoint['continuationCommand']
                        if 'token' in cmd:
                            return cmd['token']
            # Continuation structure
            if 'onResponseReceivedActions' in obj:
                for action in obj['onResponseReceivedActions']:
                    if 'appendContinuationItemsAction' in action:
                        for item in action['appendContinuationItemsAction']['continuationItems']:
                            if 'continuationItemRenderer' in item:
                                cir = item['continuationItemRenderer']
                                if 'continuationEndpoint' in cir:
                                    endpoint = cir['continuationEndpoint']
                                    if isinstance(endpoint, dict) and 'continuationCommand' in endpoint:
                                        cmd = endpoint['continuationCommand']
                                        if 'token' in cmd:
                                            return cmd['token']
            for v in obj.values():
                token = self._find_continuation_token(v)
                if token:
                    return token
        elif isinstance(obj, list):
            for item in obj:
                token = self._find_continuation_token(item)
                if token:
                    return token
        return None

    def _extract_numbers(self):
        """Extract numerical values from text fields."""
        if 'subscriberCountText' in self.data:
            self.data['subscribers'] = utils.extract_number(self.data['subscriberCountText'])
        if 'viewCountText' in self.data:
            self.data['total_views'] = utils.extract_number(self.data['viewCountText'])
        if 'videoCountText' in self.data:
            self.data['video_count'] = utils.extract_number(self.data['videoCountText'])