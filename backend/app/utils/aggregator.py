from sqlalchemy import func
from app.database.session import SessionLocal
from app.models.issues import Issue
from app.models.daily_stats import DailyStats

def aggregate_issue_counts() -> None:
    """
    Counts current issues by status and writes a row into daily_stats
    for each status.
    """
    db = SessionLocal()
    try:
        results = (
            db.query(Issue.status, func.count(Issue.id))
              .group_by(Issue.status)
              .all()
        )

        for status, cnt in results:
            stat = DailyStats(status=status, count=cnt)
            db.add(stat)

        db.commit()
    finally:
        db.close()
