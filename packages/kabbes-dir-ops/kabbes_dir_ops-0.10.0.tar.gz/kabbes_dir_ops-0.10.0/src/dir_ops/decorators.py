import functools
import dir_ops as do
import py_starter as ps

def base_instance_method(method):

    """instance methods call the corresponding staticmethod 
    Example: Dir_instance.exists(*,**) calls Dir.exists_dir( Dir_instance.path,*,** )   
    """

    @functools.wraps(method)
    def wrapper( self, *called_args, **called_kwargs):

        new_method_name = method.__name__ + self.STATIC_METHOD_SUFFIX
        return self.get_attr( new_method_name )( self.path, *called_args, **called_kwargs )
        
    return wrapper

def inherited_instance_method(method):

    """instance methods call the corresponding staticmethod 
    Example: Dir_instance.exists(*,**) calls Dir.exists_dir( Dir_instance.path,*,** )   """

    @functools.wraps(method)
    def wrapper( self, *called_args, **called_kwargs):

        new_method_name = method.__name__ + self.STATIC_METHOD_SUFFIX
        instance_args = [ self.get_attr( attr ) for attr in self.INSTANCE_METHOD_ATTS ]

        return self.get_attr( new_method_name )( *instance_args, *called_args, **called_kwargs )
      
    return wrapper

def dirs_wrap( method_name, track_success = False ):

    def dirs_gen( method ):

        @functools.wraps( method )
        def wrapper( self, *args, **kwargs ):

            valid = True
            for DirPath in self:
                value = DirPath.get_attr( method_name )( *args, **kwargs )

                if value == False:
                    valid = False

            if track_success:
                return valid

        return wrapper

    return dirs_gen
  

###

def to_from_wrapper_factory( method, action_str, self, *args, **kwargs  ):

    default_kwargs = {

        'override': False, #bool
        'print_off': False, #bool
        'Destination': None, 
        'destination': '', 
        'overwrite': False #bool
    }

    joined_kwargs = ps.merge_dicts( default_kwargs, kwargs )

    if joined_kwargs['Destination'] == None:
        if self.type_path:
            joined_kwargs['Destination'] = do.Path( joined_kwargs['destination'] )
        if self.type_dir:
            joined_kwargs['Destination'] = do.Dir( joined_kwargs['destination'] )


    ######  Insert special instructions
    if action_str == 'download' or action_str == 'copy' or action_str == 'rename':
        joined_kwargs['Destination'].create_parents( **joined_kwargs )
    
    ######
    if not joined_kwargs['override']:
        do.print_to_from( True, action_str, str(self), str(joined_kwargs['Destination']) )
        joined_kwargs['override'] = ps.confirm_raw( string = '' )

    if joined_kwargs['override']:
        ###### Check for conflicting destination locations
        if action_str == 'download' or action_str == 'copy' or action_str == 'rename':
            if self.exists() and joined_kwargs['Destination'].exists():
                if not joined_kwargs['overwrite']:
                    print ('ERROR: Destination ' +str(joined_kwargs['Destination'])+ ' already exists. Pass "overwrite=True" to overwrite existing file.')
                    return False
                else:
                    joined_kwargs['Destination'].remove( override = True )

        # perform the actual method        
        do.print_to_from( joined_kwargs['print_off'], action_str, str(self), str(joined_kwargs['Destination']) )

        if method( self, *args, destination = joined_kwargs['Destination'].path, override=joined_kwargs['override'], print_off=joined_kwargs['print_off'] ):
            return True
        else:
            do.print_to_from( True, action_str, str(self), str(joined_kwargs['Destination']) )
            print ('ERROR: could not complete ' + action_str)

    return False



def download_wrap( method ):

    @functools.wraps( method )
    def wrapper( self, *args, **kwargs ):
        return to_from_wrapper_factory( method, 'download', self, *args, **kwargs )

    return wrapper

def upload_wrap( method ):

    @functools.wraps( method )
    def wrapper( self, *args, **kwargs ):
        return to_from_wrapper_factory( method, 'upload', self, *args, **kwargs )

    return wrapper

def copy_wrap( method ):

    @functools.wraps( method )
    def wrapper( self, *args, **kwargs ):
        return to_from_wrapper_factory( method, 'copy', self, *args, **kwargs )

    return wrapper

def rename_wrap( method ):

    @functools.wraps( method )
    def wrapper( self, *args, **kwargs ):
        return to_from_wrapper_factory( method, 'rename', self, *args, **kwargs )

    return wrapper


def remove_wrap( method ):

    @functools.wraps( method )
    def wrapper( self, *args, **kwargs ):
        return to_from_wrapper_factory( method, 'remove', self, *args, **kwargs )

    return wrapper


def create_wrap( method ):

    @functools.wraps( method )
    def wrapper( self, *args, **kwargs ):
        return to_from_wrapper_factory( method, 'create', self, *args, **kwargs )

    return wrapper


###

def get_size_wrap( method ):

    @functools.wraps( method )
    def wrapper( self, *args, conversion=None, **kwargs ):

        size_bytes = method( self, *args, conversion=None, **kwargs )
        
        size, size_units = do.convert_bytes( size_bytes, conversion=conversion )
        self.size = size
        self.size_units = size_units

        return size, size_units

    return wrapper

def get_mtime_wrap( method ):

    @functools.wraps( method )
    def wrapper( self, *args, **kwargs ):

        mtime = method( self, *args, **kwargs )
        self.mtime = mtime

        return mtime

    return wrapper

