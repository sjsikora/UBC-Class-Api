from flask import Flask, jsonify, request, render_template, Blueprint
from app.api.scripts.ApiFunctions import fromCampusPullSubjects, fromCoursePullSections, fromSectionPullDetails, fromSubjectPullCourses, fromSubjectPullSections, formatInputJson

apiBP = Blueprint('api', __name__)

@apiBP.route('/')
def home():
    return render_template('index.html')

@apiBP.route('/campusSubjects', methods=["POST"])
def campusSubject():
    inputJson = request.get_json(force=True)
    inputJson = formatInputJson(inputJson)

    dictToReturn = fromCampusPullSubjects(
        campus = inputJson['campus']
    )

    return jsonify(dictToReturn)

@apiBP.route('/courseSections', methods=["POST"])
def courseSections():
    inputJson = request.get_json(force=True)
    inputJson = formatInputJson(inputJson)

    dictToReturn = fromCoursePullSections(
        subjectCode = inputJson['subjectCode'],
        courseCode = inputJson['courseCode'],
        campus = inputJson['campus'],
    )

    return jsonify(dictToReturn)

@apiBP.route('/sectionDetails', methods=["POST"])
def sectionDetails():
    inputJson = request.get_json(force=True)
    inputJson = formatInputJson(inputJson)

    dictToReturn = fromSectionPullDetails(
        subjectCode = inputJson['subjectCode'],
        courseCode = inputJson['courseCode'],
        sectionCode = inputJson['sectionCode'],
        campus = inputJson['campus']
    )

    return jsonify(dictToReturn)
    
@apiBP.route('/subjectCourses', methods=["POST"])
def subjectCourse():
    inputJson = request.get_json(force=True)
    inputJson = formatInputJson(inputJson)

    dictToReturn = fromSubjectPullCourses(
        subjectCode = inputJson['subjectCode'],
        campus = inputJson['campus'],
        fulldetails = inputJson['fullDetails']
    )

    return jsonify(dictToReturn)

@apiBP.route('/subjectSections', methods=["POST"])
def subjectSections():
    inputJson = request.get_json(force=True)
    inputJson = formatInputJson(inputJson)

    dictToReturn = fromSubjectPullSections(
        subjectCode = inputJson['subjectCode']
    )

    return jsonify(dictToReturn)