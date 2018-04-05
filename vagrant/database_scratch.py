from database_setup import Restaurant, create_db_session


def main():

    session = create_db_session()

    # new_rest = Restaurant(name='testy test')

    # session.add(new_rest)

    q = session.query(Restaurant).filter_by(name='test').first()

    print(q.name)
    session.close()


if __name__ == '__main__':
    main()
