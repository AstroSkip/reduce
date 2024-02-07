from astropy.io import fits
import pandas as pd
import glob

#here we can define a procedure to deal with all observations from a night
def make_night_log(foldername):
    # we create an empty array
    imags = []
    # This takes all the files which have the .fits extension 
    filenames = glob.glob(foldername+"*.fits")
    # looping to all the files 
    for filename in filenames:
        # Open each file to take the most importnat keyword for the header
        with fits.open(filename) as hdul:
            # load the header
            hdr = hdul[0].header
            # append a new line to the array with the elemnts containg the
            # information from the header
            imags.append([hdr['FILENAME'], hdr['OBJECT'], hdr['DATE-OBS'], 
                         hdr['EXPTIME'], hdr['ALGRNM'], hdr['ALAPRTNM'],
                         hdr['RA'], hdr['DEC'], hdr['AIRMASS']])
    # Simply create panda data frame and put it in a csv file
    df2 = pd.DataFrame(imags,columns=('Filename', 'OBJECT', 'DATE-OBS',
                                      'EXPTIME', 'Grism', 'SLit',
                                      'RA','DEC', 'AIRMASS'))
    df2.to_csv(path_or_buf=foldername + 'ObservingLog3.csv',index=False)
    return


# Procedure for creating trim script
def create_trim_script(foldername):
    
    # open the script to write the commands
    trimscr = open(foldername + 'com.trim', "w")
    
    # This takes all the files which have the .fits extension 
    filenames = glob.glob(foldername+"*.fits")
    # looping to all the files 
    for filename in filenames:
        # preparing the line you want to put in the script
        # notice: filename[-15:] is the name of each file 
        # the notation -15: means taking from the end of the string the last 15
        # characters
        l2w = 'imcopy' + ' ./' + filename[-15:] + '[41:440,0:1400] ./t_' + filename[-15:]
        # use the write command associated with the  file identifier trimscr
        # the symbol "\n" means new line
        trimscr.write(l2w + "\n" )
    
    trimscr.close()


def dobiascommand(foldername):
    '''
        This function generates the list of all bias files
        and the bias substraction script
    '''
    # open the file with the list fo all biases
    blst = open(foldername + 'bias.lst', "w")
    # open the script to write the commands
    cbf =  open(foldername + 'com.bias', "w")
    # This command takes all the files which have the .fits extension 
    filenames = glob.glob(foldername+"*_t.fits")
    print(filenames)
    # looping trough all the files 
    for filename in filenames:
        # Open each file to get the object keyword from the header
        with fits.open(filename) as hdul:
            # load the header
            hdr = hdul[0].header
            if hdr['OBJECT'] == 'alfosc-calibs bias':
                blst.write(filename[-17:-5] + "\n")
            else: # prepare the bias subbtraction command
               cbf.write('imarith ' + filename[-17:-5] + ' - finalbias.fits' + ' b_' + filename[-15:-5] + "\n")
    # close the two files identifiers
    blst.close()
    cbf.close()    
#exit()

def doflatcommands(foldername):
    '''
        This function generates the list of all flat files
        and the flat substraction script
    '''
    # open the file with the list fo all biases
    filst = open(foldername + 'flatinput.list', "w")
    folst = open(foldername + 'flatoutput.list', "w")
    # open the script to write the commands
    comflat =  open(foldername + 'com.flat', "w")
    # This command takes all the files which have the .fits extension 
    filenames = glob.glob(foldername+"b_*.fits")
    # looping trough all the files 
    for filename in filenames:
        # Open each file to get the object keyword from the header
        with fits.open(filename) as hdul:
            # load the header
            hdr = hdul[0].header
            if hdr['OBJECT'][0:7] == 'Halogen':
                filst.write(filename[-17:-5] + "\n" )
                folst.write('f_' + filename[-15:-5] + "\n" )
            else: # prepare the bias subbtraction command
               comflat.write('imarith ' + filename[-17:-5] + \
                         ' / finalflat.fits' + ' f_' + \
                         filename[-15:-5] + "\n" )
    # close the two files identifiers
    filst.close()
    folst.close()
    comflat.close()

    
    
    

# run the proecure fro this night of observations
foldername = ''
#make_night_log(foldername)
#create_trim_script(foldername)
#dobiascommand(foldername)
doflatcommands(foldername)
