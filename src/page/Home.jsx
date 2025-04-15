import { useEffect, useState } from "react";
import { useLocation, Link } from "react-router-dom";
import RecipeCard from "../components/RecipeCard";

const recipes = [
  {
    name: "Spaghetti Bolognese",
    description: "A classic Italian pasta dish with a rich, meaty sauce.",
    tags: ["Italian", "Pasta"],
    ingredients: ["Spaghetti", "Ground beef", "Tomato sauce", "Onion", "Garlic"],
  },
  {
    name: "Chicken Curry",
    description: "A flavorful dish made with tender chicken and aromatic spices.",
    tags: ["Indian", "Spicy"],
    ingredients: ["Chicken", "Onion", "Garlic", "Ginger", "Curry powder"],
  },
  {
    name: "Caprese Salad",
    description: "Basic Salad",
    tags: ["Italian", "Vegetarian"],
    ingredients: ["Tomato", "Mozzarella", "Basil"],
  },
];

const Home = () => {
  const location = useLocation();
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedTag, setSelectedTag] = useState("");
  const [selectedIngredient, setSelectedIngredient] = useState("");

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const search = params.get("search") || "";
    setSearchTerm(search);
  }, [location.search]);

  const allTags = [...new Set(recipes.flatMap((r) => r.tags))];
  const allIngredients = [...new Set(recipes.flatMap((r) => r.ingredients))];

  const filteredRecipes = recipes.filter((recipe) => {
    const matchName = recipe.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchTag = selectedTag === "" || recipe.tags.includes(selectedTag);
    const matchIngredient = selectedIngredient === "" || recipe.ingredients.includes(selectedIngredient);
    return matchName && matchTag && matchIngredient;
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-300 to-yellow-300 p-10 text-black">
      <h1 className="text-4xl font-bold text-center mb-8">Recipes</h1>
      <div className="flex flex-col md:flex-row gap-8">
        {/* Sidebar Filter */}
        <aside className="w-full md:w-1/4 bg-white p-6 rounded-xl shadow-lg">
          <h2 className="text-xl font-semibold mb-4">Filter By</h2>

          <div className="mb-4">
            <h3 className="text-sm font-bold mb-2">Tags</h3>
            <div className="flex flex-col gap-1 text-sm">
              {allTags.map((tag) => (
                <label key={tag}>
                  <input
                    type="radio"
                    name="tag"
                    value={tag}
                    checked={selectedTag === tag}
                    onChange={() => setSelectedTag(tag)}
                    className="mr-2"
                  />
                  {tag}
                </label>
              ))}
              <label>
                <input
                  type="radio"
                  name="tag"
                  value=""
                  checked={selectedTag === ""}
                  onChange={() => setSelectedTag("")}
                  className="mr-2"
                />
                All
              </label>
            </div>
          </div>

          <div>
            <h3 className="text-sm font-bold mb-2">Ingredients</h3>
            <div className="flex flex-col gap-1 text-sm">
              {allIngredients.map((ingredient) => (
                <label key={ingredient}>
                  <input
                    type="radio"
                    name="ingredient"
                    value={ingredient}
                    checked={selectedIngredient === ingredient}
                    onChange={() => setSelectedIngredient(ingredient)}
                    className="mr-2"
                  />
                  {ingredient}
                </label>
              ))}
              <label>
                <input
                  type="radio"
                  name="ingredient"
                  value=""
                  checked={selectedIngredient === ""}
                  onChange={() => setSelectedIngredient("")}
                  className="mr-2"
                />
                All
              </label>
            </div>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 space-y-6">
          {filteredRecipes.length > 0 ? (
            filteredRecipes.map((recipe) => (
              <Link
                key={recipe.name}
                to={`/recipe/${recipe.name.toLowerCase().replace(/\s+/g, "-")}`}
                className="block transition-transform hover:scale-105"
              >
                <RecipeCard recipe={recipe} />
              </Link>
            ))
          ) : (
            <p className="text-center text-gray-700 text-lg">No recipes found.</p>
          )}
        </main>
      </div>
    </div>
  );
};

export default Home;
