__all__ = [
    'ConfigurableReaderPlugins', 'CLIPlugins', 'EndpointPlugins', 'KBPlugins', 'ProcessorPlugins', 'ReaderPlugins', 'SerializerPlugins',
    'TDMPlugins', 'TrainerPlugins', 'WrapperPlugins', 'WrapperActionsPlugins'
]


from .cli import CLIPluginManager
from .endpoint import EndpointPluginManager
from .kb import KBPluginManager
from .processor import ProcessorPluginManager
from .reader import ConfigurableReaderPluginManager, ReaderPluginManager
from .serializer import SerializerPluginManager
from .tdm import TDMPluginManager
from .trainer import TrainerPluginManager
from .wrapper import WrapperPluginManager
from .wrapper_actions import WrapperActionsPluginManager

CLIPlugins = CLIPluginManager()
ConfigurableReaderPlugins = ConfigurableReaderPluginManager()
EndpointPlugins = EndpointPluginManager()
KBPlugins = KBPluginManager()
ProcessorPlugins = ProcessorPluginManager()
ReaderPlugins = ReaderPluginManager()
SerializerPlugins = SerializerPluginManager()
TDMPlugins = TDMPluginManager()
TrainerPlugins = TrainerPluginManager()
WrapperPlugins = WrapperPluginManager()
WrapperActionsPlugins = WrapperActionsPluginManager()
