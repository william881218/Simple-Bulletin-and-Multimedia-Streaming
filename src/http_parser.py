class HTTPParser(object):
    '''
    Handle http parsing
    '''

    def __init__(self):

        self.status = 'HTTP/1.1 200 OK\r\n'

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

        self.response_headers['Content-Length'] = len(text.encode())

        response_header_raw = ''.join([
            "{}: {}\r\n".format(header, value) 
                for header, value in self.response_headers.items()
        ])

        output = self.status + response_header_raw + '\r\n' + text

        return output


    @staticmethod
    def get_content_len(raw_text):
        '''
        Return the length of the context in HTTP body
        '''
        raw_text = raw_text.split('\n')
        for line in raw_text:
            if line.startswith('Content-Length'):
                return int(line.split()[1].strip('\r'))
        return None


    @staticmethod
    def get_context(raw_text):
        '''
        Return the context in HTTP response
        '''
        raw_text = raw_text.split('\n')
        context = []
        for line in raw_text:
            context.append(line)
            if line == '\r':
                context.clear()
        return ''.join(context)