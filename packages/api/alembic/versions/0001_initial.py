"""Initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2024-01-01
"""
from alembic import op
import sqlalchemy as sa

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    op.create_table('facilities',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('district', sa.String(255), nullable=False),
        sa.Column('state', sa.String(255), nullable=False),
        sa.Column('latitude', sa.Float, nullable=False),
        sa.Column('longitude', sa.Float, nullable=False),
        sa.Column('contact_phone', sa.String(20)),
    )

    op.create_table('health_workers',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('facility_id', sa.String(36), sa.ForeignKey('facilities.id'), nullable=False),
        sa.Column('phone', sa.String(20)),
        sa.Column('role', sa.String(50), nullable=False, server_default='worker'),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table('patients',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('facility_id', sa.String(36), sa.ForeignKey('facilities.id'), nullable=False),
        sa.Column('age', sa.Float, nullable=False),
        sa.Column('sex', sa.String(1), nullable=False),
        sa.Column('pregnancy_status', sa.Boolean, server_default='false'),
        sa.Column('gestational_weeks', sa.Integer),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table('assessments',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('patient_id', sa.String(36), sa.ForeignKey('patients.id'), nullable=False),
        sa.Column('facility_id', sa.String(36), sa.ForeignKey('facilities.id'), nullable=False),
        sa.Column('worker_id', sa.String(36)),
        sa.Column('vitals', sa.JSON, nullable=False),
        sa.Column('news2_score', sa.Integer, nullable=False),
        sa.Column('risk_band', sa.String(10), nullable=False),
        sa.Column('condition_detected', sa.String(50), nullable=False),
        sa.Column('action_card_id', sa.String(20)),
        sa.Column('gps_lat', sa.Float),
        sa.Column('gps_lon', sa.Float),
        sa.Column('score_type', sa.String(10), nullable=False, server_default='NEWS2'),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )
    op.create_index('ix_assessments_facility_created', 'assessments', ['facility_id', 'created_at'])
    op.create_index('ix_assessments_risk_band', 'assessments', ['risk_band'])

    op.create_table('alerts',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('assessment_id', sa.String(36), sa.ForeignKey('assessments.id'), nullable=False),
        sa.Column('facility_id', sa.String(36), sa.ForeignKey('facilities.id'), nullable=False),
        sa.Column('risk_band', sa.String(10), nullable=False),
        sa.Column('sent_via', sa.JSON, server_default='[]'),
        sa.Column('acknowledged', sa.Boolean, server_default='false'),
        sa.Column('acknowledged_by', sa.String(255)),
        sa.Column('acknowledged_at', sa.DateTime),
        sa.Column('escalation_level', sa.Integer, server_default='0'),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )
    op.create_index('ix_alerts_facility_ack', 'alerts', ['facility_id', 'acknowledged', 'created_at'])

    op.create_table('sync_log',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('device_id', sa.String(255), nullable=False),
        sa.Column('records_synced', sa.Integer, server_default='0'),
        sa.Column('synced_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('errors', sa.JSON, server_default='{}'),
    )


def downgrade() -> None:
    op.drop_table('sync_log')
    op.drop_table('alerts')
    op.drop_table('assessments')
    op.drop_table('patients')
    op.drop_table('health_workers')
    op.drop_table('facilities')
