import React from 'react';
import { useParams } from 'react-router-dom';
import recipes from '../utils/recipegit';

const RecipeDetails = () => {
  const { id } = useParams();
  const recipe = recipes.find(r => r.id === parseInt(id));

  if (!recipe) return <div className="text-center mt-10 text-red-600">Recipe not found</div>;

  return (
    <div className="max-w-3xl mx-auto p-6 bg-white rounded shadow mt-6">
      <h2 className="text-3xl font-bold mb-4">{recipe.title}</h2>
      <img src={recipe.image} alt={recipe.title} className="w-full h-64 object-cover rounded mb-4" />
      
      <div className="flex justify-between text-sm text-gray-600 mb-2">
        <span><strong>Time:</strong> {recipe.time}</span>
        <span><strong>Difficulty:</strong> {recipe.difficulty}</span>
      </div>

      <div className="mb-4">
        <h3 className="font-semibold">Tags:</h3>
        <div className="flex flex-wrap gap-2 mt-1">
          {recipe.tags.map((tag, idx) => (
            <span key={idx} className="px-2 py-1 bg-orange-200 text-orange-800 rounded text-sm">{tag}</span>
          ))}
        </div>
      </div>

      <div className="mb-4">
        <h3 className="font-semibold">Ingredients:</h3>
        <ul className="list-disc list-inside ml-2 text-gray-700">
          {recipe.ingredients.map((ing, idx) => (
            <li key={idx}>{ing}</li>
          ))}
        </ul>
      </div>

      <div>
        <h3 className="font-semibold mb-1">Instructions:</h3>
        <p className="text-gray-800">{recipe.instructions}</p>
      </div>
    </div>
  );
};

export default RecipeDetails;
