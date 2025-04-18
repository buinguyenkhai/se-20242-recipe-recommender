// src/components/FilterDropdown.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import recipes from '../utils/recipe';

const getAllTags = () => [...new Set(recipes.flatMap(r => r.tags))];
const getAllIngredients = () => [...new Set(recipes.flatMap(r => r.ingredients))];

const FilterDropdown = ({ applyFilters, clearFilters, toggleDropdown }) => {
  const navigate = useNavigate();
  const [selectedTags, setSelectedTags] = useState([]);
  const [selectedIngredients, setSelectedIngredients] = useState([]);

  const handleSelect = (value, setter, selected) => {
    setter(selected.includes(value) ? selected.filter(t => t !== value) : [...selected, value]);
  };

  const handleLucky = () => {
    const random = recipes[Math.floor(Math.random() * recipes.length)];
    navigate(`/recipe/${random.id}`);
    toggleDropdown();
  };

  const handleSearch = () => {
    applyFilters({ tags: selectedTags, ingredients: selectedIngredients });
    toggleDropdown();
  };

  const handleClear = () => {
    setSelectedTags([]);
    setSelectedIngredients([]);
    clearFilters();
    toggleDropdown();
  };

  return (
    <div className="absolute z-20 left-0 right-0 bg-white shadow-md border border-orange-300 p-4 mt-1 rounded">
      <div className="grid grid-cols-2 gap-6">
        <div>
          <h4 className="font-semibold mb-1">Tags</h4>
          <div className="flex flex-wrap gap-2">
            {getAllTags().map(tag => (
              <button
                key={tag}
                onClick={() => handleSelect(tag, setSelectedTags, selectedTags)}
                className={`px-2 py-1 rounded border ${
                  selectedTags.includes(tag) ? 'bg-orange-300 text-white' : 'bg-gray-100'
                }`}
              >
                {tag}
              </button>
            ))}
          </div>
        </div>

        <div>
          <h4 className="font-semibold mb-1">Ingredients</h4>
          <div className="flex flex-wrap gap-2">
            {getAllIngredients().map(ing => (
              <button
                key={ing}
                onClick={() => handleSelect(ing, setSelectedIngredients, selectedIngredients)}
                className={`px-2 py-1 rounded border ${
                  selectedIngredients.includes(ing) ? 'bg-orange-300 text-white' : 'bg-gray-100'
                }`}
              >
                {ing}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="flex justify-between mt-4">
        <div className="flex gap-2">
          <button
            onClick={handleSearch}
            className="px-4 py-2 bg-orange-500 text-white rounded hover:bg-orange-600"
          >
            Search
          </button>
          <button
            onClick={handleClear}
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300"
          >
            Clear Filters
          </button>
        </div>

        <button
          onClick={handleLucky}
          className="px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600"
        >
          I'm Feeling Lucky
        </button>
      </div>
    </div>
  );
};

export default FilterDropdown;
