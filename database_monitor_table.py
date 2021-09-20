import MySQLdb as mysql
import time
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt
import os

os.system("banner Database")
db = mysql.connect(host = "localhost",user="root",passwd="123",db="INFORMATION_SCHEMA")
cur = db.cursor()
console = Console()

def gprint(string): 
	console.print(Text(string,style="bold green"))
def rprint(string): 
	console.print(Text(string,style="bold red"))
def bprint(string): 
	console.print(Text(string,style="bold blue"))
def yprint(string): 
	console.print(Text(string,style="bold yellow"))
		
def table_create(res1):
	table = Table(title="PROCESSLIST")
	table.add_column("USER", justify="left", style="cyan", no_wrap=True)
	table.add_column("HOST", style="magenta")
	table.add_column("COMMAND", justify="left", style="green")
	table.add_column("INFO ", justify="left", style="blue")
	for i in res1:
		i = list(i)
		if(i[3] != None):
			table.add_row(i[0],i[1],i[2],i[3])
		else:
			i[3]="None"
			table.add_row(i[0],i[1],i[2],i[3])
	console.print(table)
	
def table_show():
	cur.execute("select USER,HOST,COMMAND,INFO from PROCESSLIST;")
	res1 = list(cur.fetchall())
	table_create(res1)

def status_code():
	count = 0 
	while True:
		cur.execute('SHOW STATUS')
		res = cur.fetchall()
		count+=1
		yprint(f"______________________________{count}______________________________________________")
		for i in res:
			if i[0] == "Threads_connected":
				yprint(f"Threads_connected => {i[1]}")
			elif i[0] == "Threads_created":
				gprint(f"[bold green]Threads_created => {i[1]}")
			elif i[0] == "Threads_running":
				bprint(f"Threads_running => {i[1]}")
			elif i[0] == "Uptime":
				rprint(f"Uptime => {i[1]}")
			elif i[0] == "Max_used_connections":
				rprint(f"Max_used_connections => {i[1]}")
			elif i[0] == "Queries":
				gprint(f"Queries => {i[1]}")
			else:
				pass
		
		enter_string = Prompt.ask("press Enter to stop:") 
		if enter_string == "Enter":
			yprint("completed")
			break
		time.sleep(1)
def menu():
	gprint("[1]. Show status")
	gprint("[2]. Process queries")
	gprint("[3]. Exit")
	
while True:
	menu()
	ch = Prompt.ask("Enter your option", choices=["1", "2", "3"])
	if ch == "1":
		status_code()
	elif ch == "2":
		table_show()
	elif ch == "3":
		break
	
db.close()