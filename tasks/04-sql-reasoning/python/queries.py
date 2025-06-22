# tasks/04‑sql‑reasoning/python/queries.py
from pathlib import Path

# --- path to donations.db --------------------------------------------------
DB_PATH = Path(__file__).resolve().parent.parent / "donations.db"

# --- Task A ---------------------------------------------------------------
SQL_A = """
    SELECT      C.id AS campaign_id,
                SUM(P.amount_thb) AS total_thb,
                ROUND(SUM(P.amount_thb) * 1.0 / C.target_thb, 4) AS pct_of_target
    FROM        pledge P
    LEFT JOIN   campaign C on C.id = P.campaign_id
    GROUP BY    C.id 
    ORDER BY    pct_of_target DESC;
"""

# --- Task B ---------------------------------------------------------------
SQL_B = """
    WITH ordered_global AS (
        SELECT P.amount_thb
        FROM pledge P
        ORDER BY P.amount_thb
    ),
    ordered_thailand AS (
        SELECT P.amount_thb
        FROM pledge P
        JOIN donor D ON D.id = P.donor_id
        WHERE D.country = 'Thailand'
        ORDER BY P.amount_thb
    ),

    global_p90 AS (
        SELECT
            'global' AS scope,
            (SELECT amount_thb
            FROM ordered_global
            LIMIT 1 
            OFFSET CAST(CEIL(0.9 * (SELECT COUNT(*) FROM ordered_global)) - 1 AS INTEGER)
            ) AS p90_thb
    ),

    thailand_p90 AS (
        SELECT
            'thailand' AS scope,
            (SELECT amount_thb
            FROM ordered_thailand
            LIMIT 1 OFFSET CAST(CEIL(0.9 * (SELECT COUNT(*) FROM ordered_thailand)) - 1 AS INTEGER)
            ) AS p90_thb
    )

    SELECT * FROM global_p90
    UNION ALL
    SELECT * FROM thailand_p90;
"""

# --- (skipped) indexes -----------------------------------------------------
INDEXES: list[str] = [
    'CREATE INDEX idx_pledge_campaign_id ON pledge(campaign_id);', 
    'CREATE INDEX idx_donor_country_id ON donor(country, id);'
] # left empty on purpose
