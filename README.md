# diet-optimiser
This code is a Python class called DietOptimiser, which is designed to help optimize a diet plan based on the nutrient values of various foods. The class has several methods for managing food items and nutrient values, including:
addItem(self, name, cost, calories, carbs, fat, protein, serving, minServings=0, maxServings=10): a method for adding food items to the class memory, with information about their nutrient values, serving size, and cost.
setServings(self, item, minServings, maxServings): a method for setting the minimum and maximum number of servings per week for a given food item.
setNutrientValues(self, nutrient, minNutrient, maxNutrient): a method for setting the minimum and maximum number of grams of a given nutrient that should be consumed per day.
makeDietPlan(self, onlyRequiredServings=False): a method for processing all the info and giving the optimal diet for each day as output.
