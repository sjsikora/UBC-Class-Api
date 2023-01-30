
# NOTE:

This project has since been dropped in accord with UBC's CWL terms of service.

# UBC Class API

This project is an API built off Flask, run on ... with the purpose of turning UBC (Vancouver and Okanagan) class data into readable JSON files. I have plans to create a degreee helper off this website, yet as I build the front end, I wanted to launch for API for any uses others may have.

## The API acceptes these following methods:

NOTE: 

Campus variable acceptes "UBCV" (UBC Vancouver Campus) and "UBCO" (UBC Okanagan Campus).

The "term" variable may be 3. This refers to the course being a year-long course. Also, in some edge cases, term may be "X", "C" or "A."

Because the data is being scraped on call, I highly suggest using the method narrowly tailored to your use case. There will be slow results if you generate every single piece of data.

### GET /campusSubjects/campus={campus}

/campusSubjects/campus=UBCO

Returns a list of all subjects offered at the campus specified where each subject is defined as follows:

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

In some special cases, courses are offered year long. In these cases, then json is defined as follows:

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
    "syllabus": "",
    "instructor": [
        "DUONG VAN HOA, FRANCK",
        "HOWE, LEANN",
        "KRISINGER, MICHAEL",
        "MAYOR, THIBAULT",
        "TOKURIKI, NOBUHIKO"
    ],
    "classSeatsTotalRemaining": "0",
    "classSeatsRegistered": "120",
    "classSeatsGeneralRemaining": "0",
    "classSeatsRestrictedRemaining": "0",
    "sectionTerms": [
        {
            "term": 2,
            "days": [
                "Mon",
                "Wed",
                "Fri"
            ],
            "start": "13:00",
            "end": "14:00",
            "building": "Earth Sciences Building",
            "room": "1012"
        },
        {
            "term": 1,
            "days": [
                "Mon",
                "Wed",
                "Fri"
            ],
            "start": "13:00",
            "end": "14:00",
            "building": "Hennings",
            "room": "201"
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

/sectionDetails/campus=UBCO/subject=COSC/course=111/section=001

Returns an object of the details of the section requested, follows the same edge case rules as the method above. Normally, object is defined as follows:

```json

{
    "syllabus": "",
    "instructor": [
        "MOHAMED, ABDALLAH"
    ],
    "classSeatsTotalRemaining": "9",
    "classSeatsRegistered": "107",
    "classSeatsGeneralRemaining": "9",
    "classSeatsRestrictedRemaining": "0",
    "term": 1,
    "days": [
        "Mon",
        "Wed"
    ],
    "start": "14:00",
    "end": "15:30",
    "building": "LIB",
    "room": "L312"
}

```

### GET /subjectCourses/campus={campus}/subject={subjectCode}

/subjectCourses/campus=UBCO/subject=COSC

Returns a list of courses offered in a subject. Where courses are defined as follows:

```json

{
    "code": "COSC 101",
    "title": "Digital Citizenship"
},
    
```

### GET /subjectCourses/campus={campus}/subject={subjectCode}/fullDetails

/subjectCourses/campus=UBCO/subject=COSC/fullDetails

Returns a list of courses offered in a subject. Where courses are defined as follows:

```json

{
    "code": "COSC 101",
    "credits": 3.0,
    "preReqs": "on is required for this course.",
    "description": "Provides knowledge and skills to navigate the digital society. The importance of digital participation will be investigated by studying issues surrounding digital access, skills, and utilization. Digital literacy is emphasized through the exploration of computer applications, the use of converging technologies, and online resources. This course does not assume students have any Computer Science background. Credit will be granted for only one of COSC 101 or COSC 132.",
    "title": "Digital Citizenship"
},

```
### GET /subjectSections/campus={campus}/subject={subjectCode} 

/subjectSections/campus=UBCV/subject=DHYG

Returns a list of every course in a subject and their respective sections where each course is defined as:

```json

{
    "code": "DHYG 110",
    "credits": 3.0,
    "preReqs": "",
    "description": "An introduction to the Dental Hygiene profession, practice roles and the process of care model.",
    "title": "Dental Hygiene Theory and Practice I",
    "sections": [
        {
            "section": "DHYG 110 001",
            "status": "STT",
            "activity": "Seminar",
            "term": 1,
            "delivery": "In-Person",
            "interval": "",
            "days": [
                "Wed"
            ],
            "start": "14:00",
            "end": "17:00",
            "comments": "",
            "inPersonAttendance": true
        }
    ]
},

```
With courses that are offered on the same term with different days, the timing variable is used.

```json

{
    "code": "DHYG 106",
    "credits": 3.0,
    "preReqs": "",
    "description": "Basic principles in the study of microorganisms and their relation to human health for dental hygiene students.",
    "title": "Basics of Oral Microbiology",
    "sections": [
        {
            "section": "DHYG 106 001",
            "status": "STT",
            "activity": "Lecture",
            "term": 2,
            "delivery": "In-Person",
            "interval": "",
            "comments": "",
            "inPersonAttendance": true,
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
        }
    ]
},

```

### GET /subjectSections/campus={campus}/subject={subjectCode}/fullDetails

/subjectSections/campus=UBCV/subject=CPSC/fullDetails

BEWARE, this is a slow method. Returns a list of courses with sections and their details where courses are defined as follows:

```json

{
    "code": "COLX 523",
    "credits": 1.0,
    "preReqs": "All of DSCI 511, COLX 521. ",
    "description": "Advanced computational techniques in multilingual corpora. Language change and linguistic variation; best practices for data collection, annotation and analysis.",
    "title": "Advanced Corpus Linguistics ",
    "sections": [
        {
            "section": "COLX 523 001",
            "status": "Restricted",
            "activity": "Lecture",
            "term": 2,
            "delivery": "In-Person",
            "interval": "",
            "days": [
                "Mon",
                "Wed"
            ],
            "start": "8:30",
            "end": "10:00",
            "comments": "This course is restricted to students registered in the MDS-CL program only.  ",
            "inPersonAttendance": true,
            "syllabus": "",
            "instructor": [
                "NICOLAI, GARRETT"
            ],
            "classSeatsTotalRemaining": "15",
            "classSeatsRegistered": "30",
            "classSeatsGeneralRemaining": "0",
            "classSeatsRestrictedRemaining": "15",
            "building": "Civil and Mechanical Engineering",
            "room": "1215"
        },
        {
            "section": "COLX 523 L01",
            "status": " ",
            "activity": "Laboratory",
            "term": 2,
            "delivery": "In-Person",
            "interval": "",
            "days": [
                "Mon"
            ],
            "start": "14:00",
            "end": "16:00",
            "comments": "",
            "inPersonAttendance": true,
            "syllabus": "",
            "instructor": [],
            "classSeatsTotalRemaining": "15",
            "classSeatsRegistered": "30",
            "classSeatsGeneralRemaining": "15",
            "classSeatsRestrictedRemaining": "0",
            "building": "Orchard Commons",
            "room": "3018"
        },
        {
            "section": "COLX 523 L02",
            "status": " ",
            "activity": "Laboratory",
            "term": 2,
            "delivery": "In-Person",
            "interval": "",
            "days": [
                "Mon"
            ],
            "start": "16:00",
            "end": "18:00",
            "comments": "",
            "inPersonAttendance": true,
            "syllabus": "",
            "instructor": [],
            "classSeatsTotalRemaining": "45",
            "classSeatsRegistered": "0",
            "classSeatsGeneralRemaining": "45",
            "classSeatsRestrictedRemaining": "0",
            "building": "Orchard Commons",
            "room": "3018"
        }
    ]
},

```

With courses that are year long, or are offered on different days at different times. In the "section" variable, there is a new variable "sectionTerms"
where sectionTerms is defined as:

Different days at different times
```json

{
    "code": "DHYG 106",
    "credits": 3.0,
    "preReqs": "",
    "description": "Basic principles in the study of microorganisms and their relation to human health for dental hygiene students.",
    "title": "Basics of Oral Microbiology",
    "sections": [
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
    ]
},

```

Year long:
```json
{
        "code": "BIOC 301",
        "credits": 3.0,
        "preReqs": "One of BIOC 300, BIOC 302, BIOC 303. ",
        "description": "Techniques by which the chemical and physical properties of fundamental components of the cell are studied.",
        "title": "Biochemistry Laboratory",
        "sections": [
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
                "comments": "Entry to this course is normally restricted to third year students in Biochemistry major and honours programs, who have completed appropriate 1st and 2nd year program requirements, and to Physiology, Pharmacology and Honours Biophysics students who have received approval for their programs.  The academic records of all students who register into the course will be checked and those not having an appropriate academic background for their designated specialization will be de-registered. Additionally, registration in co-requisite courses (Bioc 302 or Bioc 303) will be checked and any students not registered in the appropriate course may be removed from Bioc 301.No preference is given to 4th year students and, accordingly, direct registration is restricted to students with 3rd year standing in the Faculty of Science.  Eligible 4th year students needing to take the course should register into the wait-list section and contact the Biochemistry adviser (jaread@mail.ubc.ca) to request entry to the course.  Approved 4th year students will be registered by the department when their academic standing matches that of the incoming 3rd year class.  ",
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
            },...
```
