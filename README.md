# Diet Optimiser Class
<h3>Description</h3>
This class is designed to allow users to calculate optimal diets according to given constraints. Users can add food items, set minimum and maximum servings, set the minimum and maximum daily value of a nutrient, and set the diet plan for seven days. After the diet is planned, it is possible to obtain information on the number of nutrients allocated per day and the stored food information.
##### For an optimal experience add as many items as possible, using a wide range of nutrient values. 
<h3>Requirements</h3>
`python 3.8+`
<h3>How to use:</h3>

1. Import DietOptimiser class from the dietOptimiser module.\
2. Create an instance of DietOptimiser class.\
3. Use the addItem method to add food items to the class memory. The method takes arguments name, cost, calories, carbs, fat, protein, serving, minServings, and maxServings.
   * **name** is the name of the food item (string).
   * **cost** is the cost of the food item (integer).
   * **calories** is the number of calories in the food item (integer).
   * **carbs** is the number of carbohydrates in the food item (integer).
   * **fat** is the amount of fat in the food item (integer).
   * **protein** is the amount of protein in the food item (integer).
   * **serving** is the serving size for the food item (integer).\
   * minServings is the minimum number of servings per week (integer).
   * maxServings is the maximum number of servings per week (integer).
    ```
    from dietOptimiser import DietOptimiser
    dietOptimiser = DietOptimiser()
    #dietOptimiser.addItem(name, cost, calories, carbs, fat, protein, serving)
    diet.addItem("Beef", 32, 420, 0, 28, 40, 200)
    ```
4. Setting minimum and maximum portion sizes:\
The default values for food servings is min=0 and max=10, but you can set the minimum and maximum portion sizes for when adding each food item or by using **setServings**() method:
    ```
    dietOptimiser.setServings(item, minServings, maxServings)
    diet.setServings("1/2 Chicken", 3, 5)
    ```
5. Setting nutrient requirements:\
You can set your nutrient requirements using the dietOptimiserVars.py variables or by using the method **setNutrientValues**():

    `dietOptimiser.setNutrientValues(nutrient, minNutrient, maxNutrient)`

6. Generating a diet plan\

    You can generate a diet plan that meets your nutrient requirements using the **generateDietPlan**() method:\
    
    ```
   print(diet.makeDietPlan(onlyRequiredServings=True))
    print(diet.makeDietPlan())
   ```
    
    onlyRequiredServings flag can be set to show the diet with the required food servings only. 

