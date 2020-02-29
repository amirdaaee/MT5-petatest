import yaml
import os
import subprocess
from random import randrange
from datetime import timedelta, datetime


# https://www.metatrader5.com/en/terminal/help/start_advanced/start
# ======================
def random_date(start, end, l1, l2):
    delta = end - start
    delta = delta.days
    r_ = randrange(delta)
    date1 = start + timedelta(days=r_)
    r_ = randrange(int(l1), int(l2))
    date2 = date1 + timedelta(days=r_)
    return date1, date2


# ======================
with open('./config.yml') as f:
    cfg = yaml.load(f, Loader=yaml.BaseLoader)
base_dir = cfg['system']['mt5_basedir']
terminal = cfg['system']['mt5_terminal']
metatester_dir = os.path.join(base_dir, 'metatester')
if not os.path.isdir(metatester_dir):
    os.mkdir(metatester_dir)
report_dir = os.path.join(metatester_dir, 'report/')
if not os.path.isdir(report_dir):
    os.mkdir(report_dir)
with open('./cfg-template') as f:
    cfg_template = f.read()
with open('./expert.setting') as f:
    expert_setting = f.read()
cfg_file = os.path.join(metatester_dir, 'start.ini')
run_cmd = f'"{terminal}" /config:"{cfg_file}"'
# ======================
for k_ in cfg['tester'].keys():
    v_ = cfg['tester'][k_]
    cfg_template = cfg_template.replace(f'#{k_}', v_)
cfg_template += '\n'
cfg_template += expert_setting
# ======================
lower_idate = datetime.strptime(cfg['run']['start_date_min'], '%Y.%m.%d')
upper_idate = datetime.strptime(cfg['run']['start_date_max'], '%Y.%m.%d')
lower_length = cfg['run']['duration_min']
upper_length = cfg['run']['duration_max']
# ======================
for n_ in range(int(cfg['run']['n_run'])):
    idate, edate = random_date(lower_idate, upper_idate, lower_length, upper_length)
    cfg_ = cfg_template.replace('#idate', idate.strftime('%Y.%m.%d'))
    cfg_ = cfg_.replace('#edate', edate.strftime('%Y.%m.%d'))
    test_name = f'test_' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    cfg_ = cfg_.replace('#Report', f'/metatester/report/{test_name}')
    with open(cfg_file, 'w') as f:
        f.write(cfg_)
    proc = subprocess.Popen(run_cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    _ = proc.communicate()

print('reports are available at:\n', report_dir)
