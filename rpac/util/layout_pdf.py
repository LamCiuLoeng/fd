# -*- coding: utf-8 -*-
import traceback
import os
import random
# import json
import subprocess
import zipfile
import zlib

from datetime import datetime as dt

from tg import request, config

from rpac.model import *


__all__ = [
    'gen_pdf',
    'null_string_sizes',
    'format_fibers',
    'format_cares',
    'format_coo',
    'format_list']

CARES = [
    "WASH",
    "BLEACH",
    "IRON",
    "DRY",
    "DRYCLEAN",
    "SPECIALCARE"
]


def gen_pdf(header_no, details):
    try:
        public_dir = config.get( 'public_dir' )
        download_dir = os.path.join( public_dir, 'layout_pdf' )
        if not os.path.exists( download_dir ):
            os.makedirs( download_dir )

        phantomjs = os.path.join( public_dir, 'phantomjs', 'phantomjs.exe' )
        labeljs = os.path.join( public_dir, 'phantomjs', 'pdf.js' )

        pdfs = []

        for detail_id, item_code in details:
            http_url = 'http://%s/pdflayout/index?id=%s' % (request.headers.get( 'Host' ), detail_id)

            _name = '%s_%s%d' % (trim(item_code), dt.now().strftime( "%Y%m%d%H%M%S" ), random.randint( 1, 1000 ) )
            pdf_file = os.path.join( download_dir, '%s.pdf' % _name )

            cmd = '%s %s %s %s' % (phantomjs, labeljs, http_url, pdf_file)

            # print cmd

            sp = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)

            while 1:
                if sp.poll() is not None:
                    #print 'exec command completed.'
                    break
                # else:
                #     line = sp.stdout.readline().strip()

            pdfs.append(pdf_file)

        pd_zip_file = os.path.join( download_dir, "%s_pdf_%s%d.zip" % (trim(header_no), dt.now().strftime( "%Y%m%d%H%M%S" ), random.randint( 1, 1000 ) ) )
        create_zip(pd_zip_file, pdfs)
        remove_files(pdfs)

        return pd_zip_file
    except:
        traceback.print_exc()
        return None


def create_zip(zipf, files):
    _zip = zipfile.ZipFile(zipf, 'w', zlib.DEFLATED)
    for f in files:
        if os.path.exists(f):
            _zip.write(os.path.abspath(f), os.path.basename(f))
    _zip.close()
    return zipf


def remove_files(files):
    for f in files:
        remove_file(f)


def remove_file(file):
    try:
        os.remove(file)
    except:
        pass


def trim(s):
    return ''.join(s.split())


def null_string_sizes(data):
    null_list = data.get('SIZE', {'values': []})['values']

    if not null_list:
        return ['']
    return null_list


def format_fibers(data, capitalize=False):
    fibers = {
        'en': [],
        'sp': []
    }

    for ff in data['FIBERS']['values']:
        if ff:
            if capitalize:
                fibers['en'].append('%s%% %s' % (ff['percent'], ff['english'].lower().capitalize()))
                fibers['sp'].append('%s%% %s' % (ff['percent'], ff['spanish'].lower().capitalize()))
            else:
                fibers['en'].append('%s%% %s' % (ff['percent'], ff['english']))
                fibers['sp'].append('%s%% %s' % (ff['percent'], ff['spanish']))
    # print fibers
    return fibers


def format_cares(data):
    cares = {
        'en': [],
        'sp': []
    }

    for cs in CARES:
        cc = data.get(cs, {'values': []})
        for c in cc['values']:
            # print '****', c
            cares['en'].append(c['english'])
            cares['sp'].append(c['spanish'])

    return cares

def format_coo(data):
    coos = {
        'en': [],
        'sp': []
    }

    for coo in data['CO']['values']:
        coos['en'].append(coo['english'])
        coos['sp'].append(coo['spanish'])

    return coos

def format_list(ll, method=None, s=''):
    if method:
        return s.join([getattr(l, method)() for l in ll if l])
    return s.join(ll)


def format_list2(ll):
    return [l.lower().capitalize() for l in ll if l]


def format_price(data):
    try:
        price = '$%.2f' % float(data['PRICE']['values'][0])
        return price
    except:
        return '$0.00'
