# SPDX-License-Identifier: BSD-2-Clause

import logging        as log
from argparse         import (
	ArgumentDefaultsHelpFormatter, ArgumentParser, FileType, Namespace
)
from typing           import Optional, Union

from rich             import traceback
from rich.logging     import RichHandler

from .back            import cxxrtl, rtlil, verilog
from .build           import Platform
from .hdl.ir          import Elaboratable, Fragment, Signal
from .sim             import Simulator
from .util.decorators import deprecated

__all__ = (
	'main',
)

@deprecated('torii.cli.main_parser will be replaced in a future version of Torii')
def main_parser(parser: Optional[ArgumentParser] = None) -> ArgumentParser:
	if parser is None:
		parser = ArgumentParser(
			formatter_class = ArgumentDefaultsHelpFormatter,
			description     = 'Torii-HDL CLI Runner'
		)

	parser.add_argument(
		'-v', '--verbose',
		dest    = 'verbose',
		default = False,
		action  = 'store_true',
		help    = 'Enable verbose logging',
	)

	p_action = parser.add_subparsers(dest = 'action')

	p_generate = p_action.add_parser(
		'generate',
		help = 'generate RTLIL, Verilog or CXXRTL from the design'
	)
	p_generate.add_argument(
		'-t', '--type',
		dest    = 'generate_type',
		metavar = 'LANGUAGE',
		choices = ['il', 'cc', 'v'],
		help    = 'generate LANGUAGE (il for RTLIL, v for Verilog, cc for CXXRTL; default: file extension of FILE, if given)'
	)
	p_generate.add_argument(
		'--no-src',
		dest    = 'emit_src',
		default = True,
		action  = 'store_false',
		help    = 'suppress generation of source location attributes'
	)
	p_generate.add_argument(
		'generate_file',
		metavar = 'FILE',
		type    = FileType('w'),
		nargs   = '?',
		help    = 'write generated code to FILE'
	)

	p_simulate = p_action.add_parser(
		'simulate',
		help = 'simulate the design'
	)
	p_simulate.add_argument(
		'-v', '--vcd-file',
		metavar = 'VCD-FILE',
		type    = FileType('w'),
		help    = 'write execution trace to VCD-FILE'
	)
	p_simulate.add_argument(
		'-w', '--gtkw-file',
		metavar = 'GTKW-FILE',
		type    = FileType('w'),
		help    = 'write GTKWave configuration to GTKW-FILE'
	)
	p_simulate.add_argument(
		'-p', '--period',
		dest    = 'sync_period',
		metavar = 'TIME',
		type    = float,
		default = 1e-6,
		help    = 'set \'sync\' clock domain period to TIME (default: %(default)s)'
	)
	p_simulate.add_argument(
		'-c', '--clocks',
		dest     = 'sync_clocks',
		metavar  = 'COUNT',
		type     = int,
		required = True,
		help     = 'simulate for COUNT \'sync\' clock periods'
	)

	return parser


@deprecated('torii.cli.main_runner will be replaced in a future version of Torii')
def main_runner(
	parser: ArgumentParser, args: Namespace, design: Union[Fragment, Elaboratable],
	platform: Platform = None, name: str = 'top', ports: tuple[Signal] = ()
) -> None:

	level = log.INFO
	if args is not None and args.verbose:
		level = log.DEBUG

	log.basicConfig(
		force    = True,
		format   = '%(message)s',
		datefmt  = '[%X]',
		level    = level,
		handlers = [
			RichHandler(rich_tracebacks = True, show_path = True)
		]
	)


	if args.action == 'generate':
		fragment = Fragment.get(design, platform)
		generate_type = args.generate_type
		if generate_type is None and args.generate_file:
			if args.generate_file.name.endswith('.il'):
				generate_type = 'il'
			if args.generate_file.name.endswith('.cc'):
				generate_type = 'cc'
			if args.generate_file.name.endswith('.v'):
				generate_type = 'v'
		if generate_type is None:
			parser.error('Unable to auto-detect language, specify explicitly with -t/--type')
		if generate_type == 'il':
			output = rtlil.convert(fragment, name = name, ports = ports, emit_src = args.emit_src)
		if generate_type == 'cc':
			output = cxxrtl.convert(fragment, name = name, ports = ports, emit_src = args.emit_src)
		if generate_type == 'v':
			output = verilog.convert(fragment, name = name, ports = ports, emit_src = args.emit_src)
		if args.generate_file:
			args.generate_file.write(output)
		else:
			print(output)

	if args.action == 'simulate':
		fragment = Fragment.get(design, platform)
		sim = Simulator(fragment)
		sim.add_clock(args.sync_period)
		with sim.write_vcd(vcd_file = args.vcd_file, gtkw_file = args.gtkw_file, traces = ports):
			sim.run_until(args.sync_period * args.sync_clocks, run_passive = True)

@deprecated('torii.cli.main will be replaced in a future version of Torii')
def main(*args, **kwargs) -> None:
	traceback.install()
	parser = main_parser()
	main_runner(parser, parser.parse_args(), *args, **kwargs)
