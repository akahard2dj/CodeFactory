import bs4
import csv

reader = csv.reader(open('senior_lsf.csv', 'r'), delimiter=',')

svg = open('seoul_districts.svg', 'r').read()

dentist_count = {}
count_only = []
min_value = 100
max_value = 0
past_header = False
for row in reader:
    if not past_header:
        past_header = True
        continue

    try:
        unique = row[0]
        count = float(row[1].strip())
        dentist_count[unique] = count
        count_only.append(count)
    except:
        pass

soup = bs4.BeautifulSoup(svg, "html.parser")

paths = soup.findAll('path')
colors = ["#CCE0FF", "#99C2FF", "#66A3FF", "#3385FF", "#0066FF", "#0052CC", "#003D99"]
g_style = 'font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1;stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;fill:'

for p in paths:
    try:
        print p['id']
        count = dentist_count[p['id']]
    except:
        continue

    if count > 600:
        color_class = 5
    elif count > 500:
        color_class = 4
    elif count > 300:
        color_class = 3
    elif count > 200:
        color_class = 2
    elif count > 50:
        color_class = 1
    else:
        color_class = 0

    color = colors[color_class]
    p['style'] = g_style + color

f = open('test.svg', 'w')
f.write(soup.prettify())
f.close()
