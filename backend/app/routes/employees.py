"""
FastAPI routes for Employee Management API
"""
from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional, List
from app.models.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    EmployeeListResponse,
    MessageResponse,
    ErrorResponse
)
from app.utils.crud import EmployeeCRUD

router = APIRouter(prefix="/api/employees", tags=["employees"])


@router.post(
    "/",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new employee",
    description="Create a new employee record with the provided information"
)
async def create_employee(employee: EmployeeCreate):
    """Create a new employee"""
    try:
        # Convert Pydantic model to dict
        employee_data = employee.model_dump()
        
        # Check if employee_id already exists
        existing = EmployeeCRUD.get_employee_by_employee_id(employee_data['employee_id'])
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Employee with ID {employee_data['employee_id']} already exists"
            )
        
        # Create employee
        created_employee = EmployeeCRUD.create_employee(employee_data)
        
        if not created_employee:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create employee"
            )
        
        return created_employee
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=EmployeeListResponse,
    summary="Get all employees",
    description="Retrieve all employee records with optional filtering and pagination"
)
async def get_all_employees(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    department: Optional[str] = Query(None, description="Filter by department"),
    is_active: Optional[bool] = Query(None, description="Filter by active status")
):
    """Get all employees with optional filtering"""
    try:
        employees = EmployeeCRUD.get_all_employees(
            skip=skip,
            limit=limit,
            department=department,
            is_active=is_active
        )
        
        total = EmployeeCRUD.get_employee_count(
            department=department,
            is_active=is_active
        )
        
        return {
            "total": total,
            "employees": employees
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/search",
    response_model=List[EmployeeResponse],
    summary="Search employees",
    description="Search employees by name, email, or employee ID"
)
async def search_employees(
    q: str = Query(..., min_length=1, description="Search term")
):
    """Search employees"""
    try:
        employees = EmployeeCRUD.search_employees(q)
        return employees
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse,
    summary="Get employee by ID",
    description="Retrieve a specific employee by their database ID"
)
async def get_employee(employee_id: int):
    """Get a single employee by ID"""
    try:
        employee = EmployeeCRUD.get_employee_by_id(employee_id)
        
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID {employee_id} not found"
            )
        
        return employee
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse,
    summary="Update employee",
    description="Update an existing employee's information"
)
async def update_employee(employee_id: int, employee_update: EmployeeUpdate):
    """Update an employee"""
    try:
        # Check if employee exists
        existing = EmployeeCRUD.get_employee_by_id(employee_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID {employee_id} not found"
            )
        
        # Get only the fields that were actually provided
        update_data = employee_update.model_dump(exclude_unset=True)
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        # Check if employee_id is being changed and if it already exists
        if 'employee_id' in update_data:
            existing_emp = EmployeeCRUD.get_employee_by_employee_id(update_data['employee_id'])
            if existing_emp and existing_emp['id'] != employee_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Employee with ID {update_data['employee_id']} already exists"
                )
        
        # Update employee
        updated_employee = EmployeeCRUD.update_employee(employee_id, update_data)
        
        if not updated_employee:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update employee"
            )
        
        return updated_employee
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete(
    "/{employee_id}",
    response_model=MessageResponse,
    summary="Delete employee",
    description="Permanently delete an employee record"
)
async def delete_employee(employee_id: int):
    """Delete an employee (hard delete)"""
    try:
        # Check if employee exists
        existing = EmployeeCRUD.get_employee_by_id(employee_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID {employee_id} not found"
            )
        
        # Delete employee
        deleted = EmployeeCRUD.delete_employee(employee_id)
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete employee"
            )
        
        return {
            "message": f"Employee with ID {employee_id} deleted successfully",
            "success": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.patch(
    "/{employee_id}/deactivate",
    response_model=EmployeeResponse,
    summary="Deactivate employee",
    description="Soft delete an employee by setting their status to inactive"
)
async def deactivate_employee(employee_id: int):
    """Deactivate an employee (soft delete)"""
    try:
        # Check if employee exists
        existing = EmployeeCRUD.get_employee_by_id(employee_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID {employee_id} not found"
            )
        
        # Deactivate employee
        updated_employee = EmployeeCRUD.soft_delete_employee(employee_id)
        
        if not updated_employee:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to deactivate employee"
            )
        
        return updated_employee
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.patch(
    "/{employee_id}/activate",
    response_model=EmployeeResponse,
    summary="Activate employee",
    description="Reactivate an inactive employee"
)
async def activate_employee(employee_id: int):
    """Activate an employee"""
    try:
        # Check if employee exists
        existing = EmployeeCRUD.get_employee_by_id(employee_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID {employee_id} not found"
            )
        
        # Activate employee
        updated_employee = EmployeeCRUD.update_employee(employee_id, {'is_active': True})
        
        if not updated_employee:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to activate employee"
            )
        
        return updated_employee
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )