import os
from fabric.contrib.files import append, exists, upload_template
from fabric.context_managers import settings
from fabric.api import cd, env, run, sudo


DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWD = os.getenv('DB_PASSWD')
URL_REPO = 'https://github.com/paganism/37_transcendence_1.git'
PROJECT_NAME = os.getenv('PROJECT_NAME')
PROJECT_PATH = os.getenv('PROJECT_PATH')
PROJECT_ROOT = os.path.join(PROJECT_PATH, PROJECT_NAME)
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
DB_URI = os.getenv('DJANGO_DB_URI')
DJANGO_SU_PASSWD = os.getenv('DJANGO_SU_PASSWD')
DOMAIN = os.getenv('DOMAIN')
VENV_DIR = os.path.join(PROJECT_PATH, '.venv')


def install_system_packeges():
    sudo('apt -y install nginx postgres git python3-venv')


def create_db():
    with settings(warn_only=True):
        sudo('su - postgres psql -c "createdb %s"' % DB_NAME)


def create_or_update_proj_directory():
    if not exists(PROJECT_ROOT, use_sudo=True):
        run('mkdir -p %s' % PROJECT_ROOT)
        with cd(PROJECT_PATH):
            run('git clone %s' % URL_REPO)
    else:
        with cd(PROJECT_PATH):
            run('git pull')


def change_postgres_user_password():
    create_user_command = "create user %s with password %s;" % (DB_USER, DB_PASSWD)
    create_db_command = "create database %s owner %s;" % (DB_NAME, DB_USER)
    sudo('sudo -u postgres psql -c "%s"' % create_user_command)
    sudo('sudo -u postgres psql -c "%s"' % create_db_command)


def create_and_activate_venv():
    with cd('PROJECT_PATH'):
        if not exists(VENV_DIR):
            run('virtualenv-3 -p /usr/bin/python3 .venv')
        run('source .venv/bin/activate')


def install_requirements():
    with cd('PROJECT_PATH'):
        run('pip install -r requirements.txt')


def create_django_su(new_instance=False):
    with cd('PROJECT_PATH'):
        if new_instance:
            with settings(prompts={'Django superuser password: ': DJANGO_SU_PASSWD,
                                   'Django superuser password(again)': DJANGO_SU_PASSWD}):
                run('python3 manage.py createsuperuser --username admin --email admin@%s' % DOMAIN)


def django_collect_static():
    run('python3 manage.py collectstatic --no-input')


def django_migrate():
    with cd(PROJECT_PATH):
        run('manage.py migrate --noinput')
        run('manage.py collectstatic --noinput')


def install_nginx_project_conf():
    dest_path = '/etc/nginx/sites-available/%s.conf' % PROJECT_NAME
    context = {
        'DOMAIN': '%s' % DOMAIN,
        'BASE_DIR': '%s' % PROJECT_ROOT,
        'PROJECT_NAME': '%s' % PROJECT_NAME
    }
    upload_template(
        'nginx.conf',
        dest_path,
        context=context,
        template_dir='linux_server_templates',
        use_jinja=True
    )
    run('ln -s /etc/nginx/sites-available/%s.conf /etc/nginx/sites-enabled/' % PROJECT_NAME)  # noqa
    run('systemctl restart nginx.service')


def create_systemd_service():
    dest_path = '/etc/systemd/system/%s.service' % PROJECT_NAME
    context = {
        'PROJECT_NAME': '%s' % PROJECT_NAME,
        'VENV_DIR': '%s' % VENV_DIR,
        'PROJECT_ROOT': '%s' % PROJECT_ROOT,
        'DB_URI': '%s' % DB_URI,
        'SECRET_KEY': '%s' % SECRET_KEY
    }
    upload_template(
        'systemd.service',
        dest_path,
        context=context,
        template_dir='server_templates',
        use_jinja=True
    )
run('systemctl enable --now {PROJECT_NAME}.service'.format(**env))


def new_installation():
    install_system_packeges()
    create_or_update_proj_directory()
    create_and_activate_venv()
    install_requirements()
    create_db()
    create_django_su(new_instance=True)
    install_nginx_project_conf()


def bootstrap():
    if exists(PROJECT_ROOT):
        create_or_update_proj_directory()
        django_migrate()
        django_collect_static()
        run('systemctl restart %s.service' % PROJECT_NAME)
    else:
        new_installation()