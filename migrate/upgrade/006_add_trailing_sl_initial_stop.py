"""
Migration: Add trailing_sl_initial_stop column to strategies table

This column stores the initial stop level when TSL first activates.
Part of the AFL-style ratcheting trailing stop implementation:
- initial_stop: First calculated stop when P&L goes positive
- current_stop (trailing_sl_trigger_pnl): Ratchets UP only, never down
"""

from sqlalchemy import text


def upgrade(db):
    """Add trailing_sl_initial_stop column to strategies table"""

    # Check existing columns
    result = db.session.execute(text("PRAGMA table_info(strategies)"))
    columns = [row[1] for row in result.fetchall()]

    if 'trailing_sl_initial_stop' not in columns:
        db.session.execute(text(
            "ALTER TABLE strategies ADD COLUMN trailing_sl_initial_stop FLOAT"
        ))
        print("  Added column: trailing_sl_initial_stop")
        db.session.commit()
    else:
        print("  Column trailing_sl_initial_stop already exists, skipping")


def downgrade(db):
    """Remove trailing_sl_initial_stop column (SQLite doesn't support DROP COLUMN easily)"""
    # SQLite doesn't support DROP COLUMN directly
    # Would need to recreate table - not implemented for simplicity
    pass
