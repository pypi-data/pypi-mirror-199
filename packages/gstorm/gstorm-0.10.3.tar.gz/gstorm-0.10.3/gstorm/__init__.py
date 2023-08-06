# from .gstorm import mainClass
from .__version__ import __version__
from . import cli
from . import helpers
from .BaseGraphQLType import BaseGraphQLType
from .GraphQLType import GraphQLType
from .QueryBuilder import QueryBuilder
from .MutationBuilder import MutationBuilder
from ._mutation_runners import (
    create,
    save_multi_create,
    update,
    upsert,
)

# * Package name:
name = 'gstorm'
