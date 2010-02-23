from tg.configuration import AppConfig, Bunch
import toscasample
from toscasample import model
from toscasample.lib import app_globals, helpers

base_config = AppConfig()
base_config.renderers = []

base_config.package = toscasample

#Set the default renderer
base_config.default_renderer = 'genshi'
base_config.renderers.append('genshi') 
# if you want raw speed and have installed chameleon.genshi
# you should try to use this renderer instead.
# warning: for the moment chameleon does not handle i18n translations
#base_config.renderers.append('chameleon_genshi') 

#Configure the base SQLALchemy Setup
base_config.use_sqlalchemy = True
base_config.model = toscasample.model
base_config.DBSession = toscasample.model.DBSession

