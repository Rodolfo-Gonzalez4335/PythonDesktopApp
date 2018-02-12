
# defect_data_to_server.py
# Sends defect data to a MySQL database
# Last updated November 19, 2017
# Gopika Ajaykumar

# Turn on debug mode.
import cgitb
import sys
cgitb.enable()

# Print necessary headers.
print("Content-Type: text/html")
print()



# Get file names from command line and get a plot for each
def parsing(filepath):
# for i in range(1,len(sys.argv)):
    file = open(filepath,"r")
    for line in file:
        if 'DefectList' in line:
            for line in file:
                if 'SummarySpec' in line:
                    break
                nums = []
                line = line.replace(";", "")
                for num in line.split(" "):
                    try:
                        nums.append(float(num))
                    except ValueError:
                        pass
                print(nums)
                # query = "INSERT IGNORE INTO defects VALUES({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12});"
                # query = query.format(*nums)
                # c.execute(query)


# Print the contents of the database.
# c.execute("SELECT * FROM defects")
# print([(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11], r[12]) for r in c.fetchall()])
#
# conn.close()
