"""initial migration

Revision ID: 604cff316e39
Revises: 90d564ce87ba
Create Date: 2023-10-15 01:23:45.188589

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '604cff316e39'
down_revision: Union[str, None] = '90d564ce87ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
