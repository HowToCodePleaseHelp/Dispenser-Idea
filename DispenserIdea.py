import time
from datetime import datetime
import json


class Dispenser:
    def __init__(self):

        self.ingredients = {
            'water': {
                'type': 'base',
                'current_level': 1000,  # in ml
                'dispense_rate': 50     
            },
            'green_tea': {
                'type': 'base',
                'current_level': 1000,
                'dispense_rate': 50
            },
            'berry': {
                'type': 'flavor',
                'current_level': 500,
                'dispense_rate': 20
            },
            'citrus': {
                'type': 'flavor',
                'current_level': 500,
                'dispense_rate': 20
            },
            'vitamin_mix': {
                'type': 'supplement',
                'current_level': 250,
                'dispense_rate': 10
            }
        }

    def load_profiles(self):
        '''loading the user profile from a json maybe?'''
        try:
            with open('drink_profiles.json', 'r') as file:
                self.profiles = json.load(file)

        except FileNotFoundError: #Default profile in case file is not located.
            self.profiles = {
                'energize': {
                    'ingredients': {
                        'green_tea': 70,
                        'berry': 20,
                        'vitamin_mix': 10
                    },
                    'description': 'Morning energy boost'
                },
                'refresh': {
                    'ingredients': {
                        'water': 80,
                        'citrus': 15,
                        'vitamin_mix': 5
                    },
                    'description': 'Afternoon refreshment'
                }
            }
            self.save_profiles()

    def save_profiles(self):
        with open('drink_profiles.json', 'w') as file:
            json.dump(self.profiles, file, indent=4)

    def create_profile(self, name, ingredients, description=""):
        #create a new profile
        if sum(ingredients.values()) != 100:
            raise ValueError("Ingredient percentages must be 100%")
        
        if not all(ing in self.ingredients for ing in ingredients):
            raise ValueError("One or more ingredients not available")
        
        self.profiles[name] = {
            'ingredients': ingredients,
            'description': description,
            'created_at': datetime.now().isoformat()
        }

        self.save_profiles()
    
    def dispense_drink(self, profile_name, size_ml=300):
        if profile_name not in self.profiles:
            raise ValueError(f"Profile '{profile_name} not found'")
        
        profile = self.profiles[profile_name]
        dispensing_log = []

        for ingredient, percentage in profile['ingredients'].items():
            volume = (percentage / 100) * size_ml

            if self.ingredients[ingredient]['current_level'] < volume:
                raise ValueError(f"Insufficient {ingredient}")
        
        dispense_time = volume / self.ingredients[ingredient]['dispense_rate']

        time.sleep(dispense_time)

        self.ingredients[ingredient]['current_level'] -= volume

        dispensing_log.append({
            'ingredient': ingredient,
            'volume_ml': volume,
            'time_taken': dispense_time
        })

        return {
            'profile': profile_name,
            'size_ml': size_ml,
            'timestamp': datetime.now().isoformat(),
            'dispensing_log': dispensing_log
        }
    
    def get_ingredients_levels(self):
        return {name: info['current_level'] for name, info in self.ingredients.items()}
    
def demo_dispenser():
    dispenser = Dispenser()
    
    profile_name = "Panyapat's Bullshit"  
    dispenser.create_profile(
        name=profile_name,
        ingredients={
            'green_tea': 60,
            'citrus': 30,
            'vitamin_mix': 10
        },
        description="Dopamine boost, perfect for beating someone up."
    )
    
    print("Dispensing Afternoon Boost...")
    result = dispenser.dispense_drink(profile_name, size_ml=250)
    
    print("\nDispensing Log:")
    for action in result['dispensing_log']:
        print(f"- Dispensed {action['volume_ml']}ml of "
              f"{action['ingredient']} in {action['time_taken']:.1f} seconds")
    
    print("\nRemaining Ingredient Levels:")
    for ing, level in dispenser.get_ingredients_levels().items():
        print(f"- {ing}: {level}ml")


if __name__ == "__main__":
    demo_dispenser()