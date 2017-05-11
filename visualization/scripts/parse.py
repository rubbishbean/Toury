import json
import csv

data = {}

with open('slim-3.json') as f:
        data = json.load(f)
        with open('crime_cluster.csv') as c:
                reader = csv.reader(c)
                with open('crime_c2.csv','w') as op:
                        for row in reader:
                                for d in data:
                                        if d['name'] == row[0]:
                                                row[0] = d['alpha-3']
                                                print(row[0])
                                
                                if row[1] == '1':
                                        row[1] = 'Rank 1'
                                elif row[1] == '2':
                                        row[1] = 'Rank 2'
                                elif row[1] == '3':
                                        row[1] = 'Rank 3'
                                elif row[1] == '4':
                                        row[1] = 'Rank 4'
                                
                                writer = csv.writer(op,delimiter=',')
                                writer.writerow(row)
                op.close()
        c.close()
f.close()






