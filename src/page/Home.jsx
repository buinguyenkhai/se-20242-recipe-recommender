// src/pages/Home.jsx
import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import recipes from '../utils/recipe';
import FilterDropdown from '../components/FilterDropdown';
import RecipeCard from '../components/RecipeCard';

const Home = () => {
  const location = useLocation();
  const [dropdownVisible, setDropdownVisible] = useState(false);
  const [filteredRecipes, setFilteredRecipes] = useState(recipes);

  const toggleDropdown = () => setDropdownVisible(prev => !prev);

  const applyFilters = ({ tags, ingredients }) => {
    let filtered = recipes;

    if (tags.length) {
      filtered = filtered.filter(r =>
        tags.every(tag => r.tags.includes(tag))
      );
    }

    if (ingredients.length) {
      filtered = filtered.filter(r =>
        ingredients.every(ing => r.ingredients.includes(ing))
      );
    }

    setFilteredRecipes(filtered);
  };

  const clearFilters = () => {
    setFilteredRecipes(recipes);
  };

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const query = params.get('search');

    if (query) {
      const result = recipes.filter(r =>
        r.title.toLowerCase().includes(query.toLowerCase())
      );
      setFilteredRecipes(result);
    } else {
      setFilteredRecipes(recipes);
    }
  }, [location.search]);

  return (
    <div className="p-4 relative">
      <div className="flex justify-end">
        <button
          onClick={toggleDropdown}
          className="px-4 py-2 bg-orange-400 text-white rounded hover:bg-orange-500"
        >
          Categories
        </button>
      </div>

      {dropdownVisible && (
        <FilterDropdown
          applyFilters={applyFilters}
          clearFilters={clearFilters}
          toggleDropdown={toggleDropdown}
        />
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
        {filteredRecipes.map(recipe => (
          <RecipeCard key={recipe.id} recipe={recipe} />
        ))}
      </div>
    </div>
  );
};

export default Home;
