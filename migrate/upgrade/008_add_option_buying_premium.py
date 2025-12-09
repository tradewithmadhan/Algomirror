"""
Migration: Add option_buying_premium columns to margin_requirements table

These columns allow users to configure the premium per lot for option buying.
Used to calculate lot size based on cash margin for option buyers.
"""

from sqlalchemy import text


def upgrade(db):
    """Add option_buying_premium columns to margin_requirements table"""

    # Check existing columns
    result = db.session.execute(text("PRAGMA table_info(margin_requirements)"))
    columns = [row[1] for row in result.fetchall()]

    if 'option_buying_premium' not in columns:
        db.session.execute(text(
            "ALTER TABLE margin_requirements ADD COLUMN option_buying_premium FLOAT DEFAULT 20000"
        ))
        print("  Added column: option_buying_premium (default=20000)")
        db.session.commit()
    else:
        print("  Column option_buying_premium already exists, skipping")

    if 'sensex_option_buying_premium' not in columns:
        db.session.execute(text(
            "ALTER TABLE margin_requirements ADD COLUMN sensex_option_buying_premium FLOAT DEFAULT 20000"
        ))
        print("  Added column: sensex_option_buying_premium (default=20000)")
        db.session.commit()
    else:
        print("  Column sensex_option_buying_premium already exists, skipping")


def downgrade(db):
    """Remove option_buying_premium columns (SQLite doesn't support DROP COLUMN easily)"""
    # SQLite doesn't support DROP COLUMN directly
    # Would need to recreate table - not implemented for simplicity
    pass
