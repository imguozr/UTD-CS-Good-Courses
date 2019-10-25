import json

import requests

URI = 'https://v544dfea4f.execute-api.us-east-2.amazonaws.com/production/section'


def generate(aim_ratio, file):
    for num in range(1, 100):
        course_num = 'CS63' + str(num) if num > 9 else 'CS630' + str(num)
        re = requests.get(URI, params={'search': course_num})
        data = {}
        if re.text != '[]':
            data = json.loads(re.text)
            file.write('----- ' + course_num + ' -----\n')
        for section in data:
            semester = section['course']['semester']['name']
            course_name = 'CS' + section['course']['number'] + '.' + section['number']
            prof_name = section['professor']['firstName'] + ' ' + section['professor']['lastName']
            a, a_m, total_stu, ratio = 0, 0, 0, 0.0
            for k, v in section['grades'].items():
                if k == 'A':
                    a = int(v)
                elif k == 'A-':
                    a_m = int(v)
                total_stu += int(v)
                ratio = (a + a_m) / total_stu
            course = semester + ', ' + course_name + ', ' + prof_name + '\n' + \
                'A: ' + str(a) + ', A-: ' + str(a_m) + \
                ', total students: ' + str(total_stu) + \
                ', ratio: ' + ('%.3f%%' % (100 * ratio)) + '\n'
            if ratio > aim_ratio:
                file.write(course)
                file.write('\n')
            print(course)


with open('courses_80%.txt', 'w') as f:
    generate(0.8, f)

with open('courses.txt', 'w') as f:
    generate(0, f)
