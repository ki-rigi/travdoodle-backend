"""created accomodation model

Revision ID: 4c2866163aae
Revises: 207fa9c318e3
Create Date: 2025-02-07 16:27:20.956466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c2866163aae'
down_revision = '207fa9c318e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accommodations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('address', sa.String(length=300), nullable=False),
    sa.Column('check_in_date', sa.Date(), nullable=False),
    sa.Column('check_out_date', sa.Date(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('destination_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['destination_id'], ['destinations.id'], name=op.f('fk_accommodations_destination_id_destinations')),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('accommodations')
    # ### end Alembic commands ###
