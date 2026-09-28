from typing import List, Tuple

PERMISSIONS: dict[str, list[str]] = {
    # Admin - todo
    "users:manage": ["admin"],
    "roles:assign": ["admin"],
    "config:manage": ["admin"],
    
    # Inventory Manager - núcleo del negocio
    "products:create": ["admin", "inventory_manager"],
    "products:update": ["admin", "inventory_manager"],
    "products:delete": ["admin", "inventory_manager"],
    "products:manage_stock": ["admin", "inventory_manager"],
    "categories:manage": ["admin", "inventory_manager"],
    "images:upload": ["admin", "inventory_manager"],
    
    # Developer - técnico
    "logs:view": ["admin", "developer"],
    "debug:tools": ["admin", "developer"],
    "metrics:view": ["admin", "developer"],
    "health:check": ["admin", "developer"],
    
    # Viewer - base
    "dashboard:view": ["admin", "inventory_manager", "developer", "viewer"],
    "catalog:view": ["admin", "inventory_manager", "developer", "viewer"],
    "reports:view": ["admin", "inventory_manager", "viewer"],
}

VALID_ROLE_COMBOS: list[list[str]] = [
    ["admin"],
    ["inventory_manager"],
    ["developer"],
    ["viewer"],
    ["admin", "developer"],
    ["viewer", "inventory_manager"],
]

def has_permission(user_roles: List[str], permission: str) -> bool:
    allowed_roles = PERMISSIONS.get(permission, [])
    return any(role in user_roles for role in allowed_roles)

def get_user_permissions(user_roles: List[str]) -> List[str]:
    return [perm for perm in PERMISSIONS if has_permission(user_roles, perm)]

def validate_roles(roles: List[str]) -> Tuple[bool, str]:
    if not roles: 
        return False, "Debe tener al menos un rol"
    if len(roles) > 2:
        return False, "El usuario no puede tener mas de 2 roles."
    
    user_roles = frozenset(roles)
    valid_combos = { frozenset(c) for c in VALID_ROLE_COMBOS }

    if user_roles not in valid_combos: 
        return False, "Combo de roles no válida."  
    
    return True, ""