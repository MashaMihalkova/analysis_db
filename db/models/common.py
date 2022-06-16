from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData

convention = {
    'all_column_names': lambda constraint, table: '_'.join(
        [column.name for column in constraint.columns.values()]
    ),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': ('fk__%(table_name)s__%(all_column_names)s__' '%(referred_table_name)s'),
    'pk': 'pk__%(table_name)s',
}

# Registry for all tables
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)
