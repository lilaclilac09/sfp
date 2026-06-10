"""SFP bridge system package for CL-Bench.

Importing this package registers :class:`SFPSystem` under the name ``sfp`` via
the ``@register_system("sfp")`` decorator, so ``clbench run --system sfp`` can
discover it. Install by copying this directory to ``<clbench>/src/systems/sfp/``
(see ``clbench/install_adapter.py``).
"""

from .system import SFPSystem

__all__ = ["SFPSystem"]
