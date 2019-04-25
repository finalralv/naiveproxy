#!/usr/bin/env python

# Copyright 2019 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Tests for java_cpp_strings.py.

This test suite contains various tests for the C++ -> Java string generator.
"""

import unittest

import java_cpp_strings


class _TestStringsParser(unittest.TestCase):

  def testParseComments(self):
    test_data = """
/**
 * This should be ignored as well.
 */

// Comment followed by a blank line.

// Comment followed by unrelated code.
int foo() { return 3; }

// Real comment.
const char kASwitch[] = "a-value";

// Real comment that spans
// multiple lines.
const char kAnotherSwitch[] = "another-value";

// Comment followed by nothing.
""".split('\n')
    strings = java_cpp_strings.StringFileParser(test_data).Parse()
    self.assertEqual(2, len(strings))
    self.assertEqual('A_SWITCH', strings[0].name)
    self.assertEqual('"a-value"', strings[0].value)
    self.assertEqual(1, len(strings[0].comments.split('\n')))
    self.assertEqual('ANOTHER_SWITCH', strings[1].name)
    self.assertEqual('"another-value"', strings[1].value)
    self.assertEqual(2, len(strings[1].comments.split('\n')))

  def testStringValues(self):
    test_data = """
// Single line string constants.
const char kAString[] = "a-value";

// Single line switch with a big space.
const char kAStringWithSpace[]                      = "a-value";

// Wrapped constant definition.
const char kAStringWithAVeryLongNameThatWillHaveToWrap[] =
    "a-string-with-a-very-long-name-that-will-have-to-wrap";

// This is erroneous and should be ignored.
const char kInvalidLineBreak[] =

    "invalid-line-break";
""".split('\n')
    strings = java_cpp_strings.StringFileParser(test_data).Parse()
    self.assertEqual(3, len(strings))
    self.assertEqual('A_STRING', strings[0].name)
    self.assertEqual('"a-value"', strings[0].value)
    self.assertEqual('A_STRING_WITH_SPACE', strings[1].name)
    self.assertEqual('"a-value"', strings[1].value)
    self.assertEqual('A_STRING_WITH_A_VERY_LONG_NAME_THAT_WILL_HAVE_TO_WRAP',
                     strings[2].name)
    self.assertEqual('"a-string-with-a-very-long-name-that-will-have-to-wrap"',
                     strings[2].value)

  def testTemplateParsing(self):
    test_data = """
// Copyright {YEAR} The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// This file is autogenerated by
//     {SCRIPT_NAME}
// From
//     {SOURCE_PATH}, and
//     {TEMPLATE_PATH}

package my.java.package;

public any sort of class MyClass {{

{NATIVE_STRINGS}

}}
""".split('\n')
    package, class_name = java_cpp_strings.ParseTemplateFile(test_data)
    self.assertEqual('my.java.package', package)
    self.assertEqual('MyClass', class_name)


if __name__ == '__main__':
  unittest.main()
