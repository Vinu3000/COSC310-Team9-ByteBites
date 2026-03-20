from fastapi import Depends, HTTPException
from app.api.dependencies import get_current_user

def require_role(*allowed_roles: str):
    # Returns a dependency that checks the user's role
    def check(current_user=Depends(get_current_user)):
        if current_user["role"] not in allowed_roles:
            raise HTTPException(status_code=403, detail="You don't have permission")
        return current_user
    return check