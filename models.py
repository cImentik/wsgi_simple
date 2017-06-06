from core.base_model import DB

"""
Models classes.

Methods: all() - get all rows from table
         get() - get rows with attributs filter (for Region and Comment - get One row)
         as_dic() - present as a dictionary
         delete() - delete row from table
         __fix_kwargs() - fix values from kwargs for _id (like as: region.id - region_id)
         save() - put row into table. If id exists, then UPDATE, else INSERT INTO
"""


class Region():

    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    def get(self, **kwargs):
        where = " ".join(["{0}={1}".format(k, v) for k, v in kwargs.items()])
        with DB() as c:
            row = c.raw_sql("""SELECT id, name FROM region
                              WHERE """ + where + " LIMIT 1")['data'][0]
            return Region(id=row[0], name=row[1])

    def all(self):
        rows = DB().raw_sql("SELECT id, name FROM region")['data']
        return [Region(id=row[0], name=row[1]) for row in rows]

    def as_dic(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class City():

    def __init__(self, id=None, name=None, region=None):
        self.id = id
        self.name = name
        self.region = region if region else Region(id=0)

    def get(self, **kwargs):
        kwargs = self.__fix_kwargs(kwargs)
        where = " ".join(["{0}={1}".format(k, v) for k, v in kwargs.items()])
        with DB() as c:
            rows = c.raw_sql("""SELECT c.id, c.name, c.region_id, r.name
                              FROM city c
                              INNER JOIN region r ON c.region_id = r.id
                              WHERE """ + where)['data']
            return [City(id=row[0], name=row[1],
                region=Region(id=row[2], name=row[3])) for row in rows]

    def all(self):
        with DB() as c:
            rows = c.raw_sql("""SELECT c.id, c.name, c.region_id, r.name
                            FROM city c
                        INNER JOIN region r ON c.region_id = r.id""")['data']
            return [City(id=row[0], name=row[1],
                region=Region(id=row[2], name=row[3])) for row in rows]

    def __fix_kwargs(self, not_fix_kwargs):
        fix_kwargs = {}
        for k, v in not_fix_kwargs.items():
            if "region" == k:
                fix_kwargs["c."+k+"_id"] = v.id
            else:
                fix_kwargs["c."+k] = v
        return fix_kwargs

    def as_dic(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class Comment():

    def __init__(
        self, id=None, surname=None, firstname=None, patronymic=None,
        region=None, city=None, phone=None, email=None, comment=None
    ):
        self.id = id
        self.surname = surname
        self.firstname = firstname
        self.patronymic = patronymic
        self.region = region if region else Region(id=0)
        self.city = city if city else City(id=0)
        self.phone = phone
        self.email = email
        self.comment = comment

    def get(self, **kwargs):
        kwargs = self.__fix_kwargs(kwargs)
        where = " ".join(["{0}={1}".format(k, v) for k, v in kwargs.items()])
        with DB() as c:
            row = c.raw_sql("""SELECT ct.id, ct.surname, ct.firstname,
                        ct.patronymic, ct.phone, ct.email, ct.comment,
                        ct.region_id, r.name, ct.city_id, c.name
                              FROM comment ct
                              LEFT JOIN region r ON ct.region_id = r.id
                              LEFT JOIN city c ON ct.city_id = c.id
                              WHERE """ + where + " LIMIT 1")['data']
            if not row:
                return None
            return Comment(id=row[0][0], surname=row[0][1],
                firstname=row[0][2], patronymic=row[0][3],
                region=Region(id=row[0][7], name=row[0][8]),
                city=City(id=row[0][9], name=row[0][10]), phone=row[0][4],
                email=row[0][5], comment=row[0][6])

    def all(self):
        with DB() as c:
            rows = c.raw_sql("""SELECT ct.id, ct.surname, ct.firstname,
                            ct.patronymic, ct.phone, ct.email, ct.comment,
                            ct.region_id, r.name, ct.city_id, c.name
                            FROM comment ct
                            LEFT JOIN region r ON ct.region_id = r.id
                            LEFT JOIN city c ON ct.city_id = c.id""")['data']
            return [Comment(id=row[0], surname=row[1], firstname=row[2],
                patronymic=row[3], region=Region(id=row[7], name=row[8]),
                city=City(id=row[9], name=row[10]), phone=row[4],
                email=row[5], comment=row[6]) for row in rows]

    def delete(self, **kwargs):
        if not self.id:
            return None
        with DB() as c:
            c.raw_sql("""DELETE FROM comment
                         WHERE id={0}""".format(self.id))

    def save(self):
        if self.id:
            with DB() as c:
                c.raw_sql("""UPDATE comment
                    SET surname='{surname}', firstname='{firstname}',
                    patronymic='{patronymic}', region_id={region},
                    city_id={city}, phone='{phone}', email='{email}',
                    comment='{comment}'
                    WHERE id='{id}'""".format(**self.as_dic()))
                return self
        else:
            with DB() as c:
                self.id = c.raw_sql("""INSERT INTO comment
                    VALUES (NULL, '{surname}', '{firstname}', '{patronymic}',
                        {region}, {city}, '{phone}', '{email}', '{comment}'
                    )""".format(**self.as_dic()))['lastid']
                return self

    def __fix_kwargs(self, not_fix_kwargs):
        fix_kwargs = {}
        for k, v in not_fix_kwargs.items():
            if "region" == k:
                fix_kwargs["ct."+k+"_id"] = v.id
            elif "city" == k:
                fix_kwargs["ct."+k+"_id"] = v.id
            else:
                fix_kwargs["ct."+k] = v
        return fix_kwargs

    def as_dic(self):
        return {
            'id': self.id,
            'surname': self.surname,
            'firstname': self.firstname,
            'patronymic': self.patronymic,
            'region': self.region.id,
            'city': self.city.id,
            'phone': self.phone,
            'email': self.email,
            'comment': self.comment,
        }


class Stat():

    def __init__(self, id=None, name=None, comments_count=None):
        self.id = id
        self.name = name
        self.comments_count = comments_count

    def get_list(self, region_id=None):
        """
        If region_id, then getting statistics table to all cities
        """
        if region_id:
            query = """SELECT ct.city_id, c.name, COUNT(ct.city_id) as comments
                       FROM comment ct
                    INNER JOIN region r ON ct.region_id = r.id AND r.id = {0}
                    INNER JOIN city c ON ct.city_id = c.id
                       GROUP BY ct.city_id
                       ORDER BY comments DESC, c.name ASC""".format(region_id)
        else:
            query = """SELECT ct.region_id, r.name,
                              COUNT(ct.region_id) as comments
                       FROM comment ct
                       INNER JOIN region r ON ct.region_id = r.id
                       GROUP BY region_id
                       HAVING comments >= 5
                       ORDER BY comments DESC, r.name ASC """
        with DB() as c:
            rows = c.raw_sql(query)['data']
            if not rows:
                return None
            return [Stat(id=row[0], name=row[1], comments_count=row[2]) for row in rows]

    def as_dic(self):
        return {
            'id': self.id,
            'name': self.name,
            'comments_count': self.comments_count,
        }
