from app.api.scripts.ApiFunctions import fromCampusPullSubjects, fromCoursePullSections, fromSectionPullDetails, fromSubjectPullCourses, fromSubjectPullSections


test1 = fromCampusPullSubjects('UBCV')
test2 = fromSubjectPullCourses('POLS', campus='UBCV')
test3 = fromCoursePullSections('POLS', '426', campus='UBCV')

fromCoursePullSections('INDG', '295K', 'UBCV')
