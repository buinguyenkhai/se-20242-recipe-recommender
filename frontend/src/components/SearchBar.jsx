import { useState } from "react";

const SearchBar = ({ onSearch, tags, ingredients, onReset }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedTag, setSelectedTag] = useState("");
  const [selectedIngredient, setSelectedIngredient] = useState("");

  const handleSearch = () => {
    onSearch(searchTerm, selectedTag, selectedIngredient);
  };

  const handleReset = () => {
    setSearchTerm("");
    setSelectedTag("");
    setSelectedIngredient("");
    onReset();
  };

  return (
    <div className="bg-gray-800 p-4 rounded-xl shadow-md flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">
      <input
        type="text"
        placeholder="Search recipes by name..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className="p-2 rounded-md w-full md:w-1/3 text-black"
      />

      <select
        value={selectedTag}
        onChange={(e) => setSelectedTag(e.target.value)}
        className="p-2 rounded-md w-full md:w-1/4 text-black"
      >
        <option value="">Filter by tag</option>
        {tags.map((tag, index) => (
          <option key={index} value={tag}>
            {tag}
          </option>
        ))}
      </select>

      <select
        value={selectedIngredient}
        onChange={(e) => setSelectedIngredient(e.target.value)}
        className="p-2 rounded-md w-full md:w-1/4 text-black"
      >
        <option value="">Filter by ingredient</option>
        {ingredients.map((ingredient, index) => (
          <option key={index} value={ingredient}>
            {ingredient}
          </option>
        ))}
      </select>

      <div className="flex gap-2">
        <button
          onClick={handleSearch}
          className="bg-green-500 hover:bg-green-600 text-white py-2 px-4 rounded-lg"
        >
          🔍 Search
        </button>
        <button
          onClick={handleReset}
          className="bg-red-500 hover:bg-red-600 text-white py-2 px-4 rounded-lg"
        >
          🔄 Reset
        </button>
      </div>
    </div>
  );
};

export default SearchBar;
