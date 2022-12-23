"""wakaran2

Revision ID: 80f9d3c83f96
Revises: a05a2f076a1b
Create Date: 2022-12-23 17:17:42.660979

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
import sqlalchemy_utils
import uuid

# revision identifiers, used by Alembic.
revision = '80f9d3c83f96'
down_revision = 'a05a2f076a1b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('achivement',
    sa.Column('created_at', mysql.TIMESTAMP(), server_default=sa.text('current_timestamp'), nullable=False, comment='作成日時'),
    sa.Column('updated_at', mysql.TIMESTAMP(), server_default=sa.text('current_timestamp on update current_timestamp'), nullable=False, comment='更新日時'),
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), default=uuid.uuid4, nullable=False),
    sa.Column('term', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('authority',
    sa.Column('created_at', mysql.TIMESTAMP(), server_default=sa.text('current_timestamp'), nullable=False, comment='作成日時'),
    sa.Column('updated_at', mysql.TIMESTAMP(), server_default=sa.text('current_timestamp on update current_timestamp'), nullable=False, comment='更新日時'),
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), default=uuid.uuid4, nullable=False),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tasktag',
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), default=uuid.uuid4, nullable=False),
    sa.Column('name', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('created_at', mysql.TIMESTAMP(), server_default=sa.text('current_timestamp'), nullable=False, comment='作成日時'),
    sa.Column('updated_at', mysql.TIMESTAMP(), server_default=sa.text('current_timestamp on update current_timestamp'), nullable=False, comment='更新日時'),
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), default=uuid.uuid4, nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('block', sa.Enum('A1', 'A2', 'A3', 'A4', 'B12', 'B3', 'B4', 'C12', 'C34', name='block'), nullable=True),
    sa.Column('room_number', sa.String(length=10), nullable=True),
    sa.Column('point', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('achivement_table',
    sa.Column('user', sqlalchemy_utils.types.uuid.UUIDType(binary=False), default=uuid.uuid4, nullable=False),
    sa.Column('achivement', sqlalchemy_utils.types.uuid.UUIDType(binary=False), default=uuid.uuid4, nullable=False),
    sa.ForeignKeyConstraint(['achivement'], ['achivement.id'], ),
    sa.ForeignKeyConstraint(['user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user', 'achivement')
    )
    op.create_table('bid',
    sa.Column('created_at', mysql.TIMESTAMP(), server_default=sa.text('current_timestamp'), nullable=False, comment='作成日時'),
    sa.Column('updated_at', mysql.TIMESTAMP(), server_default=sa.text('current_timestamp on update current_timestamp'), nullable=False, comment='更新日時'),
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), default=uuid.uuid4, nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.Column('end_time', sa.DateTime(), nullable=True),
    sa.Column('start_point', sa.Integer(), nullable=True),
    sa.Column('lowest_point', sa.Integer(), nullable=True),
    sa.Column('second_point', sa.Integer(), nullable=True),
    sa.Column('buyout_point', sa.Integer(), nullable=True),
    sa.Column('is_complete', sa.Boolean(), nullable=True),
    sa.Column('lowest_user_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['lowest_user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('task',
    sa.Column('created_at', mysql.TIMESTAMP(), server_default=sa.text('current_timestamp'), nullable=False, comment='作成日時'),
    sa.Column('updated_at', mysql.TIMESTAMP(), server_default=sa.text('current_timestamp on update current_timestamp'), nullable=False, comment='更新日時'),
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), default=uuid.uuid4, nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('detail', sa.Text(length=400), nullable=True),
    sa.Column('creater_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['creater_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('authority_table',
    sa.Column('task', sqlalchemy_utils.types.uuid.UUIDType(binary=False), default=uuid.uuid4, nullable=False),
    sa.Column('authority', sqlalchemy_utils.types.uuid.UUIDType(binary=False), default=uuid.uuid4, nullable=False),
    sa.ForeignKeyConstraint(['authority'], ['authority.id'], ),
    sa.ForeignKeyConstraint(['task'], ['task.id'], ),
    sa.PrimaryKeyConstraint('task', 'authority')
    )
    op.create_table('experience_table',
    sa.Column('user', sqlalchemy_utils.types.uuid.UUIDType(binary=False), default=uuid.uuid4, nullable=True),
    sa.Column('task', sqlalchemy_utils.types.uuid.UUIDType(binary=False), default=uuid.uuid4, nullable=True),
    sa.ForeignKeyConstraint(['task'], ['task.id'], ),
    sa.ForeignKeyConstraint(['user'], ['user.id'], )
    )
    op.create_table('slot',
    sa.Column('created_at', mysql.TIMESTAMP(), server_default=sa.text('current_timestamp'), nullable=False, comment='作成日時'),
    sa.Column('updated_at', mysql.TIMESTAMP(), server_default=sa.text('current_timestamp on update current_timestamp'), nullable=False, comment='更新日時'),
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), default=uuid.uuid4, nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.Column('end_time', sa.DateTime(), nullable=True),
    sa.Column('creater_id', sa.String(), nullable=True),
    sa.Column('task_id', sa.String(), nullable=True),
    sa.Column('bid_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['bid_id'], ['bid.id'], ),
    sa.ForeignKeyConstraint(['creater_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['task_id'], ['task.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tasktag_table',
    sa.Column('task', sqlalchemy_utils.types.uuid.UUIDType(binary=False), default=uuid.uuid4, nullable=False),
    sa.Column('tasktag', sqlalchemy_utils.types.uuid.UUIDType(binary=False), default=uuid.uuid4, nullable=False),
    sa.ForeignKeyConstraint(['task'], ['task.id'], ),
    sa.ForeignKeyConstraint(['tasktag'], ['tasktag.id'], ),
    sa.PrimaryKeyConstraint('task', 'tasktag')
    )
    op.create_table('slots_table',
    sa.Column('user', sqlalchemy_utils.types.uuid.UUIDType(binary=False), default=uuid.uuid4, nullable=False),
    sa.Column('slot', sqlalchemy_utils.types.uuid.UUIDType(binary=False), default=uuid.uuid4, nullable=False),
    sa.ForeignKeyConstraint(['slot'], ['slot.id'], ),
    sa.ForeignKeyConstraint(['user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user', 'slot')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('slots_table')
    op.drop_table('tasktag_table')
    op.drop_table('slot')
    op.drop_table('experience_table')
    op.drop_table('authority_table')
    op.drop_table('task')
    op.drop_table('bid')
    op.drop_table('achivement_table')
    op.drop_table('user')
    op.drop_table('tasktag')
    op.drop_table('authority')
    op.drop_table('achivement')
    # ### end Alembic commands ###