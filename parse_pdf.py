#!/usr/bin/python3
import camelot
import numpy as np
import pandas as pd
import pickle
import os
import sys
import glob

exam_dt = r'[A-Z]+\s*[0-9]+\s*[A-Z.]+\s*[0-9]+\s*[A-Z]*'
exam_dt_dep = 'คณะจัดสอบเอง'
course_num = r'[A-Z]+[0-9]+\s*\(.+\)'
course_time = r'[A-Z]{1,4}\s*[0-9]{4}-[0-9]{4}'

if len(sys.argv) > 1:
    mr30_path = sys.argv[1]
else:
    print('pass in the file name. Example:')
    print('./parse_pdf.py ./MR30.pdf')
    sys.exit(1)

def load_page_from_cache(page_no):
    """ to avoid recomputation only
    """
    cache_path = f'./pages/cache/camelot-cache-page-{page_no}'
    if os.path.exists(cache_path):
        print(f"found cached csv for this page at: {cache_path}")
        with open(cache_path, 'rb') as h:
            tables = pickle.load(h)
    else:
        print(f"no cache for this page at: {cache_path}")
        tables = camelot.read_pdf(mr30_path, flavor='stream', pages=str(i), edge_tol=500, backend='poppler')
        with open(cache_path, 'wb') as h:
            pickle.dump(tables, h)
            
    return tables


def save_original(df, i):
    """ original page is saved
    """
    df.to_csv(f'./pages/00-original-{i}.csv', header=True, index=False)
    return df


def drop_headers(df, i):
    """ drop until 1st course number is found
    """
    df = df[df[0].str.contains('^[A-Z]+[0-9]{2,4}', regex=True).fillna(False).idxmax():]
    df.to_csv(f'./pages/10-truncated-{i}.csv', header=True, index=False)
    return df


def fill_values(df, i):
    """ fill na with value from cell above.
    """
    df = df.replace(r'^\s*$', np.nan, regex=True).fillna(method='ffill') #
    df.to_csv(f'./pages/20-filled-{i}.csv', header=True, index=False)
    return df


def project_columns(df, i):
    """ select only needed columns to be used in next steps
    """
    df = df.reset_index()

    for i in range(df.shape[0]): # number of rows
        row = df.iloc[i, :] # first row of the page
        selected_col_ixs = row[
            (row.str.contains(exam_dt, na=False))
            | (row.str.contains(exam_dt_dep, regex=True, na=False))
            | (row.str.contains(course_num, regex=True, na=False))
            | (row.str.contains(course_time, regex=True, na=False))
        ].index
        
        if len(selected_col_ixs) == 3:
            df = df[selected_col_ixs]
            df.columns = ['course_num', 'course_time', 'exam_dt']
            break
    else:
        raise Exception("fail to project needed columns on this page")
    
    df.to_csv(f'./pages/30-projected-{i}.csv', header=True, index=False)
    return df
    
def strip_columns(df, i):
    """ remove leading whitespaces in all cells
    """
    df = df.replace({'\s*\n.+': ''}, regex=True)
    df.to_csv(f'./pages/35-stripped-{i}.csv', header=True, index=False)
    return df

def remove_unrecognized(df, i):
    """ reject cells that is not in recognized format.
    FIXME here this drop many of the valid rows
    """
    df = df[~df['course_num'].str.contains('วิชา')] # remove in-page headers
    df = df[~df.apply(lambda r: r.str.contains('^[A-Z][A-Z][A-Z] \: [A-Z0-9]+', regex=True, na=False).any(), axis=1)] # remove header like `HIS : HISTORY`
    df = df[
        (df['course_num'].str.contains(f'^{course_num}$', regex=True))
        & (df['course_time'].str.contains(f'^{course_time}$', regex=True))
        & (df['exam_dt'].str.contains(f'^{exam_dt}|{exam_dt_dep}$', regex=True))
    ]
    df.to_csv(f'./pages/40-header-removed-{i}.csv', header=True, index=False)
    return df


def save_preprocessed_page_result(df, i):
    """ preprocessing ends.
    """
    df.to_csv(f'./pages/preprocessed-{i}.csv', header=True, index=False)
    return df


def save_full_preprocessed(df):
    """save combined preprocessed file
    """
    df.to_csv('./pages/z00-preprocessed.csv', index=False)
    return df
    
def deduplicate(df):
    """drop duplicates
    """
    df = df.drop_duplicates()
    df.to_csv('./pages/z10-unique.csv', index=False)
    return df
    
def extract_credit(df):
    """get credit from course_num
    """
    df['credit'] = df['course_num'].str.replace('^.+\(', '', regex=True).replace('\).*', '', regex=True)
    df['course_num'] = df['course_num'].str.replace(' .*', '', regex=True)
    df.to_csv('./pages/z20-credit.csv', index=False)
    return df


def extract_exam_dt(df):
    """get exam date and time
    """
    df = df.replace(exam_dt_dep, 'XX 01 JAN. 1970 X') # คณะจัดสอบเอง
    df['exam_d'] = df['exam_dt'].str.extract(r'(\d+ [A-Z.]+ \d+)') \
        .replace('\.', '', regex=True).apply(lambda xs: pd.to_datetime(xs, format="%d %b %Y")) # get date from dt (15 MAR. 2023, day is ignored)

    df['exam_t'] = df['exam_dt'].str.extract(r'([A-Z],?)+$') # get time from dt (A, B, C, X) ...
    df = df.drop('exam_dt', axis=1)
    df.to_csv('./pages/z30-exam-dt.csv', index=False)
    return df

def extract_course_dt(df):
    """get lecture day and time
    """
    df['course_d'] = df['course_time'].str.extract(r'^([A-Z]+).*')
    df['course_t_start'] = df['course_time'].str.extract(r'[A-Z]+ ([0-9]+)\-[0-9]+.*')
    df['course_t_end'] = df['course_time'].str.extract(r'.*[0-9]+\-([0-9]+).*')
    
    df = df.drop('course_time', axis=1)
    df.to_csv('./pages/z40-course-dt.csv', index=False)
    return df


def write_sqlite(df):
    """save to sqlite3 database.
    server will read from this file
    """
    import sqlite3
    conn = sqlite3.connect('./mr30.sqlite3')
    df.to_sql('courses', conn, if_exists='replace', index=False)
    return

if __name__ == '__main__':

    # preprocess
    for i in range(0, 179):
        try:
            tables = load_page_from_cache(i)
        except Exception as e:
            print("error: ", e)
            print(f"error on page {i}, skipping")
            continue

        # FIXME might not need to iterate as there is actually 1 table in 1 page.
        for ix, table in enumerate(tables):
            df = table.df
            df \
                .pipe(save_original, i=i) \
                .pipe(drop_headers, i=i) \
                .pipe(fill_values, i=i) \
                .pipe(project_columns, i=i) \
                .pipe(strip_columns, i=i) \
                .pipe(remove_unrecognized, i=i) \
                .pipe(save_preprocessed_page_result, i=i)

            print(f"end page {i}, df has shape {df.shape}")
            

    # concatenate all preprocessed results
    full = pd.concat(map(pd.read_csv, glob.glob('./pages/preprocessed-*.csv')))

    
    # run and save to sqlite3 database
    full \
        .pipe(save_full_preprocessed) \
        .pipe(deduplicate) \
        .pipe(extract_credit) \
        .pipe(extract_exam_dt) \
        .pipe(extract_course_dt) \
        .pipe(write_sqlite)

