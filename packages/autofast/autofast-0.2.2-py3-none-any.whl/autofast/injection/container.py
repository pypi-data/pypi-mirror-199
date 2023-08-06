from __future__ import annotations
# python
import inspect
from typing import Any, Dict, Optional, Callable, TypeVar, List, Type
from dataclasses import dataclass
from enum import Enum, auto
# 3rd party
from nameof import nameof
from ..config.data.configuration_options import ConfigurationOptions
# project
import autofast.verify as fdi_ver

from .validation import *
from ..config    import deserialize_config


T = TypeVar('T')


@dataclass
class ContainerOptions:
    ''' Options for container dependency injection resolving. '''

    strong_inheritance : bool = True
    '''
    Enable/disable strong inheritance rules.

    When is disable, one rule applies: register_type is descendant of resolve_type.

    When is enable, applies next rules:
        register_type is descendant of resolve_type.

        In inheritance graph from resolve_type to register_type applies next rules:
            -- All abstract methods must be implemented in descendant classes.

            -- Abstract method cannot redeclare in descendant class with abstract decorator.

            -- Once defined method cannot be signature and annotation overrided in descendant classes.

            -- Inheritance graph cannot have transitive ways of inheritance. For example, 
            A -> C; A -> B; B -> D; D -> C;
    
    '''



class ResolveType(Enum):
    ''' Dependency resolve type. '''

    Instance  = auto()
    ''' When type is resolved, every time returned new constructed object. '''
    
    Singleton = auto()
    ''' When type is resolved, every time returned once constructed object. '''



@dataclass
class _RegistrationPart:
    provide_type  : Type
    register_type : Type
    factory       : Callable[[Container], Any]
    instance      : Any
    resolve_type  : ResolveType



class _TypeResolver:
    __data_type : Type


    def __init__(self, data_type : Type):
        self.__data_type = data_type
        
        
    def __call__(self, container : Container) -> Type:
        cls_meta = get_class_meta_info(self.__data_type)

        init_args = []

        for func in cls_meta.functions:
            if func.name == '__init__':
                for arg in func.arguments[1:]:
                    arg_name = arg.name
                    arg_anno = arg.annotation

                    init_args.append((arg_name, arg_anno))

        if len(init_args) == 0:
            return self.__data_type()
        else:
            build_args = {}
            for arg_name, arg_anno in init_args:
                build_args[arg_name] = container.resolve(arg_anno)

            return self.__data_type(**build_args)
    

class _ConfigResolver:
    __config_type : Type

    __config_field : str


    def __init__(
        self, 
        config_type    : Type,
        config_field   : str
    ):
        self.__config_type    = config_type
        self.__config_field   = config_field
        
    
    def __call__(self, container : Container) -> Type:
        if container.config is None:
            raise ValueError(f'Configuration in container is not loaded.')
            
        if not self.__config_field in container.config:
            raise ValueError(f'{self.__config_field} not present in configuration')

        config = deserialize_config(self.__config_type, container.config[self.__config_field], container.config_options)
        
        return config


class Container:
    ''' Present dependency injection resolve mechanism. '''

#region data

    __container_options : ContainerOptions
    
    config : Optional[dict]

    config_options : Optional[ConfigurationOptions]

    __registrations : Dict[Type, _RegistrationPart]

    __registrations_by_name : Dict[str, _RegistrationPart]

#endregion


#region private_methods

    def __validate_registration(self, provide_type : Type, register_type : Type):
        
        if self.__container_options.strong_inheritance:
            validate_registration_strong_inheritance(provide_type, register_type)
        else:
            validate_registration(provide_type, register_type)


    def __validate_config(self, config_field : str):
        if self.config is None:
            raise ValueError(f'Configuration is not loaded.')
            
        if not config_field in self.config:
            raise ValueError(f'Field \'{config_field}\' not present in configuration')


    def __process_reg_part(self, reg_part : _RegistrationPart):
        if reg_part.resolve_type == ResolveType.Singleton:
            if reg_part.instance is None:
                reg_part.instance = reg_part.factory(self)
                
            return reg_part.instance
        
        else:
            return reg_part.factory(self)

#endregion


#region construct_and_destruct

    def __init__(
        self, 
        container_options : ContainerOptions = ContainerOptions()
    ):
        '''
        Constructs new instance.

        Args:
            container_options (ContainerOptions, optional): Options of container. Defaults to ContainerOptions().
        '''
        fdi_ver.is_none(container_options, nameof(container_options))
        
        self.__container_options = container_options
        
        self.config         = None
        self.config_options = None
        
        self.__registrations         = dict()
        self.__registrations_by_name = dict()
        
#endregion


#region methods

    def load_config(
        self, 
        config  : dict,
        options : ConfigurationOptions = ConfigurationOptions()
    ):
        '''
        Loads configuration from dict.

        Args:
            config (dict): Configuration.
            options (ConfigurationOptions, optional): Configuration options. Defaults to ConfigurationOptions().
        '''

        self.config         = config
        self.config_options = options
        
        
    def register_config(
        self, 
        config_type  : Type, 
        config_field : str
    ):
        '''
        Registers type that is in the configuration on specified field.

        Args:
            config_type (Type): Register type.
            config_field (str): Field in root configuration, which is type located.

        Raises:
            ValueError: 
                Where configuration already registered, config field is not found,
                or config not loaded.
        '''

        self.__validate_config(config_field)

        if config_type in self.__registrations:
            raise ValueError(f'Config \'{config_type}\' already registered.')
        
        self.__registrations[config_type] = _RegistrationPart(
            config_type,
            config_type,
            _ConfigResolver(config_type, config_field),
            None,
            ResolveType.Singleton
        )

    
    def register_config_by_name(
        self,
        name : str,
        config_type : Type,
        config_field : str
    ):
        '''
        Registers config by name identificator.

        Args:
            name (str): name identificator.
            config_type (Type): Register type.
            config_field (str): Field in root configuration, which is type located.

        Raises:
            ValueError: 
                Where configuration already registered, config field is not found,
                or config not loaded.
        '''

        self.__validate_config(config_field)

        if name in self.__registrations_by_name:
            raise ValueError(f'Config with name \'{name}\' already registered')

        self.__registrations_by_name[name] = _RegistrationPart(
            config_type,
            config_type,
            _ConfigResolver(config_type, config_field),
            None,
            ResolveType.Singleton
        )
        

    def register_type(
        self, 
        provide_type  : Type, 
        register_type : Type,
        resolve_type  : ResolveType
    ):
        '''
        Registers type.

        Args:
            provide_type (Type): Type to be resolved.
            register_type (Type): Type to be registered.
            resolve_type (ResolveType): Type of resolving mechanism.
        '''

        self.__validate_registration(provide_type, register_type)
        
        self.__registrations[provide_type] = _RegistrationPart(
            provide_type,
            register_type,
            _TypeResolver(register_type),
            None,
            resolve_type
        )


    def register_singleton(
        self,
        provide_type  : Type,
        register_type : Type
    ):
        '''
        Registers type as singleton.

        Args:
            provide_type (Type): Type to be resolved.
            register_type (Type): Type to be registered.
        '''

        self.register_type(provide_type, register_type, ResolveType.Singleton)


    def register_instance(
        self,
        provide_type : Type,
        register_type : Type
    ):
        '''
        Registers type as instance.

        Args:
            provide_type (Type): Type to be resolved.
            register_type (Type): Type to be registered.
        '''

        self.register_type(provide_type, register_type, ResolveType.Instance)

    
    def register_type_by_name(
        self,
        name : str,
        provide_type : Type,
        register_type : Type,
        resolve_type : ResolveType
    ):
        '''
        Registers type that is resolved by name identificator.

        Args:
            name (str): Name identificator.
            provide_type (Type): Type to be resolved.
            register_type (Type): Type to be registered.
            resolve_type (ResolveType): Type of resolving mechanism.
        '''

        self.__validate_registration(provide_type, register_type)

        self.__registrations_by_name[name] = _RegistrationPart(
            provide_type,
            register_type,
            _TypeResolver(register_type),
            None,
            resolve_type
        )
        
        
    def register_factory(
        self,
        provide_type  : Type[T],
        register_type : Type,
        factory       : Callable[[Container], T],
        resolve_type  : ResolveType
    ):
        '''
        Registers type with factory for object construction.

        Args:
            provide_type (Type[T]): Type to be resolved.
            register_type (Type): Type to be registered.
            factory (Callable[[Container], T]): Factory that constuct object.
            resolve_type (ResolveType): Type of resolving mechanism.
        '''

        self.__validate_registration(
            provide_type,
            register_type
        )
        
        self.__registrations[provide_type] = _RegistrationPart(
            provide_type,
            register_type,
            factory,
            None,
            resolve_type
        )


    def register_factory_by_name(
        self,
        name          : str,
        provide_type  : Type[T],
        register_type : Type,
        factory       : Callable[[Container], T],
        resolve_type  : ResolveType
    ):
        '''
        Registers type with factory for object construction, that
        resolved by name identificator.

        Args:
            name (str): Name identificator.
            provide_type (Type[T]): Type to be resolved.
            register_type (Type): Type to be registered.
            factory (Callable[[Container], T]): Factory that construct object.
            resolve_type (ResolveType): Type of resolving mechanism.
        '''

        self.__validate_registration(
            provide_type,
            register_type
        )
        
        self.__registrations_by_name[name] = _RegistrationPart(
            provide_type,
            register_type,
            factory,
            None,
            resolve_type
        )

        
    def resolve(self, data_type : Type[T]) -> T:
        '''
        Resolves object by type.

        Args:
            data_type (Type[T]): Type to be resolved.

        Raises:
            ValueError: if type is not registered.

        Returns:
            T: object resolved by type.
        '''
        if not data_type in self.__registrations:
            raise ValueError(f'\'{data_type}\' is not registered.')
        
        reg_part = self.__registrations[data_type]

        return self.__process_reg_part(reg_part)
        
    
    def resolve_by_name(self, name : str, data_type : Type[T]) -> T:
        '''
        Resolves object by type and name identificator.

        Args:
            name (str): Name identificator.
            data_type (Type[T]): Type to be resolved.

        Raises:
            ValueError: If not have registration with name identificator.
            ValueError: If has registration with this name, but of a different type.

        Returns:
            T: object resolved by type.
        '''

        if not name in self.__registrations_by_name:
            raise ValueError(f'Not have registration with name \'{name}\'')

        reg_part = self.__registrations_by_name[name]

        if reg_part.provide_type != data_type:
            raise ValueError(f'Not have registration with name \'{name}\' and type \'{data_type}\'.')

        return self.__process_reg_part(reg_part)

#endregion