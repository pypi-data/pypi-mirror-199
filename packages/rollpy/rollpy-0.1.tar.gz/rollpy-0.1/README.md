# diePy
**diePy** is a Python module for simulating die and dice rolls in role-playing games. This README file provides an overview of the package and how to use it.

## Installation

You can install **diePy** using *pip*:

`pip install diePy`


## Usage
The **diePy** module provides several functions for rolling dice and generating ability scores.

### roll function

The **roll** function rolls a single die with the specified number of sides.
```
python

from diePy import roll

result = roll(6)  # Roll a standard six-sided die
print(result)  # Prints a random integer between 1 and 6
```

The die parameter can also be a ***Die*** object with a ***roll*** method that takes an integer argument and returns an integer.
### rolls function

The **rolls** function rolls a specified number of dice with the specified number of sides and returns the total.
```
python

from diePy import rolls

result = rolls(2, 6)  # Roll two six-sided dice
print(result)  # Prints a random integer between 2 and 12
```
### roll_sequence function

The **roll_sequence** function rolls a specified number of dice with the specified number of sides and returns a tuple of the results.
```
python

from diePy import roll_sequence

result = roll_sequence(3, 6)  # Roll three six-sided dice
print(result)  # Prints a tuple of three random integers between 1 and 6
```
### ability_roll function

The **ability_roll** function rolls 5 six-sided dice and returns the sum of the three highest numbers.
```
python

from diePy import ability_roll

result = ability_roll()  # Roll ability scores
print(result)  # Prints a tuple of the five rolls and the sum of the three highest rolls
```

### ability_rolls function

The **ability_rolls** function rolls 6 sets of ability scores and returns a list of the 6 sets ordered from highest to lowest.
```
python

from diePy import ability_rolls

result = ability_rolls()  # Roll ability scores
print(result)  # Prints a list of the 6 sets ordered from highest to lowest
```

### check function

The **check** function compares an ability modifier to a DC (difficulty class) and returns a tuple of the result and a boolean indicating whether the roll was a success or failure.
```
python

from diePy import check

result = check(3, 15)  # Check if the ability modifier of 3 beats the DC of 15
print(result)  # Prints a tuple of the result and a boolean indicating whether the roll was a success or failure
```
