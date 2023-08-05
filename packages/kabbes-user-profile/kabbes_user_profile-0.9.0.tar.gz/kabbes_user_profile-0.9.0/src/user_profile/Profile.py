from parent_class import ParentClass
import py_starter as ps
import kabbes_config

class Profile( ParentClass ):

    _USER_PROFIlE_TRIGGER_BEG = "{UP{"
    _USER_PROFIlE_TRIGGER_END = "}UP}"

    _CFG_KEY = 'profile'

    def __init__( self ):
        ParentClass.__init__( self )
        self.load()

    def load( self ):

        if not self.cfg['profile_Path'].exists():
            self.create_profile()

        self.profile = kabbes_config.Node( Profile._CFG_KEY, dict=self.cfg['profile_Path'].read_json_to_dict() )
        self.cfg.adopt( self.profile )

    def get_template_Path( self ):

        template_Paths = self.cfg['templates_Dir'].list_contents_Paths(block_dirs=True,block_paths=False)

        # This will be an error, no template options present
        if len(template_Paths) == 0:
            print ('No templates available')
            assert False
        
        else:
            return ps.get_selection_from_list( list(template_Paths) )


    def create_profile( self ) -> None:

        template_Path = self.get_template_Path()

        #copy and paste the template
        print ('Generating your user Profile')
        template_Path.copy( Destination = self.cfg['profile_Path'], print_off = False )

        #read the contents of the newly created module
        template_contents = self.cfg['profile_Path'].read()

        #format the contents of the template 
        formatting_dict = {
            'id': self.cfg[ 'user_to_load' ]
        }

        #enter values for all other values that couldn't be filled in
        formatting_values = ps.find_string_formatting( template_contents, trigger_beg=Profile._USER_PROFIlE_TRIGGER_BEG,trigger_end=Profile._USER_PROFIlE_TRIGGER_END )

        for formatting_value in formatting_values:
            stripped_value = ps.strip_trigger( formatting_value, Profile._USER_PROFIlE_TRIGGER_BEG, Profile._USER_PROFIlE_TRIGGER_END )

            if stripped_value not in formatting_dict:
                user_value = input('Enter a value for ' + str(stripped_value) + ': ')    
                formatting_dict[stripped_value] = user_value
        
        formatted_contents = ps.smart_format( template_contents, formatting_dict, trigger_beg=Profile._USER_PROFIlE_TRIGGER_BEG,trigger_end=Profile._USER_PROFIlE_TRIGGER_END  )

        #write the formatted info back
        self.cfg['profile_Path'].write( string = formatted_contents )
    
