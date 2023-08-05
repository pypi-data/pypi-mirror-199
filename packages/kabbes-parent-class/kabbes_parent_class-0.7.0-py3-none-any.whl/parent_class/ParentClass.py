import py_starter as ps
from typing import List, Any

class ParentClass:

    _IMP_ATTS = ['type']
    _ONE_LINE_ATTS = ['type']

    def __init__( self, class_type = '' ):

        if class_type == '':
            #<class '__main__.A'>
            object_type = str(type(self))
            class_type = object_type.split('.')[-1].split( "'" )[0]

        self.type = class_type

    def __str__( self ) -> str:

        """when str(self) is executed, the returned string will be printed off"""

        return self.print_one_line_atts( leading_string = '', print_off = False )

    def print_atts( self, how: str = 'imp', **kwargs ):

        """Print attributes of the class off, if not printed off, the string will be returned"""

        if how == 'one_line' or how == 1: #print the one line atts
            return self.print_one_line_atts( **kwargs )

        elif how == 'imp' or how == 2: #print the important atts
            return self.print_imp_atts( **kwargs )

        elif how == 'all' or how == 3 : #print all atts
            return self.print_all_atts( **kwargs )

    def print_all_atts( self, **override_kwargs ):

        """Print off all Class instance attributes"""

        default_kwargs = {
        'atts': list(vars(self))
        }
        kwargs = ps.merge_dicts( default_kwargs, override_kwargs )
        return self._print_imp_atts_helper( **kwargs )

    def print_imp_atts( self, **override_kwargs ):

        """Prints off (or returns a string) with the 'important' information about a class
        Most child classes will redefine this method with custom attributes to print off"""

        default_kwargs = {
        'atts': self._IMP_ATTS
        }
        kwargs = ps.merge_dicts( default_kwargs, override_kwargs )

        return self._print_imp_atts_helper( **kwargs )

    def _print_imp_atts_helper( self, **override_kwargs ):

        """A helper function for creating quick print_imp_atts functions"""

        default_kwargs = {
        'atts': ['type'],
        'show_class_type': True,
        }

        kwargs = ps.merge_dicts( default_kwargs, override_kwargs )
        return self._print_atts_helper( **kwargs )

    def print_one_line_atts( self, **override_kwargs ):

        """Prints off (or returns a string) with information about a class in one line
        Most child classes will redefine this method with custom attributes to print off"""

        default_kwargs = {
            'atts': self._ONE_LINE_ATTS,
        }

        kwargs = ps.merge_dicts( default_kwargs, override_kwargs )
        return self._print_one_line_atts_helper( **kwargs )

    def _print_one_line_atts_helper( self, **override_kwargs ):

        default_kwargs = {
        'atts': ['type'],
        'show_class_type': False,
        'leading_string': ' ',
        'att_sep': ', ',
        }

        kwargs = ps.merge_dicts( default_kwargs, override_kwargs )
        return self._print_atts_helper( **kwargs )

    def print_class_type( self, print_off: bool = True ):

        """Shows information about what type of class self is"""

        class_type_str = '---' + self.type + ' Class---'
        return self.print_string( class_type_str, print_off = print_off )

    def print_string( self, string: str, print_off: bool = True ) -> Any:

        """Function does one of two things
        1. Prints off the string and returns NOne
        2. Returns the string
        """

        if print_off:
            print(string)
            return None
        else:
            return string

    def _print_atts_helper( self, **override_kwargs ):

        """Main helper function for printing off information about the class"""

        default_kwargs = {
        'atts': [],
        'display_names': [],
        'atts_and_display_names': {},
        'override_string': '',
        'leading_string': '',
        'att_sep': '\n',
        'show_class_type': False,
        'print_off': True
        }

        kwargs = ps.merge_dicts( default_kwargs, override_kwargs )

        atts_str = ''
        if kwargs['show_class_type']:
            atts_str += self.print_class_type( print_off = False ) + '\n'

        atts_str += kwargs['leading_string']

        if kwargs['override_string'] != '':
            atts_str += kwargs['override_string']

        else:
            # use the dictionary as priority if given
            if kwargs['atts_and_display_names'] != {}:
                kwargs['atts'] = []
                display_names = []

                for att in kwargs['atts_and_display_names']:
                    kwargs['atts'].append(att)
                    display_names.append( kwargs['atts_and_display_names'][att] )

            #loop through each attribute and show the attribute and the
            for i in range(len(kwargs['atts'])):
                att = kwargs['atts'][i]

                if len(kwargs['display_names']) > i:
                    display_name = kwargs['display_names'][i]
                else:
                    display_name = att

                value = self.get_attr( att )

                if hasattr( value, 'print_one_line_atts' ):
                    try:
                        atts_str += ( str(display_name) + ': ' + value.print_one_line_atts(print_off = False, leading_string = '') )
                    except:
                        atts_str += ( str(display_name) + ': ' + str(value) )
                else:
                    atts_str += ( str(display_name) + ': ' + str(value) )

                if (i+1) < len(kwargs['atts']):
                    atts_str += kwargs['att_sep']

        return self.print_string( atts_str, print_off = kwargs['print_off'] )

    def has_attr( self, att: str ) -> bool:

        """returns True/False whether the instance has the attribute"""

        return hasattr( self, att )

    def has_atts( self, atts: List[str] ) -> List[bool]:

        """returns a list of True/False indicating whether the class has each attribute"""

        return [ self.has_attr(att) for att in atts ]

    def set_attr( self, att: str, val: Any ) -> None:

        """sets self.att = val"""

        setattr( self, att, val )

    def set_atts( self, dictionary: dict ) -> None:

        """sets attributes of the class equal to the dictionary values"""

        for key in dictionary:
            self.set_attr( key, dictionary[key] )

    def get_attr( self, att_string: str ) -> Any:

        """returns self.<att_string>"""

        return getattr( self, att_string )

    def get_atts( self, atts: str ) -> List[Any]:

        """returns all values of atts for class instance"""

        return [ self.get_attr(att) for att in atts ]

    def run_method( self, method_name, *method_args, **method_kwargs ):

        """runs method_name associated with self and given *args and **kwargs,
        returns whatever the method_pointer returns"""

        method_pointer = getattr( self, method_name )
        return method_pointer( *method_args, **method_kwargs )

    def format_string_by_atts( self, string, **kwargs ) -> str:

        triggers_plus_atts = ps.find_string_formatting( string, **kwargs )
        atts = [ ps.strip_trigger( trigger_plus_att, **kwargs ) for trigger_plus_att in triggers_plus_atts ]

        formatting_dict = {}
        for att in atts:
            formatting_dict[ att ] = self.get_attr( att )

        formatted_string = ps.smart_format( string, formatting_dict, **kwargs )
        return formatted_string



if __name__ == '__main__':
    a = ParentClass()
    a.print_atts()