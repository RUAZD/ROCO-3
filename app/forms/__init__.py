from app.forms.f_admin import router as router_admins
from app.forms.f_advs import router as router_adv
from app.forms.f_courses import router as router_courses
from app.forms.f_groups import router as router_groups
from app.forms.f_teachers import router as router_teachers
from app.forms.f_topics import router as router_topics
from app.forms.f_users import router as router_users
from app.forms.f_users_advs import router as router_users_advs
from app.forms.f_users_courses import router as router_users_courses
from app.forms.f_users_friends import router as router_users_friends
from app.forms.f_users_groups import router as router_users_groups
from app.forms.f_users_topics import router as router_users_topics
from app.forms.f_videos import router as router_videos

routers = [
    router_users,
    router_users_advs,
    router_users_courses,
    router_users_friends,
    router_users_groups,
    router_users_topics,
    router_teachers,
    router_courses,
    router_videos,
    router_groups,
    router_topics,
    router_adv,
    router_admins
]
