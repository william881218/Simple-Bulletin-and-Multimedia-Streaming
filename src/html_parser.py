class HTMLParser(object):

    def __init__(self, template):
        self.template_path = template
        
        # read the template file
        with open(self.template_path, 'r') as f:
            self.template = f.readlines()


    def extract_body(self, raw_text):
        '''
        Given a http raw text, return text between <body> and </body>
        '''
        return raw_text


    def generate_response(self, documents_list):
        '''
        Replace VARIABLE in template html with documents in `documents_list` and return the output

        Args:
            documents_list (list of str) : list of path to document files
        '''
        output = ''

        for line in self.template:

            if line != 'VARIABLES\n':
                output += line
            else: # replace `FROM_DATABASE\n` with custumized data in template html file
                for document_path in documents_list:
                    with open(document_path, 'r') as f:
                        # we handle each post here
                        context_list = f.readlines()
                        output += ''.join(context_list) + '\n'
                        output += '<hr>'

        return output
    