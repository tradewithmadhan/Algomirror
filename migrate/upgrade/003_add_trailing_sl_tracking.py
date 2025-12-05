"""
Migration: Add trailing SL tracking columns to strategies table

These columns track the real-time state of trailing stop loss:
- trailing_sl_active: Whether TSL is currently tracking (in profit)
- trailing_sl_peak_pnl: Highest P&L reached (for trailing calculation)
- trailing_sl_trigger_pnl: Current trigger level (exit if P&L drops below)
- trailing_sl_triggered_at: Timestamp when TSL was triggered
"""

from sqlalchemy import text


def upgrade(db):
    """Add trailing SL tracking columns to strategies table"""

    # Check existing columns
    result = db.session.execute(text("PRAGMA table_info(strategies)"))
    columns = [row[1] for row in result.fetchall()]

    # Columns to add with their SQL definitions
    columns_to_add = [
        ('trailing_sl_active', 'BOOLEAN DEFAULT 0'),
        ('trailing_sl_peak_pnl', 'FLOAT DEFAULT 0.0'),
        ('trailing_sl_trigger_pnl', 'FLOAT'),
        ('trailing_sl_triggered_at', 'DATETIME')
    ]

    added_count = 0
    for col_name, col_type in columns_to_add:
        if col_name not in columns:
            db.session.execute(text(
                f"ALTER TABLE strategies ADD COLUMN {col_name} {col_type}"
            ))
            print(f"  Added column: {col_name}")
            added_count += 1
        else:
            print(f"  Column {col_name} already exists, skipping")

    if added_count > 0:
        db.session.commit()
        print(f"  Added {added_count} new column(s)")
    else:
        print("  No new columns added")


def downgrade(db):
    """Remove trailing SL tracking columns (SQLite doesn't support DROP COLUMN easily)"""
    # SQLite doesn't support DROP COLUMN directly
    # Would need to recreate table - not implemented for simplicity
    pass
