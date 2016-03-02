import sys
import re
import csv
import shutil
import os
from collections import defaultdict
#input
#query = sys.argv[1:]
distinct_entry = ['DISTINCT','distinct','Distinct']
from_entry = ['FROM','From','from']
select_entry = ['Select','select','SELECT']
where_entry = ['WHERE','where','Where']

#print query

operators = ['<', '=', '>', '<>']
#querya=query[0]
#query= query[0].split(' ')
#print query
test="CREATE TABLE (table5 A int,B int,C int)"
def create(query):  
  index=4
  tests=query  
  test_split=tests
  pat="./"+test_split[2] +'.csv'
  if os.path.exists(pat) is True: 
    print "table already exist"
    return 
  #print test_split 
  i=4
  while i < len(test_split)-1:
     if test_split[i].split(',')[0]!="int":
        print "data type incorrect"
        return 
     i=i+1
         
  if test_split[i].split(')')[0]!="int":
        print "data type incorrect"
        return          
  with open('metadata.txt','a') as myfile:
     myfile.write("<begin_table>"+'\n')
     myfile.write(test_split[2])  
     myfile.write('\n')
     myfile.write(test_split[3].split('(')[1]+'\n')
     while index < len(test_split)-1:	
        myfile.write(test_split[index].split(',')[1]+'\n')
        index=index+1 
     myfile.write("<end_table>")
  open(test_split[2]+".csv", 'w')
#create() 
test="insert into test 1,2"   
def insert(query):
   test_split=query
   if os.path.exists(test_split[2]+'.csv') is False: 
     print "table does not exist"
   with open(test_split[2]+'.csv', 'a') as fp:
      a = csv.writer(fp, delimiter=',')
      new=test_split[3].split(',')
      data=[]
      data.append(new) 
      a.writerows(data)
#insert()
#test="delete from test where B=640"
def delete_col(query):
    test_split=query
    endtab='<end_table>'
    if os.path.exists(test_split[2]+'.csv') is False: 
      print "table does not exist"
      return
    myfile=open('metadata.txt')
    filesplit = myfile.read().splitlines()
    ind = filesplit.index(test_split[2])
    ind = ind+1
    flag=0
    testa=test_split[4].split('=')[1]
    nam=test_split[4].split('=')[0]
    e=0
    print testa,  
    while filesplit[ind]!=endtab:           
         if filesplit[ind] == nam:
             flag=1
             break
         e=e+1    
         ind=ind+1    
    if flag == 0:
        print "no such column"
        return 
   # testa=test_split[4].split('=')[1]
    shutil.copy('./'+test_split[2]+'.csv','./temp.csv')    
    with open('temp.csv', 'rb') as inp, open('./'+test_split[2]+'.csv', 'wb') as out:
        writer = csv.writer(out)
        for row in csv.reader(inp):
           flag=0
           if row[e]==testa:
              flag=1 
           if flag==0:     
               writer.writerow(row)
#delete_col()
def truncate(query):
  if os.path.exists(query[2]+".csv") is False: 
      print "table does not exist"
      return
  f = open(query[2]+".csv", "w")
  f.truncate()
  f.close()
test="drop table table2"
def drop():
  if os.path.exists(query[2]+'.csv') is False: 
      print "table does not exist"
      return
  i=0
  os.remove(query[2]+".csv")
  f = open("metadata.txt","r")   
  lines = f.readlines()
  f.close()
  temp=lines.index(query[2]+'\n')  
  f = open("metadata.txt","w")
  while i < len(lines): 
     if i == temp-1:
       while lines[i]!="<end_table>\n":
           i=i+1
           if lines[i]=="<end_table>\n":
              i=i+1
              break   
     f.write(lines[i])
     i=i+1 

#drop()    
  
def query_case1(query):
  metafile = open('metadata.txt')
  ending='<end_table>'
  meta_split = metafile.read().splitlines()
  myval=query[3]
  if myval not in meta_split:
   print "table does not exist"
  else:
   index = meta_split.index(myval)
   columns = []
   index=index+1
   column_name=""
   while meta_split[index] != ending:
     if meta_split[index+1] == ending:
       column_name =column_name + myval + "." +meta_split[index]
     else:
        column_name =column_name + myval + "." +meta_split[index] + ","
     columns.append(meta_split[index])
     index=index+1
   filename = myval + ".csv"
   fileopend = open(filename)

   print column_name
   print fileopend.read()


def get_column_index(col,split_entry):
        metafile = open('metadata.txt') 
	table_name = split_entry
	metafilesplit = metafile.read().splitlines()
	index = metafilesplit.index(table_name)
	index=index+1
	temp=0
	try:
		while metafilesplit[index] != col:
			temp=temp+1
			index=index+1
		return temp
	except IndexError:
		print "column doesnt exist"
		return -1
 
def query_case2_max(query):
        count=1
	iterator=1
        filename=query[3]
        try:
	 filetable = open(filename + ".csv", 'rt')
        except IOError:
         print "No such table"
         return   
	filetoread = csv.reader(filetable)
	element = []
	for entry in filetoread:
		element.append(entry)
        func = query[1]
	func = func[func.index("(") + 1:func.rindex(")")]
	temp = get_column_index(func,query[3])
	if temp == -1:
	  return
	element = [ map(int,x) for x in element ]
        lengofElement = len(element)
	maximum = element[0][temp]
	
	while iterator < lengofElement :
		if maximum <= element[iterator][temp]:
			maximum = element[iterator][temp]
                else:
                        count=count+1   
		iterator=iterator+1
	print filename + "." + func
	print maximum

def query_case2_min(query):
        count=1
	iterator=1
        filename=query[3]
        try:
	 filetable = open(filename + ".csv", 'rt')
        except IOError:
         print "No such table"
         return   
	filetoread = csv.reader(filetable)
	element = []
	for entry in filetoread:
		element.append(entry)
        func = query[1]
	func = func[func.index("(") + 1:func.rindex(")")]
	temp = get_column_index(func,query[3])
	if temp == -1:
	  return
	element = [ map(int,x) for x in element ]
        lengofElement = len(element)
	mini = element[0][temp]
	
	while iterator < lengofElement :
		if mini >= element[iterator][temp]:
			mini = element[iterator][temp]
                else:
                        count=count+1   
		iterator=iterator+1
	print filename + "." + func
	print mini

def query_case2_sum(query):
        count=1
	iterator=1
        filename=query[3]
        try:
	 filetable = open(filename + ".csv", 'rt')
        except IOError:
         print "No such table"
         return   
	filetoread = csv.reader(filetable)
	element = []
	for entry in filetoread:
		element.append(entry)
        func = query[1]
	func = func[func.index("(") + 1:func.rindex(")")]
	temp = get_column_index(func,query[3])
	if temp == -1:
	  return
	element = [ map(int,x) for x in element ]
        lengofElement = len(element)
	mini = element[0][temp]
	sum_len=0;
	while iterator < lengofElement :
		sum_len = sum_len + element[iterator][temp]   
		iterator=iterator+1

	print filename + "." + func
	print sum_len
      
def query_case2_average(query):
        count=1
	iterator=1
        filename=query[3]
        try:
	 filetable = open(filename + ".csv", 'rt')
        except IOError:
         print "No such table"
         return   
	filetoread = csv.reader(filetable)
	element = []
	for entry in filetoread:
		element.append(entry)
        func = query[1]
	func = func[func.index("(") + 1:func.rindex(")")]
	temp = get_column_index(func,query[3])
	if temp == -1:
	  return
	element = [ map(int,x) for x in element ]
        lengofElement = len(element)
	mini = element[0][temp]
	sum_len=0;
	while iterator < lengofElement :
		sum_len = sum_len + element[iterator][temp]   
		iterator=iterator+1
        avg=sum_len/float(lengofElement)

	print filename + "." + func
	print avg
wax="select distinct(C) from table1"
wax=wax.split()
def distinct(query_split):
        value = defaultdict(list)
        dot='.'
        comma=','
        myfile=open('metadata.txt')
	t = query_split[3]
	filesplit = myfile.read().splitlines()
        func=query_split[1].split('(')
        elemen=func[1].split(')')[0]
        mylista = []
        endtab='<end_table>'
	output = ""
        flag=0
        inx=0 
	try:
			ind = filesplit.index(t)
                        start=ind 
			ind = ind+1
                        while filesplit[ind]!=endtab:           
		                 if filesplit[ind] == elemen:
                                         flag=1
                                         break      
				 inx=inx+1 
                                 ind=ind+1 
	except ValueError:
			print "table doesn't exists"
			return
        if flag ==0:
           print "column does not  exist" 
           return    
        teq=[]
        with open(query_split[3]+'.csv', 'rb') as f:
    		reader = csv.reader(f)
   		for row in reader:
                    out=""
                    if teq.count(row[inx])==0:    
        		for x in row:
                          out=out+x+','
                        print out
                    teq.append(row[inx])

#distinct(wax)                  
def query_case3(query_split):
        value = defaultdict(list)
        dot='.'
        comma=','
        myfile=open('metadata.txt')
	mytables = query_split[3].split(',')
	filesplit = myfile.read().splitlines()
        mylista = []
        endtab='<end_table>'
	output = ""
	
	for t in mytables:
		try:
			ind = filesplit.index(t)
			ind = ind+1
			while filesplit[ind] != endtab:
				if filesplit[ind+1] == endtab:
					output=output+ t + dot + filesplit[ind]
				elif filesplit[ind+1] != endtab:
					output=output + t + dot + filesplit[ind] + comma
				value[t].append(filesplit[ind])
				ind=ind+1
		except ValueError:
			print "table doesn't exists"
			return
	
	myfile.close()
	output_columns = query_split[1].split(',')
	final_output = []
	for x in output_columns:
		temp_values_list = value.values()
		try:
			for temp in temp_values_list:
				if x in temp:
					final_output.append(value.keys()[value.values().index(temp)] + "." + x)
					
					f = open(value.keys()[value.values().index(temp)] + '.csv', 'rt')
					reader = csv.reader(f)
					row_list = []
					for row in reader:
						row_list.append(row)
					row_list = [ map(int,y) for y in row_list ]
					
					ind = get_column_index(x,value.keys()[value.values().index(temp)])
				
					
				        i = 0
					length = len(row_list)
                                        mylistb = []
					while i < length:
						mylistb.append(row_list[i][ind])
						i = i + 1
					f.close()
					mylista.append(mylistb)
		except IndexError:
			print "Column doesn't exist!"
			return

	output = ""
	for temp in final_output:
		if temp != final_output[len(final_output)-1]:
			output = output + temp + ','
		else:
			output = output + temp
	print output

	i = 0
	try:
		while i < len(mylista[0]):
			row_output = ""
			j = 0
			while j < len(mylista):
				if j != len(mylista)-1:
					row_output = row_output + str(mylista[j][i]) + ","
				else:
					row_output = row_output + str(mylista[j][i])
				j = j + 1
			print row_output
			i = i + 1
	except IndexError:
		print "column doesn't exists"
		return


def query_case4(query_split):
	tables = query_split[4].split(',')
	target = open('metadata.txt')
	target_split = target.read().splitlines()
	output = ""
	columns = defaultdict(list)
        print "ass " 
	for table in tables:
		index = target_split.index(table) 
		index = index + 1
		while target_split[index] != '<end_table>':
			if target_split[index+1] == '<end_table>':
				output += table + '.' + target_split[index]
			elif target_split[index+1] != '<end_table>':
				output += table + '.' + target_split[index] + ','
			columns[table].append(target_split[index])
			index = index + 1
	
	target.close()
	
	output_columns = query_split[2].split(',')
	list1 = []
	final_output = []
	for x in output_columns:
		temp_values_list = columns.values()
		
		for temp in temp_values_list:
			if x in temp:
				final_output.append(columns.keys()[columns.values().index(temp)] + "." + x)
				list2 = []
				f = open(columns.keys()[columns.values().index(temp)] + '.csv', 'rt')
				reader = csv.reader(f)
				row_list = []
				for row in reader:
					row_list.append(row)
				row_list = [ map(int,y) for y in row_list ]
				#print columns.keys()[columns.values().index(temp)]
				#print get_column_index(x, 'table1')
				index = get_column_index(x,columns.keys()[columns.values().index(temp)])
				#print index
				i = 0
				length = len(row_list)
				while i < length:
					list2.append(row_list[i][index])
					i = i + 1
				f.close()
				list1.append(list2)
	#print list1
	#print final_output
	output = ""
	for temp in final_output:
		if temp != final_output[len(final_output)-1]:
			output = output + temp + ','
		else:
			output = output + temp
	print output

	unique_data = [list(k) for k in set(tuple(k) for k in list1)]
	#print unique_data

	i = 0
	while i < len(unique_data[0]):
		row_output = ""
		j = 0
		while j < len(unique_data):
			if j != len(unique_data)-1:
				row_output = row_output + str(unique_data[j][i]) + ","
			else:
				row_output = row_output + str(unique_data[j][i])
			j = j + 1
		
		i = i + 1
	print row_output

def query_case5(query_split):
	tables = query_split[3].split(',')
	target = open('metadata.txt')
	target_split = target.read().splitlines()
	output = ""
	columns = defaultdict(list)
	for table in tables:
		index = target_split.index(table)
		index = index + 1
		while target_split[index] != '<end_table>':
			if target_split[index+1] == '<end_table>':
				output += table + '.' + target_split[index]
			elif target_split[index+1] != '<end_table>':
				output += table + '.' + target_split[index] + ','
			columns[table].append(target_split[index])
			index = index + 1
	#print output
	target.close()
	#print columns
	output_columns = query_split[1].split(',')
	list1 = []
	final_output = []
	for x in output_columns:
		temp_values_list = columns.values()
		#print temp_values_list
		for temp in temp_values_list:
			if x in temp:
				final_output.append(columns.keys()[columns.values().index(temp)] + "." + x)
				list2 = []
				f = open(columns.keys()[columns.values().index(temp)] + '.csv', 'rt')
				reader = csv.reader(f)
				row_list = []
				for row in reader:
					row_list.append(row)
				row_list = [ map(int,y) for y in row_list ]
				#print columns.keys()[columns.values().index(temp)]
				#print get_column_index(x, 'table1')
				index = get_column_index(x,columns.keys()[columns.values().index(temp)])
				#print index
				i = 0
				length = len(row_list)
				while i < length:
					list2.append(row_list[i][index])
					i = i + 1
				f.close()
				list1.append(list2)
	#print list1
	#print final_output
	flag1 = 0
	flag2 = 1
	if len(query_split) == 12:
		pass

	if len(query_split) == 8:
		operator = query_split[7]
		left_operand = query_split[6]
		right_operand = query_split[8]
	output = ""
	for temp in final_output:
		if temp != final_output[len(final_output)-1]:
			output = output + temp + ','
		else:
			output = output + temp
	print output

	i = 0
	while i < len(list1[0]):
		row_output = ""
		j = 0
		while j < len(list1):
			if j != len(list1)-1:
				row_output = row_output + str(list1[j][i]) + ","
			else:
				row_output = row_output + str(list1[j][i])
			j = j + 1
		print row_output
		i = i + 1
insert_entry=['INSERT','insert','Insert']
delete_entry=['DELETE','Delete','delete']
def parser(query):
    if query[0] == "CREATE" and query[1] == "TABLE":
        create(query)
    elif query[0] in insert_entry and query[1]=='into':  
        insert(query)
    elif query[0] in delete_entry and query[1]=='from':
        delete_col(query)        
    elif query[0]=="truncate" and query[1]=='table': 
         truncate(query)
    elif query[0]=="drop" and  query[1]=="table":
         drop(query)
    elif query[0] not in select_entry:
        print query[0] + ":Unknown query"
    else:
        if query[1] is '*' :
          if query[2] in from_entry:
            if len(query) != 4:
              print "Format is wrong"
            else:
              query_case1(query)
        elif query[1] in distinct_entry:
          query_case4(query)  	
 
        elif query[1].startswith("max"):
		query_case2_max(query)

        elif query[1].startswith("min"):
          query_case2_min(query)

        elif query[1].startswith("avg"):
          query_case2_average(query)

        elif query[1].startswith("sum"):
          query_case2_sum(query)
        elif query[1].startswith("distinct"):
          distinct(query)

        elif len(query[3].split(',')) >= 1 and len(query) <= 4:
        	query_case3(query)
                print 1
        elif len(query) >4 and query[4] in where_entry:
        	query_case5(query)

        
	#parser()
if __name__ == "__main__":
	#load_metadata()
	while True:
		s = raw_input('mysql> ')
                f=s
                f=f.split()
                f[len(f)-1]=f[len(f)-1].split(';')[0] 
		query = s.strip()
		while not s.strip().endswith(';'):
			s = raw_input('> ')
			query += ' '+ s.strip()
		query = query.strip().lower()
		if query == 'quit;' or query == 'quit ;':
			break
		else:
			parser(f)


