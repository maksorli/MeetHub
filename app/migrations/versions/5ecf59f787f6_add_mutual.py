"""Add mutual

Revision ID: 5ecf59f787f6
Revises: 466bc2cdae30
Create Date: 2024-10-30 12:46:06.183364

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5ecf59f787f6"
down_revision: Union[str, None] = "466bc2cdae30"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("matches", sa.Column("is_mutual", sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("matches", "is_mutual")
    # ### end Alembic commands ###
