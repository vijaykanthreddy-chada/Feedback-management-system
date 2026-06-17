"""Add faculty_rating, curriculum_rating, program_structure_rating, overall_rating to feedbacks

Revision ID: 9525240e1521
Revises: 805b4ecc5563
Create Date: 2026-06-16 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9525240e1521'
down_revision = '805b4ecc5563'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('feedbacks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('faculty_rating', sa.Integer(), nullable=False, server_default='1'))
        batch_op.add_column(sa.Column('curriculum_rating', sa.Integer(), nullable=False, server_default='1'))
        batch_op.add_column(sa.Column('program_structure_rating', sa.Integer(), nullable=False, server_default='1'))
        batch_op.add_column(sa.Column('overall_rating', sa.Integer(), nullable=False, server_default='1'))

    op.execute("UPDATE feedbacks SET overall_rating = rating")

    with op.batch_alter_table('feedbacks', schema=None) as batch_op:
        batch_op.drop_column('rating')

    with op.batch_alter_table('feedbacks', schema=None) as batch_op:
        batch_op.alter_column('faculty_rating', server_default=None)
        batch_op.alter_column('curriculum_rating', server_default=None)
        batch_op.alter_column('program_structure_rating', server_default=None)
        batch_op.alter_column('overall_rating', server_default=None)


def downgrade():
    with op.batch_alter_table('feedbacks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rating', sa.Integer(), nullable=False, server_default='1'))

    op.execute("UPDATE feedbacks SET rating = overall_rating")

    with op.batch_alter_table('feedbacks', schema=None) as batch_op:
        batch_op.drop_column('overall_rating')
        batch_op.drop_column('program_structure_rating')
        batch_op.drop_column('curriculum_rating')
        batch_op.drop_column('faculty_rating')

    with op.batch_alter_table('feedbacks', schema=None) as batch_op:
        batch_op.alter_column('rating', server_default=None)
