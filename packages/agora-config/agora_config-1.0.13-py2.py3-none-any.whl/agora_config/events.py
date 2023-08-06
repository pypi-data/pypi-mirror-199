import inspect
import weakref
from agora_logging import logger

class Events:
    """
    Handles the events and callbacks
    """
    def __init__(self):
        self.setting_subscriptions = {'##':{"unbound":set(),"bound":set()}}
        self.setting_last_data = {'##':None}

    def __is_bound(self,method):
        """
        Check if a method is a bound method

        Args:
            method (method):

        Returns:
            bool: whether the method is a bound method or not
        """
        return bool(hasattr(method,"__self__"))

    def __count_arguments(self,fn,expected):
        """
        Callbacks should only have one argument to let the payload pass
        """
        args_in_signature=len(inspect.signature(fn).parameters)
        if args_in_signature != expected:
            logger.error("Callback function should have exactly one argument to accept configuration")
            return False
        return True


    def add_event(self,setting_name:str,callback):
        """
        Adds an event and callback, and checks whether the method is a bound method or not
        Keeping a reference to a bound method in container can create memory leak if the original object was removed.
        Keeps a weak reference to the method.

        Args:
            event_string (str): a key or nested key from the config file
            callback (function): callback function to be triggered
        """
        subtype="unbound"
        if self.__is_bound(callback):
            subtype = "bound"
            if self.__count_arguments(callback,1):
                callback=weakref.WeakMethod(callback)
            else:
                return False
        elif not self.__count_arguments(callback,1):
            return False

        self.setting_subscriptions[setting_name] = self.setting_subscriptions.get(setting_name,{"unbound":set(),"bound":set()})
        self.setting_last_data[setting_name] = self.setting_last_data.get(setting_name,None)
        self.setting_subscriptions[setting_name][subtype].add(callback)


    def get_event_subs(self,event_string):
        """
        Get the callbacks which are subscribing to the given event

        Args:
            event_string (str): key or nested keys eg: AEA2:Logging:Verbosity

        Yields:
            Iterable: callbacks/weakmethod will be converted to the callback
        """
        subs_unbound_set=self.setting_subscriptions[event_string]["unbound"]
        subs_bound_set_weak=self.setting_subscriptions[event_string]["bound"]
        yield from [weak() for weak in subs_bound_set_weak]
        yield from subs_unbound_set
        
    
    def get_events_to_trigger(self, config_dict):
        """
        Identifies all the events that need to be triggered
        """
        for setting_name, last_value in self.setting_last_data.items():
            data = self.get(config_dict, setting_name)
            #print( f"checking {setting_name} = '{data}'")
            if last_value != data:
                self.setting_last_data[setting_name] = data
                #print( f" {setting_name} has changed to {data}" )
                yield setting_name,data

    def get(self, config_dict, setting_name:str, default:str = ""):
        keys = setting_name.split(':')
        ld = config_dict
        for key in keys[:-1]:
            #print( f"key = {key} & ld = {ld}\n")
            if isinstance(ld, dict) and key in ld:
                ld = ld[key]
            else:
                return default
        if keys[-1] in ld:
            return ld[keys[-1]]
        return default
    