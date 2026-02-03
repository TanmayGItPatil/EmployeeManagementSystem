import React, { useState } from 'react';
import { FaSearch } from 'react-icons/fa';
import { employeeService } from '../services/api';
import { toast } from 'react-toastify';

const SearchBar = ({ onSearchResults }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    
    if (!searchTerm.trim()) {
      toast.info('Please enter a search term');
      return;
    }

    setLoading(true);
    try {
      const results = await employeeService.searchEmployees(searchTerm);
      onSearchResults(results);
      
      if (results.length === 0) {
        toast.info('No employees found matching your search');
      } else {
        toast.success(`Found ${results.length} employee(s)`);
      }
    } catch (error) {
      console.error('Error searching employees:', error);
      toast.error('Failed to search employees');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setSearchTerm('');
    onSearchResults(null);
  };

  return (
    <form className="search-box" onSubmit={handleSearch}>
      <input
        type="text"
        className="search-input"
        placeholder="Search by name, email, or employee ID..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <button 
        type="submit" 
        className="btn btn-primary"
        disabled={loading}
      >
        <FaSearch /> {loading ? 'Searching...' : 'Search'}
      </button>
      {searchTerm && (
        <button 
          type="button" 
          className="btn btn-secondary"
          onClick={handleClear}
        >
          Clear
        </button>
      )}
    </form>
  );
};

export default SearchBar;