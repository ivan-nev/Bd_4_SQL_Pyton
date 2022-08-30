from ast import Not
import psycopg2


def drop_db():
    with conn.cursor() as cur:
        cur.execute("""
        --sql
        DROP TABLE user_number;
        DROP TABLE users;
        DROP TABLE number;
        """)
        conn.commit()


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        --sql       
        CREATE TABLE IF NOT EXISTS "number" (
	    id_number serial4 NOT NULL,
	    user_number varchar NOT NULL,
	    CONSTRAINT number_pk PRIMARY KEY (id_number)
        );
        --sql
        CREATE TABLE IF NOT EXISTS "users" (
        id_user serial4 NOT NULL,
	    user_name varchar NOT NULL,
	    last_name varchar NOT NULL,
	    email varchar NOT NULL,
	    CONSTRAINT user_pk PRIMARY KEY (id_user)    
        );
        --sql        
        
        CREATE TABLE IF NOT EXISTS user_number (
        id_user int4 NOT NULL,
        id_number int4 NOT NULL,
        CONSTRAINT user_number_pk PRIMARY KEY (id_user, id_number),
        CONSTRAINT user_number_fk FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE,
        CONSTRAINT user_number_fk_1 FOREIGN KEY (id_number) REFERENCES "number"(id_number) ON DELETE CASCADE
        );
        INSERT INTO users (user_name, last_name, email) VALUES('Ivan', 'Ivanov', 'I@mail.ru');
        INSERT INTO users (user_name, last_name, email) VALUES('Petr', 'Petrov', 'P@mail.ru');
        INSERT INTO "number" (user_number) VALUES('123');
        INSERT INTO "number" (user_number) VALUES('456');
        INSERT INTO "number" (user_number) VALUES('789');
        INSERT INTO user_number (id_user, id_number) VALUES(1, 1);
        INSERT INTO user_number (id_user, id_number) VALUES(1, 2);
        INSERT INTO user_number (id_user, id_number) VALUES(2, 3);
        """)
        conn.commit()


def get_id_user(user_name, last_name):
    with conn.cursor() as cur:
        cur.execute("""
        select id_user 
        from users
        where user_name = %s and last_name = %s
        """, (user_name, last_name))
        return cur.fetchone()


def get_id_number(user_number):
    with conn.cursor() as cur:
        cur.execute("""
        select id_number 
        from number
        where user_number=%s 
        """, (user_number,))
        return cur.fetchone()


def add_client(name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO users (user_name, last_name, email) VALUES(%s, %s, %s);
        """, (name, last_name, email))
        conn.commit()
    if phones is not None:
        with conn.cursor() as cur:
            cur.execute("""       
            INSERT INTO "number" (user_number) VALUES(%s); 
            """, (phones,))
            conn.commit()
        id_user = get_id_user(name, last_name)[0]
        id_number = get_id_number(phones)[0]
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO user_number (id_user, id_number) VALUES(%s, %s);
                        """, (id_user, id_number))
            conn.commit()


def add_number(user_name, last_name, number):
    id_user = get_id_user(user_name, last_name)
    if id_user is not None:
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO "number" (user_number) VALUES(%s); 
            """, (number,))
            conn.commit()
        id_number = get_id_number(number)
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO user_number (id_user, id_number) VALUES(%s, %s);
            """, (id_user[0], id_number[0]))
            conn.commit()
        print('+')
    else:
        print('Нет такого пользователя')


def change_user(id_user, user_name=None, last_name=None, email=None, user_number=None):
    if user_name is not None:
        change_user_name(id_user, user_name)
    if last_name is not None:
        change_last_name(id_user, last_name)
    if email is not None:
        change_email(id_user, email)
    if user_number is not None:
        change_user_number(id_user, user_number)


def change_user_name(id_user, user_name):
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE users SET user_name=%s WHERE id_user=%s;
        """, (user_name, id_user))
        conn.commit()


def change_last_name(id_user, last_name):
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE users SET last_name=%s WHERE id_user=%s;
        """, (last_name, id_user))
        conn.commit()


def change_email(id_user, email):
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE users SET email=%s WHERE id_user=%s;
        """, (email, id_user))
        conn.commit()

def change_user_number(id_user, user_number):

    with conn.cursor() as cur:
        cur.execute("""
        UPDATE users SET email=%s WHERE id_user=%s;
        """, (email, id_user))
        conn.commit()

def get_all_id_number(id_user):
    with conn.cursor() as cur:
        cur.execute("""
        select n.id_number , n.user_number
        from number n
        left join user_number un on n.id_number = un.id_number
        where un.id_user = %s
        """, (id_user))
        return cur.fetchall()


if __name__ == '__main__':
    conn = psycopg2.connect(database='employee', user="postgres", password="1")
    drop_db()
    create_db(conn)
    print(get_id_user('Ivan', 'Ivanov'))
    print(get_id_number('123'))
    add_client('Alex', 'Alexandrov', 'A@mail.ru', '987')
    add_client('Bob', 'Bobovich', 'B@mail.ru')
    add_number('Ivan', 'Ivanov', '753')
    change_user('1', user_name='Ivan2', last_name='ivanov2', email='@@', user_number=None)
    print(get_all_id_number('1'))

    conn.close()
