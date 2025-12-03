"""
Migration: Add product column to strategy_executions table

This column stores the actual order product type (MIS, NRML, CNC) for each execution.
Previously this was being read from leg.product_type which stored 'options'/'futures'
instead of the actual broker product type.
"""

from sqlalchemy import text


def upgrade(db):
    """Add product column to strategy_executions table"""

    # Check if column already exists
    result = db.session.execute(text("PRAGMA table_info(strategy_executions)"))
    columns = [row[1] for row in result.fetchall()]

    if 'product' not in columns:
        db.session.execute(text(
            "ALTER TABLE strategy_executions ADD COLUMN product VARCHAR(10)"
        ))
        db.session.commit()
        print("Added product column to strategy_executions")

        # Backfill existing executions with product from their strategy's product_order_type
        # This joins strategy_executions -> strategies to get the product_order_type
        db.session.execute(text("""
            UPDATE strategy_executions
            SET product = (
                SELECT COALESCE(s.product_order_type, 'MIS')
                FROM strategies s
                WHERE s.id = strategy_executions.strategy_id
            )
            WHERE product IS NULL
        """))
        db.session.commit()
        print("Backfilled product values from strategy.product_order_type")
    else:
        print("Column already exists, skipping")


def downgrade(db):
    """Remove product column (SQLite doesn't support DROP COLUMN easily)"""
    # SQLite doesn't support DROP COLUMN directly
    # Would need to recreate table - not implemented for simplicity
    pass
