"""
This module contains a function to generate a PDF report with the data of a project.
The report is based on a markdown template and uses the FPDF library to generate the PDF.

The function `text_for_pdf` takes a list of tuples as input, where each tuple contains a key and a value.
The function will replace the key for the value in the markdown template.

The keys that are expected are:
- `project_name`
- `project_description`
- `project_colaborators`
- `project_tasks`

The function will return a string with the markdown text for the report.
"""


def text_for_pdf(data):
    return f"""
# {data[1][1]}

#### `Description project`

{data[2][1]}

##### `Created in`

Project created in {data[3][1]}

##### `Created by`

Project Created by {data[4][1]}

##### `Procet Status`

Project {data[5][1]}

##### `Project Progress`

Project Progress is in {data[6][1]} %

## Tasks

##### `Total of tasks`

The Total Number of tasks is {data[7][1]}

#### Analytics

###### by progress

| Progress          | Data |
| ----------------- | ---- |
| Tasks Open        | {data[8][1]}   |
| Tasks in progress | {data[9][1]}    |
| Tasks Done        | {data[10][1]}    |

###### by priority

| Priority     | Data |
| ------------ | ---- |
| Tasks Low    | {data[11][1]}   |
| Tasks Medium | {data[12][1]}    |
| Tasks High   | {data[13][1]}    |

---

### More about tasks

#### `Time for Done`

The average time to done a task is {data[14][1]} days

###### table for tasks by colaborator

{data[17][1]}

### More about Project

###### colaborators

{data[18][1]}


    """
