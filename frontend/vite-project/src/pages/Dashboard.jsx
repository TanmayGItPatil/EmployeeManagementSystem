import React, { useState, useEffect } from 'react';
import { FaUserPlus, FaUsers, FaUserCheck, FaUserTimes } from 'react-icons/fa';
import EmployeeList from '../components/EmployeeList';
import EmployeeForm from '../components/EmployeeForm';
import SearchBar from '../components/SearchBar';
import { employeeService } from '../services/api';

const Dashboard = () => {
  const [showForm, setShowForm] = useState(false);
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);
  const [stats, setStats] = useState({
    total: 0,
    active: 0,
    inactive: 0
  });
  const [searchResults, setSearchResults] = useState(null);

  useEffect(() => {
    fetchStats();
  }, [refreshKey]);

  const fetchStats = async () => {
    try {
      const allData = await employeeService.getAllEmployees();
      const activeData = await employeeService.getAllEmployees({ is_active: true });
      const inactiveData = await employeeService.getAllEmployees({ is_active: false });

      setStats({
        total: allData.total || 0,
        active: activeData.total || 0,
        inactive: inactiveData.total || 0
      });
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const handleAddEmployee = () => {
    setSelectedEmployee(null);
    setShowForm(true);
  };

  const handleEditEmployee = (employee) => {
    setSelectedEmployee(employee);
    setShowForm(true);
  };

  const handleCloseForm = () => {
    setShowForm(false);
    setSelectedEmployee(null);
  };

  const handleFormSuccess = () => {
    setRefreshKey(prev => prev + 1);
  };

  const handleSearchResults = (results) => {
    setSearchResults(results);
  };

  return (
    <div>
      {/* Header */}
      <div className="header">
        <div className="container">
          <h1>Employee Management System</h1>
          <p>Manage your organization's workforce efficiently</p>
        </div>
      </div>

      {/* Main Content */}
      <div className="container">
        {/* Stats */}
        <div className="stats">
          <div className="stat-card">
            <div className="stat-label">Total Employees</div>
            <div className="stat-value" style={{ color: '#667eea' }}>
              <FaUsers style={{ fontSize: '24px', marginRight: '10px' }} />
              {stats.total}
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-label">Active Employees</div>
            <div className="stat-value" style={{ color: '#10b981' }}>
              <FaUserCheck style={{ fontSize: '24px', marginRight: '10px' }} />
              {stats.active}
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-label">Inactive Employees</div>
            <div className="stat-value" style={{ color: '#ef4444' }}>
              <FaUserTimes style={{ fontSize: '24px', marginRight: '10px' }} />
              {stats.inactive}
            </div>
          </div>
        </div>

        {/* Card */}
        <div className="card">
          {/* Actions Bar */}
          <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center',
            marginBottom: '20px',
            flexWrap: 'wrap',
            gap: '10px'
          }}>
            <h2 style={{ margin: 0 }}>Employees</h2>
            <button className="btn btn-primary" onClick={handleAddEmployee}>
              <FaUserPlus /> Add Employee
            </button>
          </div>

          {/* Search Bar */}
          <SearchBar onSearchResults={handleSearchResults} />

          {/* Employee List */}
          {searchResults ? (
            <div>
              <h3 style={{ marginBottom: '20px', color: '#374151' }}>
                Search Results ({searchResults.length})
              </h3>
              {searchResults.length > 0 ? (
                <div className="table-container">
                  <table className="table">
                    <thead>
                      <tr>
                        <th>Employee ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Department</th>
                        <th>Position</th>
                        <th>Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      {searchResults.map((employee) => (
                        <tr key={employee.id} onClick={() => handleEditEmployee(employee)} style={{ cursor: 'pointer' }}>
                          <td>{employee.employee_id}</td>
                          <td>{`${employee.first_name} ${employee.last_name}`}</td>
                          <td>{employee.email}</td>
                          <td>{employee.department || 'N/A'}</td>
                          <td>{employee.position || 'N/A'}</td>
                          <td>
                            <span className={`badge ${employee.is_active ? 'badge-success' : 'badge-danger'}`}>
                              {employee.is_active ? 'Active' : 'Inactive'}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="empty-state">
                  <p>No results found</p>
                </div>
              )}
            </div>
          ) : (
            <EmployeeList 
              onEdit={handleEditEmployee}
              refresh={refreshKey}
            />
          )}
        </div>
      </div>

      {/* Form Modal */}
      {showForm && (
        <EmployeeForm
          employee={selectedEmployee}
          onClose={handleCloseForm}
          onSuccess={handleFormSuccess}
        />
      )}
    </div>
  );
};

export default Dashboard;