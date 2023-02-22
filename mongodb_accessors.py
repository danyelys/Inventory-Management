import json
from pymongo import MongoClient
mongodb = MongoClient('localhost', 27017)
db = mongodb.assignment1

def getJsonValues(header):
    array = db.aggItems.distinct(header)
    return array


### CUSTOMER SEARCH FUNCTIONS###
def simpleSearchC(criteria):
    models = db.Products.distinct("Model")
    categories = db.Products.distinct("Category")

    #print(models)
    #print(categories)
    
    
    #if criteria is a model (Light1, SmartHome1)
    if criteria in models:
        results = list(db.Products.find({"Model":criteria},\
                                {"Cost ($)":0, "ProductID":0,"_id":0})) #change is here -> made it into a list
        for result in results:
            stock = db.aggItems.count_documents({"Model":criteria,\
                                                 "Category": result["Category"],
                                          "PurchaseStatus":"Unsold"})
            result["Inventory"] = stock
        return results
         
    elif criteria in categories:
        results = list(db.Products.find({"Category":criteria},\
                                {"Cost ($)":0, "ProductID":0,"_id":0}))
        for result in results:
            stock = db.aggItems.count_documents({"Category":criteria, "Model": result["Model"],\
                                          "PurchaseStatus":"Unsold"}) 
            result["Inventory"] = stock
        return results

#print(simpleSearchC("SmartHome1"))
#print(simpleSearchC("Lights"))

def simpleSearchA(criteria):

    models = db.Products.distinct("Model")
    categories = db.Products.distinct("Category")

    #print(models)
    #print(categories)
    
    
    #if criteria is a model (Light1, SmartHome1)
    if criteria in models:
        results = list(db.Products.find({"Model":criteria},\
                                {"_id":0})) #change is here -> made it into a list
        for result in results:
            stock = db.aggItems.count_documents({"Model":criteria,\
                                                 "Category": result["Category"],
                                          "PurchaseStatus":"Unsold"})
            sold = db.aggItems.count_documents({"Model":criteria,\
                                                 "Category": result["Category"],
                                          "PurchaseStatus":"Sold"})
            result["Inventory"] = stock
            result["Sold"] = sold
        return results
         
    elif criteria in categories:
        results = list(db.Products.find({"Category":criteria},\
                                {"_id":0}))
        for result in results:
            stock = db.aggItems.count_documents({"Category":criteria, "Model": result["Model"],\
                                          "PurchaseStatus":"Unsold"})
            sold = db.aggItems.count_documents({"Category":criteria, "Model": result["Model"],\
                                          "PurchaseStatus":"Sold"})
            result["Inventory"] = stock
            result["Sold"] = sold
        return results



def advSearchC(price, warranty, category, model, color, factory, productionYear, powerSupply):
    defaultInt = 0
    defaultString = ""
    #assume that price, warranty is IntVar(), the rest is StringVar()
    #default for entry is 0 for int, "" for string
    
    sumItemsAgg = {"Price ($)": price, "Warranty (months)": warranty, \
                   "Category": category, "Model": model, "Color": color, \
                   "Factory": factory, "ProductionYear": productionYear, \
                   "PowerSupply": powerSupply}
    #put the unsold constraint into queryArray first, then put in any further constraints
    queryArray = {"PurchaseStatus": "Unsold"}
    
    for k,v in sumItemsAgg.items():
        if v != defaultInt and v != defaultString:
            queryArray[k] = v
    #print(queryArray)
    results = db.aggItems.find(queryArray,{"Cost ($)":0, "ProductID":0, "ItemID":0,\
                                        "ServiceStatus":0, "_id":0})
    return list(results)


###ADMIN SEARCH FUNCTIONS###

def advSearchA(price, warranty, itemId, category, model, color, factory, productionYear, powerSupply):
        
    defaultInt = 0
    defaultString = ""
    #assume that price, warranty is IntVar(), the rest is StringVar()
    #default for entry is 0 for int, "" for string
    #itemId is string
    
    sumItemsAgg = {"Price ($)": price, "Warranty (months)": warranty, "ItemID": itemId, \
                   "Category": category, "Model": model, "Color": color, \
                   "Factory": factory, "ProductionYear": productionYear, \
                   "PowerSupply": powerSupply}
    
    queryArray = {}
    
    for k,v in sumItemsAgg.items():
        if v != defaultInt and v != defaultString:
            queryArray[k] = v
    #print(queryArray)
    results = db.aggItems.find(queryArray,{"_id":0})
    return list(results)

#print(advSearchC(50,0,0,0,0,0,0,0))
#print(advSearchA(0,0,0,0,0,"White","China",0,0))
#print(simpleSearchA("Light2"))


###Updating items collection when item is purchased###
#everytime customer purchases item, need to update "PurchaseStatus" from Unsold to Sold

def mongoUpdatePurchase(listItemsID):
    #listItemsID is a list of itemId, etc ["1001","1002"]
    for itemID in listItemsID:
        db.aggItems.update_one( {"ItemID": itemID},
                            {'$set': {
                                "PurchaseStatus": "Sold"}
                             }
                            )
    return list(db.aggItems.find({"ItemID": itemID}, {"_id":0}))

#print(mongoUpdatePurchase(["1100"]))


###Restart the database###
def reinitializeMongo():

#Imports items.json and db.Products.json and puts it into collections
#itemsAgg is created with mongoDB script that merges items and db.Products collection
#itemsAgg = db.aggItems
    
    db.Items.drop()
    db.Products.drop()
    db.aggItems.drop()

    items = db.Items
    products = db.Products
    with open('items.json') as file:
        items.insert_many(json.load(file))
    with open('products.json') as file:
        products.insert_many(json.load(file))

    db.Items.aggregate([{

    '$lookup': {
      'from': "Products",
      'let': {
        'category': "$Category", 'model': "$Model"
      },
      'pipeline': [
        {'$match':{
          '$expr':{
            '$and':[{'$eq':["$Category", "$$category"]},
            {'$eq':["$Model", "$$model"]}
            ]
          }
        }
        },
      {'$project': {"Warranty (months)":1, "Price ($)":1, "Cost ($)":1, "_id":0}}
      ],
      'as': "info"
    }
    },

    {
     '$replaceRoot': {'newRoot': {'$mergeObjects': [{'$arrayElemAt':["$info",0]}, "$$ROOT"]}}
    },

    {'$project': {'info':0, "_id":0}
    },

    {'$out': "aggItems"}

    ])
    


###MAIN###
reinitializeMongo()
    


