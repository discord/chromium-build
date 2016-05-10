# Copyright 2014 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import json
import os
import tempfile

from devil.utils import cmd_helper
from pylib import constants
from pylib.results import json_results

class JavaTestRunner(object):
  """Runs java tests on the host."""

  def __init__(self, args):
    self._package_filter = args.package_filter
    self._runner_filter = args.runner_filter
    self._sdk_version = args.sdk_version
    self._test_filter = args.test_filter
    self._test_suite = args.test_suite
    self._coverage_dir = args.coverage_dir

  def SetUp(self):
    pass

  def RunTest(self, _test):
    """Runs junit tests from |self._test_suite|."""
    with tempfile.NamedTemporaryFile() as json_file:
      java_script = os.path.join(
          constants.GetOutDirectory(), 'bin', 'helper', self._test_suite)
      command = [java_script]

      # Add Jar arguments.
      args = ['-test-jars', self._test_suite + '.jar',
              '-json-results-file', json_file.name]
      if self._test_filter:
        args.extend(['-gtest-filter', self._test_filter])
      if self._package_filter:
        args.extend(['-package-filter', self._package_filter])
      if self._runner_filter:
        args.extend(['-runner-filter', self._runner_filter])
      if self._sdk_version:
        args.extend(['-sdk-version', self._sdk_version])
      command.extend(['--jar-args', '"%s"' % ' '.join(args)])

      # Add JVM arguments.
      args = []
      if self._coverage_dir:
        args.append('-Demma.coverage.out.file=%s' % self._coverage_dir)
      if args:
        command.extend(['--jvm-args', '"%s"' % ' '.join(args)])

      return_code = cmd_helper.RunCmd(command)
      results_list = json_results.ParseResultsFromJson(
          json.loads(json_file.read()))
      return (results_list, return_code)

  def TearDown(self):
    pass

