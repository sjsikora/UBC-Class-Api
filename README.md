# UBC Class API

This project is an API built off Flask, run on AWS with the purpose of turning UBC (Vancouver and Okanagan) class data into readable JSON files. I have plans to create a degreee helper off this website, yet as I build the front end, I wanted to launch for API for any uses others may have.

## The API acceptes these following methods:

NOTE: 

Campus variable acceptes "UBCV" (UBC Vancouver Campus) and "UBCO" (UBC Okanagan Campus).

The "term" variable may be 3. This refers to the course being a year-long course. Also, in some edge cases, term may be "X", "C" or "A."

Because the data is being scraped on call, I highly suggest using the method narrowly tailored to your use case. There will be slow results if you generate every single piece of data.

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

Some special classes are offered on different days at different times, these are defined instead with "days", "start", "end", but rather with a new variable "timing" where "timing" is defined as:

```json
"timing": [
    {
        "Mon": {
            "start": "14:00",
            "end": "15:30"
        }
    },
    {
        "Fri": {
            "start": "14:00",
            "end": "15:30"
        }
    },
    {
        "Mon": {
            "start": "15:30",
            "end": "16:30"
        }
    }
]

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

In some special cases, courses are either offered year long. In these cases, then json is defined as follows.

```json
    {
        "section": "BIOC 301 001",
        "status": "Full",
        "activity": "Lecture-Laboratory",
        "term": 3,
        "delivery": "In-Person",
        "interval": "",
        "days": [
            "Tue"
        ],
        "start": "12:30",
        "end": "13:30",
        "comments": "Entry to this course is normally restricted to third year students in Biochemistry major and honours programs, who have completed appropriate 1st and 2nd year program requireme dnts, and to Physiology, Pharmacology and Honours Biophysics students who have received approval for their programs.  The academic records of all students who register into the course will be checked and those not having an appropriate academic background for their designated specialization will be de-registered. Additionally, registration in co-requisite courses (Bioc 302 or Bioc 303) will be checked and any students not registered in the appropriate course may be removed from Bioc 301.No preference is given to 4th year students and, accordingly, direct registration is restricted to students with 3rd year standing in the Faculty of Science.  Eligible 4th year students needing to take the course should register into the wait-list section and contact the Biochemistry adviser (jaread@mail.ubc.ca) to request entry to the course.  Approved 4th year students will be registered by the department when their academic standing matches that of the incoming 3rd year class.  ",
        "inPersonAttendance": true,
        "syllabus": "http://www.biochem.ubc.ca/CourseMat.html",
        "instructor": [
            "READ, JASON"
        ],
        "classSeatsTotalRemaining": "0",
        "classSeatsRegistered": "153",
        "classSeatsGeneralRemaining": "0",
        "classSeatsRestrictedRemaining": "0",
        "sectionTerms": [
            {
                "term": 2,
                "days": [
                    "Tue"
                ],
                "start": "12:30",
                "end": "13:30",
                "building": "Friedman Building",
                "room": "153"
            },
            {
                "term": 1,
                "days": [
                    "Tue"
                ],
                "start": "12:30",
                "end": "13:30",
                "building": "Friedman Building",
                "room": "153"
            }
        ]
    },

```

In other even rarer cases, some course are offered in the same term, but on different times at different days. In these cases, the Json is defined as follows:

```json

{
    "section": "DHYG 106 001",
    "status": "STT",
    "activity": "Lecture",
    "term": 2,
    "delivery": "In-Person",
    "interval": "",
    "days": [
        "Mon",
        "Fri"
    ],
    "start": "14:00",
    "end": "15:30",
    "comments": "",
    "inPersonAttendance": true,
    "syllabus": "",
    "instructor": [
        "NAJAR, HOSSAIN"
    ],
    "classSeatsTotalRemaining": 0,
    "classSeatsRegistered": 0,
    "classSeatsGeneralRemaining": 0,
    "classSeatsRestrictedRemaining": 0,
    "sectionTerms": [
        {
            "term": 2,
            "days": [
                "Mon"
            ],
            "start": "15:30",
            "end": "16:30",
            "building": " ",
            "room": ""
        },
        {
            "term": 2,
            "days": [
                "Mon",
                "Fri"
            ],
            "start": "14:00",
            "end": "15:30",
            "building": " ",
            "room": ""
        }
    ]
}

```


### GET /sectionDetails/campus={campus}/subject={subjectCode}/course={courseCode}/section={sectionCode}

From a section pull the details where the details are defined as follows:

```json

```
