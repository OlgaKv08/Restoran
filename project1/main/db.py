
users = [
    {
        'login': 'lera',
        'password': 'val228',
        'img': 'https://www.meme-arsenal.com/memes/0a2f97e29a2a95c781d322ff3dc50d6b.jpg',
        'isAdmin': False
    },
    {
        'login': 'zheka',
        'password': 'zkh',
        'img': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRrxguXcGMjtKPsxXlShapGw7X3f-mgSUH-xodjs7krz60rWOwV3brX3po60gUnnI09hL0&usqp=CAU',
        'isAdmin': False
    },
    {
        'login': 'admin',
        'password': 'aaaddd',
        'img': 'https://koshka.top/uploads/posts/2021-12/1639030708_1-koshka-top-p-koshki-rzhut-1.jpg',
        'isAdmin': True
    }
]

restorans = [
    {
        'name': 'Вилен',
        'city': 'Кривой Рог',
        'img': 'https://lh5.googleusercontent.com/p/AF1QipMlIGjzJ9fjUfBWnnWCOD7IUS6mlfC8I6Anbsw4=w312-h210-n-k-no',
     
        'mapUrl': 'https://goo.gl/maps/ebtgAXwnWCk1v6XR8',
        'about': 'Хорошее место для отдыха с семьёй!',
        'comments': [
            {
                'user': users[0],
                'comment': "Отличный ресторан!",
                'raiting': 7
            },
        ]
    },
    {
        'name': 'Борщ Хауз 2.0',
        'city': 'Кривой Рог',
        'img': 'https://lh5.googleusercontent.com/p/AF1QipMIt3TKXRTscAHRIgDrGqJ2nJZqke2CmfxCG8wR=w312-h210-n-k-no',

        'mapUrl': 'https://goo.gl/maps/o7Gs9JJUDYWje2an9',
        'about': 'Для особых ценителей борьща!',
        'comments': [
            {
                'user': users[1],
                'comment': "Здесь готовят отличные щи!",
                'raiting': 7
            }
        ]
    },
    {
        'name': 'Веранда на Днепре',
        'city': 'Киев',
        'img': 'https://lh5.googleusercontent.com/p/AF1QipPhyqTnSD--gO_b9cMxvugYd45QDPb1bX-uUy3m=w408-h255-k-no',

        'mapUrl': 'https://goo.gl/maps/a3oshWdd8HMwGnm19',
        'about': 'Для состоятельных людей',
        'comments': [
            {
                'user': users[2],
                'comment': "Потрясающий вид на реку Днепр!!",
                'raiting': 10
            }
        ]
    },
    {
        'name': 'Grand Hall',
        'city': 'Карпаты',
        'img': 'https://lh5.googleusercontent.com/p/AF1QipMbZiCyct1eLSVyLmALVoiVyNKCnsproHMisHi-=w408-h240-k-no-pi-10-ya250.09-ro-0-fo100',
     
        'mapUrl': 'https://goo.gl/maps/cLDGjLAdmbC2tGRd9',
        'about': 'Для ещё более состоятельных людей!',
        'comments': [
            {
                'user': users[0],
                'comment': "Шикарная народная кухня!",
                'raiting': 8
            }
        ]
    },
]

city = 'All'
cityes = ['All']

for restoran in restorans:
    if not cityes.__contains__(restoran['city']):
        cityes.append(restoran['city'])
    
    if restoran['comments'] and len(restoran['comments']) > 0:
        middle = 0
        for comment in restoran['comments']:
            middle += int(comment['raiting'])
    
    restoran['raiting'] = int(middle/len(restoran['comments']))

isLogin = False
isAdmin = False

user = None

def GetRestoranByName(name: str):
    for restoran in restorans:
        if(restoran['name'] == name):
            return restoran
    return None

def CheckRaiting():
    for rest in restorans:
        if rest['comments'] and len(rest['comments']) > 0:
            middle = 0
            for comment in rest['comments']:
                middle += int(comment['raiting'])
    
        rest['raiting'] = int(middle/len(rest['comments']))

def CheckCityes():
    cityes.clear()
    for restoran in restorans:
        if not cityes.__contains__(restoran['city']):
            cityes.append(restoran['city'])

