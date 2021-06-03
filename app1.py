
from flask import Flask, request, render_template, Response
import logging

#Initiating the Flask application object
app = Flask(__name__)

#Initiating the log object for logging
logging.basicConfig(filename = './app.log', level=logging.DEBUG
                   , format = f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

#Default APIs to which the user gets redirected if the API doesn't exists 
@app.route('/')
@app.route('/<filename>/<start_line>/<last_line>')
@app.route('/<filename>/<start_line>')
def default_page(filename=None,start_line=None,last_line=None):
    """
    Description : Used to fetch the content of the given file from start line number to last line number
    params :
        filename : string
        start_line : integer(Optional)
        last_line : integer(Optional)
    Returns the content of the file as requested 
    """
    #Logging the parameters of the users request
    logging.info('The parameters of the users request for default page are : filename : {}, start_line : {}, last_line : {}'.format(filename, start_line, last_line))
    #Redirecting the user to the default page
    message = 'Please re check the end point mentioned in the url'
    return render_template('error1.html',value=message)


#REST API to access the content of the file name from start and end line numbers
@app.route('/<filename>/<int:start_line>/<int:last_line>', methods = ['GET'])
def get_file_content_with_line_number(filename='TextFile1.txt', start_line = None, last_line=None):
    """
    Description : Used to fetch the content of the given file from start line number to last line number
    params :
        filename : string
        start_line : integer(Optional)
        last_line : integer(Optional)
    Returns the content of the file as requested 
    """
    #Logging the parameters of the users request
    logging.info('The parameters of the users request for get_file_content_with_line_number are : filename : {}, start_line : {}, last_line : {}'.format(filename, start_line, last_line))
    
    #Checking if the request method is GET or not
    if request.method == 'GET':
        message = None
        try:
            #Opening the file to fetch its content as per users request
            with open(filename,'r',encoding = 'utf-8') as f:
                content = f.readlines()
                #Validating start_line and last_line param values
                if (start_line != None and 0 <= start_line <= len(content)) and (last_line != None and 0 <= last_line <= len(content)):
                    content = content[start_line:last_line+1]
                    #Returing the content of the file to the HTML page
                    return Response(content, mimetype='text/plain')
                else:
                    logging.warning('Unable to fetch the content of the file as the start line and last line are not valid') 
                    #Raising an Exception if the start line and last line values are invalid
                    message = 'Please re-check the starting and ending line numbers of the file'
                    raise Exception
        except Exception as e:
            #Logging the error the log file for reference
            logging.warning('The API is aborted with the exception : {}'.format(repr(e)))
            #Redirecting the user to the error page
            if message == None:
                message = 'Please re check the file name mentioned in the url'
            return render_template('error1.html',value=message)
           
#REST API to access the content of the file
@app.route('/<filename>', methods = ['GET'])
def get_file_content(filename='TextFile1.txt'):
    """
    Description : Used to fetch the content of the given file
    params :
        filename : string
    Returns the content of the file as requested 
    """
    #Logging the params of the users request
    logging.info('The parameters of the users request for get_file_content are : filename : {}'.format(filename))
    
    #Checking if the users request method is GET or not
    if request.method == 'GET':
        try:
            #Opening the file to fetch its content as the users request
            with open(filename,'r',encoding = 'utf-8') as f:
                content = f.readlines()
                #Returning the conetent of the file as per users request
                return Response(content, mimetype='text/plain')
        except Exception as e:
            #Logging the exception raised for reference
            logging.warning('The API is aborted with the exception : {}'.format(repr(e)))
            #Redirecting to the error page
            message = 'Please re-check the file name mentioned in the url.'
            return render_template('error1.html',value=message)
 
            

if __name__ == '__main__':
    # Running the app server on localhost:4449
    app.run('localhost', 4449, debug = True)