import pandas as pd

df = pd.read_csv("generated_and _solved_sudokus.txt")

# Print descriptive statistics
print(df.describe())

# Print hard puzzles
print(df[df.time_to_solve > 1])