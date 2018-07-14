import base64
import re
import glob
import tarfile
import sqlite3

IMAGE_FILE_RE = re.compile('^.*\.(png|eps|ps|svg|pdf)$', re.IGNORECASE)
TAG_RE= re.compile('matplotlib', re.IGNORECASE)

total_figure = 0
total_papers = 0

db_filename = "arxiv_meta.sql"

def create_db(path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    # name of the paper: month day; number of figures, number of figures with matplotlib
    table_creation_query = """create table if not exists
                                img_meta (
                                filename      varchar(1000),
                                tot_img_count integer,
                                mpl_img_count integer ) """
    cursor.execute(table_creation_query)
    # not closing the connection
    return conn, cursor

def parse_source_tarball(fname):

    # for inserting metadata into a sqlite db
    conn, cursor = create_db(db_filename)

    try:
        with tarfile.open(name=fname, mode='r:gz') as tf:
            current_no_figures = 0
            current_no_mpl_figures = 0
            for image_fname in filter(IMAGE_FILE_RE.match, tf.getnames()):
                current_no_figures += 1
                fp = tf.extractfile(image_fname)
                data = fp.read()
                if data.find(b'matplotlib') > 0:
                    current_no_mpl_figures += 1
            insert_query = "insert into img_meta values ('%s', '%s', '%s');" % (fname, current_no_figures, current_no_mpl_figures)
            cursor.execute(insert_query)
                # data = base64.b64encode(fp.read()).decode(tarfile.ENCODING)
                # import pudb; pudb.set_trace()
        print('In paper {} there {} MPL images out of total {} images'
              .format(fname, current_no_mpl_figures, current_no_figures))
    except tarfile.TarError:
        pass

    cursor.close()
    conn.commit() # otherwise you won't get any data...
    conn.close()


if __name__ == "__main__":
    for fname in glob.glob('1803/1803*.gz'):
        parse_source_tarball(fname)
        total_papers += 1
