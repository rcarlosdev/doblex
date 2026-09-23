"""Initial baseline schema

Revision ID: 26301bc82e97
Revises: 
Create Date: 2026-09-19 14:58:01.909858

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26301bc82e97'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('ots', schema=None) as batch_op:
        try:
            batch_op.create_index(batch_op.f('ix_ots_id_actividad'), ['id_actividad'], unique=False)
        except Exception:
            pass
        try:
            batch_op.create_index(batch_op.f('ix_ots_sitio_id'), ['sitio_id'], unique=False)
        except Exception:
            pass
        try:
            batch_op.create_foreign_key('fk_ots_sitios', 'sitios', ['sitio_id'], ['id'])
        except Exception:
            pass


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('ots', schema=None) as batch_op:
        try:
            batch_op.drop_constraint('fk_ots_sitios', type_='foreignkey')
        except Exception:
            pass
        try:
            batch_op.drop_index(batch_op.f('ix_ots_sitio_id'))
        except Exception:
            pass
        try:
            batch_op.drop_index(batch_op.f('ix_ots_id_actividad'))
        except Exception:
            pass

