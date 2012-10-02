import os
from django.core.management.base import CommandError
from tempfile import mkstemp
from subprocess import check_call
from shutil import copy

def backup(database, outfile):
    engine = database['ENGINE']
    if 'mysql' in engine:
        __mysql_backup(database, outfile)
    elif engine in ('postgresql_psycopg2', 'postgresql') or 'postgresql' in engine:
        __postgresql_backup(database, outfile)
    elif 'sqlite3' in engine:
        __sqlite_backup(database, outfile)
    else:
        raise CommandError('Backup in %s engine not implemented' % engine)

def __sqlite_backup(database, outfile):
    copy(database['NAME'], outfile)

def __mysql_backup(database, outfile):
    command = ['mysqldump']
    if 'USER' in database:
        command += ["--user=%s" % database['USER']]
    if 'PASSWORD' in database:
        command += ["--password=%s" % database['PASSWORD']]
    if 'HOST' in database:
        command += ["--host=%s" % database['HOST']]
    if 'PORT' in database:
        command += ["--port=%s" % database['PORT']]
    command += [database['NAME']]
    
    with open(outfile, 'w') as f:
        check_call(command, stdout=f)

def __postgresql_backup(database, outfile):
    command = ['pg_dump', '-Ox']
    if 'USER' in database:
        command += ["--username=%s" % database['USER']]
    if 'HOST' in database:
        command += ["--host=%s" % database['HOST']]
    if 'PORT' in database:
        command += ["--port=%s" % database['PORT']]
    if 'NAME' in database:
        command += [database['NAME']]
    
    if 'PASSWORD' in database:
        # create a pgpass file that always returns the same password, as a secure temp file
        password_fd, password_path = mkstemp()
        password_file = os.fdopen(password_fd, 'w')
        password_file.write('*:*:*:*:{}'.format(database['PASSWORD']))
        password_file.close()
        os.environ['PGPASSFILE'] = password_path
    else:
        command.append('-w')
    
    with open(outfile, 'w') as f:
        check_call(command, stdout=f)
        
    # clean up
    if password_path:
        os.remove(password_path)