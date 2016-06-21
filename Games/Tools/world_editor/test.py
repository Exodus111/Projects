from path import Path

here = Path(__file__).parent
save = Path("save")

there = here / save

print(there)
