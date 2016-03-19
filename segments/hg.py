import os
import subprocess

def get_hg_status():
    has_modified_files = False
    has_untracked_files = False
    has_missing_files = False

    p = subprocess.Popen(['hg', 'status'], stdout=subprocess.PIPE)
    output = p.communicate()[0].decode("utf-8")

    for line in output.split('\n'):
        if line == '':
            continue
        elif line[0] == '?':
            has_untracked_files = True
        elif line[0] == '!':
            has_missing_files = True
        else:
            has_modified_files = True
    return has_modified_files, has_untracked_files, has_missing_files

def get_mq_patch():
    NO_PATCHES="no patches applied"
    p = subprocess.Popen(['hg', 'qtop'], stdout=subprocess.PIPE)
    stdout = p.communicate()[0].decode('utf-8')

    patch_applied = NO_PATCHES
    for line in stdout.split('\n'):
        l = line.rstrip()
        if l != '':
            patch_applied = l
            break

    if patch_applied == NO_PATCHES:
        return ''
    else:
        return patch_applied

def add_hg_segment(powerline):
    branch = os.popen('hg branch 2> /dev/null').read().rstrip()
    if len(branch) == 0:
        return False

    extra = ''
    bg = Color.REPO_CLEAN_BG
    fg = Color.REPO_CLEAN_FG

    has_mq_patch = get_mq_patch()
    if has_mq_patch:
        extra += '[%s]' % has_mq_patch

    has_modified_files, has_untracked_files, has_missing_files = get_hg_status()
    if has_modified_files or has_untracked_files or has_missing_files:
        bg = Color.REPO_DIRTY_BG
        fg = Color.REPO_DIRTY_FG
        if has_untracked_files:
            extra += ' +'
        if has_missing_files:
            extra += ' !'

    branch += (' ' + extra if extra != '' else '')
    return powerline.append('%s ' % branch, fg, bg)
