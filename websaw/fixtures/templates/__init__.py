from .spa_component import SPAComponent
from .upytl_template import UTemplate

YATLTemplate = None
try:
    from .yatl_template.template import YATLTemplate
except ImportError:
    pass

__all__ = (
    'YATLTemplate',
    'UTemplate',
    'SPAComponent',
)
