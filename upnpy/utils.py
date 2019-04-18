def parse_http_header(header, header_key):

    """

    Parse HTTP header value

    :param header: String containing HTTP headers
    :type header: str
    :param header_key: The header of which to extract a value from
    :type header_key: str
    :return: Header value
    :rtype: str

    """

    split_headers = header.split('\r\n')

    for entry in split_headers:
        header = entry.strip().split(':', 1)

        if header[0].strip().lower() == header_key.strip().lower():
            return ''.join(header[1::]).split()[0]
