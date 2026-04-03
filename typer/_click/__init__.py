"""
Vendored Click: https://github.com/pallets/click/releases/tag/8.3.1
"""

from __future__ import annotations

from ._utils import FLAG_NEEDS_VALUE as FLAG_NEEDS_VALUE
from ._utils import UNSET as UNSET
from .core import ParameterSource as ParameterSource
from .decorators import help_option as help_option
from .decorators import option as option
from .exceptions import Abort as Abort
from .exceptions import BadArgumentUsage as BadArgumentUsage
from .exceptions import BadOptionUsage as BadOptionUsage
from .exceptions import BadParameter as BadParameter
from .exceptions import ClickException as ClickException
from .exceptions import Exit as Exit
from .exceptions import FileError as FileError
from .exceptions import MissingParameter as MissingParameter
from .exceptions import NoArgsIsHelpError as NoArgsIsHelpError
from .exceptions import NoSuchOption as NoSuchOption
from .exceptions import UsageError as UsageError
from .formatting import HelpFormatter as HelpFormatter
from .formatting import join_options as join_options
from .formatting import wrap_text as wrap_text
from .globals import get_current_context as get_current_context
from .parser import _OptionParser as _OptionParser
from .shell_completion import CompletionItem as CompletionItem
from .termui import confirm as confirm
from .termui import getchar as getchar
from .termui import launch as launch
from .termui import progressbar as progressbar
from .termui import prompt as prompt
from .termui import secho as secho
from .termui import style as style
from .types import BOOL as BOOL
from .types import FLOAT as FLOAT
from .types import INT as INT
from .types import STRING as STRING
from .types import UUID as UUID
from .types import BoolParamType as BoolParamType
from .types import Choice as Choice
from .types import DateTime as DateTime
from .types import File as File
from .types import FloatRange as FloatRange
from .types import IntRange as IntRange
from .types import OptionHelpExtra as OptionHelpExtra
from .types import ParamType as ParamType
from .types import Tuple as Tuple
from .types import _NumberRangeBase as _NumberRangeBase
from .types import convert_type as convert_type
from .utils import echo as echo
from .utils import format_filename as format_filename
from .utils import get_app_dir as get_app_dir
from .utils import get_binary_stream as get_binary_stream
from .utils import get_text_stream as get_text_stream
from .utils import make_str as make_str
