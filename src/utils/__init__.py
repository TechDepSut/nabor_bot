import os
import pygsheets


service_file = os.environ["service_file"]
gc = pygsheets.authorize(service_file=service_file)
sheetname = "Заявки 2022"
sh = gc.open(sheetname)

wks = sh.worksheet_by_title("Лист1")
