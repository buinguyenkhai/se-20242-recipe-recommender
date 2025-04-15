import React from "react";

const RecipeCard = ({ recipe }) => {
  return (
    <div className="rounded-xl shadow-lg bg-gradient-to-br from-orange-100 via-yellow-100 to-orange-200 p-6 hover:scale-105 transform transition duration-300">
      <h3 className="text-2xl font-semibold text-orange-800">{recipe.name}</h3>
      <p className="mt-2 text-gray-700 italic">{recipe.description}</p>
      {recipe.tags && (
        <div className="mt-3">
          <span className="text-sm font-medium text-gray-600">Tags:</span>
          <ul className="flex flex-wrap gap-2 mt-1">
            {recipe.tags.map((tag, i) => (
              <li key={i} className="bg-orange-300 text-white text-xs px-2 py-1 rounded-full">
                {tag}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default RecipeCard;
