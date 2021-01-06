class HTTPParser(object):
    '''
    Handle http parsing
    '''

    def __init__(self):

        self.status = 'HTTP/1.1 200 OK\n'

        # header content
        self.response_headers = {
            'Content-Type': 'text/html; encoding=utf8', 
            'Connection': 'keep-alive',
        }


    @staticmethod
    def get_method(raw_text):
        '''
        Check which http type `raw_text` is. 
        '''
        method_line = raw_text.split('\n')[0].split()
        assert len(method_line) == 3
        assert method_line[2] == 'HTTP/1.1'

        http_method, url = method_line[0], method_line[1]
        return http_method, url


    def parse(self, text):
        '''
        Given `text` as context of http response, return the full http response (including header).
        '''

        self.response_headers['Content-Length'] = len(text)

        response_header_raw = ''.join([
            "{}: {}\n".format(header, value) 
                for header, value in self.response_headers.items()
        ])

        output = self.status + response_header_raw + '\n' + text

        return output