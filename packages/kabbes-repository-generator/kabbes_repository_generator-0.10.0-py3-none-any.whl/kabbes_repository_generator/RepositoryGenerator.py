import dir_ops as do
import py_starter as ps
from parent_class import ParentClass

class RepositoryGenerator( ParentClass ):

    TRIGGER_BEG = '{-{'
    TRIGGER_END = '}-}'

    DEFAULT_KWARGS = {
    }

    _IMP_ATTS = []
    _ONE_LINE_ATTS = []

    def __init__( self ):
        ParentClass.__init__( self )

    def generate( self, overwrite: bool = False ):

        print ('Generating from Repository template')
        self.copy_template_files( overwrite=overwrite )

    def get_attr( self, att_string ):

        if not self.cfg.has_key( att_string ):
            att_value = input('Enter a value for ' + att_string + ': ')
            self.cfg.set_key( att_string, att_value )

        return self.cfg.get_key( att_string )

    def copy_template_files( self, overwrite: bool = False ) -> None:
        
        # if not overwrite
        if not overwrite:
            overwrite = self.cfg['overwrite']

        # if the user has overwritten the default template, use that one
        if self.cfg['user_template.Dir'].exists():
            template_Dir = self.cfg['user_template.Dir']
        else:
            template_Dir = self.cfg['template.Dir']

        copy_Paths = template_Dir.walk_contents_Paths( block_dirs = False, block_paths = False, folders_to_skip = self.cfg['folders_to_skip']  )
        rel_Paths = copy_Paths.get_rels( template_Dir )
        paste_Paths = rel_Paths.join_Dir( self.cfg['repo.Dir'] )

        for i in range(len(paste_Paths)):

            unformatted_Path = list(paste_Paths)[i]

            if unformatted_Path.type_path:
                copy_Path = list(copy_Paths)[i]
                paste_Path = do.Path( self.format_string_by_atts( unformatted_Path.path, trigger_beg = self.TRIGGER_BEG, trigger_end = self.TRIGGER_END ) )
                print (paste_Path)

                if not paste_Path.exists() or overwrite:
                    print ('Copying Template Path: ' + str(paste_Path) )            

                    if paste_Path.exists():
                        paste_Path.remove( override = True )

                    copy_Path.copy( Destination = paste_Path, print_off=False, override = True ) 

                    try:
                        string = paste_Path.read()
                    except:
                        print ('Skipping formatting, cannot read')
                        continue
                    
                    # if we are able to read, then we shouldn't be copying it over
                    formatted_string = self.format_string_by_atts( paste_Path.read(), trigger_beg = self.TRIGGER_BEG, trigger_end = self.TRIGGER_END )
                    paste_Path.write( string = formatted_string, override = True )

                else:
                    print ('Skipping existing Path: ' + str(paste_Path) )

            if unformatted_Path.type_dir:
                copy_Dir = list(copy_Paths)[i]
                paste_Dir = do.Dir( self.format_string_by_atts( unformatted_Path.path, trigger_beg = self.TRIGGER_BEG, trigger_end = self.TRIGGER_END ) )
                print (paste_Dir)

                if not paste_Dir.exists():
                    print ('Copying Template Dir: ' + str(paste_Dir))
                    paste_Dir.create( override = True )

                else:
                    print ('Skipping Template Dir: ' + str(paste_Dir))


