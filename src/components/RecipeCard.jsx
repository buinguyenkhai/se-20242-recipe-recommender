// src/components/RecipeCard.jsx
import React from 'react';
import { Link } from 'react-router-dom';

const RecipeCard = ({ recipe }) => {
  return (
    <Link to={`/recipe/${recipe.id}`}>
      <div className="rounded overflow-hidden shadow-lg hover:shadow-xl transition">
        <img src={recipe.image} alt={recipe.title} className="w-full h-48 object-cover" />
        <div className="p-4">
          <h3 className="text-lg font-bold mb-1">{recipe.title}</h3>
          <p className="text-sm text-gray-500 mb-2">{recipe.time} - {recipe.difficulty}</p>
          <div className="flex flex-wrap gap-1">
            {recipe.tags.map(tag => (
              <span key={tag} className="text-xs bg-orange-100 text-orange-800 px-2 py-1 rounded">
                {tag}
              </span>
            ))}
          </div>
        </div>
      </div>
    </Link>
  );
};

export default RecipeCard;
