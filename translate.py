#!/usr/bin/python
# This Python file uses the following encoding: utf-8

import sys
import translator

def fixMode(arg):

	if len(arg) != 3:
		print 'Error! No such mode: {0}'.format(arg)
		print 'A three-characters mode is required.'
		sys.exit()

	mode = ''
	for each in arg:
		if each == 'Y' or each == 'y':
			mode += 'Y'
		else:
			mode += 'N'

	if mode == 'NNN':
		print "Error! Mode 'NNN' can't by used."
		sys.exit()

	return mode


if len(sys.argv) != 3:
	print 'Usage: {0} XXX file'.format(sys.argv[0])
	print ''
	print 'Mode:'
	print '  Y__\t search tokens in the English dictionary'
	print '  _Y_\t search tokens in the Lingo dictionary'
	print '  __Y\t keep original tokens'
	print ''
	print 'Any combination can be used. Examples:'
	print '  YYY - it will search tokens in both dictionaries and ḱeep original tokens'
	print '  YYN - it will search tokens in both dictionaries and discard original tokens'
	print '  YNY - it will search tokens only in the English dictionary and ḱeep original tokens'
	sys.exit()

else:
	mode = fixMode(sys.argv[1])

	print "Translating file '{0}' with mode '{1}'.".format(sys.argv[2], mode)
	translator.init(mode)
	translator.translate_file(sys.argv[2], mode)
	print 'Done!'
