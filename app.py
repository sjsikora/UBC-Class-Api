from flask import Flask, jsonify, request, render_template
from scripts.ApiFunctions import fromCampusPullSubjects, fromCoursePullSections, fromSectionPullDetails, fromSubjectPullCourses, fromSubjectPullSections, formatInputJson

#docker image build -t ubcApi .

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/campusSubject', methods=["POST"])
def campusSubject():
    inputJson = request.get_json(force=True)
    inputJson = formatInputJson(inputJson)

    dictToReturn = fromCampusPullSubjects(
        campus = inputJson['campus']
    )

    return jsonify(dictToReturn)

@app.route('/courseSections', methods=["POST"])
def courseSections():
    inputJson = request.get_json(force=True)
    inputJson = formatInputJson(inputJson)

    dictToReturn = fromCoursePullSections(
        subjectCode = inputJson['subjectCode'],
        courseCode = inputJson['courseCode'],
        campus = inputJson['campus'],
    )

    return jsonify(dictToReturn)

@app.route('/sectionDetails', methods=["POST"])
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
    
@app.route('/subjectCourses', methods=["POST"])
def subjectCourse():
    inputJson = request.get_json(force=True)
    inputJson = formatInputJson(inputJson)

    dictToReturn = fromSubjectPullCourses(
        subjectCode = inputJson['subjectCode'],
        campus = inputJson['campus'],
        fulldetails = inputJson['fullDetails']
    )

    return jsonify(dictToReturn)

@app.route('/subjectSections', methods=["POST"])
def subjectSections():
    inputJson = request.get_json(force=True)
    inputJson = formatInputJson(inputJson)

    dictToReturn = fromSubjectPullSections(
        subjectCode = inputJson['subjectCode']
    )

    return jsonify(dictToReturn)


if __name__ == '__main__':
    app.run(debug=True, port=8000)