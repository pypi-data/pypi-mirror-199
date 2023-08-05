iometer_template_str = """Version 1.1.0 
'TEST SETUP ====================================================================
'Test Description
	[*TEST_NAME*]
'Run Time
'	hours      minutes    seconds
	0          0          [*TIME_SECS*]
'Ramp Up Time (s)
	0
'Default Disk Workers to Spawn
	NUMBER_OF_CPUS
'Default Network Workers to Spawn
	0
'Record Results
	ALL
'Worker Cycling
'	start      step       step type
	1          1          LINEAR
'Disk Cycling
'	start      step       step type
	1          1          LINEAR
'Queue Depth Cycling
'	start      end        step       step type
	1          32         2          EXPONENTIAL
'Test Type
	NORMAL
'END test setup
'RESULTS DISPLAY ===============================================================
'Record Last Update Results,Update Frequency,Update Type
	ENABLED,1,LAST_UPDATE
'Bar chart 1 statistic
	Total I/Os per Second
'Bar chart 2 statistic
	Total MBs per Second (Decimal)
'Bar chart 3 statistic
	Average I/O Response Time (ms)
'Bar chart 4 statistic
	Maximum I/O Response Time (ms)
'Bar chart 5 statistic
	% CPU Utilization (total)
'Bar chart 6 statistic
	Total Error Count
'END results display
'ACCESS SPECIFICATIONS =========================================================
[*ACCESS_SPEC_DEFINE*]
'END access specifications
'MANAGER LIST ==================================================================
'Manager ID, manager name
	1,[*MANAGER*]
'Manager network address
	
'Worker
	Worker [*WORKER_#*]
'Worker type
	DISK
'Default target settings for worker
'Number of outstanding IOs,test connection rate,transactions per connection,use fixed seed,fixed seed value
	1,DISABLED,1,DISABLED,0
'Disk maximum size,starting sector,Data pattern
	0,0,0
'End default target settings for worker
'Assigned access specs
	[*SPEC_1*]
'End assigned access specs
'Target assignments
'Target
	[*TARGET_1*]
'Target type
	DISK
'End target
'End target assignments
'End worker
'End manager
'END manager list
Version 1.1.0 
"""

def generate_iometer_template():
    with open("IometerTemplate.dat", "w") as f:
        f.write(iometer_template_str)
