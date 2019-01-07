import datetime


def sortFirst(val):
    return val[0]

class Lookup():

    def stage_group_lookup(self, stage, group, forecast = 5):

        f = open("tshwane.csv")

        line = f.readline()

        time_now = datetime.datetime.now()
        #print("Time Now:", time_now)
        list = []
        while line != None:
            line = line.replace("\n", "")
            entries = line.split(",")

            if "From" not in entries[0]:
                file_stage = int(entries[2].split(" ")[1])

                if file_stage <= stage:
                    day = time_now.day

                    # forecast
                    offset = 2
                    for i in range(0 + offset + day, 0 + offset + day + forecast):

                        if int(entries[i]) == group and int(entries[0].split(":")[0]) >= 9:
                            #print(i - 3, entries)
                            list.append([i - 3 + 1, entries[0], entries[1], entries[2]])


            line = f.readline()

            if line == "":
                break

        list = sorted(list, key=sortFirst)

        for item in list:
            affected_date = datetime.date(time_now.year, time_now.month, item[0])
            #print(affected_date, str(item[1] + "-" +  item[2]), item[3])

        return list