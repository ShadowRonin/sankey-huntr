import plotly.graph_objects as go
from csvToDict import csvToDict
from datetime import datetime

def plotJobs(activitiesPath, plotTitle, jobBoardName = None):
    activities = csvToDict(activitiesPath)

    totals = {
        "Apply": {
            "order": 1,
            "count": 0,
            "jobNames": [],
            "color": "#7D44BB",
            "lineColor": "rgba(125, 68, 187, 0.2)",
        },
        "Interview": {
            "order": 2,
            "count": 0,
            "jobNames": [],
            "color": "#4497bb",
            "lineColor": "rgba(68, 151, 187, 0.2)",
        },
        "Second Interview": {
            "order": 3,
            "count": 0,
            "jobNames": [],
            "color": "#44a7bb",
            "lineColor": "rgba(68, 167, 187, 0.2)",
        },
        "Third Interview": {
            "order": 4,
            "count": 0,
            "jobNames": [],
            "color": "#44b5bb",
            "lineColor": "rgba(68, 181, 187, 0.2)",
        },
        "Forth Interview": {
            "order": 5,
            "count": 0,
            "jobNames": [],
            "color": "#44bba9",
            "lineColor": "rgba(68, 187, 169, 0.2)",
        },
        "Offer Received": {
            "order": 6,
            "count": 0,
            "jobNames": [],
            "color": "#44bb95",
            "lineColor": "rgba(68, 187, 149, 0.2)",
        },
        "Offer Accepted": {
            "order": 7,
            "count": 0,
            "jobNames": [],
            "color": "#48bb44",
            "lineColor": "rgba(72, 187, 68, 0.2)",
        }
    }

    for row in activities:
        cat = row["activityCategoryName"]
        company = row["companyName"]

        if jobBoardName != None and row["boardName"] != jobBoardName:
            continue

        if cat == "Apply":
            if company not in totals["Apply"]["jobNames"]:
                totals["Apply"]["count"] += 1
                totals["Apply"]["jobNames"].append(company)
        elif "Interview" in cat or "Screen" in cat:
            if company not in totals["Interview"]["jobNames"]:
                totals["Interview"]["count"] += 1
                totals["Interview"]["jobNames"].append(company)
            elif company not in totals["Second Interview"]["jobNames"]:
                totals["Second Interview"]["count"] += 1
                totals["Second Interview"]["jobNames"].append(company)
            elif company not in totals["Third Interview"]["jobNames"]:
                totals["Third Interview"]["count"] += 1
                totals["Third Interview"]["jobNames"].append(company)
            elif company not in totals["Forth Interview"]["jobNames"]:
                totals["Forth Interview"]["count"] += 1
                totals["Forth Interview"]["jobNames"].append(company)
        elif cat == "Offer Received":
            if company not in totals["Offer Received"]["jobNames"]:
                totals["Offer Received"]["count"] += 1
                totals["Offer Received"]["jobNames"].append(company)
        elif cat == "Accept Offer":
            if company not in totals["Offer Accepted"]["jobNames"]:
                totals["Offer Accepted"]["count"] += 1
                totals["Offer Accepted"]["jobNames"].append(company)
        else:
            print("Unknown category!")

    def mapTotals(name):
        data = totals[name]
        data["name"] = name
        return data

    totals = list(map(mapTotals, totals.keys()))

    totals = list(filter(lambda x: x["count"] > 0, totals))

    totals = sorted(totals, key=lambda x: x["order"])

    labels = list(map(lambda x: x["name"], totals))
    labels.append("Rejected")

    colors = list(map(lambda x: x["color"], totals))
    colors.append("#BB4446")

    sources = []
    targets = []
    values = []
    lineColors = []
    lineLabels = []

    for i, total in enumerate(totals):
        nextCount = totals[i + 1]["count"] if i < len(totals) - 1 else 0
        rejectCount = total["count"] - nextCount

        if(nextCount > 0):
            sources.append(i)
            targets.append(i + 1)
            values.append(nextCount)
            lineLabels.append(total["name"])
            lineColors.append(total["lineColor"])

        if(i < len(totals) - 1):
            sources.append(i)
            targets.append(len(labels) - 1)
            values.append(rejectCount)
            lineLabels.append(total["name"])
            lineColors.append("rgba(187, 68, 70, 0.4)")

    for i, label in enumerate(labels):
        count = 0
        for j, target in enumerate(targets if i > 0 else sources):
            if target == i:
                count += values[j]

        labels[i] = f'{label}: {count}'
    


    fig = go.Figure(data=[go.Sankey(
        node = dict(
        pad = 5,
        thickness = 10,
        line = dict(color = "black", width = 0.5),
        label = labels,
        color = colors,
        ),
        link = dict(
        source = sources,
        target = targets,
        value = values,
        label = lineLabels,
        color = lineColors,
    ))])

    fig.update_layout(title_text=plotTitle, font_size=10)
    fig.show()