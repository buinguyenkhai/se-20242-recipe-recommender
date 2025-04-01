import React from "react";

const RecipeCard = ({ recipe }) => {
  return (
    <div className="border rounded-lg p-4 shadow-md bg-white">
      <h3 className="text-xl font-bold">{recipe.name}</h3>
      <p className="text-gray-600">{recipe.description}</p>
    </div>
  );
};

export default RecipeCard;
