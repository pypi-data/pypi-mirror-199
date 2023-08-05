from parent_class import ParentPlural

class ParentPluralDict( ParentPlural ):

    def __init__( self, att = 'dict' ):

        ParentPlural.__init__( self, att = att )
        self.set_attr( self.att, {} )

    def __len__( self ):

        return len(self.get_dict())

    def __next__( self ):

        self.i += 1

        if self.i >= len(self):
            raise StopIteration
        else:
            return self.get_dict()[ list(self.get_dict().keys())[self.i] ]

    def _add( self, key, value ):

        dict = self.get_dict()
        dict[key] = value
        self.set_dict( dict )

    def _remove( self, key ) -> bool:

        dict = self.get_dict()

        if key in dict:
            del dict[key]
            return True
        
        else:
            return False

    def set_dict( self, dict ):

        self.set_attr( self.att, dict )

    def get_dict( self ):

        return self.get_attr( self.att )

if __name__ == '__main__':
    a = ParentPluralDict()
    a.print_atts()