import random
from datacenter.models import Mark, Chastisement, Commendation, Schoolkid, Lesson


COMMENDATION_TEXTS = [
    "Молодец",
    "Отлично!",
    "Хорошо!",
    "Ты меня приятно удивил!",
    "Великолепно!",
    "Прекрасно!",
    "Именно этого я давно ждал от тебя!",
    "Сказано здорово – просто и ясно!",
    "Очень хороший ответ!",
    "Талантливо!",
]


def find_schoolkid(schoolkid_name):
    schoolkid = Schoolkid.objects.filter(full_name__contains=schoolkid_name)
    if schoolkid.count() == 0:
        print(f'Ученик с именем "{schoolkid_name}" не найден.')
    elif schoolkid.count() == 1:
        name = schoolkid.get()
        print(f'Найден ученик {name}')
        return name
    else:
        print(f'Найдено несколько учеников {schoolkid_name}')


def fix_marks(schoolkid_name):
    schoolkid = find_schoolkid(schoolkid_name)
    if not schoolkid:
        return
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    bad_marks.update(points=5)
    print(f'Оценки {schoolkid} исправлены')


def remove_chastisements(schoolkid_name):
    schoolkid = find_schoolkid(schoolkid_name)
    if not schoolkid:
        return
    chastisement = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisement.delete()
    print(f'Замечания {schoolkid} удалены')


def create_commendation(schoolkid_name, subject_title):
    schoolkid = find_schoolkid(schoolkid_name)
    if not schoolkid:
        return
    last_lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=subject_title
    ).order_by('-date').first()
    if not last_lesson:
        print(f"Урок {subject_title} для {schoolkid.year_of_study}{schoolkid.group_letter} не найден")
        return
    commendation = Commendation.objects.create(
        text=random.choice(COMMENDATION_TEXTS),
        created=last_lesson.date,
        schoolkid=schoolkid,
        subject=last_lesson.subject,
        teacher=last_lesson.teacher
    )
    print(f"Похвала создана: {commendation.text}. Для ученика {schoolkid}. Предмет {commendation.subject}, дата {commendation.created}")
