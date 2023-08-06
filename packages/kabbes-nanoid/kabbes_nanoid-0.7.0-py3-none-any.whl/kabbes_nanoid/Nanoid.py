from parent_class import ParentClass
import random

class Nanoid( ParentClass ):

    _IMP_ATTS = ['nanoid','size','alphabet']
    _ONE_LINE_ATTS = ['type','nanoid']

    def __init__( self, alphabet='-_1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', size=21 ):

        """Initializes the class with default attributes"""

        ParentClass.__init__( self )

        self.alphabet = alphabet
        self.size = size
        self.nanoid = None

        #Generate the NanoID string
        self.generate()

    def __str__( self ):
        return self.nanoid

    def generate( self ):

        """Generates a Nanoid from stored 'size' and 'alphabet' attributes, stores in 'nanoid' attribute """

        string = ''
        for i in range(self.size):
            string += ( random.choice( self.alphabet ) )

        self.nanoid = string
