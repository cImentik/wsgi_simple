import html
import re
import json

from core.base_views import BaseView, render
from models import Stat, Comment, Region, City

"""
View classes is here
"""


class HomeView(BaseView):
    def __init__(self, environ, start_fn):
        super(HomeView, self).__init__(environ, start_fn)

    def get(self):
        return render('templates/home.html')


class StatView(BaseView):
    def __init__(self, environ, start_fn):
        super(StatView, self).__init__(environ, start_fn)

    def get(self):
        """
        If region_id is in the query string, then we want to see statistics
        by cities, and we do not need links
        """
        if 'rid' in self.req_get:
            context = {
                'rows': [s.as_dic() for s in Stat().get_list(region_id=self.req_get['rid'][0])],
                'city': 1,
            }
        else:
            context = {
                'rows': [],
                'city': 0,
            }
            rows = Stat().get_list() 
            if rows:
                context['rows'] = [stat.as_dic() for stat in rows]
        return render('templates/stat.html', context)


class CommentView(BaseView):
    def __init__(self, environ, start_fn):
        super(CommentView, self).__init__(environ, start_fn)

        self.context = {
            'comment': Comment().as_dic(),
            'regions': [r.as_dic() for r in Region().all()],
            'warn': None,
            'success': None,
        }

    def get(self):
        return render('templates/comment.html', self.context)

    def post(self):
        """
        Сhecking that there are all an attributes
        and they are correct for creating a comment,
        if not, we return as is and a notification.
        """
        def is_phone_valid(phone):
            return re.match(r"^(\(\d+\))(\s)?\d+", phone)

        def is_email_valid(email):
            return re.match(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$", email)

        com = Comment()
        if 'surname' in self.req_post:
            com.surname = html.escape(self.req_post['surname'][0])
        if 'firstname' in self.req_post:
            com.firstname = html.escape(self.req_post['firstname'][0])
        if 'patronymic' in self.req_post:
            com.patronymic = html.escape(self.req_post['patronymic'][0])
        if 'region' in self.req_post:
            com.region = Region(id=int(self.req_post['region'][0]))
        if 'city' in self.req_post:
            com.city = City(id=int(self.req_post['city'][0]))
        if 'phone' in self.req_post:
            com.phone = html.escape(self.req_post['phone'][0])
        if 'email' in self.req_post:
            com.email = html.escape(self.req_post['email'][0])
        if 'comment' in self.req_post:
            com.comment = html.escape(self.req_post['comment'][0])

        if not com.surname or not com.firstname or not com.comment:
            self.context['warn'] = "You have required fields"
            self.context['comment'] = com.as_dic()
            return render('templates/comment.html', self.context)

        if com.phone and not is_phone_valid(com.phone):
            self.context['warn'] = "Invalid phone number format"
            self.context['comment'] = com.as_dic()
            return render('templates/comment.html', self.context)

        if com.email and not is_email_valid(com.email):
            self.context['warn'] = "Invalid email format"
            self.context['comment'] = com.as_dic()
            return render('templates/comment.html', self.context)

        com.save()
        self.context['success'] = "Comment has been added successfully"

        return render('templates/comment.html', self.context)

    def ajax(self):
        """
        If XMLHttpRequest, geting all City() for region_id
         and make json.dump()
        """
        region_id = self.req_post.get('region_id', None)
        if not region_id:
            return "{}"
        context = [r.as_dic() for r in City().get(region=Region(id=region_id[0]))]
        return json.dumps(context)


class ViewView(BaseView):
    def __init__(self, environ, start_fn):
        super(ViewView, self).__init__(environ, start_fn)

    def get(self):
        context = {
            'comments': [c.as_dic() for c in Comment().all()]
        }
        return render('templates/view.html', context)

    def post(self):
        if 'comment' in self.req_post:
            com = Comment().get(id=self.req_post['comment'][0])
            com.delete()
        context = {
            'comments': [c.as_dic() for c in Comment().all()]
        }
        return render('templates/view.html', context)
