from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.models import Proxy, get_db
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/admin/proxies", tags=["admin"])


# Request/Response Models
class ProxyCreate(BaseModel):
    name: str
    provider: str
    model: str
    api_key: str
    base_url: Optional[str] = None
    priority: int = 0
    description: Optional[str] = None


class ProxyUpdate(BaseModel):
    name: Optional[str] = None
    provider: Optional[str] = None
    model: Optional[str] = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    priority: Optional[int] = None
    description: Optional[str] = None
    enabled: Optional[bool] = None


class ProxyResponse(BaseModel):
    id: int
    name: str
    provider: str
    model: str
    base_url: Optional[str]
    priority: int
    enabled: bool
    description: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# Endpoints
@router.get("/", response_model=List[ProxyResponse])
def list_proxies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all proxies."""
    proxies = db.query(Proxy).offset(skip).limit(limit).all()
    return proxies


@router.get("/{proxy_id}", response_model=ProxyResponse)
def get_proxy(proxy_id: int, db: Session = Depends(get_db)):
    """Get a specific proxy by ID."""
    proxy = db.query(Proxy).filter(Proxy.id == proxy_id).first()
    if not proxy:
        raise HTTPException(status_code=404, detail="Proxy not found")
    return proxy


@router.post("/", response_model=ProxyResponse)
def create_proxy(proxy_data: ProxyCreate, db: Session = Depends(get_db)):
    """Create a new proxy configuration."""
    # Check if proxy with same name exists
    existing = db.query(Proxy).filter(Proxy.name == proxy_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Proxy with this name already exists")

    proxy = Proxy(
        name=proxy_data.name,
        provider=proxy_data.provider,
        model=proxy_data.model,
        base_url=proxy_data.base_url,
        priority=proxy_data.priority,
        description=proxy_data.description,
    )
    proxy.set_api_key(proxy_data.api_key)

    try:
        db.add(proxy)
        db.commit()
        db.refresh(proxy)
        return proxy
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to create proxy")


@router.put("/{proxy_id}", response_model=ProxyResponse)
def update_proxy(proxy_id: int, proxy_data: ProxyUpdate, db: Session = Depends(get_db)):
    """Update an existing proxy."""
    proxy = db.query(Proxy).filter(Proxy.id == proxy_id).first()
    if not proxy:
        raise HTTPException(status_code=404, detail="Proxy not found")

    # Check if new name conflicts with existing
    if proxy_data.name and proxy_data.name != proxy.name:
        existing = db.query(Proxy).filter(Proxy.name == proxy_data.name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Proxy with this name already exists")

    # Update fields
    if proxy_data.name:
        proxy.name = proxy_data.name
    if proxy_data.provider:
        proxy.provider = proxy_data.provider
    if proxy_data.model:
        proxy.model = proxy_data.model
    if proxy_data.base_url is not None:
        proxy.base_url = proxy_data.base_url
    if proxy_data.priority is not None:
        proxy.priority = proxy_data.priority
    if proxy_data.description is not None:
        proxy.description = proxy_data.description
    if proxy_data.enabled is not None:
        proxy.enabled = proxy_data.enabled
    if proxy_data.api_key:
        proxy.set_api_key(proxy_data.api_key)

    proxy.updated_at = datetime.utcnow()

    try:
        db.commit()
        db.refresh(proxy)
        return proxy
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to update proxy")


@router.delete("/{proxy_id}")
def delete_proxy(proxy_id: int, db: Session = Depends(get_db)):
    """Delete a proxy."""
    proxy = db.query(Proxy).filter(Proxy.id == proxy_id).first()
    if not proxy:
        raise HTTPException(status_code=404, detail="Proxy not found")

    db.delete(proxy)
    db.commit()
    return {"message": "Proxy deleted successfully"}


@router.post("/{proxy_id}/enable")
def enable_proxy(proxy_id: int, db: Session = Depends(get_db)):
    """Enable a proxy."""
    proxy = db.query(Proxy).filter(Proxy.id == proxy_id).first()
    if not proxy:
        raise HTTPException(status_code=404, detail="Proxy not found")

    proxy.enabled = True
    proxy.updated_at = datetime.utcnow()
    db.commit()
    return {"message": "Proxy enabled"}


@router.post("/{proxy_id}/disable")
def disable_proxy(proxy_id: int, db: Session = Depends(get_db)):
    """Disable a proxy."""
    proxy = db.query(Proxy).filter(Proxy.id == proxy_id).first()
    if not proxy:
        raise HTTPException(status_code=404, detail="Proxy not found")

    proxy.enabled = False
    proxy.updated_at = datetime.utcnow()
    db.commit()
    return {"message": "Proxy disabled"}
