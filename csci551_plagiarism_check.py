import os
import mosspy
import shutil

# Path to your directories that contain current and previous submissions. 
# In this sample script, current submission year is 2022.
work_dir = "/home/rajrup/tmp/moss_check/"
paths = {
	'2019': os.path.join(work_dir, '551-labs-fall19'),
	'2021': os.path.join(work_dir, '551-labs-spring21'),
	'2022': os.path.join(work_dir, '551-labs-spring22'),
	'base': os.path.join(work_dir, '551-labs-Rajrup') # Base code that is supplied by the instructor
}

# Change to the directory you want to compare
lab = "lab3"
year = "2022" # Current year
year2compare = "" # Previous year or empty string if you want to compare within the current year

userid = 236615579 # add your userid here
if lab == "lab2":
	language = "python"
else:
    language = "c"
m = mosspy.Moss(userid, language)

# Adding base files

base_path = os.path.join(paths['base'], lab)
if lab == "lab1":
	base_path = os.path.join(base_path, "router")

base_files = []
for file in os.listdir(base_path):
    # check only file extensions
    if file.endswith('.c') or file.endswith('.h') or file.endswith('.cpp') or file.endswith('.hpp'):
        base_files.append(file)
        m.addBaseFile(os.path.join(base_path, file))
    if lab == "lab2" and file.endswith('.py'):
        base_files.append(file)
        m.addBaseFile(os.path.join(base_path, file))
        
# print(base_files)

# Adding submission Files

sub_paths = []
for key, value in paths.items():
	if (key == year or key == year2compare) and key != 'base':
		tmp_paths = [os.path.join(paths[key], student, lab) for student in os.listdir(paths[key])]
		if lab == "lab1":
			tmp_paths = [os.path.join(sub_path, "router") for sub_path in tmp_paths]
		sub_paths.extend(tmp_paths)

for sub_path in sub_paths:
	# print(sub_path)
	assert(os.path.exists(sub_path))
	if language == "c":
		m.addFilesByWildcard(os.path.join(sub_path, "*.c"))
		m.addFilesByWildcard(os.path.join(sub_path, "*.h"))
	elif language == "cc":
		m.addFilesByWildcard(os.path.join(sub_path, "*.cpp"))
		m.addFilesByWildcard(os.path.join(sub_path, "*.hpp"))
	elif language == "python":
		m.addFilesByWildcard(os.path.join(sub_path, "*.py"))

# print(f"Sub Paths: {sub_paths}")

# progress function optional, run on every file uploaded
# result is submission URL
url = m.send(lambda file_path, display_name: print('*', end='', flush=True))
print()

print ("Report URL: " + url)

# Find the reports under work_dir/report/
if year2compare != "":
    report_path = os.path.join(work_dir, "report", year2compare, lab) # Previous year
else:
    report_path = os.path.join(work_dir, "report", year, lab) # Current year
if os.path.exists(report_path):
    shutil.rmtree(report_path)
os.makedirs(report_path)

# Save report file
m.saveWebPage(url, os.path.join(report_path, "report.html"))

mosspy.download_report(url, os.path.join(report_path, "report"), connections=1, log_level=10, on_read=lambda url: print('*', end='', flush=True)) 
# log_level=logging.DEBUG (20 to disable)
# on_read function run for every downloaded file

print("Please find the report in {}".format(os.path.join(report_path, "report", "index.html")))