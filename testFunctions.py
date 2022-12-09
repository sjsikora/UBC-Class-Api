from scripts.ApiFunctions import fromCampusPullSubjects, fromCoursePullSections, fromSectionPullDetails, fromSubjectPullCourses, fromSubjectPullSections
import json

test1 = fromCampusPullSubjects("UBCO") #Test 1
test2 = fromCampusPullSubjects("UBCV") #Test 2
test3 = fromCoursePullSections("COSC", '121', 'UBCO') #Test 3
test4 = fromCoursePullSections("COSC", '121', 'UBCO', fulldetails=True) #Test 4
test5 = fromSectionPullDetails('GISC', '381', '101', campus='UBCO') #Test 5
test6 = fromSectionPullDetails('GISC', '381', 'L01', campus='UBCO') #Test 6
test7 = fromSubjectPullCourses('GISC', 'UBCO') #Test 7
test8 = fromSubjectPullCourses('GISC', 'UBCO', fulldetails=True) #Test 8
test9 = fromSubjectPullSections('DATA') #Test 9

testList = [test1, test2, test3, test4, test5, test6, test7, test8, test9]

i=1
for test in testList:
    with open(f'./test/test{i}.json', 'w') as f:
        json.dump(test, f)
    i +=1


test1 = fromCampusPullSubjects("UBC") #Test 1
test2 = fromCampusPullSubjects("HELLO") #Test 2
test3 = fromCoursePullSections("FAKECODE", '333i3o3', 'UBCO') #Test 3
test4 = fromCoursePullSections("COSC", '121', 'UBC', fulldetails=True) #Test 4
test5 = fromSectionPullDetails('FJC', '381', '999', campus='UBCO') #Test 5
test6 = fromSectionPullDetails('GISC', 'fff81', 'L01', campus='UBCO') #Test 6
test7 = fromSubjectPullCourses('GISC', 'CEL') #Test 7
test8 = fromSubjectPullCourses('HELLO', 'UBCO', fulldetails=True) #Test 8
test9 = fromSubjectPullSections('FAKE') #Test 9

print('hello')