import pandas as pd
import re
#be careful with the date format
file_name = "reviews2.csv"
df = pd.read_csv(file_name,encoding='utf-8')

def get_by_year(df):
	year_list = [[] for x in range(6)]
	'''
	for i in range(2012,2018):
		df[ not re.search("[0-9]+/[0-9]+/"+str(i),str(df.date)) == None].to_csv("toronto"+str(i)+".csv",index=False)
	'''
	for i in range(len(df)):
		row = df.loc[i]
		if not re.search("2012-[0-9]+-[0-9]+",row.date) == None:
			year_list[0].append(row.comments)
		elif not re.search("2013-[0-9]+-[0-9]+",row.date) == None:
			year_list[1].append(row.comments)
		elif not re.search("2014-[0-9]+-[0-9]+",row.date) == None:
			year_list[2].append(row.comments)
		elif not re.search("2015-[0-9]+-[0-9]+",row.date) == None:
			year_list[3].append(row.comments)
		elif not re.search("2016-[0-9]+-[0-9]+",row.date) == None:
			year_list[4].append(row.comments)
		elif not re.search("2017-[0-9]+-[0-9]+",row.date) == None:
			year_list[5].append(row.comments)
	d_year={}
	for i in range(2012,2018):
		d_year[str(i)] = pd.Series(year_list[i-2012])
	df_year = pd.DataFrame(d_year)
	df_year.to_csv('Hongkong_by_year.csv',index=False)

def get_by_season(df):
        s_list = [[] for x in range(4)]
        for i in range(len(df)):
                row = df.loc[i]
                if not re.search("[0-9]+-(0[3-5])-[0-9]+",row.date) == None:
                        s_list[0].append(row.comments)
                elif not re.search("[0-9]+-(0[6-8])-[0-9]+",row.date) == None:
                        s_list[1].append(row.comments)
                elif not re.search("[0-9]+-(0|1)(0|1|9)-[0-9]+",row.date) == None:
                        s_list[2].append(row.comments)
                else:
                        s_list[3].append(row.comments)

        d_s={'Spring':pd.Series(s_list[0]), 'Summer':pd.Series(s_list[1]), 'Fall':pd.Series(s_list[2]), 'Winter':pd.Series(s_list[3])}
        df_s = pd.DataFrame(d_s)
        df_s.to_csv('Hongkong_by_season.csv',index=False)
get_by_year(df)
get_by_season(df)
