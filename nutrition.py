from datetime import datetime   
import csv
import os

date_recorded = datetime.now().strftime("%Y-%m-%d")
filename = "nutrition.csv"



class Animal:
    """A class representing an animal with its nutritional needs."""
    def __init__(self, name, species, target_total, target_protein, target_fat):
        self.name = name
        self.species = species
        self.target_total = target_total
        self.target_protein = target_protein
        self.target_fat = target_fat
        self.consumed_total = 0.0
        self.consumed_protein = 0.0
        self.consumed_fat = 0.0

    def log_daily_intake(self, food_item, quantity_grams):
        """Logs the daily intake of nutrients for the animal."""
        """Calculates daily intake and updates the consumed nutrients."""
        protein_added = (food_item.protein_per_100g / 100) * quantity_grams
        fat_added = (food_item.fat_per_100g / 100) * quantity_grams
        self.consumed_total += quantity_grams      
        self.consumed_protein += protein_added
        self.consumed_fat += fat_added
        

        print(
            f"Logged {quantity_grams}g of {food_item.name} for {self.name}. Total: {self.consumed_total} grams, Protein: {self.consumed_protein} grams, Fat: {self.consumed_fat} grams."

        )   
    
    def get_nutritional_status(self):
        """Returns the nutritional status of the animal."""
        total_status = "OK" if self.consumed_total >= self.target_total else "Below Target"
        protein_status = "OK" if self.consumed_protein >= self.target_protein else "Below Target"
        fat_status = "OK" if self.consumed_fat >= self.target_fat else "Below Target"
        
        return {
            "name": self.name,
            "species": self.species,
            "total": {
                "target": self.target_total,
                "consumed": round(self.consumed_total, 2),
                "remaining": max(
                    0.0,
                    round(self.target_total - self.consumed_total, 2)
                ),
            },
            "protein": {
                "target": self.target_protein,
                "consumed": round(self.consumed_protein, 2),
                "remaining": max(
                    0.0,
                    round(self.target_protein - self.consumed_protein, 2)
                ),
            },
            "fat": {
                "target": self.target_fat,
                "consumed": round(self.consumed_fat, 2),
                "remaining": max(
                    0.0,
                    round(self.target_fat - self.consumed_fat, 2)
                ),
            },
        }

    def reset_daily_intake(self):
        """Resets the daily intake for the animal."""
        self.consumed_total = 0.0
        self.consumed_protein = 0.0
        self.consumed_fat = 0.0
        print(f"Daily intake reset for {self.name}.")

class FoodItem:
    """A class representing a food item with its nutritional content."""
    def __init__(self, name, protein_per_100g, fat_per_100g):
        self.name = name
        self.protein_per_100g = protein_per_100g
        self.fat_per_100g = fat_per_100g

squid = FoodItem("Squid", protein_per_100g=15.6, fat_per_100g=1.4)
salmon = FoodItem("Salmon", protein_per_100g=21.5, fat_per_100g=1.5)
trout = FoodItem("Trout", protein_per_100g=16.5, fat_per_100g=3.9)
mackerel = FoodItem("Pacific Mackerel", protein_per_100g=20.2, fat_per_100g=4.0)
shrimp = FoodItem("Shrimp", protein_per_100g=17.9, fat_per_100g=0.8)
herring = FoodItem("Pacific Herring", protein_per_100g=17.1, fat_per_100g=5.4)
clams = FoodItem("Surf Clam", protein_per_100g=16.3, fat_per_100g=0.6)
sardines = FoodItem("Sardines", protein_per_100g=17.6, fat_per_100g=8.0)
silversides = FoodItem("Silversides", protein_per_100g=16.7, fat_per_100g=6.2)
capelin = FoodItem("Capelin", protein_per_100g=14.4, fat_per_100g=1.7)

agave = Animal(
    name="Agave",
    species="Stegostoma fasciatum",
    target_total=200.0,
    target_protein=55.0,
    target_fat=10.0
)
nebula = Animal(
    name="Nebula",
    species="Stegostoma fasciatum",
    target_total=200.0,
    target_protein=55.0,
    target_fat=10.0
)

def main():
    animals = [agave, nebula]

    while True:
        print("\n1. Add Animal 2. Log Daily Intake 3. View Nutritional Status 4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter animal name: ")
            species = input("Enter animal species: ")
            target_total = float(input("Enter target total intake (grams): "))
            target_protein = float(input("Enter target protein intake (grams): "))
            target_fat = float(input("Enter target fat intake (grams): "))
            new_animal = Animal(name, species, target_total, target_protein, target_fat)
            animals.append(new_animal)
            print(f"Added {name} ({species}) to the system.")
        elif choice == "2":
            if not animals:
                print("No animals available. Please add an animal first.")
                continue
            print("Select an animal:")
            for idx, animal in enumerate(animals):
                print(f"{idx + 1}. {animal.name} ({animal.species})")
            animal_choice = int(input("Enter the number of the animal: ")) - 1
            if 0 <= animal_choice < len(animals):
                selected_animal = animals[animal_choice]
                print("Select a food item:")
                food_items = [squid, salmon, trout, mackerel, shrimp, herring, clams, sardines, silversides, capelin]
                for idx, food in enumerate(food_items):
                    print(f"{idx + 1}. {food.name}")
                food_choice = int(input("Enter the number of the food item: ")) - 1
                if 0 <= food_choice < len(food_items):
                    selected_food = food_items[food_choice]
                    quantity = float(input(f"Enter quantity of {selected_food.name} in grams: "))
                    selected_animal.log_daily_intake(selected_food, quantity)
                    protein_added = (selected_food.protein_per_100g / 100) * quantity
                    fat_added = (selected_food.fat_per_100g / 100) * quantity
                    row = [date_recorded, selected_animal.name, selected_food.name, quantity, protein_added, fat_added]
                    try:
                        with open(filename, mode="a", newline="") as file:
                            writer = csv.writer(file)
                            if os.stat(filename).st_size == 0:
                                writer.writerow(["Date", "Animal Name", "Food Item", "Total Consumed (g)", "Protein Consumed (g)", "Fat Consumed (g)"])
                            writer.writerow(row)
                        print(f"Logged date: {filename}")
                    except Exception as e:
                        print(f"Error writing to file: {e}")
                else:
                    print("Invalid food item choice.")
            else:
                print("Invalid animal choice.")
        elif choice == "3":
            print("\n---- Nutritional Status ----")
            for animal in animals:
                status = animal.get_nutritional_status()
                print(f"{status['name']} ({status['species']}):")
                print(f"  Total: {status['total']['consumed']}g consumed, {status['total']['remaining']}g remaining (Target: {status['total']['target']}g)")
                print(f"  Protein: {status['protein']['consumed']}g consumed, {status['protein']['remaining']}g remaining (Target: {status['protein']['target']}g)")
                print(f"  Fat: {status['fat']['consumed']}g consumed, {status['fat']['remaining']}g remaining (Target: {status['fat']['target']}g)")
        elif choice == "4":
            print("Exiting the program.")
            break
if __name__ == "__main__":
    main()



