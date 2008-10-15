########################
########################
##                    ##
## ANALYSIS QUESTIONS ##
##                    ##
########################
########################

def question2():
  YOUR_ANSWER = 7
  return YOUR_ANSWER

def question3():
  YOUR_ANSWER = (0.9, 0.014)
  return YOUR_ANSWER
  
def question4a():
  YOUR_ANSWER = (0.8, 0, 4)
  return YOUR_ANSWER

def question4b():
  YOUR_ANSWER = 'NOT POSSIBLE'
  return YOUR_ANSWER

def question4c():
  YOUR_ANSWER = (0.8, 0, 0)
  return YOUR_ANSWER

def question4d():
  YOUR_ANSWER = (0.8, 0.5, 0.0)
  return YOUR_ANSWER

def question4e():
  YOUR_ANSWER = (.01, .9, -0.01)
  return YOUR_ANSWER

def question7():
  YOUR_ANSWER = 'NOT POSSIBLE'
  return YOUR_ANSWER

if __name__ == '__main__':
  print 'Answers to analysis questions:'
  import agent
  for q in ['2','3','4a','4b','4c','4d','4e','7']:
    response = getattr(agent, 'question' + q)()
    print '  Question %s:\t%s' % (q, str(response))
