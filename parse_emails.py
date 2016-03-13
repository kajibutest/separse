#!/usr/bin/python

from bs4 import BeautifulSoup
from validate_email import validate_email
import HTMLParser
import argparse
import sys
import string
import xml.etree.cElementTree

PRINT_INTERVAL = 10000

def get_emails(text):
  emails = []
  p = -1
  while True:
    p = text.find('@', p+1)
    if p < 0:
      break
    s, e = p-1, p+1
    while s >= 0:
      if text[s] in string.whitespace:
        break
      s -= 1
    s += 1
    while e < len(text):
      if text[e] in string.whitespace:
        break
      e += 1
    email = text[s:e]
    if validate_email(email):
      emails.append(email)
  return emails

def parse(args):
  parser = HTMLParser.HTMLParser()
  ifp = open(args.input_file, 'r')
  ofp = open(args.output_file, 'w')
  count = 0
  while True:
    line = ifp.readline()
    count += 1
    if count % PRINT_INTERVAL == 0:
      print 'processed %d lines' % count
      sys.stdout.flush()
    if line == '':
      break
    line = line.strip()
    if not line.startswith('<row '):
      continue
    el = xml.etree.cElementTree.fromstring(line)
    if 'AboutMe' not in el.attrib:
      continue
    soup = BeautifulSoup(parser.unescape(el.attrib['AboutMe']))
    text = soup.get_text().strip()
    emails = get_emails(text)
    if len(emails) > 0:
      el.attrib['Emails'] = emails
      print >> ofp, el.attrib
  ifp.close()
  ofp.close()

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--input_file', required=True)
  parser.add_argument('--output_file', required=True)
  parse(parser.parse_args())

if __name__ == '__main__':
  main()

