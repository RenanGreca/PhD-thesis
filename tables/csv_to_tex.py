import csv
from select import select

            #   'es': 'Exp. Subj.',
            #   'pl': 'Prog. Lng.',
            #   'ip': 'Ind. Part.',


papers = []

properties = {'im': 'Ind. Mot.',
              'ie': 'Ind. Eval.',
              'ia': 'Ind. Auth.',
              'pf': 'Prac. Feed.',
              'at': 'Avail. Tool',
              'pp': 'In Practice'}
colors     = {'im': 'olive',
              'ie': 'teal',
              'ia': 'brown',
              'pf': 'purple',
              'at': 'orange',
              'pp': 'cyan'}

counts      = {'tcp': 0,
               'tcs': 0,
               'tsr': 0,
               'tsa': 0
                }

def text_to_table(text):
    if ('TRUE' in text) or ('X' in text):
        return "\\checkmark"
    if 'MAYBE' in text:
        return "?"
    return " "


def text_to_bool(text):
    return ('TRUE' in text) or ('X' in text)


def text_to_circ(text):
    if ('TRUE' in text) or ('X' in text):
        return "\\fullcirc"
    if 'MAYBE' in text:
        return "\\halfcirc"
    return "\\emptycirc"


with open("secondary_list.csv") as csvfile:
    reader = csv.reader(csvfile) #, delimiter=',', quitechar='"')
    next(reader)
    next(reader)
    for row in reader:
        paper = {}

        paper['year'] = row[0]
        paper['title'] = row[2]
        paper['bibtex'] = row[3]
        paper['publisher'] = row[6]

        paper['tcp'] = row[17]
        if text_to_bool(paper['tcp']):
            counts['tcp'] += 1
        paper['tcs'] = row[18]
        if text_to_bool(paper['tcs']):
            counts['tcs'] += 1
        paper['tsr'] = row[19]
        if text_to_bool(paper['tsr']):
            counts['tsr'] += 1
        paper['tsa'] = row[20]
        if text_to_bool(paper['tsa']):
            counts['tsa'] += 1

        paper['im'] = row[23]
        paper['ie'] = row[24]
        paper['ia'] = row[28]
        paper['pf'] = row[29]
        paper['at'] = row[30]
        paper['pp'] = row[31]

        if text_to_bool(row[33]):
            papers.append(paper)

with open('numpapers.tex', 'w') as numpapersfile:
    numpapersfile.write("\\newcommand{\\numpapers}{"+str(len(papers))+"\\xspace}")

with open('csv_aliases.tex', 'w') as aliasesfile:
    for i in range(0, len(papers)):
        paper = papers[i]
        line = '\\defcitealias{'
        line += paper['bibtex']
        line += '}{'
        line += 'S'+str(i+1)
        line += '}\n'
        aliasesfile.write(line)

with open('nociteS.tex', 'w') as nocitefile:
    for i in range(0, len(papers)):
        paper = papers[i]
        line = '\\nociteS{'
        line += paper['bibtex']
        line += '}\n'
        nocitefile.write(line)

with open('csv_selected.tex', 'w') as selectedfile:
    for i in range(0, len(papers)):
        paper = papers[i]
        line = '\\rowselected{'
        line += paper['bibtex']
        line += '}{'
        line += paper['title']
        line += '}{'
        line += text_to_circ(paper['tcp'])
        line += '}{'
        line += text_to_circ(paper['tcs'])
        line += '}{'
        line += text_to_circ(paper['tsr'])
        line += '}{'
        line += text_to_circ(paper['tsa'])
        line += '}\n'
        selectedfile.write(line)
    selectedfile.write("\\hiderowcolors\n")
    selectedfile.write("\\midrule\n")
    selectedfile.write("& & & Totals & {} & {} & {} & {} \n \\\\ ".format(counts['tcp'], counts['tcs'], counts['tsr'], counts['tsa']))
    selectedfile.write("\\bottomrule\n")
    selectedfile.write("\\caption{Selected papers.}\n") 

with open('csv_relevance.tex', 'w') as relevancefile:
    for i in range(0, len(papers)):
        paper = papers[i]
        line = '\\rowrelevance{'
        line += paper['bibtex']
        line += '}{'            
        line += text_to_table(paper['im'])
        line += '}{'
        line += text_to_table(paper['ie'])
        line += '}{'
        line += text_to_table(paper['ia'])
        line += '}{'
        line += text_to_table(paper['pf'])
        line += '}{'
        line += text_to_table(paper['at'])
        line += '}{'
        line += text_to_table(paper['pp'])
        line += '}\n'
        relevancefile.write(line)
    relevancefile.write("\\hiderowcolors\n")
    relevancefile.write("\\bottomrule\n")
    relevancefile.write("\\caption{Relevance properties found in the papers.}\n")

def text_to_table2(text):
    if ('TRUE' in text) or ('X' in text):
        return True
    if 'MAYBE' in text:
        return False
    return False

# with open('csv_relevance.tex', 'w') as relevancefile:
#     half = int(len(papers)/2)
#     for i in range(0, half):
#         paper = papers[i]
        
#         line = '\\rowrelevance{'
#         line += paper['bibtex']
#         line += '}{'
#         paper_properties = []
#         for key, property in properties.items():
#             if text_to_table2(paper[key]):
#                 paper_properties.append("{\\color{"+colors[key]+"}"+property+"}")
#         line += ", ".join(paper_properties)
#         line += '}{'
#         paper = papers[i+half]
#         line += paper['bibtex']
#         line += '}{'
#         paper_properties = []
#         for key, property in properties.items():
#             if text_to_table2(paper[key]):
#                 paper_properties.append("{\\color{"+colors[key]+"}"+property+"}")
#         line += ", ".join(paper_properties)
#         line += '}\n'
#         relevancefile.write(line)
#     relevancefile.write("\\hiderowcolors\n")
#     relevancefile.write("\\bottomrule\n")

with open('csv_relevance.tex', 'w') as relevancefile:
    split = 5
    third = int(len(papers)/split)+1
    for i in range(0, third):
        paper = papers[i]

        line = ''
        for j in range(0, split):
            if i+(third*j) >= len(papers):
                continue
            paper = papers[i+(third*j)]
            line += '\\rowrelevance'
            line += '{'
            line += paper['bibtex']
            line += '}'
            paper_properties = []
            for key, property in properties.items():
                line += '{'+text_to_circ(paper[key])+'}'
            if j < split-1:
                line += ' & '
        line += '\\tabularnewline \n'
        relevancefile.write(line)
    relevancefile.write("\\hiderowcolors\n")
    relevancefile.write("\\bottomrule\n")

metrics = []
with open("metrics.csv") as csvfile:
    reader = csv.reader(csvfile) #, delimiter=',', quitechar='"')
    next(reader)
    for row in reader:
        metric = {}

        metric['type'] = row[0]
        metric['name'] = row[1]
        metric['refs'] = row[2]
        metric['tcp'] = row[3]
        metric['tcs'] = row[4]
        metric['tsr'] = row[5]
        metric['tsa'] = row[6]
        metric['desc'] = row[7]

        metrics.append(metric)


def cite_papers(selected):
    selected = selected.split(', ')
    tex = []
    for i in range(0, len(papers)):
        paper = papers[i]['bibtex']
        if paper in selected:
            tex.append("\citetalias{"+paper+"}")
    return ", ".join(tex)


with open('csv_metrics_effectiveness.tex', 'w') as metricsfile:
    for i in range(0, len(metrics)):
        metric = metrics[i]

        if metric['type'] == 'Effectiveness' and len(metric['refs']) > 1:
            line = '\\rowmetric{'
            line += metric['name']
            line += '}{'
            line += cite_papers(metric['tcp'])
            line += '}{'
            line += cite_papers(metric['tcs'])
            line += '}{'
            line += cite_papers(metric['tsr'])
            line += '}{'
            line += cite_papers(metric['tsa'])
            line += '}{'
            line += metric['desc']
            line += '}\n'
            metricsfile.write(line)
    metricsfile.write("\\hiderowcolors\n")
    metricsfile.write("\\bottomrule\n")

with open('csv_metrics_efficiency.tex', 'w') as metricsfile:
    for i in range(0, len(metrics)):
        metric = metrics[i]

        if metric['type'] == 'Efficiency' and len(metric['refs']) > 1:
            line = '\\rowmetric{'
            line += metric['name']
            line += '}{'
            line += cite_papers(metric['tcp'])
            line += '}{'
            line += cite_papers(metric['tcs'])
            line += '}{'
            line += cite_papers(metric['tsr'])
            line += '}{'
            line += cite_papers(metric['tsa'])
            line += '}{'
            line += metric['desc']
            line += '}\n'
            metricsfile.write(line)
    metricsfile.write("\\hiderowcolors\n")
    metricsfile.write("\\bottomrule\n")
        
with open('csv_metrics_other.tex', 'w') as metricsfile:
    for i in range(0, len(metrics)):
        metric = metrics[i]

        if metric['type'] == 'Other' and len(metric['refs']) > 1:
            line = '\\rowmetric{'
            line += metric['name']
            line += '}{'
            line += cite_papers(metric['tcp'])
            line += '}{'
            line += cite_papers(metric['tcs'])
            line += '}{'
            line += cite_papers(metric['tsr'])
            line += '}{'
            line += cite_papers(metric['tsa'])
            line += '}{'
            line += metric['desc']
            line += '}\n'
            metricsfile.write(line)
    metricsfile.write("\\hiderowcolors\n")
    metricsfile.write("\\bottomrule\n")

approaches = []
with open("approaches.csv") as csvfile:
    reader = csv.reader(csvfile) #, delimiter=',', quitechar='"')
    next(reader)
    for row in reader:
        approach = {}

        approach['type'] = row[0]
        approach['name'] = row[1]
        approach['refs'] = row[2]
        approach['tcp'] = row[3]
        approach['tcs'] = row[4]
        approach['tsr'] = row[5]
        approach['tsa'] = row[6]
        approach['desc'] = row[7]

        approaches.append(approach)



with open('csv_approaches_information.tex', 'w') as approachesfile:
    for i in range(0, len(approaches)):
        approach = approaches[i]

        if approach['type'] == 'Information' and len(approach['refs']) > 1:
            line = '\\rowapproach{'
            line += approach['name']
            line += '}{'
            line += cite_papers(approach['tcp'])
            line += '}{'
            line += cite_papers(approach['tcs'])
            line += '}{'
            line += cite_papers(approach['tsr'])
            line += '}{'
            line += cite_papers(approach['tsa'])
            line += '}{'
            line += approach['desc']
            line += '}\n'
            approachesfile.write(line)
    approachesfile.write("\\hiderowcolors\n")
    approachesfile.write("\\bottomrule\n")

with open('csv_approaches_algorithm.tex', 'w') as approachesfile:
    for i in range(0, len(approaches)):
        approach = approaches[i]

        if approach['type'] == 'Algorithm' and len(approach['refs']) > 1:
            line = '\\rowapproach{'
            line += approach['name']
            line += '}{'
            line += cite_papers(approach['tcp'])
            line += '}{'
            line += cite_papers(approach['tcs'])
            line += '}{'
            line += cite_papers(approach['tsr'])
            line += '}{'
            line += cite_papers(approach['tsa'])
            line += '}{'
            line += approach['desc']
            line += '}\n'
            approachesfile.write(line)
    approachesfile.write("\\hiderowcolors\n")
    approachesfile.write("\\bottomrule\n")
           
# with open('csv_approaches.tex', 'w') as approachesfile:
#     for i in range(0, len(papers)):
#         paper = papers[i]
        