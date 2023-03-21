import pprint
from dietOptimiserVars import *
import time
from functools import reduce


class DietOptimiser:

    def __init__(self):
        self.foodStorage = {}
        self.map = {"Calories": {},
                    "Carbs": {},
                    "Fats": {},
                    "Proteins": {},
                    }
        self.nutrientValues = {"Proteins": {"minValue": minProteins,
                                            "maxValue": maxProteins},
                               "Fats": {"minValue": minFats,
                                        "maxValue": maxFats},
                               "Carbs": {"minValue": minCarbs,
                                         "maxValue": maxCarbs},
                               "Calories": {"minValue": minCalories,
                                            "maxValue": maxCalories}
                               }
        self.dailyMeals = {"day1": [], "day2": [], "day3": [], "day4": [], "day5": [], "day6": [], "day7": [], }
        self.caloMap = {}
        self.fatsMap = {}
        self.protMap = {}
        self.carbMap = {}
        self.minsMap = {}
        self.maxsMap = {}
        self.costMap = {}
        self.calorieCost = {}
        self.fatCost = {}
        self.proteinCost = {}
        self.carbCost = {}
        self.mapCost = {}

    def __call__(self, *args, **kwargs):
        """
        Prints the current state of Nutrients alocated in each day and the food info stored.
        :param args:
        :param kwargs:
        :return:
        """
        pprint.pprint(self.foodStorage)
        print(self.calculateDailyNutrient("Calories"))
        print(self.calculateDailyNutrient("Carbs"))
        print(self.calculateDailyNutrient("Fats"))
        print(self.calculateDailyNutrient("Proteins"))

    def reset(self):
        """
        Resets the current state of dailyMeals variable to the initial state, to allow multiple requests for diet calculation.
        :return:
        """
        self.dailyMeals = {"day1": [], "day2": [], "day3": [], "day4": [], "day5": [], "day6": [], "day7": [], }

    # decorator that checks if args are in the stored list of nutrients
    @staticmethod
    def checkArgs(func):
        def inner(*args, **kwargs):
            if not any(x in args for x in ["Calories", "Carbs", "Fats", "Proteins"]):
                print(f"Nutrient {args[1]} not in storage!")
                return False
            return func(*args, **kwargs)

        return inner

    def addItem(self, name, cost, calories, carbs, fat, protein, serving):
        """
        Adds food items to class memory. Stores each item in a dictionary.
        :param name: Name of food item
        :param cost: Cost of item
        :param calories: Number of calories of food serving in grams
        :param carbs: Number of carbs of food serving in grams
        :param fat: Number of fat of food serving in grams
        :param protein: Number of protein of food serving in grams
        :param serving: Weight of Food serving in grams or milliliters
        :return: True if item was added successfully
        """
        if not all(isinstance(i, int) for i in [cost, calories, carbs, fat, protein, serving]):
            print(f"Item nutrients and cost must be integers!")
            return False
        else:
            self.foodStorage[name] = {
                "Calories": calories,
                "Carbs": carbs,
                "Fats": fat,
                "Proteins": protein,
                "Serving": serving,
                "Cost": cost,
                "minServings": 0,
                "maxServings": 10
            }
            self.updateMaps()
            return True

    def setServings(self, item, minServings, maxServings):
        """
        Sets a min and max servings of an item per week
        :param item: food name
        :param minServings: Number of minimum servings per week
        :param maxServings: Number of maximum servings per week
        :return: True if it was set successfully
        """
        if item not in self.foodStorage.keys():
            print(f"Food {item} not in storage!")
            return False
        elif 10 < minServings < 1 and 10 < maxServings < 1:
            print(f"Number of servings not allowed!")
            return False
        else:
            self.foodStorage[item]["minServings"] = minServings
            self.foodStorage[item]["maxServings"] = maxServings
            self.updateMaps()
            return True

    @checkArgs
    def setNutrientValues(self, nutrient, minNutrient, maxNutrient):
        """
        Sets min and max servings of an item
        :param nutrient: food name
        :param minNutrient: Number of minimum grams of nutrient per day
        :param maxNutrient: Number of maximum grams of nutrient per day
        :return: True if it was set successfully
        """
        if minNutrient < 1 or maxNutrient < 1:
            print(f"Number of grams for {nutrient} not allowed!")
            return False
        else:
            self.nutrientValues[nutrient]["minValue"] = minNutrient
            self.nutrientValues[nutrient]["maxValue"] = maxNutrient
            return True

    def updateMaps(self):
        """
        Updates maps used in optimizations
        :return:
        """
        self.caloMap = {c: self.foodStorage[c]["Calories"] for c in self.foodStorage.keys()}
        self.fatsMap = {c: self.foodStorage[c]["Fats"] for c in self.foodStorage.keys()}
        self.protMap = {c: self.foodStorage[c]["Proteins"] for c in self.foodStorage.keys()}
        self.carbMap = {c: self.foodStorage[c]["Carbs"] for c in self.foodStorage.keys()}
        self.minsMap = {c: self.foodStorage[c]["minServings"] for c in self.foodStorage.keys()}
        self.maxsMap = {c: self.foodStorage[c]["maxServings"] for c in self.foodStorage.keys()}
        self.costMap = {c: self.foodStorage[c]["maxServings"] for c in self.foodStorage.keys()}
        self.map = {"Calories": self.caloMap,
                    "Fats": self.fatsMap,
                    "Proteins": self.protMap,
                    "Carbs": self.carbMap,
                    "minServings": self.minsMap,
                    "maxServings": self.maxsMap,
                    "Cost": self.costMap
                    }
        self.calorieCost = dict(sorted({c: self.foodStorage[c]["Cost"] / (self.foodStorage[c]["Calories"] or 0.1) for c in self.foodStorage.keys()}.items(), key=lambda item: item[1], reverse=False))
        self.fatCost = dict(sorted({c: self.foodStorage[c]["Cost"] / (self.foodStorage[c]["Fats"] or 0.1) for c in self.foodStorage.keys()}.items(), key=lambda item: item[1], reverse=False))
        self.proteinCost = dict(sorted({c: self.foodStorage[c]["Cost"] / (self.foodStorage[c]["Proteins"] or 0.1) for c in self.foodStorage.keys()}.items(), key=lambda item: item[1], reverse=False))
        self.carbCost = dict(sorted({c: self.foodStorage[c]["Cost"] / (self.foodStorage[c]["Carbs"] or 0.1) for c in self.foodStorage.keys()}.items(), key=lambda item: item[1], reverse=False))
        self.mapCost = {"Calories": self.calorieCost,
                        "Fats": self.fatCost,
                        "Proteins": self.proteinCost,
                        "Carbs": self.carbCost,
                        }

    def makeDietPlan(self, onlyRequiredServings=False):
        """
        Makes a daily diet for 1 person for 1 week with the lowest cost
        :return: A daily meal plan for 1 week
        """
        self.reset()
        # distribute the minimum required servings of meals each other day
        day = 1
        for food, value in dict(sorted(self.minsMap.items(), key=lambda x: x[1], reverse=False)).items():
            for count in range(value):
                day = self.checkNutrientLimits(food, day, checkOther=True)
                if not type(day) == int:
                    print(day)
                    return day
                self.dailyMeals["day" + str(day)].append(food)
                day += 2
                if day == 8:
                    day = 1
                elif day == 9:
                    day = 2
        if onlyRequiredServings:
            return self.createMessage("only the required servings and")

        # Add optimal food portions until all nutrients are fulfilled
        for day in self.dailyMeals.keys():
            for nutrient in ["Proteins", "Fats", "Carbs", "Calories"]:
                value = self.calculateDailyNutrient(nutrient, day)
                if value <= self.nutrientValues[nutrient]["minValue"]:
                    timeout = time.time() + 2
                    while value <= self.nutrientValues[nutrient]["minValue"] and time.time() < timeout:
                        # add items based on cost/nutrient
                        for item in self.mapCost[nutrient].keys():
                            count_servings = reduce(lambda x, y: x + y, [x for x in self.dailyMeals.values()]).count(item)
                            if self.checkNutrientLimits(item, day[-1]) and count_servings + 1 <= self.foodStorage[item]["maxServings"]:
                                self.dailyMeals[day].append(item)
                                value += self.map[nutrient][item]
                                timeout = time.time() + 2
                    if time.time() > timeout:
                        message = f"No values can be found that apply to the limits set! Add more servings, increase the limits for nutrients or add more food items and retry!"
                        return message
        return self.createMessage()

    def createMessage(self, text=""):
        message = f"\nDaily Diet optimised by cost for {text} foods you have added and limits set is:\n\n"
        for day, items in self.dailyMeals.items():
            sum_items = sum(self.foodStorage[x]["Cost"] for x in self.dailyMeals[day])
            message += f"######### {day} #########\nFor a cost of : {sum_items} RON\nit includes the following items:\n\
{', '.join([str(self.foodStorage[food]['Serving']) + 'grams of ' + food for food in self.dailyMeals[day]])}\nand has a daily nutrient intake of:\n"
            for nutrient in ["Calories", "Carbs", "Fats", "Proteins"]:
                message += f"{nutrient} : {self.calculateDailyNutrient(nutrient, day)}\n"
            message += "\n"
        return message

    def checkNutrientLimits(self, food, day, checkOther=False):
        """
        Checks if food can exceed maxValue of nutrition for a given day. Returns possible days to add item within limits or error.
        :param food: name of item
        :param day: day of the week to check value
        :param checkOther: flag this param if you want to check other days for availability
        :return: True/False if it can be added within limits. day of the week when it can be added or error if flag checkOther is set
        """
        ok = False
        error = False
        timeout = time.time() + 2
        while not ok and time.time() < timeout:
            for nutrient in ["Fats", "Carbs", "Proteins", "Calories"]:
                if self.calculateDailyNutrient(nutrient, day="day" + str(day)) + self.map[nutrient][food] <= self.nutrientValues[nutrient]["maxValue"]:
                    ok = True
                    continue
                else:
                    ok = False
                    if checkOther:
                        day += 1
                        if day == 8:
                            day = 1
                        error = f'Required food servings are more than the maximum nutritional value of {self.nutrientValues[nutrient]["maxValue"]} for {nutrient}! \n\
Please reduce the required food servings or increase the maximum nutritional values!'
                    else:
                        return False
        if time.time() > timeout:
            return error
        elif checkOther:
            return int(day)
        elif ok:
            return True

    @checkArgs
    def calculateDailyNutrient(self, nutrient, day="day0"):
        """
        Calculates nutrients of a specific day or all days
        :param nutrient:
        :param day:
        :return:
        """
        each_day = ""
        for d in self.dailyMeals.keys():
            total_value = 0
            for item in self.dailyMeals[d]:
                for x, y in self.map[nutrient].items():
                    if x == item:
                        total_value += int(y)
            if day == d:
                return total_value
            each_day += f"{d} total {nutrient} is {total_value}\n"
        return each_day


if __name__ == "__main__":
    diet = DietOptimiser()
    diet.addItem("Beef", 32, 420, 0, 28, 40, 200)
    diet.addItem("Chicken Breast", 22, 286, 0, 4, 56, 200)
    diet.addItem("Chicken Feet", 20, 150, 0, 7, 21, 200)
    diet.addItem("Oat", 12, 240, 41, 4, 8, 200)
    diet.addItem("Wheat", 10, 240, 51, 1, 10, 200)
    diet.addItem("Rice", 6, 260, 58, 0, 5, 200)
    diet.addItem("Almonds", 9, 280, 10, 20, 10, 50)
    diet.addItem("Tender Loin", 42, 440, 0, 36, 40, 200)
    diet.addItem("Chicken Wings", 22, 410, 0, 30, 32, 200)
    diet.addItem("1/2 Chicken", 30, 570, 0, 40, 50, 400)
    diet.addItem("Peanuts", 5, 250, 6, 22, 12, 50)
    diet.addItem("Ramen", 49, 1160, 88, 19, 14, 400)
    diet.addItem("Bologna", 24, 556, 4, 40, 20, 200)
    diet.addItem("Tofu", 8, 160, 6, 10, 15, 200)
    diet.addItem("Scrambled Eggs", 5, 360, 2, 28, 24, 200)
    diet.addItem("Omelette & Bacon", 9, 630, 3, 50, 40, 200)
    diet.addItem("Chocolate Cookie", 4, 233, 32, 12, 2, 50)
    diet.addItem("Baked Potatoes", 8, 260, 60, 0, 6, 200)
    diet.addItem("Fried Potatoes", 8, 508, 62, 26, 6, 200)
    diet.addItem("Banana", 6, 180, 46, 1, 2, 200)
    diet.addItem("Apple", 4, 100, 26, 0, 0, 200)
    diet.addItem("Salad", 8, 60, 12, 0, 0, 200)
    diet.addItem("Protein", 1, 10, 0, 0, 10, 100)

    diet.setServings("1/2 Chicken", 3, 5)
    diet.setServings("Oat", 4, 9)
    diet.setServings("Chicken Feet", 3, 8)
    diet.setServings("Almonds", 10, 10)
    diet.setServings("Ramen", 2, 7)
    diet.setServings("Tofu", 3, 7)
    diet.setServings("Apple", 8, 10)
    diet.setServings("Banana", 8, 10)
    diet.setServings("Salad", 3, 10)
    diet.setServings("Beef", 3, 5)

    diet.setNutrientValues("Calories", 1800, 2340)
    diet.setNutrientValues("Carbs", 50, 200)
    diet.setNutrientValues("Fats", 30, 200)
    diet.setNutrientValues("Proteins", 50, 200)
    print(diet.makeDietPlan(onlyRequiredServings=True))
    print(diet.makeDietPlan())
    diet()
