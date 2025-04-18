// src/App.jsx
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/NavBar';
import Home from './page/Home';
import RecipeDetails from './page/RecipeDetails';

const App = () => {
  const [search, setSearch] = useState('');
  const [showDropdown, setShowDropdown] = useState(false);

  const toggleDropdown = () => setShowDropdown((prev) => !prev);

  return (
    <Router>
      <Navbar search={search} setSearch={setSearch} toggleDropdown={toggleDropdown} />
      <Routes>
        <Route path="/" element={<Home search={search} showDropdown={showDropdown} />} />
        <Route path="/recipe/:id" element={<RecipeDetails />} />
      </Routes>
    </Router>
  );
};

export default App;
