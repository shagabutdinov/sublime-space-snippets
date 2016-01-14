import unittest

try: # suppress import exception when loading package to sublime
  from processor import process
except ImportError:
  pass

class ProcessTest(unittest.TestCase):

  def __init__(self, *args):
    self._ignored_symbols = [
      '$', '@', '#',
    ]

    self._no_space_symbols = [
      '==', '!=', '===', '&&', '||', '**', '++', '--', '//',
      '+=', '-=', '*=', '/=', '&=', '|=', '^=', '=>', '<-',
      '->', '>=', '<=', ':=', '<%', '<%=', '<%-', '%>',
    ]

    self._space_symbols = [
      '= !', '= &', '= *', '= -', '= +', '= ^',
      ', &', ', *', '= :', '&& !', '&& -', '|| !', '|| -',
      ': &', '=== ,'
    ]

    self._no_space_before = [
      ',', ':', '?', ';',
      '::', '++', '--', '//', '<?',
      '->',
    ]

    self._space_before = [
      '+', '-', '*', '/', '|', '&', '=',
      '||', '&&', '**', '==', '===',
      '*=', '+=', '-=', '/=', '&=', '|=', '^=', '=>',
      '= -', '= +', '=== -', ': &',
    ]

    self._no_space_after = [
      '?', '!',
      '::', '++', '--',
      '(-', '(*', ', *', ', &', ': &', '(+', '(&',
      '= -', '= +',
    ]

    self._space_after = [
      ',', '+', '-', '/', ':', '=', '<', '>',
      '||', '&&', '**',
      '*=', '+=', '-=', '/=', '^=', '&=', '|=', '==', '===', '!=', '=>',
      '),', '],', '},', '//',
      '<-',
    ]

    self._extra_cases = [
      ('[0...-1', ']', []),
      ('test = :t', '', []),
      ('test == :t', '', []),
      ('/regexp/,', '', [(0, 0, ' ')]),
      ('/regexp/, ', '', []),
      ('test!(', ')', []),
      ('test {|', '', [(-1, -1, ' ')]),
      ('test { |', '', []),
      ('test { |test|', '', []),
      ('test { |(a,b)|', '', []),
      ('test { |(a,b), c|', '', []),
      ('asd && !a', '', []),
      ('asd:::a', '', [(-4, -1, ': ::')]),
      ('asd, :a', '', []),
      ('asd, -1', '', []),
      ('asd: :', '', [(-3, 0, '::')]),
      ('asd:', '', [(0, 0, ' ')]),
      ('test),(', '', [(-1, -1, ' ')]),
      ('test],[', '', [(-1, -1, ' ')]),
      ('test)+', '', [(-1, -1, ' '), (0, 0, ' ')]),
      ('test) + ', '', []),
      ('and + ', '', []),
      ('and + =', '', [(-3, 0, '+='), (0, 0, ' ')]),
      ('and + =', ' ', [(-3, 0, '+='), (0, 0, ' '), (0, 1, '')]),
      ('test(!', '', []),
      ('!test', '', []),
      ('test!', '', []),
      ('if !', '', []),
      ('  attr_reader :', '', []),
      ('attr_reader :t', '', []),
      ('!==-1', '', [(-5, -1, '!== -')]),
      ('!== -1', '', []),
      ('==-1', '', [(-4, -1, '== -')]),
      ('=-1', '', [(-3, -1, '= -')]),
      ('== -1', '', []),
      ('===-1', '', [(-5, -1, '=== -')]),
      ('=== -1', '', []),
      ('> -1', '', []),
      ('test !', '=', [(1, 1, ' ')]),
      ('=', '>', [(1, 1, ' ')]),
      ('<0', ':', [(-1, -1, ' ')]),
      ('test +', '= test', [(-1, 2, '+='), (1, 1, ' ')]),
      ('test !==', ', test', [(-3, 2, '!== ,'), (2, 2, ' ')]),
      ('test ==', ', test', [(-2, 2, '== ,'), (2, 2, ' ')]),
    ]

    self._language_cases = [
      ('test -> t', '', 'source.go', []),
      ('test *T', '', 'source.go', []),
      ('test* T', '', 'source.go', []),
    ]

    super().__init__(*args)

  # ignored_symbols

  def test_process_ignored_symbols_returns_empty_modifications(self):
    for symbols in self._ignored_symbols:
      actual = process('test' + symbols, '')
      self.assertEqual(0, len(actual))

  # no_space_symbols

  def test_process_no_space_symbols_removes_space(self):
    for symbols in self._no_space_symbols:
      actual = process('test ' + symbols[0] + ' ' + symbols[1:], '')
      self.assertIn((-1 - len(symbols), 0, symbols), actual)

  def test_process_no_space_symbols_not_inserts_space(self):
    for symbols in self._no_space_symbols:
      actual = process('test ' + symbols, '')
      self.assertNotIn((-1, -1, ' '), actual)

  # space_symbols

  def test_process_space_symbols_inserts_space(self):
    for symbols in self._space_symbols:
      actual = process('test ' + symbols.replace(' ', ''), '')
      self.assertIn((-len(symbols.replace(' ', '')), 0, symbols), actual)

  def test_process_space_symbols_not_inserts_space(self):
    for symbols in self._space_symbols:
      actual = process('test ' + symbols, '')
      self.assertNotIn((-1, -1, ' '), actual)

  # space_before

  def test_process_space_before_not_inserts_spaces_after_indentation(self):
    for symbol in self._space_before:
      actual = process(symbol, '')
      self.assertNotIn((-len(symbol), -len(symbol), ' '), actual)

  def test_process_space_before_replaces_spaces_before_symbol(self):
    for symbol in self._space_before:
      actual = process('test  ' + symbol, '')
      self.assertIn((-2 - len(symbol), -len(symbol), ' '), actual)

  def test_process_space_before_not_modify_space_before_symbol(self):
    for symbol in self._space_before:
      actual = process('test ' + symbol, '')
      self.assertNotIn((-1 - len(symbol), -1, ' '), actual)

  # no_space_before

  def test_process_no_space_before_removes_spaces_before_symbol(self):
    for symbol in self._no_space_before:
      actual = process('test ' + symbol, '')
      self.assertIn((-1 - len(symbol), -len(symbol), ''), actual)

  def test_process_no_space_before_not_removes_spaces_before_symbol(self):
    for symbol in self._no_space_before:
      actual = process('test' + symbol, '')
      self.assertNotIn((-len(symbol), -len(symbol), ''), actual)

  def test_process_no_space_before_not_inserts_spaces_before_symbol(self):
    for symbol in self._no_space_before:
      actual = process('test' + symbol, '')
      self.assertNotIn((-len(symbol), -len(symbol), ' '), actual)

  def test_process_no_space_before_not_removes_indentation(self):
    for symbol in self._no_space_before:
      actual = process(' ' + symbol, '')
      self.assertNotIn((-1 - len(symbol), -len(symbol), ''), actual)

  # space_after

  def test_process_space_after_replaces_spaces_after_symbol(self):
    for symbol in self._space_after:
      self.assertIn((-2, 0, ' '), process('test' + symbol + '  ', ''))

  def test_process_space_after_not_modify_space_after_symbol(self):
    for symbol in self._space_after:
      self.assertNotIn((-1, 0, ' '), process('test' + symbol + ' ', ''))

  def test_process_space_after_inserts_space_after_symbol_before_char(self):
    for symbol in self._space_after:
      self.assertIn((-1, -1, ' '), process('test' + symbol + 'a', ''))

  def test_process_space_after_replaces_spaces_after_symbol_after_cursor(self):
    for symbol in self._space_after:
      self.assertIn((0, 2, ''), process('test' + symbol + '', '  '))

  def test_process_space_after_not_replaces_spaces_after_symbol_with_char(self):
    for symbol in self._space_after:
      self.assertNotIn((0, 2, ''), process('test' + symbol + ' a', '  '))

  # no_space_after

  def test_process_no_space_after_removes_spaces_after_symbol(self):
    for symbol in self._no_space_after:
      self.assertIn((-1, 0, ''), process('test' + symbol + ' ', ''))

  def test_process_no_space_after_not_removes_spaces_after_symbol(self):
    for symbol in self._no_space_after:
      self.assertNotIn((0, 0, ''), process('test' + symbol, ''))

  def test_process_no_space_after_removes_spaces_after_symbol(self):
    for symbol in self._no_space_after:
      self.assertIn((0, 1, ''), process('test' + symbol, ' '))

  def test_process_no_space_after_not_insert_spaces_after_symbol(self):
    for symbol in self._no_space_after:
      self.assertNotIn((0, 0, ' '), process('test' + symbol, ' '))

  def test_process_space_before_inserts_spaces_before_symbol(self):
    for symbol in self._space_before:
      actual = process('test' + symbol, '')
      self.assertIn((-len(symbol), -len(symbol), ' '), actual)

  def test_process_extra_cases(self):
    for value in self._extra_cases:
      self.assertEqual(value[2], process(value[0], value[1]), 'token: "' +
        value[0] + value[1] + '"')

  def test_process_language_cases(self):
    for value in self._language_cases:
      self.assertEqual(value[3], process(value[0], value[1], value[2]),
        'token: "' + value[0] + value[1] + '"')

if __name__ == '__main__':
  unittest.main()