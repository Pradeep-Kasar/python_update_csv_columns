from tempfile import NamedTemporaryFile
import shutil
import csv

table1 = r'/Users/Pradeep/Downloads/DailyPEI-mmddyyyy.csv'
table2 = r'/Users/Pradeep/Downloads/CheckCutting_Lookup.csv'

feed_lookup = dict()
feed_pei = dict()

with open(table2) as tbl2:
    t2csv = csv.reader(tbl2)
    next(t2csv)  # skip heading
    for t2row in t2csv:
        feed_rpt = t2row[0]
        feed_cc = t2row[1]
        feed_lookup[feed_rpt] = feed_cc
    # print(feed_lookup)


tempfile = NamedTemporaryFile(mode='w', delete=False)

fields = ['id', 'ReportNumber', 'CheckCutting', 'indexid', 'date']

with open(table1, 'r', encoding='ascii') as csvfile, tempfile:
    reader = csv.DictReader(csvfile, fieldnames=fields)
    writer = csv.DictWriter(tempfile, fieldnames=fields, quoting=csv.QUOTE_ALL)
    for row in reader:
        for lookup_row in feed_lookup.items():
            if row['ReportNumber'] == str(lookup_row[0]):
                row['CheckCutting'] = lookup_row[1]
        row = {'id': row['id'], 'ReportNumber': row['ReportNumber'], 'CheckCutting': row['CheckCutting'], 'indexid': row['indexid'], 'date': row['date']}
        writer.writerow(row)

shutil.move(tempfile.name, table1)
