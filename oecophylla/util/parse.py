import re
import pandas as pd

# Option 1 : parse samples from directory

def parse_filenames_to_df(filepaths, pattern = None, column_names = None):
    """ Generates sample sheet from filenames using a regex pattern.

    Parameters
    ----------
    filepaths: list of str
        List of file paths to parse
    pattern: str
        Regex pattern to recognize the filenames, to load into the
        sample sheet.
        default: '^((.+?)_(S\d+)_(L\d+)_(R[12])_(\d+)\.(.+))$'
    column_names: list
        Column names for the generated sample sheet.  Note that this
        is assumed to be in the same ordering as the regex pattern.
        default: ['File', 'Sample', 'Index', 'Lane',
                  'Read', 'Run', 'Extension']


    """
    if pattern is None:
        pattern = '^((.+?)_(S\d+)_(L\d+)_(R[12])_(\d+)\.(.+))$'
    if column_names is None:
        column_names = ['File', 'Sample', 'Index', 'Lane',
                         'Read', 'Run', 'Extension']
    p = re.compile(pattern)
    df = pd.DataFrame(columns = column_names)

    for f in filepaths:
        m = p.match(f)
        if m:
            df = df.append(dict(zip(column_names, m.groups())),
                           ignore_index = True)
    return df


def get_sample_reads_df(df, seq_dir):
    """
    Parameters
    ----------
    df : pd.DataFrame

    seq_dir : str

    """
    sample_reads_dict = {}

    samples = list(set(df['Sample']))

    for s in samples:
        f_fps = sorted(list(df.loc[(df['Sample'] == s) & (df['Read'] == 'R1'),'File'].values))
        r_fps = sorted(list(df.loc[(df['Sample'] == s) & (df['Read'] == 'R2'),'File'].values))

        sample_reads_dict[s] = {'forward': [os.path.join(seq_dir, x) for x in f_fps],
                                'reverse': [os.path.join(seq_dir, x) for x in r_fps]}

    return(sample_reads_dict)

def get_sample_paths(seq_dir):
    """
    Parameters
    ----------
    seq_dir : str
    """
    fps = os.listdir(seq_dir)

    files_df = parse_ilm_fps_to_df(fps)
    sample_reads_dict = get_sample_reads_df(files_df, seq_dir)

    return(sample_reads_dict)


def add_filter_db(sample_fp_dict, db_fp, samples = None):

    if samples is None:
        samples = sample_fp_dict.keys()

    samples_dict = copy.deepcopy(sample_fp_dict)

    for s in samples_dict:
        if s in samples:
            samples_dict[s]['filter_db'] = db_fp
        elif 'filter_db' in samples_dict[s]:
            continue
        else:
            samples_dict[s]['filter_db'] = None

    return(samples_dict)

# Option 2: read samples from manifest
def read_sample_sheet(f, sep='\t'):
    data = False
    data_lines = ''
    for line in f:
        if data:
            if line.startswith('[') or line.strip() == '':
                data = False
                continue
            data_lines += line
        elif line.startswith('[Data]'):
            data = True
            continue
        else:
            continue

    data_df = pd.read_csv(StringIO(data_lines), sep = '\t', comment='#')
    return(data_df)

def get_sample_reads_df_from_sample_sheet(ss_df, seq_dir,
                                          sample_col='Description',
                                          prefix_col='Sample_ID'):
    sample_reads_dict = {}

    samples = list(set(ss_df[sample_col]))

    fps = os.listdir(seq_dir)

    files_df = parse_ilm_fps_to_df(fps)

    for s in samples:
        # get the subset of sample sheet rows for that sample
        sample_rows = ss_df.loc[ss_df[sample_col] == s,]

        f_fps = []
        r_fps = []

        # iter across subset table and find file corresponding to each row
        for idx, row in sample_rows.iterrows():
            lane = 'L{0:03d}'.format(row['Lane'])

            f_fps.extend(files_df.loc[(files_df['Sample'] == row['Sample_ID']) &
                                      (files_df['Lane'] == lane) &
                                      (files_df['Read'] == 'R1'), 'File'].values)

            r_fps.extend(files_df.loc[(files_df['Sample'] == row['Sample_ID']) &
                                      (files_df['Lane'] == lane) &
                                      (files_df['Read'] == 'R2'), 'File'].values)

        f_fps = sorted(f_fps)
        r_fps = sorted(r_fps)

        sample_reads_dict[s] = {'forward': [os.path.join(seq_dir, x) for x in f_fps],
                                'reverse': [os.path.join(seq_dir, x) for x in r_fps]}

    return(sample_reads_dict)
