
from src import BacktrackingGenerator, BacktrackingSolver

print("Generuji hrací plochu...")
generator = BacktrackingGenerator(45)  # Vyprázdni 45 políček
grid = generator.generate()
print(grid)

print("\nVyprázňuji políčka...")
emptied_grid = generator.empty_values(grid)
print(emptied_grid)

print("\nHledám řešení...")
solver = BacktrackingSolver()
print(solver.solve(emptied_grid))

