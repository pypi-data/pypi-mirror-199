from openseize import producer
from openseize.demos import paths
from openseize.file_io import edf
from openseize.filtering import iir

if __name__ == '__main__':

    fp = paths.locate('recording_001.edf')
    reader = edf.Reader(fp)
    pro = producer(reader, chunksize=1e5, axis=-1)
    notch = iir.Notch(fstop=60, width=4, fs=5000)

    notched = notch(pro, chunksize=1e5, axis=-1, dephase=True)

    for idx, arr in enumerate(notched):
        print(idx, arr.shape)
