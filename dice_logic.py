# ============================================
# File: dice_logic.py
# ============================================
# Core logic for dice rolling
# ============================================

import random

class DiceLogic:
    def __init__(self):
        self.dice_types = {
            'd4': 4,
            'd6': 6,
            'd8': 8,
            'd10': 10,
            'd12': 12,
            'd20': 20,
            'd100': 100
        }
        
    def get_max_value(self, dice_type):
        """Get the maximum value for a given dice type"""
        return self.dice_types.get(dice_type, 20)
    
    def roll_dice(self, dice_type, num_dice=1):
        """
        Roll dice of the specified type
        
        Args:
            dice_type (str): Type of dice (e.g., 'd6', 'd20')
            num_dice (int): Number of dice to roll
            
        Returns:
            list: List of individual roll results
        """
        if dice_type not in self.dice_types:
            raise ValueError(f"Invalid dice type: {dice_type}")
        
        max_value = self.dice_types[dice_type]
        results = []
        
        for _ in range(num_dice):
            # For d100, use 1-100 (0-99 + 1)
            if dice_type == 'd100':
                result = random.randint(1, 100)
            else:
                result = random.randint(1, max_value)
            results.append(result)
        
        return results
    
    def roll_with_modifier(self, dice_type, num_dice=1, modifier=0):
        """
        Roll dice and add a modifier
        
        Args:
            dice_type (str): Type of dice
            num_dice (int): Number of dice to roll
            modifier (int): Modifier to add to the total
            
        Returns:
            dict: Contains individual rolls, total, and modified total
        """
        rolls = self.roll_dice(dice_type, num_dice)
        total = sum(rolls)
        modified_total = total + modifier
        
        return {
            'rolls': rolls,
            'total': total,
            'modifier': modifier,
            'modified_total': modified_total
        }
    
    def roll_advantage(self, dice_type='d20'):
        """
        Roll with advantage (roll two d20 and take the higher)
        
        Returns:
            dict: Contains both rolls and the result
        """
        roll1 = self.roll_dice('d20', 1)[0]
        roll2 = self.roll_dice('d20', 1)[0]
        
        return {
            'rolls': [roll1, roll2],
            'result': max(roll1, roll2),
            'advantage': True
        }
    
    def roll_disadvantage(self, dice_type='d20'):
        """
        Roll with disadvantage (roll two d20 and take the lower)
        
        Returns:
            dict: Contains both rolls and the result
        """
        roll1 = self.roll_dice('d20', 1)[0]
        roll2 = self.roll_dice('d20', 1)[0]
        
        return {
            'rolls': [roll1, roll2],
            'result': min(roll1, roll2),
            'disadvantage': True
        }
    
    def roll_with_exploding(self, dice_type, num_dice=1):
        """
        Roll with exploding dice (reroll and add on max value)
        
        Args:
            dice_type (str): Type of dice
            num_dice (int): Number of dice to roll
            
        Returns:
            dict: Contains all rolls and total
        """
        max_value = self.dice_types[dice_type]
        all_rolls = []
        total = 0
        
        for _ in range(num_dice):
            roll = random.randint(1, max_value)
            rolls_for_die = [roll]
            
            # Explode on max value
            while roll == max_value:
                roll = random.randint(1, max_value)
                rolls_for_die.append(roll)
            
            all_rolls.extend(rolls_for_die)
            total += sum(rolls_for_die)
        
        return {
            'rolls': all_rolls,
            'total': total,
            'exploding': True
        }
