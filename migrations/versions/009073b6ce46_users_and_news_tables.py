"""users and news tables

Revision ID: 009073b6ce46
Revises: 
Create Date: 2023-03-19 01:47:07.028629

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '009073b6ce46'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('articles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('author', sa.String(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('written', sa.DateTime(), nullable=False),
    sa.Column('is_published', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('number_of_seen', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('pic', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('url')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('regisration_date', sa.DateTime(), nullable=True),
    sa.Column('role', sa.String(length=20), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=300), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('birthday_date', sa.DateTime(), nullable=True),
    sa.Column('avatar', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_role'), ['role'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_role'))

    op.drop_table('user')
    op.drop_table('articles')
    # ### end Alembic commands ###
