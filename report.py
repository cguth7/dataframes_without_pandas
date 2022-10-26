import argparse
import csv


parser = argparse.ArgumentParser()



parser.add_argument('-t')
parser.add_argument('-p')
parser.add_argument('-s')
parser.add_argument('--team-report', dest = "team_report")
parser.add_argument('--product-report', dest = "product_report")
args = parser.parse_args()

if args.t == None or args.s == None or args.p == None or args.team_report == None or args.product_report == None:
    print("usage: report.py -t TeamMap.csv -p ProductMaster.csv -s Sales.csv --team-report=TeamReport.csv --product-report=ProductReport.csv")
    exit()


with open(args.s) as f:
    page = f.read()

slist = page.split("\n")
saleslist = []

for row in slist:
    row = row.split(",")
    saleslist.append(row)

with open(args.t) as f:
    page = f.read()

tlist = page.split("\n")
teamlist = []

for row in tlist:
    row = row.split(",")
    teamlist.append(row)

with open(args.p) as f:
    page = f.read()
    
plist = page.split("\n")
productlist = []

for row in plist:
    row = row.split(",")
    productlist.append(row)

teamnamemap = {}
for i in range(1, len(teamlist)):
    teamnamemap[teamlist[i][0]] = teamlist[i][1]

teamsummap = {}
for i in range(1, len(teamlist)):
    teamsummap[teamlist[i][1]] = 0


productnamemap = {}
for i in range(0, len(productlist)):
    productnamemap[productlist[i][0]] = productlist[i][1]
        
productsummap = {}
for i in range(0, len(teamlist)):
    productsummap[productlist[i][1]] = 0
      
discountmap = {}
for i in range(0, len(teamlist)):
    discountmap[productlist[i][1]] = 0

unitsmap = {}
for i in range(0, len(teamlist)):
    unitsmap[productlist[i][1]] = 0

for row in saleslist:
    price = float(productlist[int(row[1]) - 1][2])
    quantity = int(row[3])
    lotsize = int(productlist[int(row[1]) - 1][3])
    discount = (1- (float(row[4])/100))
    teamsummap[teamnamemap[str(row[2])]] += price * quantity * lotsize * discount



header = ["Team", "Gross Revenue"]
data = [ [teamlist[i][1],teamsummap[teamlist[i][1]]] for i in range(1,len(teamlist))]

with open(args.team_report, 'w+') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)


for row in saleslist:
    price = float(productlist[int(row[1]) - 1][2])
    quantity = int(row[3])
    lotsize = int(productlist[int(row[1]) - 1][3])
    discount = (1- (float(row[4])/100))
    productsummap[productnamemap[str(row[1])]] += price * quantity * lotsize * discount
    

for row in saleslist:
    price = float(productlist[int(row[1]) - 1][2])
    quantity = int(row[3])
    lotsize = int(productlist[int(row[1]) - 1][3])
    discount = (1- (float(row[4])/100))
    discountmap[productnamemap[str(row[1])]] += price * quantity * lotsize *  (float(row[4])/100)

for row in saleslist:
    quantity = int(row[3])
    unitsmap[productnamemap[str(row[1])]] += quantity

productheader = ["Name","GrossRevenue","TotalUnits","DiscountCost"]
productdata = [ [productlist[i][1], productsummap[productlist[i][1]], unitsmap[productlist[i][1]], discountmap[productlist[i][1]] ] for i in range(len(productlist))]


with open(args.product_report, 'w+') as f:
    writer = csv.writer(f)
    writer.writerow(productheader)
    writer.writerows(productdata)
    


