import base64
import re
import glob
import tarfile

IMAGE_FILE_RE = re.compile('^.*\.(png|eps|ps|svg|pdf)$', re.IGNORECASE)
TAG_RE= re.compile('matplotlib', re.IGNORECASE)

total_figure = 0
total_papers = 0

def parse_source_tarball(fname):
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
                # data = base64.b64encode(fp.read()).decode(tarfile.ENCODING)
                # import pudb; pudb.set_trace()
        print('In paper {} there {} MPL images out of total {} images'
              .format(fname, current_no_mpl_figures, current_no_figures))
    except tarfile.TarError:
        pass


if __name__ == "__main__":
    for fname in glob.glob('1803/1803*.gz'):
        parse_source_tarball(fname)
        total_papers += 1
