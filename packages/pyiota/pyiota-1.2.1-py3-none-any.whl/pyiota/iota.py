"""Simple Go lang iota pattern implementation"""

# This file is a part of pyiota package
# Licensed under Do-What-The-Fuck-You-Want license
# Initially made by @jedi2light (aka Carey Minaieva)

class iota:
  _counter = -1
  def start(n: int):
    """Let you to start it over from n"""
  def __new__(cls):
    cls._counter += 1
    return cls._counter

class start:
  _initial = -1
  _iota_class = iota
  def __init__(self, n=0):
    self._initial = n - 1 or self._initial
  def __enter__(self):
    self._iota_class._counter = self._initial
    return self
  def __exit__(self, _, __, ___):
    self._iota_class._counter = self._initial

iota.start = start  # thanks to the first-class classes
