# UBC Class Api

This project is an API built off flask with the purpose of turning UBC (Vancouver and Okanagan) class data into readable JSON files. Anyone is welcome to use this API for any projects as well.

## The API acceptes these following methods:

NOTE: 

Campus variable acceptes "UBCV" (UBC Vancouver Campus) and "UBCO" (UBC Okanagan Campus).

The "term" variable may be 3. This refers to the course being a year-long course.

### GET /campusSubjects/campus={campus}

/campusSubjects/campus=UBCO

Returns a list of all subjects offered at the campus specficed where each subject is defined as follows:

```json
{
    "code": "CCS",
    "properName": "Creative and Critical Studies",
    "faculty": "Faculty of Creative and Critical Stds",
    "offered": true
}
```

### GET /courseSections/campus={campus}/subject={subjectCode}/course={courseCode}

/courseSections/campus=UBCO/subject=PHYS/course=112

Returns a list of sections from a specified course where each section is each subject is defined as follows:

```json
{
    "section": "PHYS 121 L01",
    "status": "Full",
    "activity": "Laboratory",
    "term": 2,
    "delivery": "In-Person",
    "interval": "",
    "days": [
        "Mon"
    ],
    "start": "13:00",
    "end": "16:00",
    "comments": "",
    "inPersonAttendance": true
}
```

#### GET /courseSections/campus={campus}/subject={subjectCode}/course={courseCode}/fullDetails

/courseSections/campus=UBCV/subject=BIOC/course=303/fullDetails

Returns a list of sections from a specified course where each section is each subject is defined as follows:

```json
{
    "section": "BIOC 303 001",
    "status": "Full",
    "activity": "Lecture",
    "term": 3,
    "delivery": "In-Person",
    "interval": "",
    "days": [
        "Mon",
        "Wed",
        "Fri"
    ],
    "start": "13:00",
    "end": "14:00",
    "comments": "",
    "inPersonAttendance": true,
    "syllabusUrl": "",
    "instructor": [
        "DUONG VAN HOA, FRANCK"
    ],
    "building": "Hennings",
    "room": "201",
    "seatsTotalRemaining": "0",
    "seatsRegistered": "120",
    "seatsGeneralRemaining": "0",
    "seatsRestrictedRemaining": "0"
}
```