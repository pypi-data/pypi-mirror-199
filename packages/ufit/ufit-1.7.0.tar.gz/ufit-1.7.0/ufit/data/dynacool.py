#  -*- coding: utf-8 -*-
# *****************************************************************************
# ufit, a universal scattering fitting suite
#
# Copyright (c) 2013-2023, Georg Brandl and contributors.  All rights reserved.
# Licensed under a 2-clause BSD license, see LICENSE.
# *****************************************************************************

"""Load routine for DynaCool PPMS data files."""

import io

from numpy import genfromtxt, mean, ptp


def guess_cols(colnames, coldata, meta):
    xcol = 'Time Stamp (sec)'
    ycol = dycol = None
    if 'AC Moment (emu)' in colnames:
        ycol = 'AC Moment (emu)'
        dycol = 'AC Std. Dev. (emu)'
    elif 'Moment (emu)' in colnames:
        ycol = 'Moment (emu)'
        dycol = 'M. Std. Err. (emu)'
    xcands = ['Magnetic Field (Oe)', 'Temperature (K)', 'Time Stamp (sec)']
    spreads = []
    for xcand in xcands:
        if xcand in colnames:
            data = coldata[:, colnames.index(xcand)]
            spreads.append((ptp(data)/mean(data), xcand))
    if spreads:
        xcol = sorted(spreads)[-1][1]
    return xcol, ycol, dycol, None


def check_data(fp):
    fp.readline()
    try:
        line2 = fp.readline()
        fp.seek(0, 0)
        return line2.startswith((b'; VSM Data File',
                                 b'; ACMS II Data File'))
    except IOError:
        return False


def read_data(filename, fp):
    fp = io.TextIOWrapper(fp, 'ascii', 'ignore')

    meta = {}
    meta['filenumber'] = 0
    try:
        meta['filenumber'] = int(filename.split('_')[-1].split('.')[0])
    except Exception:
        pass
    meta['instrument'] = 'VSM'
    remark = ''
    title = ''

    # parse headers
    lines = iter(fp)
    for line in lines:
        line = line.strip()
        if line == '[Data]':
            break
        if not line or line.startswith(';'):
            continue
        parts = line.split(',', 2)
        if parts[0] == 'TITLE':
            title = parts[1]
            continue
        if parts[0] != 'INFO' or len(parts) < 3:
            continue

        if parts[2] == 'VSM_SERIAL_NUMBER':
            meta['instrument'] = parts[1]
        elif parts[2] == 'ACMS_SERIAL_NUMBER':
            meta['instrument'] = parts[1]
        elif parts[2] == 'SAMPLE_MATERIAL':
            remark = parts[1]
        elif parts[2] == 'SAMPLE_COMMENT':
            meta['subtitle'] = parts[1]
        try:
            val = float(parts[1])
        except ValueError:
            val = parts[1]
        meta[parts[2]] = val

    if remark:
        title += ', ' + remark
    meta['title'] = title

    # parse data table
    colnames = next(lines).split(',')
    arr = genfromtxt(lines, delimiter=',', missing_values='0')

    cols = dict((name, arr[:, i]) for (i, name) in enumerate(colnames))
    meta['environment'] = []
    for col in cols:
        meta[col] = cols[col].mean()

    return colnames, arr, meta
