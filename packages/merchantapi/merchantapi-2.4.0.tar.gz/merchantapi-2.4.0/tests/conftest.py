import pytest
import time
import json
import os.path
import math
from _pytest.reports import CollectReport
from _pytest.reports import TestReport

mocha_output						= dict()
mocha_output['stats']				= dict()
mocha_output['stats']['suites']		= 0
mocha_output['stats']['tests']		= 0
mocha_output['stats']['passes']		= 0
mocha_output['stats']['failures']	= 0
mocha_output['stats']['pending']	= 0
mocha_output['stats']['start']		= 0
mocha_output['stats']['end']		= 0
mocha_output['stats']['duration']	= 0
mocha_output['passes']				= []
mocha_output['failures']			= []
mocha_output['skipped']				= []

@pytest.hookimpl()
def pytest_sessionstart(session):
	mocha_output['stats']['start']	= time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

@pytest.hookimpl()
def pytest_report_teststatus(report, config):
	if isinstance(report, TestReport):
		entry				= dict()
		entry['title']		= report.location[2]
		entry['fullTitle']	= report.location[2]
		entry['duration']   = math.floor(report.duration)
	
		mocha_output['stats']['tests'] = mocha_output['stats']['tests'] + 1

		if report.outcome == 'passed':
			mocha_output['stats']['passes'] = mocha_output['stats']['passes'] + 1
			mocha_output['passes'].append(entry)
		elif report.outcome == 'failed':
			mocha_output['stats']['failures'] = mocha_output['stats']['failures'] + 1
			entry['error'] = f'File: {report.location[0]} Test: {report.location[2]} Line {report.location[1]}: {report.longrepr}'

			mocha_output['failures'].append(entry)
		elif report.outcome == 'skipped':
			mocha_output['skipped'].append(entry)

@pytest.hookimpl()
def  pytest_terminal_summary(terminalreporter, exitstatus, config):
	mocha_output['stats']['end'] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
	filename = 'report.json'
	with open(filename, 'w') as fh:
		fh.write(json.dumps(mocha_output))