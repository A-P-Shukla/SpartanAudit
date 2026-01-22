from app.database import SessionLocal, engine
from app.models import Audit

# Create session
db = SessionLocal()

try:
    # Delete all audits
    deleted = db.query(Audit).delete()
    db.commit()
    print(f"✅ Cleared {deleted} audits from the database.")
except Exception as e:
    db.rollback()
    print(f"❌ Error: {e}")
finally:
    db.close()
