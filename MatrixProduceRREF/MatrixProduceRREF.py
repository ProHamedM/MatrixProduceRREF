

# Ask client path
#path = input ('Please enter excel File\'s Path?')
#print (path)

from pandas import pd


def produceMatrix ():
    mydataset = {
    'cars': ["BMW", "Volvo", "Ford"],
    'passings': [3, 7, 2]}
    myvar = pd.DataFrame(mydataset)
    print(myvar)





    #doc = pd.DataFrame(pd.read_excel(path))
    

  #print (doc)