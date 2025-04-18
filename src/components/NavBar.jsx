import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { FaUser } from 'react-icons/fa';
import logo from '../assets/image.png'

const NavBar = ({ onToggleDropdown, showDropdown }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const [searchQuery, setSearchQuery] = useState(queryParams.get('search') || '');

  const handleSearch = () => {
    const trimmed = searchQuery.trim();
    if (trimmed) {
      navigate(`/?search=${trimmed}`);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <nav className="flex items-center justify-between px-6 py-3 bg-orange-100 shadow-md">
      <div
        className="flex items-center gap-2 cursor-pointer"
        onClick={() => navigate('/')}
      >
        <img src={logo} alt="logo" className="w-25 h-20" />
        <h1 className="text-xl font-bold text-orange-600">Let Me Cook!</h1>
      </div>

      <div className="flex items-center gap-2 flex-1 max-w-xl mx-10">
        <input
          type="text"
          placeholder="Search recipes..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-orange-300"
        />
        <button
          className="px-3 py-2 bg-orange-500 text-white rounded hover:bg-orange-600"
          onClick={handleSearch}
        >
          Search
        </button>
      </div>

      <div className="flex items-center gap-4">
        <FaUser className="text-xl text-orange-700" />
      </div>
    </nav>
  );
};

export default NavBar;
