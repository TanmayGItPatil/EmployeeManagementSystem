import React, { useState, useEffect } from 'react';
import { FaEdit, FaTrash, FaToggleOn, FaToggleOff, FaUserSlash } from 'react-icons/fa';
import { employeeService } from '../services/api';
import { toast } from 'react-toastify';

const EmployeeList = ({ onEdit, refresh }) => {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    department: '',
    is_active: ''
  });

  useEffect(() => {
    fetchEmployees();
  }, [refresh, filters]);

  const fetchEmployees = async () => {
    try {
      setLoading(true);
      const params = {};
      
      if (filters.department) {
        params.department = filters.department;
      }
      
      if (filters.is_active !== '') {
        params.is_active = filters.is_active === 'true';
      }

      const data = await employeeService.getAllEmployees(params);
      setEmployees(data.employees || []);
    } catch (error) {
      console.error('Error fetching employees:', error);
      toast.error('Failed to fetch employees');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id, employeeName) => {
    if (window.confirm(`Are you sure you want to delete ${employeeName}?`)) {
      try {
        await employeeService.deleteEmployee(id);
        toast.success('Employee deleted successfully');
        fetchEmployees();
      } catch (error) {
        console.error('Error deleting employee:', error);
        toast.error('Failed to delete employee');
      }
    }
  };

  const handleToggleStatus = async (id, currentStatus, employeeName) => {
    try {
      if (currentStatus) {
        await employeeService.deactivateEmployee(id);
        toast.success(`${employeeName} deactivated`);
      } else {
        await employeeService.activateEmployee(id);
        toast.success(`${employeeName} activated`);
      }
      fetchEmployees();
    } catch (error) {
      console.error('Error toggling status:', error);
      toast.error('Failed to update status');
    }
  };

  const getDepartments = () => {
    const depts = [...new Set(employees.map(emp => emp.department).filter(Boolean))];
    return depts.sort();
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  if (employees.length === 0) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">
          <FaUserSlash />
        </div>
        <h3>No Employees Found</h3>
        <p>Add your first employee to get started</p>
      </div>
    );
  }

  return (
    <div>
      {/* Filters */}
      <div className="filters">
        <div className="filter-group">
          <label className="filter-label">Department</label>
          <select
            className="form-select"
            value={filters.department}
            onChange={(e) => setFilters({ ...filters, department: e.target.value })}
          >
            <option value="">All Departments</option>
            {getDepartments().map(dept => (
              <option key={dept} value={dept}>{dept}</option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label className="filter-label">Status</label>
          <select
            className="form-select"
            value={filters.is_active}
            onChange={(e) => setFilters({ ...filters, is_active: e.target.value })}
          >
            <option value="">All Status</option>
            <option value="true">Active</option>
            <option value="false">Inactive</option>
          </select>
        </div>
      </div>

      {/* Table */}
      <div className="table-container">
        <table className="table">
          <thead>
            <tr>
              <th>Employee ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Department</th>
              <th>Position</th>
              <th>Salary</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {employees.map((employee) => (
              <tr key={employee.id}>
                <td>{employee.employee_id}</td>
                <td>{`${employee.first_name} ${employee.last_name}`}</td>
                <td>{employee.email}</td>
                <td>{employee.phone || 'N/A'}</td>
                <td>{employee.department || 'N/A'}</td>
                <td>{employee.position || 'N/A'}</td>
                <td>
                  {employee.salary 
                    ? `₹${parseFloat(employee.salary).toLocaleString('en-IN')}` 
                    : 'N/A'}
                </td>
                <td>
                  <span className={`badge ${employee.is_active ? 'badge-success' : 'badge-danger'}`}>
                    {employee.is_active ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td>
                  <div className="actions">
                    <button
                      className="btn btn-primary btn-sm"
                      onClick={() => onEdit(employee)}
                      title="Edit"
                    >
                      <FaEdit />
                    </button>
                    <button
                      className={`btn ${employee.is_active ? 'btn-warning' : 'btn-success'} btn-sm`}
                      onClick={() => handleToggleStatus(
                        employee.id, 
                        employee.is_active,
                        `${employee.first_name} ${employee.last_name}`
                      )}
                      title={employee.is_active ? 'Deactivate' : 'Activate'}
                    >
                      {employee.is_active ? <FaToggleOn /> : <FaToggleOff />}
                    </button>
                    <button
                      className="btn btn-danger btn-sm"
                      onClick={() => handleDelete(
                        employee.id,
                        `${employee.first_name} ${employee.last_name}`
                      )}
                      title="Delete"
                    >
                      <FaTrash />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div style={{ marginTop: '20px', textAlign: 'center', color: '#6b7280' }}>
        Total Employees: {employees.length}
      </div>
    </div>
  );
};

export default EmployeeList;