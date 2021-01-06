class HTMLParser(object):

    def __init__(self, template):
        self.template_path = template
        
        # read the template file
        with open(self.template_path, 'r') as f:
            self.template = f.readlines()

        self.documents = [] # list of str, each entry representing an article

    
    def extract_body(self, raw_text):
        '''
        Given a http raw text, return text between <body> and </body>
        '''
        return raw_text


    def update_documents(self, http_text):
        '''
        Given a http raw text, extract the body part of the html and add it into document list
        '''
        # self.documents.append(self._parse_body(http_text))
        pass


    def generate_response(self):
        '''
        Replace VARIABLE in template html with documents and return the output
        '''
        output = ''

        for line in self.template:

            if line != 'VARIABLES\n':
                output += line
            else: # replace `FROM_DATABASE\n` with custumized data in template html file
                output += ''.join(self.documents)

        return output
    