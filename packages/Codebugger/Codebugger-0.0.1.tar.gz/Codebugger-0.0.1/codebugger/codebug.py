"""
This module implements the main functionality of Codebugger.

Author: Gabriel Cha 
"""

__author__ = "Gabriel Cha"
__email__ = "gcha@ucsd.edu"
__status__ = "planning"

import linecache
import openai
import sys

class Codebug:
    """
    Class for debug explanation.

    Attributes 
    ---------- 

    error_message: str
        Error message.

    Methods
    ----------

    getMessage: Get the original error message. 
    explnation: Openai api call to explain error message in simple terms.
    suggestive: Openai api call to suggest ways to fix error.

    """

    def __init__(self):
        """
        Creates new instance of gpt debug explnation. 
        
        Parameters
        ----------
        error_message: str
            Error message.

        """
        self.error_message = "No errors found!"
       
    def setError(self):
        """
        Retrieves the representation of the handled exception
        
        Parameters
        ----------
        exc_type : Exception type.
        exc_obj : Object causing the exception, can be None.
        tb : Traceback objects represent a stack trace of an exception.

        """
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        
        # Exception description
        self.error_message = 'ERROR {} IN LINE {}: "{}": {}'.format(exc_type, lineno, line.strip(), exc_obj)

    def setAPI(self, api):
        """
        Sets the user's openai api
        """
        openai.api_key = api

    def getMessage(self):
        """
        Gets cause of error
        """
        return self.error_message

    def explnation(self):
        """
        Retrieves explnation of error message from openapi gpt.
        """
        # Configure openai key
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": 'Explain this error message:' + self.error_message}
            ]
            )
        return completion.choices[0].message['content']
    
    def suggestive(self):
        """
        Retrieves suggestions to fix error from openapi gpt.
        """
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": 'Explain this error message and suggest ways to fix the error:' + self.error_message}
            ]
            )
        return completion.choices[0].message['content']
