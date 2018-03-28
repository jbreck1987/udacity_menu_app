from database_setup import Restaurant, create_db_session


def main():

    session = create_db_session()

    q = session.query(Restaurant.name).all()

    print(q)


if __name__ == '__main__':
    main()
