from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app import models as app_models
from app import oauth2
from app.database import get_db
from app.isha import models, schemas
from app.utils import Language, Philosophy
from .utils import get_sutra_or_404
import logging

# Logger setup
logger = logging.getLogger(__name__)

# FastAPI Router
router = APIRouter(prefix="/sutras", tags=["Bhashyams"])


def get_bhashyam_or_404(sutra_no: int, language: Language, philosophy: Philosophy, db: Session):
    """Retrieve a Bhashyam object or raise a 404 error."""
    logger.info(f"Fetching Bhashyam: Sutra {sutra_no}, Language {language}, Philosophy {philosophy}")
    db_bhashyam = (
        db.query(models.Bhashyam)
        .join(models.Sutra, models.Bhashyam.sutra_id == models.Sutra.id)
        .filter(models.Sutra.number == sutra_no)
        .filter(models.Bhashyam.language == language)
        .filter(models.Bhashyam.philosophy == philosophy)
        .first()
    )
    if not db_bhashyam:
        logger.error(f"Bhashyam not found for Sutra {sutra_no}, Language {language}, Philosophy {philosophy}")
        raise HTTPException(status_code=404, detail="Bhashyam not found.")
    return db_bhashyam


@router.get("/{sutra_no}/bhashyam", response_model=schemas.BhashyamOut)
def get_bhashyam(
    sutra_no: int,
    lang: Language = Language.en,
    philosophy: Philosophy = Philosophy.advaita,
    db: Session = Depends(get_db),
):
    """Retrieve a Bhashyam for a specific Sutra."""
    sutra = get_sutra_or_404(sutra_no, db)
    return get_bhashyam_or_404(sutra_no, lang, philosophy, db)


@router.post("/{sutra_no}/bhashyam", status_code=status.HTTP_201_CREATED)
def add_bhashyam(
    sutra_no: int,
    bhashyam: schemas.BhashyamCreate,
    db: Session = Depends(get_db),
    current_user: app_models.User = Depends(oauth2.get_current_user),
):
    """Add a new Bhashyam."""
    logger.info(f"Adding Bhashyam for Sutra {sutra_no} by User {current_user.id}")
    
    # Validate if Sutra exists
    sutra = get_sutra_or_404(sutra_no, db)

    # Check for existing Bhashyam
    db_bhashyam = (
        db.query(models.Bhashyam)
        .filter(models.Bhashyam.sutra_id == sutra.id)
        .filter(models.Bhashyam.language == bhashyam.language)
        .filter(models.Bhashyam.philosophy == bhashyam.philosophy)
        .first()
    )
    if db_bhashyam:
        logger.warning(f"Bhashyam for Sutra {sutra_no} already exists!")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Bhashyam for Sutra {sutra_no} already exists!"
        )

    # Create the new Bhashyam
    new_bhashyam = models.Bhashyam(
        sutra_id=sutra.id,
        language=bhashyam.language,
        philosophy=bhashyam.philosophy,
        text=bhashyam.text,
    )
    db.add(new_bhashyam)
    db.commit()
    db.refresh(new_bhashyam)

    logger.info(f"Bhashyam created with ID: {new_bhashyam.id}")
    return {"id": new_bhashyam.id}


@router.put("/{sutra_no}/bhashyam", status_code=status.HTTP_204_NO_CONTENT)
def update_bhashyam(
    sutra_no: int,
    lang: Language,
    phil: Philosophy,
    bhashyam: schemas.BhashyamUpdate,
    db: Session = Depends(get_db),
    current_user: app_models.User = Depends(oauth2.get_current_user),
):
    """Update an existing Bhashyam."""
    logger.info(f"Updating Bhashyam for Sutra {sutra_no}, Language {lang}, Philosophy {phil}")

    # Validate if Sutra and Bhashyam exist
    sutra = get_sutra_or_404(sutra_no, db)
    db_bhashyam = get_bhashyam_or_404(sutra_no, lang, phil, db)

    # Update fields
    for key, value in bhashyam.dict(exclude_unset=True).items():
        setattr(db_bhashyam, key, value)

    db.commit()
    logger.info(f"Bhashyam updated for Sutra {sutra_no}")


@router.delete("/{sutra_no}/bhashyam", status_code=status.HTTP_204_NO_CONTENT)
def delete_bhashyam(
    sutra_no: int,
    lang: Language,
    phil: Philosophy,
    db: Session = Depends(get_db),
    current_admin: app_models.User = Depends(oauth2.get_current_admin),
):
    """Delete a Bhashyam."""
    logger.info(f"Deleting Bhashyam for Sutra {sutra_no}, Language {lang}, Philosophy {phil}")

    # Validate if Sutra and Bhashyam exist
    sutra = get_sutra_or_404(sutra_no, db)
    bhashyam = get_bhashyam_or_404(sutra_no, lang, phil, db)

    # Delete the Bhashyam
    db.delete(bhashyam)
    db.commit()
    logger.info(f"Bhashyam deleted for Sutra {sutra_no}")
