import asyncio
import json
import logging
import socket
import ssl
import time
import urllib.parse
from typing import List, Dict

class Yumikogram:
    def __init__(self, bot_token: str, api_id: int, api_hash: str):
        self.bot_token = bot_token
        self.api_id = api_id
        self.api_hash = api_hash
        self.server = 'api.telegram.org'
        self.port = 443
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        self.last_update_id = None

    async def send_message(self, chat_id: int, text: str, **kwargs) -> Dict:
        url = f'https://{self.server}:{self.port}/bot{self.bot_token}/sendMessage'
        data = {'chat_id': chat_id, 'text': text}
        data.update(kwargs)
        response = await self._send_request(url, data)
        return response.get('result', {})

    async def get_updates(self, **kwargs) -> List[Dict]:
        url = f'https://{self.server}:{self.port}/bot{self.bot_token}/getUpdates'
        data = {'timeout': 60}
        if self.last_update_id:
            data['offset'] = self.last_update_id + 1
        data.update(kwargs)
        response = await self._send_request(url, data)
        updates = response.get('result', [])
        for update in updates:
            self.last_update_id = update['update_id']
        return updates

    async def _send_request(self, url: str, data: Dict) -> Dict:
        encoded_data = urllib.parse.urlencode(data).encode('utf-8')
        request = f'POST {url} HTTP/1.1\r\nHost: {self.server}\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {len(encoded_data)}\r\n\r\n{encoded_data.decode("utf-8")}'
        with socket.create_connection((self.server, self.port)) as sock:
            with self.ssl_context.wrap_socket(sock, server_hostname=self.server) as ssl_sock:
                ssl_sock.sendall(request.encode())
                response = b''
                while True:
                    chunk = ssl_sock.recv(4096)
                    if not chunk:
                        break
                    response += chunk
                response = response.decode('utf-8')
                response_headers, response_body = response.split('\r\n\r\n', 1)
                response_headers_dict = {}
                for header in response_headers.split('\r\n')[1:]:
                    name, value = header.split(': ', 1)
                    response_headers_dict[name] = value
                response_data = json.loads(response_body)
                if response_headers_dict.get('Content-Type', '').startswith('application/json'):
                    if not response_data.get('ok', False):
                        logging.error(response_data.get('description', ''))
                    return response_data
                else:
                    logging.error(f'Invalid response: {response_headers_dict.get("Content-Type", "")}')
        return {}

