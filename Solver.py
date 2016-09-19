from pyasp.asp import *


goptions = ''
soptions = '2'

solver = Gringo4Clasp(gringo_options=goptions, clasp_options=soptions)


encoding = 'queens.lp'
facts = 'facts.lp'
result = solver.run([encoding, facts], collapseTerms=True, collapseAtoms=False)

print result