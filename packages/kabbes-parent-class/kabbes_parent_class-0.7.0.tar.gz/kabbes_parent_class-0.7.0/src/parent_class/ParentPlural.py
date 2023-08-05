from parent_class import ParentClass
import py_starter as ps
import random

class ParentPlural( ParentClass ):

    DEFAULT_KWARGS = {
        'MAX_PRINT_ATTS': 10
    }

    def __init__( self, att = None, **kwargs ):

        ParentClass.__init__( self )
        joined_kwargs = ps.merge_dicts( ParentPlural.DEFAULT_KWARGS, kwargs )
        self.set_atts( ParentPlural.DEFAULT_KWARGS )

        if att == None:
            att = self.type

        self.att = att

    def __contains__( self, Obj_to_check ) -> bool:

        for Obj in self:
            if Obj == Obj_to_check:
                return True
        return False

    def __iter__( self ):

        self.i = -1
        return self

    def print_imp_atts( self, print_off = True, max_print_atts: int = -1 ):
        
        if max_print_atts == -1:
            max_print_atts = self.MAX_PRINT_ATTS

        string = self.print_class_type( print_off = False ) + '\n'
        string += (self.att + '\n')

        Insts = list(self)
        inds = []
        if len(Insts) != 0:
            inds = list(range( min( len(Insts)-1, max_print_atts-1) ))
            inds.append( len(Insts) -1 )

        for i in inds:
            Inst = Insts[i]
            string += ( str(i+1) + '. ' + Inst.print_one_line_atts( print_off = False ) ) + '\n'

        if len(self._IMP_ATTS) > 0:
            string += self._print_imp_atts_helper( atts = self._IMP_ATTS, show_class_type = False, print_off = False )
        else:
            string = string[:-1]

        return self.print_string( string, print_off = print_off )

    def print_one_line_atts( self, print_off = True, leading_string = '\t' ):
        
        string = leading_string + 'len_' + self.att + ': ' + str(len(self))

        if len(self._ONE_LINE_ATTS) > 0:
            string += ','
            string += self._print_one_line_atts_helper( atts = self._ONE_LINE_ATTS, print_off=False )

        return self.print_string( string, print_off = print_off )

    def get_random( self ):

        Insts = list(self)
        if len(Insts) > 0:
            return Insts[ random.randrange(len(Insts)) ]
        else:
            return None

    def user_select( self ):

        return ps.get_selection_from_list( self )

    def user_select_multiple( self ):

        return ps.get_user_selection_for_list_items( self )


if __name__ == '__main__':
    a = ParentPlural()
    a.print_atts()