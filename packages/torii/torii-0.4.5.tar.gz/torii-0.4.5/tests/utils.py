# SPDX-License-Identifier: BSD-2-Clause

import os
import re
import shutil
import subprocess
import textwrap
import traceback

from torii.hdl.ast    import *
from torii.hdl.ir     import *
from torii.back       import rtlil
from torii.tools      import require_tool
from torii.test       import ToriiTestCase


__all__ = (
	'ToriiTestSuiteCase',
)


class ToriiTestSuiteCase(ToriiTestCase):
	def assertRepr(self, obj, repr_str):
		if isinstance(obj, list):
			obj = Statement.cast(obj)

		def prepare_repr(repr_str):
			repr_str = re.sub(r'\s+', ' ',  repr_str)
			repr_str = re.sub(r'\( (?=\()', '(', repr_str)
			repr_str = re.sub(r'\) (?=\))', ')', repr_str)
			return repr_str.strip()
		self.assertEqual(prepare_repr(repr(obj)), prepare_repr(repr_str))

	# TODO: Once the Torii formal bits are better defined remove this and add formal to ToriiTestCase
	def assertFormal(self, spec, mode = 'bmc', depth = 1):
		stack = traceback.extract_stack()
		for frame in reversed(stack):
			if os.path.dirname(__file__) not in frame.filename:
				break
			caller = frame

		spec_root, _ = os.path.splitext(caller.filename)
		spec_dir = os.path.dirname(spec_root)
		spec_name = '{}_{}'.format(
			os.path.basename(spec_root).replace('test_', 'spec_'),
			caller.name.replace('test_', '')
		)

		# The sby -f switch seems not fully functional when sby is reading from stdin.
		if os.path.exists(os.path.join(spec_dir, spec_name)):
			shutil.rmtree(os.path.join(spec_dir, spec_name))

		if mode == 'hybrid':
			# A mix of BMC and k-induction, as per personal communication with Claire Wolf.
			script = 'setattr -unset init w:* a:torii.sample_reg %d'
			mode   = 'bmc'
		else:
			script = ''

		config = textwrap.dedent('''\
		[options]
		mode {mode}
		depth {depth}
		wait on
		multiclock on

		[engines]
		smtbmc

		[script]
		read_rtlil top.il
		prep
		{script}

		[file top.il]
		{rtlil}
		''').format(
			mode = mode,
			depth = depth,
			script = script,
			rtlil = rtlil.convert_fragment(Fragment.get(spec, platform = 'formal').prepare())[0]
		)

		with subprocess.Popen(
			[require_tool('sby'), '-f', '-d', spec_name],
			cwd = spec_dir,
			env = {**os.environ, 'PYTHONWARNINGS': 'ignore'},
			universal_newlines = True,
			stdin = subprocess.PIPE, stdout = subprocess.PIPE
		) as proc:
			stdout, stderr = proc.communicate(config)
			if proc.returncode != 0:
				self.fail('Formal verification failed:\n' + stdout)
