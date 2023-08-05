from parent_class import ParentPlural
from typing import List

class ParentPluralList( ParentPlural ):

    def __init__( self, att = 'list' ):

        ParentPlural.__init__( self, att = att )
        self.set_attr( self.att, [] )

    def __iter__( self ):

        self.i = -1
        return self
        
    def __len__( self ):

        return len(self.get_list())

    def __next__( self ):

        self.i += 1

        if self.i >= len(self):
            raise StopIteration
        else:
            return self.get_list()[ self.i ]

    def _add( self, value ):

        list = self.get_list()
        list.append( value )
        self.set_list( list )

    def _remove( self, Inst, all_occurences = False ) -> bool:

        """remove the Inst from the class List"""

        removed = False        

        inds = []        
        Insts = list(self)
        for i in range(len(self)):
                      
            if Insts[i] == Inst:
                inds.append(i)
                removed = True

                if not all_occurences:
                    break
        
        self._remove_inds( inds )
        return removed

    def _remove_inds( self, inds: List[int] ):
        
        """Given a list of indices, remove the Objects at those indicies from the class List"""

        list = self.get_list()

        inds.sort( reverse=True )
        for ind in inds:
            del list[ind]

        self.set_list( list )

    def set_list( self, list ):

        self.set_attr( self.att, list )

    def get_list( self ):

        return self.get_attr( self.att )


if __name__ == '__main__':
    a = ParentPluralList()
    a.print_atts()