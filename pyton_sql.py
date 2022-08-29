
import psycopg2

conn = psycopg2.connect(database='employee', user="postgres", password="1")

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
	    user_number int4 NOT NULL,
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
        CONSTRAINT user_number_fk FOREIGN KEY (id_user) REFERENCES "users"(id_user),
        CONSTRAINT user_number_fk_1 FOREIGN KEY (id_number) REFERENCES "number"(id_number)
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
        return cur.fetchone()[0]
        
def get_id_number(user_number):
    with conn.cursor() as cur:
        cur.execute("""
        select id_number 
        from number
        where user_number=%s 
        """, (user_number,))
        return cur.fetchone()[0]
    
def add_client(name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO users (user_name, last_name, email) VALUES(%s, %s, %s);
        INSERT INTO "number" (user_number) VALUES(%s); 
        """, (name, last_name, email, phones))
        conn.commit()
    id_user = get_id_user(name, last_name)
    id_number = get_id_number(phones)
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO user_number (id_user, id_number) VALUES(%s, %s);
                    """,(id_user, id_number))
        conn.commit()
    

drop_db()
create_db(conn)
print(get_id_user('Ivan','Ivanov'))
print(get_id_number('123'))
add_client('Alex','Alexandrov', 'A@mail.ru', 987)

conn.close()




