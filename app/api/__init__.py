from flask import jsonify, Blueprint
from app.api.scripts.ApiFunctions import fromCampusPullSubjects, fromCoursePullSections, fromSectionPullDetails, fromSubjectPullCourses, fromSubjectPullSections


#FISH 500 001


apiBP = Blueprint('api', __name__)

@apiBP.route('/campusSubjects/campus=<campus>', methods=["GET"])
def campusSubject(campus: str):

    dictToReturn = fromCampusPullSubjects(
        campus = campus
    )

    return jsonify(dictToReturn)

@apiBP.route('/courseSections/campus=<campus>/subject=<subjectCode>/course=<courseCode>', methods=["GET"])
def courseSections(campus: str, subjectCode: str, courseCode: str):

    dictToReturn = fromCoursePullSections(
        subjectCode = subjectCode,
        courseCode = courseCode,
        campus = campus,
    )

    return jsonify(dictToReturn)

@apiBP.route('/courseSections/campus=<campus>/subject=<subjectCode>/course=<courseCode>/fullDetails', methods=["GET"])
def courseSectionsFull(campus: str, subjectCode: str, courseCode: str):

    dictToReturn = fromCoursePullSections(
        subjectCode = subjectCode,
        courseCode = courseCode,
        campus = campus,
        fulldetails= True
    )

    return jsonify(dictToReturn)

@apiBP.route('/sectionDetails/campus=<campus>/subject=<subjectCode>/course=<courseCode>/section=<sectionCode>', methods=["GET"])
def sectionDetails(campus: str, subjectCode: str, courseCode: str, sectionCode: str):

    dictToReturn = fromSectionPullDetails(
        subjectCode = subjectCode,
        courseCode = courseCode,
        sectionCode = sectionCode,
        campus = campus
    )

    return jsonify(dictToReturn)
    
@apiBP.route('/subjectCourses/campus=<campus>/subject=<subjectCode>', methods=["GET"])
def subjectCourse(campus: str, subjectCode: str):

    dictToReturn = fromSubjectPullCourses(
        campus = campus,
        subjectCode = subjectCode,
        fulldetails = False
    )

    return jsonify(dictToReturn)

@apiBP.route('/subjectCourses/campus=<campus>/subject=<subjectCode>/fullDetails', methods=["GET"])
def subjectCourseFull(campus: str, subjectCode: str):

    dictToReturn = fromSubjectPullCourses(
        campus = campus,
        subjectCode = subjectCode,
        fulldetails = True
    )

    return jsonify(dictToReturn)

@apiBP.route('/subjectSections/campus=<campus>/subject=<subjectCode>', methods=["GET"])
def subjectSections(campus: str, subjectCode: str):

    dictToReturn = fromSubjectPullSections(
        campus = campus,
        subjectCode = subjectCode
    )

    return jsonify(dictToReturn)

@apiBP.route('/subjectSections/campus=<campus>/subject=<subjectCode>/fullDetails', methods=["GET"])
def subjectSectionsFull(campus: str, subjectCode: str):

    dictToReturn = fromSubjectPullSections(
        campus = campus,
        subjectCode = subjectCode,
        fulldetails = True
    )

    return jsonify(dictToReturn)