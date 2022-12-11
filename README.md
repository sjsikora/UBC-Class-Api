# UBC Class Api

This project is an API built off flask with the purpose of turning UBC (Vancouver and Okanagan) class data into readable JSON files. Anyone is welcome to use this API for any projects as well.

## The API acceptes these following methods:

### GET /campusSubjects/campus=<campus>

campus = ['UBCO', 'UBCV']

This method will return a list of all subjects offered at the campus specficed where each subject looks like

```json
{
    "code": "CCS",
    "properName": "Creative and Critical Studies",
    "faculty": "Faculty of Creative and Critical Stds",
    "offered": true
}
```

