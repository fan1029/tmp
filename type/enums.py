from enum import Enum


class TAG_THEME(Enum):
    DARK = 'dark'
    LIGHT = 'light'
    PLAIN = 'plain'
    DEFAULT = ''


class TAG_ROUND(Enum):
    TRUE = True
    FALSE = False
    DEFAULT = False


class TAG_SIZE(Enum):
    SMALL = 'small'
    DEFAULT = 'default'
    LARGE = 'large'


class TEXT_SIZE(Enum):
    SMALL = 'small'
    DEFAULT = 'default'
    LARGE = 'large'


class TEXT_TYPE(Enum):
    PRIMARY = 'primary'
    SUCCESS = 'success'
    INFO = 'info'
    WARNING = 'warning'
    DANGER = 'danger'
    DEFAULT = ''


class TEXT_TAG(Enum):
    BOLD = 'bold'
    DEL = 'del'
    MARKED = 'marked'
    NONE = ''


class TOOL_TIP_THEME(Enum):
    DARK = 'dark'
    LIGHT = 'light'
    DEFAULT = 'dark'


class TOOL_TIP_PLACEMENT(Enum):
    TOP = 'top'
    BOTTOM = 'bottom'
    LEFT = 'left'
    RIGHT = 'right'
    DEFAULT = 'top'


class POPOVER_THEME(Enum):
    DARK = 'dark'
    LIGHT = 'light'
    DEFAULT = 'dark'


class POPOVER_PLACEMENT(Enum):
    TOP = 'top'
    BOTTOM = 'bottom'
    LEFT = 'left'
    RIGHT = 'right'
    DEFAULT = 'top'


class ALERT_TYPE(Enum):
    INFO = 'info'
    SUCCESS = 'success'
    WARNING = 'warning'
    DANGER = 'danger'
    DEFAULT = 'info'


class ALERT_THEME(Enum):
    DARK = 'dark'
    LIGHT = 'light'
    DEFAULT = 'light'


class NOTIFICATION_TYPE(Enum):
    INFO = 'info'
    SUCCESS = 'success'
    WARNING = 'warning'
    DEFAULT = 'info'


class NOTIFICATION_POS(Enum):
    TOP_LEFT = 'top-left'
    TOP_RIGHT = 'top-right'
    BOTTOM_LEFT = 'bottom-left'
    BOTTOM_RIGHT = 'bottom-right'
    DEFAULT = 'top-right'


#######################
class COLOR(Enum):
    RED = 5
    GREEN = 4
    YELLOW = 3
    BLUE = 2
    ORANGE = 1
    DEFAULT = 0
