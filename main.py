import pandas as pd
# import map_visual

def main():
    file_name = "calles_de_medellin_con_acoso.csv"
    medellin = pd.read_csv(file_name, sep=';')

    medellin_full = medellin.fillna({"harassmentRisk":medellin.harassmentRisk.mean()}).fillna({"name":"---"})
    print(f"{file_name} was now saved on medellin_full.csv without empty values")
    medellin_full.to_csv("medellin_full.csv")

main()