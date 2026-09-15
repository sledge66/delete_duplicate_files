import os
import sys
import argparse
import hashlib
import logging

from pathlib import Path

# ############################################################
#
# ############################################################
def sha256sum(filename):
    with open(filename, 'rb', buffering=0) as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def compute_file_hash(file_path, algorithm='sha256'):
    """Compute the hash of a file using the specified algorithm."""
    hash_func = hashlib.new(algorithm)
    
    with open(file_path, 'rb') as file:
        # Read the file in chunks of 8192 bytes
        while chunk := file.read(8192):
            hash_func.update(chunk)
    
    return hash_func.hexdigest()

# ############################################################
# Main
# ############################################################

# Parameter:
# --dest_dir, -d Dest-Dir
# --log_file, -l Log-File
# --protocol_dir, -p Protocol-Dir
# --testmode, -t

parser = argparse.ArgumentParser(prog='hash_files', description='Hashwerte von Dateien berechnen.')
parser.add_argument('-r', '--root_dir', required=True, help='Basisverzeichnis')
parser.add_argument('-l', '--log_file', help='(Verzeichnis und) Name der Log-Datei')
parser.add_argument('-p', '--protocol_dir', help='Verzeichnis für Protokolldateien')
#parser.add_argument('-t', '--testmode', action='store_true', help='Testmodus; nur Protokolldateien schreiben, keine Verzeichnisse tatsächlich umbenennen')

# Parameternamen und -werte in Dictionary schreiben
#args = parser.parse_args()
params = vars(parser.parse_args())
#print(params)

# Defaultwerte für Parameter setzen
if params['log_file'] == None:
    params['log_file'] = Path(sys.argv[0]).stem + '.log'
if params['protocol_dir'] == None:
    params['protocol_dir'] = 'D:\\temp'

#print(params)

# Parameter prüfen
if not Path(params['root_dir']).exists():
    print('Basisverzeichnis "%s" existiert nicht.' % (params['root_dir']))
    exit(1)
elif not Path(params['protocol_dir']).exists():
    print('Verzeichnis "%s" für Protokolldateien existiert nicht.' % (params['protocol_dir']))
    exit(1)


# Logging initialisieren
logging.basicConfig(
    filename=params['log_file'],
    filemode="w",
    encoding='utf-8',
    level=logging.DEBUG)

logging.info('-' * 50)
logging.info('Basisverzeichnis: ' + params['root_dir'])
logging.info('Protokollverzeichnis: ' + params['protocol_dir'])
#if params['testmode']:
#    logging.info('Testmode: Ja' )
#else:
#    logging.info('Testmode: Nein' )
#logging.info('-' * 50)

walk_dir = params['root_dir'] # sys.argv[1]

logging.info('walk_dir = ' + walk_dir)

# If your current working directory may change during script execution, it's recommended to
# immediately convert program arguments to an absolute path. Then the variable root below will
# be an absolute path as well. Example:
# walk_dir = os.path.abspath(walk_dir)
logging.info('walk_dir (absolute) = ' + os.path.abspath(walk_dir))

file_list = {}

for root, subdirs, files in os.walk(walk_dir):
    logging.info('--\nroot = ' + root)
#    list_file_path = os.path.join(root, 'my-directory-list.txt')
#    logging.info('list_file_path = ' + list_file_path)

#    with open(list_file_path, 'wb') as list_file:
#    for subdir in subdirs:
#        logging.info('\t- subdirectory ' + subdir)

    for filename in files:
        extension = os.path.splitext(filename)[1]
        if extension.lower() in ['.jpg', '.jpeg', '.png']:
            file_path = os.path.join(root, filename)
            hash_value = compute_file_hash(file_path)

            logging.info('\t- file %s (full path: %s)' % (filename, file_path))
            logging.info('\t- hash ' + hash_value)

            file_list[file_path] = hash_value

#            with open(file_path, 'rb') as f:
#                f_content = f.read()
#                list_file.write(('The file %s contains:\n' % filename).encode('utf-8'))
#                list_file.write(f_content)
#                list_file.write(b'\n')

logging.info('')
logging.info('----------')
logging.info('')

last_file_path = ''
last_hash_value = ''

for k, v in sorted(file_list.items(), key=lambda item: item[1]):
#    logging.info('%s, %s' % (k, v))
    if v == last_hash_value:
        logging.info('----- Duplikat %s' % last_hash_value)
        logging.info('%s' % last_file_path)
        logging.info('%s' % k)

    last_file_path = k
    last_hash_value = v
