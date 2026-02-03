"""
CRUD operations for Employee Management
"""
from typing import Optional, List, Dict, Any
from mysql.connector import Error
from datetime import date
from decimal import Decimal
from app.db.database import get_db_connection


class EmployeeCRUD:
    """Class containing all CRUD operations for employees"""
    
    @staticmethod
    def create_employee(employee_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create a new employee record
        
        Args:
            employee_data: Dictionary containing employee information
            
        Returns:
            Created employee data with ID or None if failed
        """
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
            INSERT INTO employees 
            (employee_id, first_name, last_name, email, phone, department, 
             position, salary, hire_date, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            values = (
                employee_data.get('employee_id'),
                employee_data.get('first_name'),
                employee_data.get('last_name'),
                employee_data.get('email'),
                employee_data.get('phone'),
                employee_data.get('department'),
                employee_data.get('position'),
                employee_data.get('salary'),
                employee_data.get('hire_date'),
                employee_data.get('is_active', True)
            )
            
            cursor.execute(query, values)
            connection.commit()
            
            # Get the created employee
            employee_id = cursor.lastrowid
            cursor.close()
            
            return EmployeeCRUD.get_employee_by_id(employee_id)
            
        except Error as e:
            print(f"Error creating employee: {e}")
            if connection:
                connection.rollback()
            raise Exception(f"Database error: {str(e)}")
    
    @staticmethod
    def get_all_employees(
        skip: int = 0, 
        limit: int = 100,
        department: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve all employee records with optional filtering
        
        Args:
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            department: Filter by department
            is_active: Filter by active status
            
        Returns:
            List of employee dictionaries
        """
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = "SELECT * FROM employees WHERE 1=1"
            params = []
            
            if department:
                query += " AND department = %s"
                params.append(department)
            
            if is_active is not None:
                query += " AND is_active = %s"
                params.append(is_active)
            
            query += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
            params.extend([limit, skip])
            
            cursor.execute(query, params)
            employees = cursor.fetchall()
            cursor.close()
            
            # Convert date and datetime objects to strings
            for emp in employees:
                if emp.get('hire_date'):
                    emp['hire_date'] = emp['hire_date'].isoformat()
                if emp.get('created_at'):
                    emp['created_at'] = emp['created_at'].isoformat()
                if emp.get('updated_at'):
                    emp['updated_at'] = emp['updated_at'].isoformat()
                if emp.get('salary'):
                    emp['salary'] = float(emp['salary'])
            
            return employees
            
        except Error as e:
            print(f"Error retrieving employees: {e}")
            raise Exception(f"Database error: {str(e)}")
    
    @staticmethod
    def get_employee_by_id(employee_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single employee by database ID
        
        Args:
            employee_id: Database ID of the employee
            
        Returns:
            Employee dictionary or None if not found
        """
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = "SELECT * FROM employees WHERE id = %s"
            cursor.execute(query, (employee_id,))
            employee = cursor.fetchone()
            cursor.close()
            
            if employee:
                # Convert date and datetime objects
                if employee.get('hire_date'):
                    employee['hire_date'] = employee['hire_date'].isoformat()
                if employee.get('created_at'):
                    employee['created_at'] = employee['created_at'].isoformat()
                if employee.get('updated_at'):
                    employee['updated_at'] = employee['updated_at'].isoformat()
                if employee.get('salary'):
                    employee['salary'] = float(employee['salary'])
            
            return employee
            
        except Error as e:
            print(f"Error retrieving employee: {e}")
            raise Exception(f"Database error: {str(e)}")
    
    @staticmethod
    def get_employee_by_employee_id(emp_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single employee by employee ID (not database ID)
        
        Args:
            emp_id: Employee ID string
            
        Returns:
            Employee dictionary or None if not found
        """
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = "SELECT * FROM employees WHERE employee_id = %s"
            cursor.execute(query, (emp_id,))
            employee = cursor.fetchone()
            cursor.close()
            
            if employee:
                # Convert date and datetime objects
                if employee.get('hire_date'):
                    employee['hire_date'] = employee['hire_date'].isoformat()
                if employee.get('created_at'):
                    employee['created_at'] = employee['created_at'].isoformat()
                if employee.get('updated_at'):
                    employee['updated_at'] = employee['updated_at'].isoformat()
                if employee.get('salary'):
                    employee['salary'] = float(employee['salary'])
            
            return employee
            
        except Error as e:
            print(f"Error retrieving employee: {e}")
            raise Exception(f"Database error: {str(e)}")
    
    @staticmethod
    def update_employee(employee_id: int, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an employee record
        
        Args:
            employee_id: Database ID of the employee
            update_data: Dictionary containing fields to update
            
        Returns:
            Updated employee data or None if not found
        """
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # Build dynamic update query
            update_fields = []
            values = []
            
            for key, value in update_data.items():
                if value is not None:
                    update_fields.append(f"{key} = %s")
                    values.append(value)
            
            if not update_fields:
                return EmployeeCRUD.get_employee_by_id(employee_id)
            
            query = f"UPDATE employees SET {', '.join(update_fields)} WHERE id = %s"
            values.append(employee_id)
            
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            
            if cursor.rowcount == 0:
                return None
            
            return EmployeeCRUD.get_employee_by_id(employee_id)
            
        except Error as e:
            print(f"Error updating employee: {e}")
            if connection:
                connection.rollback()
            raise Exception(f"Database error: {str(e)}")
    
    @staticmethod
    def delete_employee(employee_id: int) -> bool:
        """
        Delete an employee record (hard delete)
        
        Args:
            employee_id: Database ID of the employee
            
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            query = "DELETE FROM employees WHERE id = %s"
            cursor.execute(query, (employee_id,))
            connection.commit()
            
            deleted = cursor.rowcount > 0
            cursor.close()
            
            return deleted
            
        except Error as e:
            print(f"Error deleting employee: {e}")
            if connection:
                connection.rollback()
            raise Exception(f"Database error: {str(e)}")
    
    @staticmethod
    def soft_delete_employee(employee_id: int) -> Optional[Dict[str, Any]]:
        """
        Soft delete an employee (set is_active to False)
        
        Args:
            employee_id: Database ID of the employee
            
        Returns:
            Updated employee data or None if not found
        """
        return EmployeeCRUD.update_employee(employee_id, {'is_active': False})
    
    @staticmethod
    def get_employee_count(department: Optional[str] = None, is_active: Optional[bool] = None) -> int:
        """
        Get total count of employees
        
        Args:
            department: Filter by department
            is_active: Filter by active status
            
        Returns:
            Total count of employees
        """
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            query = "SELECT COUNT(*) as count FROM employees WHERE 1=1"
            params = []
            
            if department:
                query += " AND department = %s"
                params.append(department)
            
            if is_active is not None:
                query += " AND is_active = %s"
                params.append(is_active)
            
            cursor.execute(query, params)
            result = cursor.fetchone()
            cursor.close()
            
            return result[0] if result else 0
            
        except Error as e:
            print(f"Error counting employees: {e}")
            raise Exception(f"Database error: {str(e)}")
    
    @staticmethod
    def search_employees(search_term: str) -> List[Dict[str, Any]]:
        """
        Search employees by name, email, or employee ID
        
        Args:
            search_term: Search string
            
        Returns:
            List of matching employees
        """
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT * FROM employees 
            WHERE first_name LIKE %s 
               OR last_name LIKE %s 
               OR email LIKE %s 
               OR employee_id LIKE %s
            ORDER BY created_at DESC
            """
            
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern))
            employees = cursor.fetchall()
            cursor.close()
            
            # Convert date and datetime objects
            for emp in employees:
                if emp.get('hire_date'):
                    emp['hire_date'] = emp['hire_date'].isoformat()
                if emp.get('created_at'):
                    emp['created_at'] = emp['created_at'].isoformat()
                if emp.get('updated_at'):
                    emp['updated_at'] = emp['updated_at'].isoformat()
                if emp.get('salary'):
                    emp['salary'] = float(emp['salary'])
            
            return employees
            
        except Error as e:
            print(f"Error searching employees: {e}")
            raise Exception(f"Database error: {str(e)}")