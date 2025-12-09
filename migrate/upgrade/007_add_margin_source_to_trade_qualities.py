"""
Migration: Add margin_source column to trade_qualities table

This column specifies the margin calculation base:
- 'available': Uses available margin (cash + collateral) - for option sellers/hedgers
- 'cash': Uses cash only - for option buyers

Option buyers use a percentage of cash margin to calculate premium budget.
"""

from sqlalchemy import text


def upgrade(db):
    """Add margin_source column to trade_qualities table"""

    # Check existing columns
    result = db.session.execute(text("PRAGMA table_info(trade_qualities)"))
    columns = [row[1] for row in result.fetchall()]

    if 'margin_source' not in columns:
        db.session.execute(text(
            "ALTER TABLE trade_qualities ADD COLUMN margin_source VARCHAR(20) DEFAULT 'available'"
        ))
        print("  Added column: margin_source (default='available')")
        db.session.commit()
    else:
        print("  Column margin_source already exists, skipping")


def downgrade(db):
    """Remove margin_source column (SQLite doesn't support DROP COLUMN easily)"""
    # SQLite doesn't support DROP COLUMN directly
    # Would need to recreate table - not implemented for simplicity
    pass
