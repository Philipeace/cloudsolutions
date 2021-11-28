import re
import os
import snowflake.connector as sf
import pandas as pd
import config
from flask import Flask, request, render_template,  send_file, redirect
from werkzeug.middleware.proxy_fix import ProxyFix


app = Flask(__name__)

#important for nginx otherwise only timeouts while trying to make calls to functions
app.wsgi_app = ProxyFix(app.wsgi_app)

if os.name == "nt":
	files = "files"
else:
	files = "./files"


#create '/' endpoint
@app.route("/", methods=['POST','GET'])
def home():
	try:
		if request.method == 'POST':
			conn = sf.connect(user=config.username,account=config.account,password=config.password,role=config.role, warehouse = config.warehouse, database = config.database, schema = config.schema)
			#save files downloaded under POST
			f = request.files['file']
			f.save(os.path.join(files,f.filename))
			df = script(f.filename)
			#setting warehouse, database and schema
			cur = conn.cursor()
			cur.execute("USE WAREHOUSE \"{}\";".format(config.warehouse))
			cur.execute("USE DATABASE \"{}\";".format(config.database))
			cur.execute("USE SCHEMA \"{}\".\"{}\";".format(config.database,config.schema))
			cur.execute("SELECT * FROM \"{}\".\"{}\".\"{}\" LIMIT 10".format(config.database, config.schema,config.table))
			rows = cur.fetchall()
			return render_template('home3.html', rows=rows, filename=df)
		return render_template('home.html')
	except Exception as e:
		print(e)
		return render_template('home.html')
	finally:
		if request.method == 'POST':
			conn.close()

#create '/data' endpoint
@app.route('/data', methods=['GET'])
def data():
	#establish a snowflake connection and set working parameters
	conn = sf.connect(user=config.username,account=config.account,password=config.password,role=config.role, warehouse = config.warehouse, database = config.database, schema = config.schema)
	try:
		#setting warehouse, database and schema
		conn = sf.connect(user=config.username,account=config.account,password=config.password,role=config.role, warehouse = config.warehouse, database = config.database, schema = config.schema)
		cur = conn.cursor()
		cur.execute("USE WAREHOUSE \"{}\";".format(config.warehouse))
		cur.execute("USE DATABASE \"{}\";".format(config.database))
		cur.execute("USE SCHEMA \"{}\".\"{}\";".format(config.database,config.schema))
		# get data
		cur.execute("SELECT * FROM \"{}\".\"{}\".\"{}\" LIMIT 100".format(config.database, config.schema,config.table))
		rows = cur.fetchall()
		return render_template('data.html',rows=rows)
	except Exception as e:
		return render_template('data.html',rows=e)
	finally:
		conn.close()

#enable POST on '/data' endpoint to delete rows
@app.route('/data', methods=['POST','DELETE'])
def delete_data():
	create_row_delete_procedure()
	#establish a snowflake connection and set working parameters
	conn = sf.connect(user=config.username,account=config.account,password=config.password,role=config.role, warehouse = config.warehouse, database = config.database, schema = config.schema)
	try:
		#setting warehouse, database and schema
		cur = conn.cursor()
		cur.execute("USE WAREHOUSE \"{}\";".format(config.warehouse))
		cur.execute("USE DATABASE \"{}\";".format(config.database))
		cur.execute("USE SCHEMA \"{}\".\"{}\";".format(config.database,config.schema))
		#delete and show data
		cur.execute("CALL delete_row ({}) ;".format(request.form.get('col')))
		cur.execute("SELECT * FROM \"{}\".\"{}\".\"{}\" LIMIT 100".format(config.database, config.schema,config.table))
		rows = cur.fetchall()
		return render_template('data.html',rows=rows)
	except Exception as e:
		print(e)
		return render_template('data.html')
	finally:
		conn.close()

#create endpoint '/download' and redirect to home
@app.route('/download',methods=['GET'])
def getdown():
	return redirect("/")

#create download route to specific file
@app.route('/download/<string:filename>', methods=['GET'])
def download(filename):
	try:
		redirect("/")
		return send_file(os.path.join(files,filename), download_name=filename, as_attachment=True)
	except Exception as e:
		print(e)
		return redirect("/")

#procedure to stop SQL injections inside the .txt-files on endpoint '/'
def create_row_push_procedure():
	query =		'''CREATE OR REPLACE PROCEDURE add_row(docID string, Quelle string, Text string, Datum string, Titel string, Vorkommen string, Extra_Info string, Ressort string, Fachgebiet string)
				RETURNS Object
				LANGUAGE JAVASCRIPT
				AS
				$$
				var sql_query = `INSERT INTO \"{}\".\"{}\".\"{}\" VALUES (DEFAULT, :1, :2,:3,:4,:5,:6,:7,:8,:9);`
				var stmt = snowflake.createStatement( {} sqlText: sql_query, binds: [DOCID,QUELLE,TEXT,DATUM,TITEL,VORKOMMEN,EXTRA_INFO,RESSORT,FACHGEBIET] {} );
				var res  = stmt.execute();
				$$
				;'''.format(config.database,config.schema,config.table,"{","}")
	conn = sf.connect(user=config.username,account=config.account,password=config.password,role=config.role, warehouse = config.warehouse, database = config.database, schema = config.schema)
	cur = conn.cursor()
	try:
		cur.execute("USE WAREHOUSE \"{}\";".format(config.warehouse))
		cur.execute("USE DATABASE \"{}\";".format(config.database))
		cur.execute("USE SCHEMA \"{}\".\"{}\";".format(config.database,config.schema))
		cur.execute(query)
	except Exception as e:
		print(e)
	finally:
		conn.close()

#procedure to stop sql injections with POST on endpoint '/data'
def create_row_delete_procedure():
	query =		'''CREATE OR REPLACE PROCEDURE delete_row(ID float)
				RETURNS Object
				LANGUAGE JAVASCRIPT
				AS
				$$
				var sql_query = `DELETE FROM \"{}\".\"{}\".\"{}\" where \"id\" = :1;`
				var stmt = snowflake.createStatement( {} sqlText: sql_query, binds: [ID] {} );
				var res  = stmt.execute();
				$$
				;'''.format(config.database,config.schema,config.table,"{","}")
	conn = sf.connect(user=config.username,account=config.account,password=config.password,role=config.role, warehouse = config.warehouse, database = config.database, schema = config.schema)
	cur = conn.cursor()
	try:
		cur.execute("USE WAREHOUSE \"{}\";".format(config.warehouse))
		cur.execute("USE DATABASE \"{}\";".format(config.database))
		cur.execute("USE SCHEMA \"{}\".\"{}\";".format(config.database,config.schema))
		cur.execute(query)
	except Exception as e:
		print(e)
	finally:
		conn.close()




# insert single row into standard table
def push_data_row(data_row):
	create_row_push_procedure()
	conn = sf.connect(user=config.username,account=config.account,password=config.password,role=config.role, warehouse = config.warehouse, database = config.database, schema = config.schema)
	cur = conn.cursor()
	#clean up for sql:
	#create new list
	nl = []
	for str in data_row:
		if str == "":
			str = "null"
		else:
			str = "\'"+"".join(str.split("\""))+"\'"
		nl.append(str)
	try:
		#push single datarow
		cur.execute("CALL add_row ({},{},{},{},{},{},{},{},{});".format(nl[0],nl[1],nl[2],nl[3],nl[4],nl[5],nl[6],nl[7],nl[8]))
	except Exception as e:
		print(e)
	finally:
		conn.close()

#insert as many rows as needed
def push_data(data):
	create_row_push_procedure()
	sf.paramstyle = 'qmark'
	conn = sf.connect(user=config.username,account=config.account,password=config.password,role=config.role, warehouse = config.warehouse, database = config.database, schema = config.schema)
	cur = conn.cursor()
	#clean up for sql:
	final_dict = []
	l = len(data.get("docID"))
	for i in range(l):
		nl=[]
		for k,v in data.items():
			if v[i] == "":
				str = "null"
			else:
				str = "\'"+"".join(v[i].split("\""))+"\'"
			nl.append(str)
		final_dict.append((nl[0],nl[1],nl[2],nl[3],nl[4],nl[5],nl[6],nl[7],nl[8]))
	try:
		#push datarow
		cur.execute("USE WAREHOUSE \"{}\";".format(config.warehouse))
		cur.execute("USE DATABASE \"{}\";".format(config.database))
		cur.execute("USE SCHEMA \"{}\".\"{}\";".format(config.database,config.schema))
		cur.executemany("CALL add_row (?,?,?,?,?,?,?,?,?);", final_dict)
	except Exception as e:
		print(e)
	finally:
		conn.close()

#seperates the found texts from the rest of the file
def generate_texts_from_txt(file):
	x = open('files/'+file,"r", encoding="ISO-8859-1")
	relevanttext = str.split(x.read(),"gesamten Treffer")
	splittext = str.split(relevanttext[2],"\n\n")
	splittext = splittext[1:]
	x.close()
	return splittext

#generator to find occurences of characters on strings
def find_idx(str, ch):
	yield [i for i, c in enumerate(str) if c == ch]

#blackbox to extract information in rows/columns instead of .txt-file (with full texts)
def script(file):	
	all_texts = generate_texts_from_txt(file)
	resource_list, version_list, date_list, text_list, usage_list, area_list, title_list, ressort_list, docID_list = [[],[],[],[],[],[],[],[],[]]
	#loop through all texts
	for t in all_texts:
		#contingency code in case there is more than one date in the text
		#the date is relevant to determine where the other informations in the text are
		dates_found = re.search(r'\d{2}(\.|-)\d{2}(\.|-)\d{4}',t)
		if dates_found != None:
			span = dates_found.span()
			while dates_found != None:
				dates_found = re.search(r'\d{2}(\.|-)\d{2}(\.|-)\d{4}',t[span[1]:-1])
				if dates_found == None:
					break
				else:
					span = ((span[0]+ab.span()[0]),(span[1]+ab.span()[1]))
		#finding the relative position of the the informations parenthesis in the end of a text
		h = []		
		for idx in find_idx(t,"("):
			h+=idx
		if h != []:	
			if h[-1]<span[0] and '/' in t[h[-1]:span[0]]:
				text_only =t[0:h[-1]]
				info = t[h[-1]+1:-1]
			else:
				c = -1
				while h[c]>span[0] or '/' not in t[h[c]:span[0]]:
					print("running in while oooooh boy")
					if c == len(h)*-1:
						c =0 
						break
					c-=1
				text_only =t[0:h[c]]
				info = t[h[c]+1:-1]
		else:
			text_only =t
			info = t
		#extracting the usage found in the texts marked by <B> block(s)
		if "<B>" in text_only:
			search_container = str.split(text_only,"<B>")
			if len(search_container) >2:
				search_container = [search_container[0], "".join(search_container[1:])]
		else: search_container = ""
		if info:
			ab = re.search(r'\d{2}(\.|-)\d{2}(\.|-)\d{4}',info)
		else:         
			ab = ""
		if ab:
			date=info[ab.span()[0]:ab.span()[1]]
			info_start = info[0:ab.span()[0]]
			info_end = info[ab.span()[1]:]
		else:
			info_start= ""
			info_end = ""
			date=""
		origressort , sachgebiet= info_end, info_end
		source = str.split(info_start," ")
		origressort = str.split(origressort, "Originalressort: ")
		sachgebiet  = str.split(sachgebiet, "Sachgebiet: ")
		#save data on lists and variables
		if "Originalressort: " in info_end:
			ressort = str.split(origressort[1],';')[0]
		else:
			ressort = ""
		if "Sachgebiet: " in info_end:
			sachgebiet = str.split(sachgebiet[1],',')[0]
		else:
			sachgebiet = ""
		if ';' in info_end:
			title = str.split(info_end,';')[-1]
		else:
			title = ""
		if search_container:
			if "</>" in search_container[1]:
				search_results = str.split(search_container[1],"</>")[0]
				vorkommen = search_results
			else: vorkommen = ""
		else: vorkommen = ""
		h = []
		for idx in find_idx(info,'/'):
			h+=idx
		if h != []:
			docID=info[0:h[0]]
		else:
			docID=""
		quelle = "".join(source[1:])[:-1]
		version = source[0]
		text="".join(text_only)
		#add data to lists to create the csv from later
		docID_list.append(docID)
		resource_list.append(quelle)
		text_list.append(text)
		date_list.append(date)
		title_list.append(title)
		usage_list.append(vorkommen)
		version_list.append(version)
		ressort_list.append(ressort)
		area_list.append(sachgebiet)	
	#create dict to convert into pandas dataframe to export as csv
	d = {"docID":docID_list,"Quelle":resource_list,"Text":text_list,"Datum":date_list,"Titel":title_list,"Vorkommen":usage_list,"Extra-Info":version_list,"Ressort":ressort_list,"Fachgebiet":area_list}
	d = pd.DataFrame(data=d)
	d.to_csv(os.path.join("files",os.path.splitext(file)[0]+".csv"),index=False)
	return os.path.splitext(file)[0]+".csv"


if __name__ == '__main__':
	app.run()