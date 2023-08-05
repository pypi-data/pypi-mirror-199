
import os
import tempfile
import sys
import time
import logging
import re
import traceback
import subprocess
from sys import platform
from abc import ABC

# Quarchpy imports
from quarchpy.disk_test.dtsGlobals import dtsGlobals
from quarchpy.disk_test.base_test import BaseTest
from quarchpy.disk_test.driveTestCore import get_quarch_modules_qps, DiskStatusCheck, is_tool
from quarchpy.fio.performanceClass import FioPerformance
from quarchpy.disk_test.Drive_wrapper import DriveWrapper


class PowerVsPerformance(BaseTest, ABC):
    def __init__(self):
        # All tests call super.__init__() to declare parent class values ( e.g. dtscomms )
        super(PowerVsPerformance, self).__init__()

        ### Declaring custom variables for the test ###

        self.cv_averaging = self.declare_custom_variable(custom_name="averaging", default_value="512",
                                                         description="Sampling rate for QPS",
                                                         accepted_vals=['32k', '16k', '8k', '4k', '2k', '1k', '512',
                                                                        '256', '128', '64'])


        ### Declare additional variables that may not be visible to the user by default ###

        self.cv_fio_job = self.declare_custom_variable(custom_name="Custom FIO Job", default_value="",
                                                       description="Supply custom FIO job file here.", is_file=True)  # made internal

        self.cv_drivename = self.declare_custom_variable(custom_name="driveName", default_value=None,
                                                         var_purpose="internal")

        self.cv_quarchname = self.declare_custom_variable(custom_name="quarchName", default_value=None,
                                                          var_purpose="internal")


        ### Declaring child class variables - Never to be altered by user ###

        self.callbacks = {"workload_end_callback": self.notifyTestEnd, "stream_data_callback": self.notifyTestPoint}
        self.stream_data = ['stream_read_iops', 'stream_write_iops', "stream:jobs:job options:bs"]
        self.bs_retrieval = "find:jobs:job options:bs"
        self.iodepth_retrieval = "find:jobs:job options:iodepth"
        self.read_mean_iops = "find:jobs:read:iops_mean"
        self.write_mean_iops = "find:jobs:write:iops_mean"

        self.best_qd = 1
        self.bst_qd_mb_s = 0
        self.quarch_stream = None
        self.is_streaming = False
        self.annotation_time_correction_start = 0
        self.annotation_time_correction_end = 0
        self.performance = FioPerformance()
        self.fio_error = ""
        self.fio_job_args = []
        self.fio_job_args_dict = {}

        self.output = {}

        self.highest_QD = 1

        # If on a linux machine, Power vs Perf 1.00 uses smartctl for drive detection
        self.linux_drive_search = None


    def check_prerequisites(self, document_mode=False):
        # All child classes call super to check all mandatory imports are here.
        super(PowerVsPerformance, self).check_prerequisites()

        if not is_tool("fio"):
            self.test_errors.append("Fio Not found on server machine. Please install and restart server")

        try:
            import pandas as pd
        except ImportError as IE:
            self.test_errors.append("Pandas python library not found. Please install and restart server.")

        # If on a linux machine, check smartctl is available on the system
        if not platform == "win32":
            if not is_tool("smartctl"):
                self.test_errors.append("Smartctl not found on server machine. Please install and restart server")


    def start_test(self, document_mode=False):

        self.reset_test_variables(document_mode)

        if not self.setup_test():
            return


        try:

            group_name = "Custom FIO Job"

            self.test_id.up_tier(description=group_name)

            self.test_point(self.test_id.gen_next_id(), function=self._add_qps_comment,
                            function_description="Adding start of test comment",
                            function_args={"description": "Starting " + str(group_name)})

            self.custom_fio_job(group_name)

            self.check_point(self.test_id.gen_next_id(), function=self.check_stream_state,
                             description=str(self.test_id.return_parent_id()) + " " + group_name, function_args={"x": "Unused"})

            self.test_id.down_tier()

        except Exception as e:
            print(e)
            print(traceback.format_exc())

        self._end_quarch_stream()

    def setup_test(self):
        self.test_point(self.test_id.gen_next_id(), test_description="Setting up required test resources")
        self.test_id.up_tier(singular=True)

        # Request QPS start if not already open
        if not self.request_qps():
            self.test_errors.append("No running QPS instance found. Is QPS running on client Java PC?")
            return False

        # checking the user provided job file to see if it's OK to proceed with the test.
        if not self.check_fio_job_file():
            self.comms.send_stop_test(reason="Invalid file sent for FIO : ")
            return False

        self.cv_quarchname.custom_value = self.select_quarch_module(use_qps=True, power_on=True)

        if not self.cv_quarchname.custom_value:
            self.comms.send_stop_test(reason="No Quarch Module Selected")
            return False

        # Potentially already have a target drive specified in the job file.
        if not self.cv_drivename.custom_value:

            if platform == "win32":
                self.cv_drivename.custom_value = self.select_drive("sas")
            else:
                # Selecting drives via SmartCTL - ( Fulfill FIO need for /dev/sda )
                self.cv_drivename.custom_value = self.select_drive("smart")

        if not self.cv_drivename.custom_value:
            self.comms.send_stop_test(reason="No Drive Selected")
            return False

        self._start_quarch_stream()

        self.test_id.down_tier()

    def reset_test_variables(self, document_mode):
        self._set_documentation_mode(document_mode)
        self.test_id.reset()

    def custom_fio_job(self, group_name):

        """
        Function to run custom workload
        1 - report arguments
        2 - start workload
        3 - check if errors occured
        4 - plot start + end annotations
        5 -

        :param group_name:
        :return:
        """

        self.test_id.up_tier("Custom FIO Job", add_to_current_tier=True, singular=True)

        self._report_fio_args(self.fio_job_args_dict)

        retval = self.test_point(self.test_id.gen_next_id(), function_description="Performance test",
                                 function=self.performance.start_workload, has_return=True, stop_timeout=True,
                                 function_args={"cmd_line_args": self.fio_job_args, "output_data": self.output})

        if not self.check_for_errors(retval, self.fio_job_args_dict):
            self.test_id.down_tier(singular=True)
            return

        self.add_qps_job_annotations(retval)

        self.test_point(self.test_id.gen_next_id(), function_description="Results of mixed IO test",
                        function=self._results_mixed_IO_performance,
                        function_args={"results_dict": retval, "group_name": group_name,
                                       "parent_id": self.test_id.return_parent_id()})

        self.test_id.down_tier(singular=True)

    def _results_mixed_IO_performance(self, parent_id, results_dict, group_name):
        """
        MB/s
        IOPS
        MB/S PER WATT
        AVG POWER
        MAX POWER
        """
        read_iops = 0
        write_iops = 0
        bs = "4k"
        io_depth = 0
        for key, value in results_dict.items():
            if key in self.write_mean_iops[5:]:
                write_iops = value
            elif key in self.read_mean_iops[5:]:
                read_iops = value
            if key in self.bs_retrieval[5:]:
                bs = value

        qps_results = {}
        item_to_get = [["power Tot Max", "uW"], ["power Tot Mean", "uW"]]
        if not self._request_stats_qps(parent_id=parent_id, request_dict=qps_results, items_to_get=item_to_get):
            return

        read_mb_s = self.get_mb_s(bs=bs, iops=read_iops)
        write_mb_s = self.get_mb_s(bs=bs, iops=write_iops)

        watts = float(qps_results["power Tot Mean uW"]) / 1000000
        read_mb_s_per_watt = read_mb_s / watts
        write_mb_s_per_watt = write_mb_s / watts

        results = {"Average read MB/S": str(read_mb_s) + "MB/s",
                   "Average read IOPS": read_iops,
                   "Avg read MB/S per watt": str(read_mb_s_per_watt) + "MB/s/W",
                   "Average write MB/S": str(write_mb_s) + "MB/s",
                   "Average write IOPS": write_iops,
                   "Avg write MB/S per watt": str(write_mb_s_per_watt) + "MB/s/W",
                   "Average power": str(self.convert_to_base_unit(qps_results["power Tot Mean uW"], "u")) + "W",
                   "Max power": str(self.convert_to_base_unit(qps_results["power Tot Max uW"], "u")) + "W",
                   }

        self.log_results(results, str(parent_id) + " " + str(group_name))

    def log_results(self, results, group):
        for key, value in results.items():
            if "Issue retrieving QPS Data" in str(value):
                self.comms.create_request_log(time.time(), "error", "Error executing Function",
                                              sys._getframe().f_code.co_name,
                                              {key: str(value)}, uId="")
            else:
                # Note for reader - formatted values to 3dp
                try:
                    format_value = 0
                    if isinstance(value, str):
                        units_value = re.compile("[^\W\d]").search(str(value))

                        units = value[units_value.start():]
                        value = value[:units_value.start()]
                        value = str(format(float(value), ".3f")) + " " + str(units)
                    elif not value:
                        value = "N/A"
                    else:
                        value = str(format(float(value), ".3f"))

                    self.comms.sendMsgToGUI(
                        self.comms.create_request_log(time.time(), "result_statistic",
                                                      str(key) + " : " + value,
                                                      sys._getframe().f_code.co_name,
                                                      messageData={'group': group}, uId=""))
                except ValueError as e:
                    logging.warning(traceback.print_exc())

                    self.comms.sendMsgToGUI(
                        self.comms.create_request_log(time.time(), "error",
                                                      "Error logging statistics",
                                                      sys._getframe().f_code.co_name,
                                                      messageData={'group': group}, uId=""))

    def _request_stats_qps(self, parent_id, request_dict, items_to_get=None, is_idle=False):

        logging.debug("Entered request stats")

        # Giving time for stats to be calculated
        time.sleep(1)

        start_annotation = "START:" + str(parent_id)
        end_annotation = "END:" + str(parent_id)
        idle_annotaton = "IDLE:" + str(parent_id)

        # check we can / are still streaming prior to attempting get stats.
        if not self.check_stream_state():
            return False

        logging.debug("Stream still available")

        stats = self.quarch_stream.get_stats()

        logging.debug("Got stats from QPS")

        try:
            anno = idle_annotaton
            if is_idle:
                stat = stats.loc[stats['Text', "NA"] == idle_annotaton]
            else:
                anno = start_annotation
                stat = stats.loc[stats['Text', "NA"] == start_annotation]
            if items_to_get:
                for item in items_to_get:
                    x = stats.loc[:, "Text"]
                    index_row = stats[stats["Text", "NA"] == anno].index.values
                    index_col = stats.columns.values.tolist()
                    index_col = index_col.index((item[0], item[1]))
                    value = stats.iloc[index_row, index_col]
                    key = " ".join(item)
                    request_dict[key] = value.iloc[0]
                return True

            return True
        except Exception as e:
            logging.warning(e)
            return False

    def get_mb_s(self, bs, iops):

        ibs = 0

        if str(bs).endswith("k"):
            # MBps = (IOPS * KB per IO) / 1024
            ibs = (iops * int(str(bs).replace("k", ""))) * 1024
        else:
            ibs = iops * int(bs)

        # https://stackoverflow.com/questions/8905164/how-do-i-calculate-mb-s-mib-s
        # MiB/s = 1,048,576 bytes per second
        # MB/s = 1,000,000 bytes per second
        # conversion Mibs > mb/s = (1,000,000/1,048,576) = 0.95367 and a bit..
        # MB/S = MiBs / 0.95367
        mb_s = (float(ibs) / 0.95367) / 1000000

        return mb_s

    def _report_fio_args(self, fio_args):
        """
        Adds every key + value to QCS as comments

        :param fio_args: dictionary of FIO args + values
        :return: N/A
        """
        if not dtsGlobals.continueTest:
            return

        if self.document_mode is False:
            for item, value in fio_args.items():
                self.comms.sendMsgToGUI(
                    self.comms.create_request_log(time.time(), "Comment", "{0} : {1}".format(str(item), str(value)),
                                                  sys._getframe().f_code.co_name, uId=""))

    def check_for_errors(self, fio_dict, fio_args):
        if self.document_mode is True:
            return True

        if not fio_dict or not isinstance(fio_dict, dict):
            description = "Failure occured during retrieval of FIO results"

            self.comms.sendMsgToGUI(
                self.comms.create_request_log(time.time(), "testResult", description, sys._getframe().f_code.co_name,
                                              messageData=fio_args, test_result="False",
                                              uId=self.test_id.gen_next_id()))
            return False

        if "error" in fio_dict.keys():
            description = "Failure occured during execution of FIO workload : {0}".format(str(fio_dict["error"]))

            self.comms.sendMsgToGUI(
                self.comms.create_request_log(time.time(), "testResult", description, sys._getframe().f_code.co_name,
                                              messageData=fio_args, test_result="False",
                                              uId=self.test_id.gen_next_id()))
            return False

        return True

    def notifyTestEnd(self, unused_str, timeStamp):

        # print("entered end seq : " + time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime()) + " : " + str(time.time()) +
        #       " : time_stamp = " + str(timeStamp))

        # breaking data input to graph between tests
        self.quarch_stream.addDataPoint('read_iops', 'IOPS', "endSeq", str(int(timeStamp) + 100))
        self.quarch_stream.addDataPoint('write_iops', 'IOPS', "endSeq", str(int(timeStamp) + 100))
        self.quarch_stream.addDataPoint('write_throughput', 'MB/s', "endSeq", str(int(timeStamp) + 100))
        self.quarch_stream.addDataPoint('read_throughput', 'MB/s', "endSeq", str(int(timeStamp) + 100))

    def notifyTestPoint(self, ret_val):

        # print("entered test point : " + time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime()) + " : " + str(time.time()) +
        #       " : time_stamp = " + str(ret_val['timestamp_ms']))
        self.quarch_stream.addDataPoint('read_iops', 'IOPS', ret_val['stream_read_iops'], ret_val['timestamp_ms'])
        self.quarch_stream.addDataPoint('write_iops', 'IOPS', ret_val['stream_write_iops'], ret_val['timestamp_ms'])

        bs = "4k"
        # bs = ret_val["jobs:job options:bs"]

        read_mb_s = self.get_mb_s(bs, ret_val['stream_read_iops'])
        write_mb_s = self.get_mb_s(bs, ret_val['stream_write_iops'])

        self.quarch_stream.addDataPoint('write_throughput', 'MB/s', write_mb_s, ret_val['timestamp_ms'])
        self.quarch_stream.addDataPoint('read_throughput', 'MB/s', read_mb_s, ret_val['timestamp_ms'])

    def check_stream_state(self, x=None):

        if self.document_mode is True:
            return True

        running = self.test_point(function=self._add_quarch_command, has_return=True,
                                  function_args={"command": "stream?", "expected_response": ["running"],
                                                 "quarch_device": self.cv_quarchname.custom_value})

        if not running:
            self.comms.sendMsgToGUI(
                self.comms.create_request_log(time.time(), "error", "Quarch device has stopped streaming",
                                              sys._getframe().f_code.co_name, uId=""))

            # self.comms.send_stop_test(reason="Device has stopped streaming.")
            self.is_streaming = False
            dtsGlobals.continueTest = False
            self.comms.send_stop_test(reason="No Drive Selected")
            return False

        return True

    def convert_to_base_unit(self, value, output_unit, precision=None):
        """

        Output unit : (Char) - Represents the unit to convert to

        m = Milli
        u = Micro
        n = Nano

        """

        conversion_dict = {"m": -3, "u": -6, "n": -9}

        output_val = None
        if output_unit in conversion_dict.keys():
            output_val = conversion_dict[output_unit]
        else:
            logging.debug("Wrong output unit " + str(output_unit))
            return value

        ret_val = value * (10 ** output_val)

        if not precision:
            return ret_val
        else:
            return round(ret_val, precision)



    """
    Job file arguments and setup
    """

    def check_fio_job_file(self):
        """
        Things checked in the method :
            - Was a fio job file provided?
            - Is there a drive provided in that job file?
            -

        :return: Boolean : True if good job file else False
        """


        if self.document_mode:
            return True

        # Need to reset this here as the documentation mode sets a drive wrapper value
        # Skips drive selection if drivewrapper is assigned to this value
        self.cv_drivename.custom_value = None

        if not self.cv_fio_job.custom_value:
            self.fio_error = "No custom test file selected. \nPlease choose a jobfile using custom variables"
            return False

        # Find all filenames and directories.

        self.find_filename()

        self.create_cmd_line_job_args()

        self.assign_output_values()

        return True

    def create_cmd_line_job_args(self):
        job = str(self.cv_fio_job.custom_value).split("\n")
        # remake all valid lines as --key=value
        output_file = False
        for item in job:
            if "output" in item:
                if not "format" in item:
                    output_file = True
            if item == "":
                continue
            if "global" in item:
                continue
            if item.startswith("["):
                self.fio_job_args_dict["--" + "name"] = item[1:-1]
                self.fio_job_args.append("--name=" + item[1:-1])
                continue
            if "=" in item:
                key_value = item.split("=")
                self.fio_job_args_dict["--" + key_value[0]] = key_value[1]
                self.fio_job_args.append("--" + item)
            else:
                self.fio_job_args_dict["--" + item] = ""
                self.fio_job_args.append("--" + item)

        if not output_file:
            self.fio_job_args.insert(1, "--output=fioOutput.txt")
            self.fio_job_args_dict["output"] = "fioOutput.txt"
            self.fio_job_args.insert(1, "--output-format=json")
            self.fio_job_args_dict["output-format"] = "json"

    def find_filename(self):
        """
        checks for filename argument
            - tries to find drives from drives found on system
            - If found in file, but not on system, returns a custom drive wrapper
            - If not found filename argument - Test will prompt user for drive selection

        :return: N/A
        """

        if "filename" in self.cv_fio_job.custom_value:
            count = self.cv_fio_job.custom_value.count("filename=")
            if count > 1:
                # TODO : what happens if there's double filename?
                value = str(self.cv_fio_job.custom_value).split("filename")
            else:
                drive_path = self.get_filename_value()
                self.cv_drivename.custom_value = self.find_drive_from_fio_path(drive_path)

    def assign_output_values(self):
        """
        Reads through the send fio job

        Finds specific arguments in order to determine what output to draw

        :return:
        """

        summary_data = []
        is_read = False
        if "read" in self.cv_fio_job.custom_value:
            is_read = True
            summary_data.append("read_iops")
            summary_data.append(self.read_mean_iops)
        if "write" in self.cv_fio_job.custom_value:
            summary_data.append("write_iops")
            summary_data.append(self.write_mean_iops)
        if "percentile_list" in self.cv_fio_job.custom_value:
            if is_read:
                summary_data.append("latency_percentiles_read")
            else:
                summary_data.append("latency_percentiles_write")

        summary_data.append(self.bs_retrieval)

        self.output = {"summary_data": summary_data, "stream_workload_callbacks": self.callbacks,
                       "stream_data": self.stream_data}

    def get_filename_value(self):
        """
        Returning the value of 'filename' argument if it was provided in the FIO job

        :return: FIO job path
        """

        # Cannot make exception as requires 1 filename parameter in order to get to this function
        end_index = str(self.cv_fio_job.custom_value).split("filename=")
        drive_path = end_index[1]
        drive_path = drive_path[: str(drive_path).find("\n")]

        if ":" in drive_path:
            # TODO : There are 2 + filenames the job is being performed on
            drive_path = drive_path.split(":")
            drive_path = drive_path[0]
            # TODO : Make user aware that we only chose the first filename parameter in order to record values?

        return drive_path

    def find_drive_from_fio_path(self, fio_path):
        """
        Attempts to find the drive from currently working drive detection mechanisms

        :param fio_path: String, filename parameter passed to FIO
                                Windows: \\.\PHYSICALDRIVEx
                                LINUX  : /dev/sda
        :return: DriveWrapper :
                    If drive was found, returns other properties from found drive
                    If not, returns drive with just the critical stuff for the report.
        """

        drive_list = self.my_host_info.return_wrapped_drives()

        # if we find the drive, exit loop and return wrapper
        for drive in drive_list:
            if drive.FIO_path == fio_path:
                return drive

        # else create a drive wrapper with user values - to keep consistency of test
        user_drive = DriveWrapper()
        user_drive.drive_path = fio_path
        user_drive.FIO_path = fio_path
        user_drive.identifier_str = "User Drive - FIO"
        return user_drive



    """
    Quarch Product comunication
    """

    def add_qps_job_annotations(self, retval):
        self.test_point(self.test_id.gen_next_id(),
                        function_description="Adding start of FIO job annotation",
                        function=self._add_qps_annotation,
                        function_args={"parent_id": self.test_id.return_parent_id(), "anno_point": "start",
                                       "result_dict": retval})
        self.test_point(self.test_id.gen_next_id(), function_description="Adding end of FIO job annotation",
                        function=self._add_qps_annotation,
                        function_args={"parent_id": self.test_id.return_parent_id(), "anno_point": "end",
                                       "result_dict": retval})

    def _end_quarch_stream(self):
        if not self.document_mode:
            if self.is_streaming:
                self.quarch_stream.stopStream()
        else:
            return

    def _start_quarch_stream(self):
        # Begin Stream
        file_name = time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())
        if not self.document_mode:
            self.quarch_stream = self.cv_quarchname.custom_value.startStream(dtsGlobals.qcs_dir + file_name)
            self.quarch_stream.createChannel('read_iops', 'IOPS', 'IOPS', "Yes")
            self.quarch_stream.createChannel('write_iops', 'IOPS', 'IOPS', "Yes")
            self.quarch_stream.createChannel('write_throughput', 'MB/s', 'MB/s', "Yes")
            self.quarch_stream.createChannel('read_throughput', 'MB/s', 'MB/s', "Yes")
            self.is_streaming = True

        else:
            self.quarch_stream = None

    def _add_qps_comment(self, description, y_position=50):

        self.quarch_stream.addComment(title=str(description), yPos=y_position)

    def _add_qps_annotation(self, parent_id, anno_point, result_dict=None):

        """
        Adds QPS annotations with specific identifiers
        These are used to gather stats from QPS at a later point in test.

        :param parent_id: Unique ID of parent - Postfix of the annotation identifier
                    > Also substituted for counter during idle time.
        :param anno_point: Which annotation to add (start/end)
        :return:
        """

        start_annotation = "START:" + str(parent_id)
        end_annotation = "END:" + str(parent_id)
        idle_annotaton = "IDLE:" + str(parent_id)
        # will need to change to assign colours.
        if "start" in str(anno_point):
            if isinstance(result_dict, dict):
                start_time = float(result_dict["timestamp_ms"]) - float(
                    result_dict["runtime"]) - self.annotation_time_correction_start
                self.quarch_stream.addAnnotation(title=start_annotation, annotationTime=start_time)
            else:
                self.quarch_stream.addAnnotation(title=start_annotation)
        if "end" in str(anno_point):
            if isinstance(result_dict, dict):
                end_time = result_dict["timestamp_ms"] - self.annotation_time_correction_end
                self.quarch_stream.addAnnotation(title=end_annotation, annotationTime=end_time,
                                                 yPos=70)
            else:
                self.quarch_stream.addAnnotation(title=end_annotation, yPos=70)
        if "idle" in str(anno_point):
            self.quarch_stream.addAnnotation(title=idle_annotaton)


# x = PowerVsPerformance()
# x.cv_fio_job.custom_value = \
# "[global]\n\
# rw=randread\n\
# size=128m\n\
# filename=/dev/nvme0n1\n\
# runtime=10\n\
# time_based\n\
# \n\
# [job1]\n\
# \n\
# [job2]"
# x.create_cmd_line_job_args()
# print(x.fio_job_args)