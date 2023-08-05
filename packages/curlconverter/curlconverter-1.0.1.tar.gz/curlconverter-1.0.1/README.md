Here's an example of how to use the curlconverter library:

from curlconverter import CurlConverter

# Example cURL command string
curl_string = 'curl \'https://api.example.com\' -H \'Content-Type: application/json\' -d \'{"foo": "bar"}\''

# Create an instance of CurlConverter with the cURL string
curl_converter = CurlConverter(curl_string)

# Convert the cURL string to a dictionary
parsed_data = curl_converter.convert()

# Print the parsed data
print(parsed_data)


Output:
{'method': 'GET', 'url': 'https://api.example.com', 'headers': {'Content-Type': 'application/json'}, 'data': '{"foo": "bar"}'}


In this example, we create an instance of CurlConverter with a cURL command string that makes a GET request to https://api.example.com with a Content-Type header and a JSON payload. We then call the convert() method on the instance to parse the cURL string and return a dictionary with the parsed data. Finally, we print the parsed data to the console.