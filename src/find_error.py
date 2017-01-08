'''I think this was the very beginning of trying to create a model for
time series clustering'''


def mse(tester, trainer):
    mses = {}
    for i, row in enumerate(trainer):
        mse = sum([(tester-row)**2])
        mses[i] = mse
    return mses


'''
What I want to do:
Find the 1st and second derivatives
'''

floral_dress=[5,4,10,11,6,3,4,9,9,15,13,18,29,19,19,12,11,14,13,16,21,31,40,43,40
,38,26,28,18,22,22,25,30,24,28,30,20,25,28,24,30,34,12,17,43,40,79,45]


maxi_dress=[1,5,8,9,4,7,12,15,5,8,14,26,11,13,23,12,7,9
,5,7,13,15,34,41,70,43,40,25,38,25,27,26,34,39,59,62
,94,99,82,128,124,72,47,37,45,80,138,105]


harem_pants=[0,2,2,3,6,11,10,8,11,19,21,29,14,28,12,14,11,20,6,18,17,18,16,21,16
,18,21,21,15,11,17,20,18,13,13,11,17,11,13,24,22,13,8,3,20,3,16,12]

def first_der(lst):
    der1 = []
    pct_chg = []
    for i in xrange(len(lst)-2):
        der1.append(lst[i+1] - lst[i])
        pct_chg.append(der1[i]*1.0/(lst[i] + 1))
    return der1, pct_chg

#what I am actually interested in is the change since this time last year
#I think I might have already started writing something for that

def change_over_time(lst):
    #currently assuming monthly data. Will generalize this to handle quarters, weeks, etc.
    #for each point, I want to look at


'''
iterate through the list of all possible trends. Determine a threshold below which
something is too sparse to be considered a trend (at least x people need to have posted
about it each year, or at least x in one year?)
Find their 1st and second derivatives and their percent change (1st derivative normalized)


perform k-means clustering on sliding windows, looking at similarities between
--raw numbers
--1st derivative
--1st derivative normalized
--yoy changes
--2nd derivative

Current goal: year over year change, by month, for a three year period.
Plot this. It will only show two years' worth of data.
'''
