
import psycopg2


def drop_db(cur):
        cur.execute("""
        --sql
       DROP TABLE number;
       DROP TABLE users;
        """)
        # conn.commit()


def create_db(cur):
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
        id_user serial4 NOT NULL,
	    user_name varchar NOT NULL,
	    last_name varchar NOT NULL,
	    email varchar NOT NULL,
	    CONSTRAINT user_pk PRIMARY KEY (id_user),
	    CONSTRAINT user_un UNIQUE (email)    
        );
        
        CREATE TABLE IF NOT EXISTS number(       
        id_number serial4 NOT NULL,
        user_number int4 NOT NULL,
        id_user int4 NOT NULL,
        CONSTRAINT number_pk PRIMARY KEY (id_number),
        CONSTRAINT number_un UNIQUE (user_number),
        CONSTRAINT number_fk FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE
        );
        INSERT INTO users (user_name, last_name, email) VALUES('Ivan', 'Ivanov', 'I@mail.ru');
        INSERT INTO users (user_name, last_name, email) VALUES('Petr', 'Petrov', 'P@mail.ru');
        INSERT INTO number (user_number, id_user) VALUES('123', '1'),('456', '1'),('789', '2');      
        """)
        # conn.commit()


def get_id_user(cur, user_name, last_name):
    cur.execute("""
    select id_user 
    from users
    where user_name = %s and last_name = %s
    """, (user_name, last_name))
    return cur.fetchone()


def get_id_number(cur, user_number):
    cur.execute("""
    select id_number 
    from number
    where user_number=%s 
    """, (user_number,))
    return cur.fetchone()


def add_client(cur, name, last_name, email, phones=None):
        cur.execute("""
        INSERT INTO users (user_name, last_name, email) VALUES(%s, %s, %s) RETURNING id_user;
        """, (name, last_name, email))
        id_user = cur.fetchone()[0]
        # conn.commit()
        if phones is not None:
            # id_user = get_id_user(name, last_name)
            with conn.cursor() as cur:
                cur.execute("""       
                INSERT INTO "number" (user_number, id_user) VALUES(%s ,%s); 
                """, (phones, id_user))




def add_number(cur, user_name, last_name, number):
    id_user = get_id_user(cur, user_name, last_name)
    if id_user is not None:
        cur.execute("""
        INSERT INTO "number" (user_number, id_user) VALUES(%s, %s); 
        """, (number, id_user))
        conn.commit()
        print('+')
    else:
        print('Нет такого пользователя')


# def change_user(cur, id_user, user_name=None, last_name=None, email=None, user_number=None):
#     if user_name is not None:
#         change_user_name(cur, id_user, user_name)
#     if last_name is not None:
#         change_last_name(cur, id_user, last_name)
#     if email is not None:
#         change_email(cur, id_user, email)
#     if user_number is not None:
#         change_user_number(cur, id_user, user_number)

def change_user(cur, id_user, user_number=None, **kwargs):
    for key, values in kwargs.items():
        cur.execute("""
        UPDATE users SET %s='%s' WHERE id_user=%s;
        """ % (key, values, id_user))
    if user_number is not None:
        change_user_number(cur, id_user, user_number)


def change_user_name(cur, id_user, user_name):
    cur.execute("""
    UPDATE users SET user_name=%s WHERE id_user=%s;
    """, (user_name, id_user))
    conn.commit()


def change_last_name(cur, id_user, last_name):
    cur.execute("""
    UPDATE users SET last_name=%s WHERE id_user=%s;
    """, (last_name, id_user))
    conn.commit()


def change_email(cur, id_user, email):
    cur.execute("""
    UPDATE users SET email=%s WHERE id_user=%s;
    """, (email, id_user))


def change_user_number(cur, id_user, user_number):
    id_numbers = get_all_id_number(cur, id_user)
    if len(id_numbers) == 0:
        print('У пользователя нет номеров')
    elif len(id_numbers) == 1:
        cur.execute("""
        UPDATE number SET user_number=%s WHERE id_number=%s;
        """, (user_number, id_numbers[0][0]))
    else:
        print('номер с каким ID заменить')
        id_number = int(input (f'{id_numbers}: '))
        for id in id_numbers:
            if id_number == id[0]:
                cur.execute("""
                UPDATE number SET user_number=%s WHERE id_number=%s;
                """, (user_number, id_number))
                return
        print('ID_number Error')


def get_all_id_number(cur, id_user):
    cur.execute("""
    select n.id_number , n.user_number
    from number n
    where n.id_user = %s
    """, (id_user))
    return cur.fetchall()

def del_number(cur, id_user):
    id_numbers = get_all_id_number(cur, id_user)
    if len(id_numbers) == 0:
        print('У пользователя нет номеров')
    elif len(id_numbers) == 1:
        cur.execute("""
        DELETE FROM number WHERE id_user=%s;
        """, (id_user,))
        print('единственный номер удалён')
    else:
        print('номер с каким ID удалить?')
        id_number = int(input (f'{id_numbers}: '))
        for id in id_numbers:
            if id_number == id[0]:
                cur.execute("""
                DELETE FROM number WHERE id_number=%s;
                """, (id_number,))
                conn.commit()
                print('Номер удалён')
                return
        print('ID_number Error')


def del_user(cur, id_user):
    cur.execute("""
    DELETE FROM users WHERE id_user=%s;
    """, (id_user,))


def find_id_user(cur, user_name=None, last_name=None, email=None, user_number=None):
    select_id = set()
    check = False
    if user_name is not None:
        cur.execute("""
        select id_user
        from users
        where user_name = %s
        """, (user_name,))
        a = {i[0] for i in cur.fetchall()}
        if check:
            select_id = select_id & a
        else:
            select_id = a
            check = True

    if last_name is not None:
        cur.execute("""
        select id_user
        from users
        where last_name = %s
        """, (last_name,))
        a = {i[0] for i in cur.fetchall()}
        if check:
            select_id = select_id & a
        else:
            select_id = a
            check = True

    if email is not None:
        cur.execute("""
        select id_user
        from users
        where email = %s
        """, (email,))
        a = {i[0] for i in cur.fetchall()}
        if check:
            select_id = select_id & a
        else:
            select_id = a
            check = True
    if user_number is not None:
        cur.execute("""
        select id_user
        from number
        where user_number = %s
        """, (user_number,))
        a = {i[0] for i in cur.fetchall()}
        if check:
            select_id = select_id & a
        else:
            select_id = a
    return select_id



if __name__ == '__main__':
    with psycopg2.connect(database='employee', user="postgres", password="1") as conn:
        with conn.cursor() as cur:
            drop_db(cur)
            create_db(cur)
            add_client(cur, 'Alex', 'Alexandrov', 'A@mail.ru', '987')
            add_client(cur, 'Alex', 'Alexandrov', '22@mail.ru', '555')
            add_client(cur, 'Bob', 'Bobovich', 'B@mail.ru')
            add_number(cur, 'Ivan', 'Ivanov', '753')
            change_user(cur, id_user='1', user_name='Ivan2', last_name='ivanov2', user_number='999')
            print(get_all_id_number(cur, '1'))
            # del_number(cur, id_user='1')
            # print(get_all_id_number(cur, '1'))
            # del_user(cur, id_user='1')
            # print(find_id_user(cur, user_name='Alex', last_name='Alexandrov', email='22@mail.ru', user_number='555'))
            # conn.close()
