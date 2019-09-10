import Drain
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#File_dialog
from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog


root = Tk()
name = tkFileDialog.askopenfilename()
input_dir    = ''  # The input directory of log file
output_dir   = './results/'  # The output directory of parsing results
log_file     = name  # The input log file name
log_format   = '<Date_Time>,<Thread>,<Level>,<Logger>,<Content>'  # log format
regex      = []
st         = 0.5  # Similarity threshold
depth      = 4  # Depth of all leaf nodes

parser = Drain.LogParser(log_format, indir=input_dir, outdir=output_dir,  depth=depth, st=st, rex=regex)
parser.parse(log_file)
