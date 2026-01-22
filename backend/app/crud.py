from sqlalchemy.orm import Session
from sqlalchemy import desc
from . import models, schemas

def get_audit_by_url(db: Session, repo_url: str):
    """Fetches an existing audit record from the DB by its repo URL."""
    return db.query(models.Audit).filter(models.Audit.repo_url == repo_url).first()

def get_audit(db: Session, audit_id: int):
    """Fetches a single audit record from the DB by its ID."""
    return db.query(models.Audit).filter(models.Audit.id == audit_id).first()

def get_audits(db: Session, skip: int = 0, limit: int = 100):
    """Fetches a list of all audits, ordered by the most recent."""
    return db.query(models.Audit).order_by(desc(models.Audit.id)).offset(skip).limit(limit).all()

def create_audit(db: Session, audit_data: schemas.AuditCreate) -> models.Audit:
    """Creates a new audit record in the database."""
    db_audit = models.Audit(**audit_data.model_dump())
    db.add(db_audit)
    db.commit()
    db.refresh(db_audit)
    return db_audit