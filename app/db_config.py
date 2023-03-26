from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()   # create a parser
    parser.read(filename)   # read the config file

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            "Section {} not found in the {} file.".format(
                section, filename))
    return db


if __name__ == '__main__':
    print(config())

    # 若是外部使用此函数
    # import db_config
    # params = config(filename, section)
    # connection = psycopg2.connect(**params)
