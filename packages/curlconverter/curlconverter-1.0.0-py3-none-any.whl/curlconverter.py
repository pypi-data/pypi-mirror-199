import re
import shlex

class CurlConverter:
    def __init__(self, curl_command):
        self.curl_command = curl_command

    def convert(self):
        parsed = shlex.split(self.curl_command)
        method = parsed[0]
        url = parsed[1]
        headers = {}
        data = None

        for i in range(2, len(parsed)):
            if parsed[i] == "-H":
                headers[parsed[i+1].replace("'", "")] = parsed[i+2].replace("'", "")
            elif parsed[i] == "--compressed":
                continue
            else:
                data = parsed[i]

        return {'method': method, 'url': url, 'headers': headers, 'data': data}
