import React, { useState, useEffect } from 'react';
import { employeeService } from '../services/api';
import { toast } from 'react-toastify';

const EmployeeForm = ({ employee, onClose, onSuccess }) => {
  const [formData, setFormData] = useState({
    employee_id: '',
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    department: '',
    position: '',
    salary: '',
    hire_date: '',
    is_active: true
  });

  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (employee) {
      setFormData({
        employee_id: employee.employee_id || '',
        first_name: employee.first_name || '',
        last_name: employee.last_name || '',
        email: employee.email || '',
        phone: employee.phone || '',
        department: employee.department || '',
        position: employee.position || '',
        salary: employee.salary || '',
        hire_date: employee.hire_date || '',
        is_active: employee.is_active !== undefined ? employee.is_active : true
      });
    }
  }, [employee]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
    
    // Clear error for this field
    if (errors[name]) {
      setErrors({ ...errors, [name]: '' });
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.employee_id.trim()) {
      newErrors.employee_id = 'Employee ID is required';
    }

    if (!formData.first_name.trim()) {
      newErrors.first_name = 'First name is required';
    }

    if (!formData.last_name.trim()) {
      newErrors.last_name = 'Last name is required';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }

    if (formData.salary && formData.salary < 0) {
      newErrors.salary = 'Salary must be positive';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      // Prepare data - convert empty strings to null for optional fields
      const dataToSubmit = {
        ...formData,
        phone: formData.phone || null,
        department: formData.department || null,
        position: formData.position || null,
        salary: formData.salary ? parseFloat(formData.salary) : null,
        hire_date: formData.hire_date || null
      };

      if (employee) {
        // Update existing employee
        await employeeService.updateEmployee(employee.id, dataToSubmit);
        toast.success('Employee updated successfully');
      } else {
        // Create new employee
        await employeeService.createEmployee(dataToSubmit);
        toast.success('Employee created successfully');
      }

      onSuccess();
      onClose();
    } catch (error) {
      console.error('Error saving employee:', error);
      const errorMessage = error.response?.data?.detail || 'Failed to save employee';
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{employee ? 'Edit Employee' : 'Add New Employee'}</h2>
          <button className="modal-close" onClick={onClose}>&times;</button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Employee ID *</label>
              <input
                type="text"
                name="employee_id"
                className="form-input"
                value={formData.employee_id}
                onChange={handleChange}
                disabled={employee !== null}
              />
              {errors.employee_id && (
                <span style={{ color: 'red', fontSize: '12px' }}>{errors.employee_id}</span>
              )}
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label">First Name *</label>
              <input
                type="text"
                name="first_name"
                className="form-input"
                value={formData.first_name}
                onChange={handleChange}
              />
              {errors.first_name && (
                <span style={{ color: 'red', fontSize: '12px' }}>{errors.first_name}</span>
              )}
            </div>

            <div className="form-group">
              <label className="form-label">Last Name *</label>
              <input
                type="text"
                name="last_name"
                className="form-input"
                value={formData.last_name}
                onChange={handleChange}
              />
              {errors.last_name && (
                <span style={{ color: 'red', fontSize: '12px' }}>{errors.last_name}</span>
              )}
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Email *</label>
              <input
                type="email"
                name="email"
                className="form-input"
                value={formData.email}
                onChange={handleChange}
              />
              {errors.email && (
                <span style={{ color: 'red', fontSize: '12px' }}>{errors.email}</span>
              )}
            </div>

            <div className="form-group">
              <label className="form-label">Phone</label>
              <input
                type="tel"
                name="phone"
                className="form-input"
                value={formData.phone}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Department</label>
              <input
                type="text"
                name="department"
                className="form-input"
                value={formData.department}
                onChange={handleChange}
                list="departments"
              />
              <datalist id="departments">
                <option value="Engineering" />
                <option value="Sales" />
                <option value="Marketing" />
                <option value="HR" />
                <option value="Finance" />
                <option value="Operations" />
              </datalist>
            </div>

            <div className="form-group">
              <label className="form-label">Position</label>
              <input
                type="text"
                name="position"
                className="form-input"
                value={formData.position}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Salary (₹)</label>
              <input
                type="number"
                name="salary"
                className="form-input"
                value={formData.salary}
                onChange={handleChange}
                min="0"
                step="0.01"
              />
              {errors.salary && (
                <span style={{ color: 'red', fontSize: '12px' }}>{errors.salary}</span>
              )}
            </div>

            <div className="form-group">
              <label className="form-label">Hire Date</label>
              <input
                type="date"
                name="hire_date"
                className="form-input"
                value={formData.hire_date}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="form-group">
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
              <input
                type="checkbox"
                name="is_active"
                checked={formData.is_active}
                onChange={handleChange}
              />
              <span className="form-label" style={{ margin: 0 }}>Active Employee</span>
            </label>
          </div>

          <div className="modal-footer">
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Saving...' : employee ? 'Update' : 'Create'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default EmployeeForm;