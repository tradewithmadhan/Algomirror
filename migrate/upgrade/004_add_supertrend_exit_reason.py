"""
Migration: Add supertrend exit reason columns to strategies table

These columns store the reason and timestamp when a Supertrend exit is triggered:
- supertrend_exit_reason: Detailed reason for the exit (e.g., "supertrend_breakout (Close: 150.25, ST: 145.50)")
- supertrend_exit_triggered_at: Timestamp when the exit was triggered
"""

from sqlalchemy import text


def upgrade(db):
    """Add supertrend exit reason columns to strategies table"""

    # Check existing columns
    result = db.session.execute(text("PRAGMA table_info(strategies)"))
    columns = [row[1] for row in result.fetchall()]

    # Columns to add with their SQL definitions
    columns_to_add = [
        ('supertrend_exit_reason', 'VARCHAR(200)'),
        ('supertrend_exit_triggered_at', 'DATETIME')
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
    """Remove supertrend exit reason columns (SQLite doesn't support DROP COLUMN easily)"""
    # SQLite doesn't support DROP COLUMN directly
    # Would need to recreate table - not implemented for simplicity
    pass
