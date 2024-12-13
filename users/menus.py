MENU_ITEMS = {
    'premium': [
        {
            'name': 'Profile CV',
            'url': 'profilecv/',
            'submenu': [
                {'name': 'Basics', 'url': "/profile/profiles",'icon':'bi bi-person-lines-fill'},
                {'name': 'Works', 'url': '/users/add/','icon':'bi bi-person-workspace'},
                {'name': 'Education', 'url': '/users/view/','icon':'bi bi-mortarboard-fill'},
                {'name': 'Skills', 'url': '/users/add/','icon':'bi bi-tags'},
                {'name': 'Projects', 'url': '/users/view/','icon':'bi bi-file-code'},
                {'name': 'Awards', 'url': '/users/add/','icon':'bi bi-award'},
                
                ]
        },
        {
            'name': 'Management CV',
            'url': '/users/',
            'submenu': [
                {'name': 'My Profiles', 'url': '/users/view/','icon':'bi bi-file-earmark-person'},
                {'name': 'Add Profile', 'url': '/users/add/','icon':'bi bi-file-earmark-plus'},
            ]
        },
        {
            'name': 'My JobOffers',
            'url': '/settings/',
            'submenu': [
                {'name': 'Work Offers', 'url': '/settings/profile/','icon':'bi bi-card-checklist'},
                {'name': 'Find Offer', 'url': '/settings/system/','icon':'bi bi-search'},
            ]
        },
       
        {
            'name': 'My Test',
            'url': '/settings/',
            'submenu': [  
                 {'name': 'My Test', 'url': '/settings/profile/','icon':'bi bi-check2-square'},
                 {'name': 'Blog', 'url': '/blog','icon':'bi bi-plus-square'},
                     ]
        },
        {
            'name': 'Messages',
            'url': '/profile/',
            'submenu': [
                  {'name': 'Inbox', 'url': '/messaging/inbox/','icon':'bi bi-check2-square'},
                 {'name': 'Send', 'url': '/messaging/send/','icon':'bi bi-plus-square'},
                 {'name': 'Sent', 'url': '/messaging/sent/','icon':'bi bi-plus-square'},
            ]
        },
        {
            'name': 'Blog',
            'url': '/blog',
            'submenu': [
                
            ]
        },
    ],
    'teacher': [
        {
            'name': 'Dashboard',
            'url': '/',
            'submenu': [
                 {'name': 'My Test', 'url': '/settings/profile/','icon':'bi bi-check2-square'},
                 {'name': 'Add Test', 'url': '/settings/system/','icon':'bi bi-plus-square'},

            ]
        },
        {
            'name': 'Courses',
            'url': '/profile/',
            'submenu': [
                 

                
            ]
        },
        {
            'name': 'Messages',
            'url': '/profile/',
            'submenu': [
                {'name': 'Inbox', 'url': '/messaging/inbox/','icon':'bi bi-check2-square'},
                 {'name': 'Send', 'url': '/messaging/send/','icon':'bi bi-plus-square'},
                 {'name': 'Sent', 'url': '/messaging/sent/','icon':'bi bi-plus-square'},
            ]
        },
        
    ],
    'headhunter': [
        {
            'name': 'Dashboard',
            'url': '/',
            'submenu': [
                 {'name': 'Blog', 'url': '/blog','icon':'bi bi-check2-square'},
                 {'name': 'Add Test', 'url': '/settings/system/','icon':'bi bi-plus-square'},

            ]
        },
        {
            'name': 'Offers',
            'url': '/blog',
            'submenu': [
                
            ]
        },
        {
            'name': 'Messages',
            'url': '/profile/',
            'submenu': [
                  {'name': 'Inbox', 'url': '/messaging/inbox/','icon':'bi bi-check2-square'},
                 {'name': 'Send', 'url': '/messaging/send/','icon':'bi bi-plus-square'},
                 {'name': 'Sent', 'url': '/messaging/sent/','icon':'bi bi-plus-square'},
            ]
        },
        
    ],
    'guest': [
        {
            'name': 'Home',
            'url': '/',
            'submenu': []
        },
        {
            'name': 'Courses',
            'url': '/blog',
            'submenu': [  
                {'name': 'Blog', 'url': '/blog','icon':'bi bi-plus-square'},
]
        },
        {
            'name': 'JobOffers',
            'url': '/blog',
            'submenu': [
                  {'name': 'Blog', 'url': '/blog','icon':'bi bi-plus-square'},

            ]
        },
        {
            'name': 'Tests',
            'url': '/register/',
            'submenu': []
        },
           {
            'name': 'Events',
            'url': '/register/',
            'submenu': []
        },
           {
            'name': 'Mentorship',
            'url': '/register/',
            'submenu': []
        },
            {
            'name': 'Blog',
            'url': '/blog',
            'submenu': []
        },
            {
            'name': 'Tips',
            'url': '/register/',
            'submenu': []
        },
            {
            'name': 'Contact',
            'url': '/register/',
            'submenu': []
        },
        
    ],
}