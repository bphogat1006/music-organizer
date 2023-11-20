import os
import pymysql

connection = pymysql.connect(host=os.environ['MARIADB_HOST'],
                             user=os.environ['MARIADB_USER'],
                             password=os.environ['MARIADB_PASSWORD'],
                             database=os.environ['DATABASE'],
                             cursorclass=pymysql.cursors.DictCursor,
                             autocommit=True)

def convertNullToEmptyString(data: dict):
    for key in data.keys():
        if data[key] is None:
            data[key] = ''
    return data

class ListeningDB:
    def __init__(self) -> None:
        pass

    def getEntries(self):
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM `listening`')
            return cursor.fetchall()

class LearningDB:
    def __init__(self) -> None:
        pass

    def updateLastViewed(self, id):
        with connection.cursor() as cursor:
            cursor.execute('UPDATE `learning` SET `last_viewed` = CURRENT_TIMESTAMP WHERE `id` = %s;', [id])

    def getFormattedTable(self):
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM `learning`')
            entries = cursor.fetchall()
        # format entries for table
        for entry in entries:
            # format backlog attribute
            entry['backlog'] = 'yes' if entry['backlog'] else 'no'
            # format rest of columns
            entry = convertNullToEmptyString(entry)
            # join and format links
            entry['links'] = []
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM `learning_links` WHERE `learning_id`=%s;', [entry['id']])
                links = cursor.fetchall()
                for link in links:
                    html = None
                    if link['url'] is None or link['url'] == '':
                        html = link['type']
                    else:
                        html = f'<a target="_blank" href="{link["url"]}">{link["type"]}</a>'
                    html = '<strong>'+html+'</strong>'
                    if link['description'] is not None and link['description'] != '':
                        html += ' - ' + link['description']
                    entry['links'].append(html)
        return entries

    # Learning entries
    
    def getEntry(self, id):
        # get entry
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM `learning` WHERE `id`=%s', [id])
            entry = cursor.fetchone()
            entry = convertNullToEmptyString(entry)
        # get links associated with entry
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM `learning_links` WHERE `learning_id`=%s;', [id])
            links = cursor.fetchall()
            for i in range(len(links)):
                links[i] = convertNullToEmptyString(links[i])
        return entry, links

    def updateEntry(self, artist, album, track, instrument, reason, backlog, id):
        with connection.cursor() as cursor:
            cursor.execute(
                'UPDATE `learning` SET `artist`=%s, `album`=%s, `track`=%s, `instrument`=%s, `reason`=%s, `backlog`=%s WHERE `id`=%s',
                [artist, album, track, instrument, reason, backlog, id]
            )

    def insertEntry(self, artist, album, track, instrument, reason, backlog):
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO `learning` (`artist`, `album`, `track`, `instrument`, `reason`, `backlog`) VALUES (%s, %s, %s, %s, %s, %s)',
                [artist, album, track, instrument, reason, backlog]
            )

    def deleteEntry(self, id):
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM `learning_links` WHERE `learning_id`=%s', [id])
            cursor.execute('DELETE FROM `learning` WHERE `id`=%s', [id])

    # Learning entry links
    
    def getLink(self, id):
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM `learning_links` WHERE `id`=%s;', [id])
            link = cursor.fetchone()
            link = convertNullToEmptyString(link)
            return link

    def updateLink(self, type, url, description, id):
        with connection.cursor() as cursor:
            cursor.execute(
                'UPDATE `learning_links` SET `type`=%s, `url`=%s, `description`=%s WHERE `id`=%s',
                [type, url, description, id]
            )

    def insertLink(self, type, url, description, learning_id):
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO `learning_links` (`url`, `type`, `description`, `learning_id`) VALUES (%s, %s, %s, %s)',
                [url, type, description, learning_id]
            )

    def deleteLink(self, id):
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM `learning_links` WHERE `id`=%s', [id])
