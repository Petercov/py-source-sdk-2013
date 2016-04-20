from _entitiesmisc import *
from _entities import *
from core.fields import SetupClassFields, SetupInputMethods

# Lists of all entity classes
if isclient:
    list_ents = [ 
        C_BaseEntity,
        C_BaseAnimating,
        C_BaseAnimatingOverlay,
        C_BaseFlex,
        C_BaseCombatCharacter,
        C_BaseGrenade,
        C_BasePlayer,
        C_BaseCombatWeapon,
    ]
    
    # List of aliases
    CBaseEntity = C_BaseEntity
    CBaseAnimating = C_BaseAnimating
    CBaseAnimatingOverlay = C_BaseAnimatingOverlay
    CBaseFlex = C_BaseFlex
    CBaseCombatCharacter = C_BaseCombatCharacter
    CBaseGrenade = C_BaseGrenade
    CBasePlayer = C_BasePlayer
    CBaseCombatWeapon = C_BaseCombatWeapon
    
    # Server only, add an alias anyway (for convenience)
    CPointEntity = CBaseEntity
    
    # Client sub
    entlist = None

else:
    list_ents = [ 
        CBaseEntity, 
        CBaseAnimating, 
        CBaseAnimatingOverlay, 
        CBaseFlex, 
        CBaseCombatCharacter,
        CBaseGrenade,
        CBasePlayer,
        CPointEntity,
        CServerOnlyEntity,
        CServerOnlyPointEntity,
        CLogicalEntity,
        CFuncBrush,
        CBaseToggle,
        CBaseTrigger,
        # TODO CTriggerMultiple,
        CBaseCombatWeapon,
        # TODO CBaseFilter,
    ]

# Friendly aliases
eventqueue = g_EventQueue if isserver else None
    
@classmethod    
def InitEntityClass(cls):
    """ Entity Class initializer, could be seen as a metaclass.
        It is called when the class is created and when a new map is loaded.
        Used for one time initializations per map.
    """
    SetupClassFields(cls)
    SetupInputMethods(cls)
    
# Bind the following methods to each entity class
for cls in list_ents:
    # InitEntityClass: Called on level initialization and on the first time the entity factory is initialized.
    cls.InitEntityClass = InitEntityClass
    
clstoclstype = {
    'CBaseEntity' : ('@PointClass', ['Targetname', 'Origin']),
    'CFuncBrush' : ('@SolidClass', ['Targetname', 'Parentname', 'Origin', 'RenderFields', 'Global', 'Inputfilter', 'EnableDisable', 'Shadow']),
    'CBaseTrigger' : ('@SolidClass', ['Targetname', 'Parentname', 'Origin', 'RenderFields', 'Global', 'Inputfilter', 'EnableDisable', 'Shadow']),
    'CBaseFilter' : ('@FilterClass', ['BaseFilter']),
}
def DetermineClsType(cls):
    if cls.__name__ in clstoclstype:
        return clstoclstype[cls.__name__]
    for basecls in cls.__bases__:
        rs = DetermineClsType(basecls)
        if rs: 
            return rs
    return None

def networked(cls):
    """ Makes the class networked, which can serve as a base for entities which don't need to be
        networked. """
    if 'networkinst' not in cls.__dict__:
        networkname = '%s.__%s' % (cls.__module__, cls.__name__)
        cls.networkinst = NetworkedClass(networkname, cls)
    return cls
    
def entity( clsname, 
            networked=False, 
            helpstring='',
            clstype='',
            entityextraproperties='',
            base=[],
            studio='',
            iconsprite='',
            cylinder=[],
            color='',
            size='',
            cppproperties='',
            nofgdentry=False):
    """ Decorator for turning a class into an entity.
        The class entity must be derived from CBaseEntity. """
    def wrapcls(cls):
        # FIXME: This creates a circular reference between the class and factory/network instance
        #        Although new factories will remove the old factories, it does not clean up nicely yet.
        factoryname = 'factory__%s' % (clsname)
        factory = EntityFactory(clsname, cls)
        factory.entityname = clsname
        factory.clstype = clstype
        factory.entityextraproperties = entityextraproperties
        factory.cppproperties = cppproperties
        factory.helpstring = helpstring
        factory.nofgdentry = nofgdentry
        
        factory.fgdbase = base
        factory.fgdstudio = studio
        factory.fgdiconsprite = iconsprite
        factory.fgdcylinder = cylinder
        factory.fgdcolor = color
        factory.fgdsize = size
        
        setattr(cls, factoryname, factory)
        
        if not factory.clstype:
            info = DetermineClsType(cls)
            if info: 
                factory.clstype = info[0]
        else: 
            info = None
        
        if not factory.fgdbase:
            if info: 
                factory.fgdbase = info[1]

        if networked and 'networkinst' not in cls.__dict__:
            networkname = '%s.__%s' % (cls.__module__, cls.__name__)
            cls.networkinst = NetworkedClass(networkname, cls)
            
        # Initialize the class so the fields are setup
        cls.InitEntityClass()
            
        return cls
    return wrapcls
    