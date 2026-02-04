import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://34.228.54.218:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Employee API methods
export const employeeService = {
  // Get all employees
  getAllEmployees: async (params = {}) => {
    const response = await api.get('/api/employees/', { params });
    return response.data;
  },

  // Get single employee
  getEmployee: async (id) => {
    const response = await api.get(`/api/employees/${id}`);
    return response.data;
  },

  // Create new employee
  createEmployee: async (employeeData) => {
    const response = await api.post('/api/employees/', employeeData);
    return response.data;
  },

  // Update employee
  updateEmployee: async (id, employeeData) => {
    const response = await api.put(`/api/employees/${id}`, employeeData);
    return response.data;
  },

  // Delete employee
  deleteEmployee: async (id) => {
    const response = await api.delete(`/api/employees/${id}`);
    return response.data;
  },

  // Deactivate employee
  deactivateEmployee: async (id) => {
    const response = await api.patch(`/api/employees/${id}/deactivate`);
    return response.data;
  },

  // Activate employee
  activateEmployee: async (id) => {
    const response = await api.patch(`/api/employees/${id}/activate`);
    return response.data;
  },

  // Search employees
  searchEmployees: async (searchTerm) => {
    const response = await api.get('/api/employees/search', {
      params: { q: searchTerm }
    });
    return response.data;
  },
};

// Health check
export const healthCheck = async () => {
  const response = await api.get('/api/health');
  return response.data;
};

export default api;