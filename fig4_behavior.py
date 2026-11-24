# MED arrays: K = trial starts, B/C = left choice times (unrewarded/rewarded), D/E = right choice
# times (unrewarded/rewarded), N = block start times, O = high prob side of each block (0 right,
# 1 left), P = choice (0 right, 1 left), R = reward, Q = MED's copy of O for each trial, M = rewards per block
# FR1 programs leave N/O/P/Q/R at 0 so choice/reward come from B/C/D/E there
# MED pads arrays with 0s, and the last trial start usually has no choice (session timed out)

import argparse
import json
import os
import re
from datetime import datetime

import numpy as np
import pandas as pd

msnToStage = {
    'JN_ASAP_B_FR1_BOTH': 'FR1 both sides',
    'JN_ASAP_C_FR1_LEFT': 'FR1 single side',
    'JN_ASAP_C_FR1_RIGHT': 'FR1 single side',
    'JN_ASAP_D_100_0_40RewardsSwitch': '100/0',
    'JN_ASAP_F_90_10_50RewardsSwitch': '90/10',
    'JN_ASAP_G_75_25_50RewardsSwitch': '75/25',
}
stageOrder = ['FR1 both sides', 'FR1 single side', '100/0', '90/10', '75/25']
countedStages = stageOrder[:4]  # 75/25 isn't in the figure
reversalStages = ['100/0', '90/10', '75/25']
litSide = {'JN_ASAP_C_FR1_LEFT': 1, 'JN_ASAP_C_FR1_RIGHT': 0}
groups = ['asyn', 'control']

# rows of days_per_stage.csv. FR1 in the figure is FR1 both sides (phase 2)
daysRows = {'FR1': 'FR1 both sides', '100/0': '100/0', '90/10': '90/10'}

switchStages = ['100/0', '90/10']
trialsToSee = 25

# panel F
sampleMouse = '575-14335'
sampleDate = '2023-08-04'

# choice time arrays -> (choice, reward)
choiceArrays = {'E': (0, 1), 'D': (0, 0), 'C': (1, 1), 'B': (1, 0)}

trialCols = ['trial', 'start_index', 'start_time', 'response_time', 'choice', 'reward',
             'block', 'block_side', 'block_trial', 'stage']

# MED line types: header (Subject: ...), single value (M: 40), array name (K:), array row (     0:  1.2  3.4 ...)
headerLine = re.compile(r'^([A-Za-z][A-Za-z ]+):\s?(.*)$')
scalarLine = re.compile(r'^([A-Z]):\s+(-?\d+(?:\.\d+)?)\s*$')
arrayStart = re.compile(r'^([A-Z]):\s*$')
arrayRow = re.compile(r'^\s+(\d+):((?:\s+-?\d+(?:\.\d+)?)+)\s*$')


#%% load the MED files

def readMedFile(path):
    # one MED file can have more than one session in it
    sessions = []
    ses = None
    letter = None
    with open(path, 'r', encoding='latin-1') as f:
        lines = f.read().splitlines()
    for line in lines:
        if not line.strip():
            letter = None
            continue
        if line.startswith('Start Date:'):
            ses = {'file': os.path.basename(path), 'sesNum': len(sessions), 'header': {}, 'arrays': {}}
            sessions.append(ses)
            letter = None
        if ses is None:
            continue

        row = arrayRow.match(line)
        if row and letter is not None:
            ses['arrays'][letter] += [float(v) for v in row.group(2).split()]
        elif arrayStart.match(line):
            letter = line[0]
            ses['arrays'][letter] = []
        elif scalarLine.match(line):
            letter = None
            ses['arrays'][line[0]] = [float(scalarLine.match(line).group(2))]
        else:
            m = headerLine.match(line)
            if m and len(m.group(1).strip()) > 1:
                letter = None
                ses['header'][m.group(1).strip()] = m.group(2).strip()

    for ses in sessions:
        ses['arrays'] = {k: np.array(v, dtype=float) for k, v in ses['arrays'].items()}
    return sessions


def getTrials(ses):
    # one row per completed trial = a trial start with a choice before the next trial start
    arrays = ses['arrays']
    msn = ses['header'].get('MSN', '')
    stage = msnToStage.get(msn, 'other')

    starts = arrays.get('K', np.zeros(0))
    starts = starts[starts != 0]
    assert np.all(np.diff(starts) > 0), ses['file']

    # every choice time in order, then match each one to the last trial start before it
    resp = []
    for letter, (choice, reward) in choiceArrays.items():
        t = arrays.get(letter, np.zeros(0))
        resp.append(pd.DataFrame({'time': t[t != 0], 'choice': choice, 'reward': reward}))
    resp = pd.concat(resp, ignore_index=True).sort_values('time', kind='mergesort')
    resp['start_index'] = np.searchsorted(starts, resp['time'].to_numpy(), side='right') - 1
    # only the first choice after each trial start counts
    resp = resp[resp['start_index'] >= 0].drop_duplicates('start_index').set_index('start_index')
    idx = np.sort(resp.index.to_numpy()).astype(np.int64)

    trials = pd.DataFrame({'start_index': idx, 'start_time': starts[idx],
                           'response_time': resp.loc[idx, 'time'].to_numpy()})

    if stage in reversalStages:
        trials['choice'] = arrays['P'][idx].astype(np.int64)
        trials['reward'] = arrays['R'][idx].astype(np.int64)
        # block = last block start (N) at or before the trial start
        blockStarts = np.trim_zeros(arrays['N'], 'b')
        block = np.searchsorted(blockStarts, trials['start_time'].to_numpy(), side='right') - 1
        assert (block >= 0).all(), ses['file']
        trials['block'] = block.astype(np.int64)
        trials['block_side'] = arrays['O'][block]
        rewPerBlock = float(arrays['M'][0])

        # P/R should match the choice times and Q should match O
        nOff = ((trials['choice'].to_numpy() != resp.loc[idx, 'choice'].to_numpy()).sum()
                + (trials['reward'].to_numpy() != resp.loc[idx, 'reward'].to_numpy()).sum()
                + (arrays['Q'][idx] != trials['block_side'].to_numpy()).sum())
        if nOff:
            print(f"{ses['file']}: P/R/Q don't match the choice times in {nOff} places")
    else:
        # FR1: one block, block_side = lit port (NaN in FR1 both sides)
        trials['choice'] = resp.loc[idx, 'choice'].to_numpy().astype(np.int64)
        trials['reward'] = resp.loc[idx, 'reward'].to_numpy().astype(np.int64)
        trials['block'] = np.zeros(len(trials), dtype=np.int64)
        trials['block_side'] = np.full(len(trials), float(litSide.get(msn, np.nan)))
        rewPerBlock = np.nan

    trials['trial'] = np.arange(1, len(trials) + 1, dtype=np.int64)
    trials['block_trial'] = (trials.groupby('block').cumcount() + 1).astype(np.int64)
    trials['stage'] = stage
    return trials[trialCols].reset_index(drop=True), len(starts), rewPerBlock


def loadSessions(rawDir, mouseInfo):
    rows = []
    notInMouseInfo = {}
    for fileName in sorted(os.listdir(rawDir)):
        path = os.path.join(rawDir, fileName)
        if not os.path.isfile(path):
            continue
        for ses in readMedFile(path):
            h = ses['header']
            if 'MSN' not in h or 'Subject' not in h:
                continue
            mouse = h['Subject']
            # IDs have to match mouse_info exactly as written
            if mouse not in mouseInfo:
                notInMouseInfo[mouse] = notInMouseInfo.get(mouse, 0) + 1
                continue
            trials, nStarts, rewPerBlock = getTrials(ses)
            start = datetime.strptime(h['Start Date'] + ' ' + h.get('Start Time', '00:00:00'),
                                      '%m/%d/%y %H:%M:%S')
            rows.append({'mouse': mouse, 'group': mouseInfo[mouse].get('group'),
                         'sex': mouseInfo[mouse].get('sex'), 'date': start.strftime('%Y-%m-%d'),
                         'start_time': h.get('Start Time'), 'start': start, 'msn': h['MSN'],
                         'stage': msnToStage.get(h['MSN'], 'other'), 'experiment': h.get('Experiment'),
                         'file': ses['file'], 'sesNum': ses['sesNum'], 'nStarts': nStarts,
                         'rewPerBlock': rewPerBlock, 'trials': trials})

    sessions = pd.DataFrame(rows)
    sessions = sessions.sort_values(['start', 'mouse', 'file', 'sesNum'], kind='mergesort').reset_index(drop=True)
    print(f"{len(sessions)} sessions for {sessions['mouse'].nunique()} of the {len(mouseInfo)} mice in mouse_info")
    if notInMouseInfo:
        print('not in mouse_info (skipped): ' + ', '.join(f'{m} ({n})' for m, n in sorted(notInMouseInfo.items())))
    return sessions


def mouseOrder(mouseInfo):
    # asyn first then control, each in mouse_info order
    order = [m for g in groups for m, info in mouseInfo.items() if info.get('group') == g]
    assert len(order) == len(mouseInfo), 'every mouse needs group asyn or control'
    return order


#%% days per stage (C, E)

def experimentNumber(text):
    # the Experiment field is the day number typed in at the box (NaN if blank or not a whole number)
    try:
        value = float(str(text).strip())
    except ValueError:
        return np.nan
    if not np.isfinite(value) or value != int(value):
        return np.nan
    return value


def trainingDays(sessions):
    # one row per session (one session = one day), in date order for each mouse
    rows = []
    for _, s in sessions.iterrows():
        t = s['trials']
        nRew = int(t['reward'].sum())
        pctCorrect = np.nan
        if s['stage'] in reversalStages and len(t):
            # picked the high prob port (same as % rewarded in 100/0)
            pctCorrect = 100.0 * (t['choice'] == t['block_side']).mean()
        rows.append({'mouse': s['mouse'], 'group': s['group'], 'sex': s['sex'],
                     'date': s['date'], 'start_time': s['start_time'], 'stage': s['stage'],
                     'msn': s['msn'], 'experiment': s['experiment'],
                     'n_trials': len(t), 'n_rewards': nRew,
                     'pct_rewarded': 100.0 * nRew / len(t) if len(t) else np.nan,
                     'pct_correct': pctCorrect, 'n_blocks': t['block'].nunique(),
                     'rewards_per_block': s['rewPerBlock'], 'file': s['file']})
    days = pd.DataFrame(rows)
    assert days['stage'].isin(stageOrder).all(), 'MSN not in msnToStage'
    days = days.sort_values(['mouse', 'date', 'start_time'], kind='mergesort').reset_index(drop=True)
    days['experiment_number'] = days['experiment'].map(experimentNumber)

    days['day_overall'] = days.groupby('mouse').cumcount() + 1
    # a run = days in a row on the same stage
    newRun = days['stage'] != days.groupby('mouse')['stage'].shift()
    days['run'] = newRun.astype(int).groupby(days['mouse']).cumsum()
    # the main run of a stage is the last one before the mouse moves on to a later stage
    # (only 575-14334 has more than one, it went back to FR1 in the middle of 100/0)
    days['main_run'] = False
    for _, g in days.groupby('mouse', sort=False):
        for stage, gs in g.groupby('stage', sort=False):
            later = g.loc[g['stage'].map(stageOrder.index) > stageOrder.index(stage), 'day_overall']
            firstLater = later.min() if len(later) else np.inf
            runs = gs.loc[gs['day_overall'] < firstLater, 'run']
            mainRun = runs.max() if len(runs) else gs['run'].max()
            days.loc[gs.index[gs['run'] == mainRun], 'main_run'] = True
    main = days['main_run']
    days['day_in_stage'] = ((days[main].groupby(['mouse', 'stage']).cumcount() + 1)
                            .reindex(days.index).astype(float))
    cols = ['mouse', 'group', 'sex', 'day_overall', 'date', 'start_time', 'stage', 'msn',
            'experiment', 'main_run', 'day_in_stage', 'n_trials', 'n_rewards', 'pct_rewarded',
            'pct_correct', 'n_blocks', 'rewards_per_block', 'file']
    return days[cols + ['experiment_number', 'run']]


def runDays(days, mouse, stage):
    # main run of a stage day by day (None = day with no file)
    # skipped Experiment numbers only count as days if there's room for them (other mice ran those days)
    mine = days[days['mouse'] == mouse]
    run = mine[mine['main_run'] & (mine['stage'] == stage)]
    notes = []
    if not len(run):
        return [], notes
    exp = run['experiment_number'].to_numpy()
    inOrder = (not np.isnan(exp).any()) and exp[0] >= 1 and bool(np.all(np.diff(exp) > 0))
    if not inOrder:
        typed = ','.join(str(x) if str(x).strip() else '?' for x in run['experiment'])
        notes.append(f'Experiment numbers missing or not in order ({typed}); counted the files')
        return list(run.index), notes

    labDays = set(days['date'])
    mouseDays = set(mine['date'])
    before = mine[mine['day_overall'] < run['day_overall'].min()]
    prev = before.iloc[-1] if len(before) else None  # the mouse's last file before the run
    prevNum = 0
    slots = []
    for idx, num in zip(run.index, exp.astype(int)):
        date = days.at[idx, 'date']
        gap = num - prevNum - 1
        if gap > 0:
            missing = f'{prevNum + 1}' if gap == 1 else f'{prevNum + 1}-{num - 1}'
            if prev is None:
                free = gap
                notes.append(f'Experiment {missing} has no file (before the first file in the folder)')
            else:
                free = sum(1 for d in labDays if prev['date'] < d < date and d not in mouseDays)
                if free >= gap:
                    notes.append(f'Experiment {missing} has no file ({prev["date"]} to {date})')
                else:
                    notes.append(f'Experiment {missing} missing but only {free} free day(s) between '
                                 f'{prev["date"]} ({prev["stage"]} exp {prev["experiment"]}) and {date}; '
                                 f'{gap - free} not counted')
            slots += [None] * min(gap, free)
        slots.append(idx)
        prevNum, prev = num, days.loc[idx]
    return slots, notes


def daysPerStage(days):
    # days_all also counts sessions outside the main run
    rows = []
    mice = days[['mouse', 'group', 'sex']].drop_duplicates('mouse')
    for _, m in mice.iterrows():
        g = days[days['mouse'] == m['mouse']]
        for stage in countedStages:
            gs = g[g['stage'] == stage]
            gm = gs[gs['main_run']]
            row = {'mouse': m['mouse'], 'group': m['group'], 'sex': m['sex'], 'stage': stage}
            if not len(gs):
                row['note'] = 'no sessions in this stage'
                rows.append(row)
                continue
            slots, notes = runDays(days, m['mouse'], stage)
            other = gs[~gs['main_run']]
            if len(other):
                notes.append(f'{len(other)} other session(s) of this stage not counted: ' + ', '.join(
                    f"{r.date} exp {r.experiment or '?'} ({r.n_trials} trials)" for r in other.itertuples()))
            exp = gm['experiment_number'].dropna().astype(int).tolist()
            later = g[g['stage'].map(stageOrder.index) > stageOrder.index(stage)]
            after = g[g['day_overall'] > gm['day_overall'].max()]
            row.update({
                'days_run': len(slots),
                'days_with_file': len(gm),
                'missing_file_days': sum(s is None for s in slots),
                'days_all': len(gs),
                'first_date': gm['date'].min(),
                'last_date': gm['date'].max(),
                'experiment_numbers': ','.join(str(x) for x in gm['experiment'].tolist()),
                'last_experiment': exp[-1] if exp else np.nan,
                'missing_experiment_numbers': ','.join(
                    str(x) for x in sorted(set(range(1, max(exp) + 1)) - set(exp))) if exp else '',
                'next_stage': after['stage'].iloc[0] if len(after) else 'end of data',
                'ran_later_stage': bool(len(later)),
                'note': '; '.join(notes),
            })
            rows.append(row)
    cols = ['mouse', 'group', 'sex', 'stage', 'days_run', 'days_with_file', 'missing_file_days',
            'days_all', 'first_date', 'last_date', 'experiment_numbers', 'last_experiment',
            'missing_experiment_numbers', 'next_stage', 'ran_later_stage', 'note']
    out = pd.DataFrame(rows, columns=cols)
    for col in ['days_run', 'days_with_file', 'missing_file_days', 'days_all', 'last_experiment']:
        out[col] = out[col].astype('Int64')
    return out


def daysCsvText(perStage, mouseInfo):
    # prism layout: group row, mouse ID row, then FR1 / 100/0 / 90/10
    mice = mouseOrder(mouseInfo)
    sub = perStage[perStage['stage'].isin(daysRows.values())]
    wide = sub.pivot(index='stage', columns='mouse', values='days_run')
    wide = wide.reindex(index=list(daysRows.values()), columns=mice)
    lines = ['group,' + ','.join(mouseInfo[m]['group'] for m in mice),
             'stage,' + ','.join(mice)]
    for rowName, (_, vals) in zip(daysRows, wide.iterrows()):
        lines.append(rowName + ',' + ','.join('' if pd.isna(v) else str(int(v)) for v in vals))
    return '\n'.join(lines) + '\n'


#%% switching (G)

def reversalBlocks(sessions):
    # one row per reversal block. block 0 starts with the session so it's not a reversal
    rows = []
    for _, ses in sessions[sessions['stage'].isin(switchStages)].iterrows():
        trials = ses['trials']
        trials = trials[trials['block'] >= 1]
        for block, tr in trials.groupby('block', sort=True):
            side = tr['block_side'].to_numpy()
            rows.append({'mouse': ses['mouse'], 'group': ses['group'], 'stage': ses['stage'],
                         'block': int(block), 'n_trials': len(tr),
                         'correct': (tr['choice'].to_numpy() == side).astype(np.int64)})
    return pd.DataFrame(rows)


def correctByTrial(blocks):
    # % correct on trials 1-25 after a switch, all of a mouse's blocks pooled
    # blocks cut off by the end of the session just drop out (not counted wrong)
    out = []
    for (stage, mouse), b in blocks.groupby(['stage', 'mouse'], sort=True):
        mat = np.full((len(b), trialsToSee), np.nan)  # one row per block, NaN after it ended
        for i, c in enumerate(b['correct']):
            c = np.asarray(c, dtype=float)[:trialsToSee]
            mat[i, :len(c)] = c
        nBlocks = (~np.isnan(mat)).sum(axis=0)
        nCorrect = np.nansum(mat, axis=0)
        prop = np.full(trialsToSee, np.nan)
        prop[nBlocks > 0] = nCorrect[nBlocks > 0] / nBlocks[nBlocks > 0]
        out.append(pd.DataFrame({
            'group': b['group'].iloc[0], 'mouse': mouse, 'stage': stage,
            'trial': np.arange(1, trialsToSee + 1, dtype=np.int64),
            'n_blocks': nBlocks.astype(np.int64), 'n_correct': nCorrect.astype(np.int64),
            'prop_correct': prop, 'n_blocks_total': len(b)}))
    return pd.concat(out, ignore_index=True)


def switchingTable(long, stage, mice):
    # prism layout: rows = trial after the switch, one column per mouse
    one = long[long['stage'] == stage]
    wide = one.pivot(index='trial', columns='mouse', values='prop_correct')
    wide = wide.reindex(index=np.arange(1, trialsToSee + 1, dtype=np.int64), columns=mice)
    wide.index.name = 'trial'
    wide.columns.name = None
    return wide.reset_index()


#%% sample session (F)

def rasterTable(trials):
    # one row per trial, blank where there's no tick. right port on top
    right = trials['choice'].to_numpy() == 0
    left = trials['choice'].to_numpy() == 1
    rewarded = trials['reward'].to_numpy() == 1
    return pd.DataFrame({
        'Trial': trials['trial'].to_numpy(),
        'Right Picked Trials': np.where(right, 1.05, np.nan),
        'Left Picked Trials': np.where(left, 0.05, np.nan),
        'Right Rewarded': np.where(right & rewarded, 1.0, np.nan),
        'Left Rewarded': np.where(left & rewarded, 0.0, np.nan),
    })


def switchTable(trials):
    # first trial of every block after block 0 (dashed lines)
    blocks = (trials.groupby('block', sort=True)
              .agg(switch_trial=('trial', 'min'), side=('block_side', 'first'))
              .reset_index())
    blocks = blocks[blocks['block'] > 0].reset_index(drop=True)
    return pd.DataFrame({
        'block': blocks['block'].to_numpy(),
        'switch_trial': blocks['switch_trial'].to_numpy(),
        'last_trial_before': blocks['switch_trial'].to_numpy() - 1,
        'new_high_side': ['right' if s == 0 else 'left' for s in blocks['side']],
    })


#%% run

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw-dir', required=True)
    parser.add_argument('--mouse-info', required=True)
    parser.add_argument('--out-dir', required=True)
    parser.add_argument('--sample-mouse', default=sampleMouse)
    parser.add_argument('--sample-date', default=sampleDate)
    args = parser.parse_args()

    with open(args.mouse_info, 'r') as f:
        mouseInfo = json.load(f)
    sessions = loadSessions(args.raw_dir, mouseInfo)
    mice = mouseOrder(mouseInfo)

    days = trainingDays(sessions)
    perStage = daysPerStage(days)
    long = correctByTrial(reversalBlocks(sessions))

    sample = sessions[(sessions['mouse'] == args.sample_mouse) & (sessions['date'] == args.sample_date)]
    assert len(sample) == 1 and sample['stage'].iloc[0] in reversalStages, 'sample session not found'
    sample = sample.iloc[0]

    out = args.out_dir
    os.makedirs(out, exist_ok=True)

    # C, E
    daysText = daysCsvText(perStage, mouseInfo)
    with open(os.path.join(out, 'days_per_stage.csv'), 'w', newline='') as f:
        f.write(daysText)
    perStage.to_csv(os.path.join(out, 'days_per_stage_long.csv'), index=False, lineterminator='\n')
    days = days.loc[days['stage'].isin(countedStages)].drop(columns=['experiment_number', 'run'])
    days.to_csv(os.path.join(out, 'training_days.csv'), index=False, lineterminator='\n')

    # F
    rasterTable(sample['trials']).to_csv(os.path.join(out, 'sample_session.csv'), index=False,
                                         float_format='%g', lineterminator='\n')
    switches = switchTable(sample['trials'])
    switches.to_csv(os.path.join(out, 'sample_session_switches.csv'), index=False, lineterminator='\n')

    # G
    for stage in switchStages:
        fileName = 'switching_' + stage.replace('/', '_') + '.csv'
        switchingTable(long, stage, mice).to_csv(os.path.join(out, fileName), index=False, lineterminator='\n')
    long.to_csv(os.path.join(out, 'switching_long.csv'), index=False, lineterminator='\n')

    print('\ndays run per stage:')
    print(daysText)
    noted = perStage[perStage['stage'].isin(daysRows.values()) & (perStage['note'] != '')]
    for r in noted.itertuples():
        print(f'{r.mouse} {r.stage}: {r.days_run} days ({r.missing_file_days} with no file) - {r.note}')
    print(f"\nsample session: {args.sample_mouse} {args.sample_date} {sample['stage']} ({sample['file']}), "
          f"{sample['nStarts']} trial starts, {len(sample['trials'])} completed trials, "
          f"switches at trials {switches['switch_trial'].tolist()}")
