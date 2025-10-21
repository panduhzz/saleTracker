"""
Azure Static Web Apps authentication utilities.
"""
from fastapi import HTTPException, Request, Depends
from typing import Dict, Optional
import json
import base64


def get_current_user(request: Request) -> Dict:
    """
    Extract user information from Azure Static Web Apps headers.
    
    Args:
        request: FastAPI request object
        
    Returns:
        Dict containing user information
        
    Raises:
        HTTPException: If user is not authenticated
    """
    # Get the client principal from SWA headers
    client_principal_header = request.headers.get('x-ms-client-principal')
    
    if not client_principal_header:
        raise HTTPException(
            status_code=401, 
            detail="Authentication required. No client principal found."
        )
    
    try:
        # Decode the base64 encoded client principal
        decoded_bytes = base64.b64decode(client_principal_header)
        client_principal = json.loads(decoded_bytes)
        
        # Extract user information
        user_id = client_principal.get('userId')
        user_details = client_principal.get('userDetails')
        provider = client_principal.get('identityProvider')
        
        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication. User ID not found."
            )
        
        return {
            "userId": user_id,
            "userDetails": user_details or "Unknown User",
            "provider": provider or "unknown",
            "claims": client_principal.get('claims', [])
        }
        
    except (json.JSONDecodeError, ValueError) as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid authentication data: {str(e)}"
        )


def get_user_id(request: Request) -> str:
    """
    Get just the user ID from the request.
    
    Args:
        request: FastAPI request object
        
    Returns:
        User ID string
    """
    user = get_current_user(request)
    return user["userId"]


def get_user_claims(request: Request) -> list:
    """
    Get user claims from the request.
    
    Args:
        request: FastAPI request object
        
    Returns:
        List of user claims
    """
    user = get_current_user(request)
    return user.get("claims", [])


def is_authenticated(request: Request) -> bool:
    """
    Check if the request is authenticated.
    
    Args:
        request: FastAPI request object
        
    Returns:
        True if authenticated, False otherwise
    """
    try:
        get_current_user(request)
        return True
    except HTTPException:
        return False


# Dependency for FastAPI endpoints
CurrentUser = Depends(get_current_user)
UserID = Depends(get_user_id)
