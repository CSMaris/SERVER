from requests import request, RequestException


def send(method='GET', url=None, data=None, headers={}, auth=None):
    # the response dictionary, initially empty
    response_dict = dict()

    # check that the URL is not empty
    if url is not None:
        # try to call the URL
        result = None
        try:
            # get the result
            if auth is not None:
                # HTTP Basic Auth is needed
                result = request(method, url, data=data, headers=headers, auth=auth)

            else:
                # without HTTP Basic Auth
                result = request(method, url, data=data, headers=headers)

        except RequestException as e:
            # print the error
            print(e)

        # check result
        if result is not None:
            # consider the response content as JSON and put it in the dictionary
            try:
                response_dict = result.json()
            except ValueError as ve:
                # no JSON, return the plain result
                response_dict = result

    return response_dict
