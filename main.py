from fastapi import FastAPI
import pandas
import json
import csv

app = FastAPI()

def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = [] 
    with open(csvFilePath, encoding='utf-8') as csvf: 
        csvReader = csv.DictReader(csvf) 

        for row in csvReader: 
            jsonArray.append(row)
  
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(jsonArray, indent=4, ensure_ascii=False)
        jsonf.write(jsonString)

csvFilePath = r'hotels_agoda_danang_20221207-024938.csv'
jsonFilePath = r'/tmp/hotels.json'
csv_to_json(csvFilePath, jsonFilePath)

def moneyRange(minMoney,maxMoney): 
    df = pandas.read_json("hotels.json")
    df['price'] = df['price'].astype('int')
    df = df[(df['price'] >= minMoney) & (df['price'] <= maxMoney)]
    return df.to_dict(orient="records")

@app.get("/")
def read_root():
    df = pandas.read_json("hotels.json")
    return df.to_dict(orient="records")

@app.get("/budget")
def money_range(minMoney: int, maxMoney: int):
    return moneyRange(minMoney,maxMoney)

@app.get("/stars")
def stars_range(minStars: int, maxStars: int):

    df = pandas.read_json("hotels.json")
    df['stars'] = df['stars'].astype('int')
    df = df[(df['stars'] >= minStars) & (df['stars'] <= maxStars)]
    return df.to_dict(orient="records")

@app.get("/hotels/{hotel_id}")
def read_item(hotel_id: int):
    df = pandas.read_json("hotels.json")
    return df[df['hotel_id'] == hotel_id].to_dict(orient="records")
