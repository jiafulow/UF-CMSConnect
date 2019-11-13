#!/usr/bin/env python

import numpy as np
import os


class Hadd(object):

  def __init__(self):
    self.d = {}
    self.dout = {}

  def _stack_row_splits(self, v):
    # Set the first entry to zero.
    new_row_splits = [0]
    for row_splits in v:
      if not (isinstance(row_splits, (np.ndarray, np.generic)) and
              row_splits.dtype in (np.int64, np.int32) and row_splits.ndim == 1):
        raise TypeError("row_splits must be a 1D int32 or int64 numpy array")
      # Ignore the first entry in row_splits, because the first entry is always zero.
      # Increment all the entries in row_splits by the last value in new_row_splits.
      new_row_splits.extend(row_splits[1:] + new_row_splits[-1])
    new_row_splits = np.asarray(new_row_splits, dtype=np.int32)
    return new_row_splits

  def process(self, target, source, force=False):
    print('hadd Target file: {0}'.format(target))

    if not force:
      if os.path.isfile(target):
        print('hadd error opening target file (does {0} exist?).'.format(target))
        print('Pass "-f" argument to force re-creation of output file.')

    for i, s in enumerate(source):
      print('hadd Source file {0}: {1}'.format(i+1, s))
      with np.load(s) as data:
        if i == 0:
          for k in data.files:
            self.d[k] = []
        for k in data.files:
          self.d[k].append(data[k])

    print('hadding...')
    for k, v in self.d.iteritems():
      print('array: {0}'.format(k))
      if k.endswith('_row_splits'):
        vv = self._stack_row_splits(v)
      elif v[0].ndim == 0:
        vv = np.array(v)
      elif v[0].ndim == 1:
        vv = np.hstack(v)
      else:
        vv = np.vstack(v)
      self.dout[k] = vv

    np.savez_compressed(target, **self.dout)
    print('DONE')


if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser(description='hadd for npz files.')
  parser.add_argument('-f', '--force', action='store_true', help='Force write the target file')
  parser.add_argument('target', help='target file')
  parser.add_argument('source', nargs='+', help='source files')
  args = parser.parse_args()

  hadd = Hadd()
  hadd.process(args.target, args.source, force=args.force)
