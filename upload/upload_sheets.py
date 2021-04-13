import pandas as pd

df = pd.read_json("updated_diversityorgs.tech.json")
df.to_csv("updated_diversityorgs.tech.csv")
