import csv
import os

def splitCSV(path, multiple):
    numTeams = {}   # dictionary for keeping track of institution team numbers
    institutionIndex = 0   # index for institution id
    # if there are multiple csv we name each csv "filename+Info.csv"
    # otherwise it will just be "Info.csv"
    if multiple:
        name = path[:-4]
    else:
        name = ""
    # Output directory. Check if it exists, if not make one.
    directory = os.path.join(".", "output")
    if not os.path.exists(directory):
        os.mkdir(directory)

    with open(path, 'r') as file:   # open the file in read mode
        csv_read = csv.reader(file)   # make a csv reader from the file
        for row in csv_read:   # iterate over the csv
            outstanding = 0   # flag for if the institution has an outstanding team
            meritorious = 0   # flag for if the institution has an meritorious or better team
            if row[7].lower() == "outstanding winner":
                outstanding = 1
                meritorious = 1
            if row[7].lower() in ["meritorious", "finalist"]:
                meritorious = 1
            if institutionIndex == 0:   # skip the header line
                institutionIndex += 1
                continue
            if numTeams.get(row[0].lower()) is None:   # if we haven't seen this institution before
                if row[4].lower() in ["us", "usa", "united states", "united states of america"]:
                    numTeams[row[0].lower()] = [row[0].lower(), 1, outstanding, meritorious]
                else:
                    numTeams[row[0].lower()] = [row[0].lower(), 1, outstanding]
                institutionIndex += 1
            else:
                currentTeam = numTeams.get(row[0].lower())
                if len(currentTeam) == 4:
                    numTeams[row[0].lower()] = [currentTeam[0], currentTeam[1] + 1, max(currentTeam[2], outstanding),
                                                max(currentTeam[3], meritorious)]
                else:
                    numTeams[row[0].lower()] = [currentTeam[0], currentTeam[1]+1, max(currentTeam[2], outstanding)]

    # actually write the info csv.
    try:
        with open(os.path.join(directory, name + "Info.csv"), "x", newline="") as file:
            sums = 0
            for row in numTeams.values():
                sums += row[1]
            average = sums / len(numTeams.values())
            newLine = ["Average Number of Teams per Institution"]
            csv_write = csv.writer(file)
            csv_write.writerow(newLine)
            csv_write.writerow([average])
            csv_write.writerow([""])
            newLine = ["Institution", "Teams Entered"]
            csv_write.writerow(newLine)
            toSort = []
            for row in numTeams.values():
                toSort.append(row)
            sortedList = sorted(toSort, key=lambda x: x[1], reverse=True)
            for row in sortedList:
                csv_write.writerow([row[0], row[1]])
            csv_write.writerow([""])
            csv_write.writerow(["Institutions who had Outstanding teams"])
            toSort = []
            for row in numTeams.values():
                if row[2] == 1:
                    toSort.append(row)
            sortedList = sorted(toSort, key=lambda x: x[0])
            for row in sortedList:
                csv_write.writerow([row[0]])
            csv_write.writerow([""])
            csv_write.writerow(["USA institutions with Meritorious or better teams"])
            for row in numTeams.values():
                if len(row) == 4:
                    csv_write.writerow([row[0]])

    except FileExistsError:
        print(name + "Info.csv already exists. Move or delete file in directory")


if __name__ == '__main__':
    # First we check if there are multiple csv to convert
    multipleCSV = False
    csvCount = 0
    for file in os.listdir("."):
        if file.endswith(".csv"):
            csvCount += 1
            if csvCount > 1:
                multipleCSV = True
                break
    # if there are multiple csv, we pass true for the 'multiple' flag
    for file in os.listdir("."):
        if file.endswith(".csv"):
            splitCSV(file, multipleCSV)
