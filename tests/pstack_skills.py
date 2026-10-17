"""Skills this catalog delegates to the installed pstack plugin.

These names were vendored copies until the pstack migration. They now resolve
from the pstack plugin (https://github.com/cursor/plugins/tree/main/pstack),
so catalog dependency checks accept them without a local skill directory.
"""

PSTACK_SKILLS = frozenset({
    "architect", "arena", "blast-radius", "how", "interrogate",
    "teach", "tdd", "technical-writing", "unslop", "why",
})
