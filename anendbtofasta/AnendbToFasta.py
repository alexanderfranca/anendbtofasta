import os
import sys
import pprint
import logging
import logging.handlers
from Ec import *
from Connection import *


class AnendbToFasta:
    """
    Deals with the process of generating Fasta EC files to be clustered.
    """

    def __init__(
            self,
            user=None,
            password=None,
            host=None,
            database=None,
            log_file=None,
            destination_directory=None):

        # Database parameters.
        self.user = user
        self.password = password
        self.host = host
        self.database = database

        # We have to log everything. This package can deal with huge amount of
        # data.
        self.log_file = log_file

        # Where to write the Fasta files.
        self.destination_directory = destination_directory

        # To store the logging system.
        self.log = None

        # -------------------------------------------------------------------------------- #
        # Database session. We need one.                                                   #
        # -------------------------------------------------------------------------------- #
        # ---- IF YOU WANT TO REFACTOR THIS CLASS TO REMOVE DEPENDENCY, YOU ONLY HAVE ---- #
        # ---- TO PROVIDE A VALID SQLAlchemy Session and attach to the self.session   ---- #
        # -------------------------------------------------------------------------------- #
        self.session = None
        # -------------------------------------------------------------------------------- #

        c = Connection()
        self.session = c.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database)

    def create_log_system(self, log_file=None):
        """
        Set all logger parameters (file log path, for example), output format and set the class p

        Log the process is extremely important because we don't know how long it will take.

        """

        log = logging.getLogger('')
        log.setLevel(logging.DEBUG)
        format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(format)
        log.addHandler(ch)

        fh = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=0, backupCount=0)
        fh.setFormatter(format)
        log.addHandler(fh)

        self.log = log

    # TOD: test
    def generate_ec_proteins_files(self, ecs=None):
        """
        Generate the text files containing sequences by EC number file.

        Args:
            ecs(list): List of EC numbers.


        """

        self.create_log_system(self.log_file)

        self.log.info('-- START --:anendbtofasta:generate_ec_proteins_files')

        if ecs:
            # Maybe user forgotten to set the parameter as a list.
            if not isinstance(ecs, list):
                ecs = ecs.split(',')

            self.log.info('Will process total of: ' +
                          str(len(ecs)) + ' EC numbers.')

            self.log.info('EC numbers selected: ' + str(ecs))

            for ec in ecs:

                self.log.info('Will process EC number: ' + str(ec))

                ec_record = self.session.query(
                    Ec).filter_by(ec=str(ec)).first()

                if ec_record:
                    ec_data = self.data_from_ec(ec_record)

                    self.log.info(
                        'Will write data for the EC number: ' + str(ec))

                    self.write_ec_file(ec_data)

                    self.log.info(
                        'Done write data for the EC number: ' + str(ec))

        # Generate all data from all EC numbers. A very, very, very looooongggg
        # process.
        else:

            self.log.info(
                'Will process ALL EC numbers from the relational database.')

            ecs = self.session.query(Ec).all()

            self.log.info('Will process total of: ' +
                          str(len(ecs)) + ' EC numbers.')

            for ec in ecs:

                self.log.info('Will process EC number: ' + str(ec.ec))

                ec_data = self.data_from_ec(ec)

                self.log.info(
                    'Will write data for the EC number: ' + str(ec.ec))

                self.write_ec_file(ec_data)

                self.log.info(
                    'Done write data for the EC number: ' + str(ec.ec))

        self.log.info('-- DONE --:anendbtofasta:generate_ec_proteins_files')

    # TODO: test
    def data_from_ec(self, ec=None):
        """
        Iterate through an EC number record and return its data.

        Args:
            ec(obj): EC record object from ORM.

        """

        data = {}

        proteins = ec.protein
        ec = ec.ec
        ec = str(ec)

        data[ec] = []

        for protein in proteins:
            data[ec].append({'header': str(protein.full_fasta_header), 'identification': str(
                protein.identification), 'sequence': str(protein.sequence)})

        return data

    # TODO: test
    def write_ec_file(self, data=None):
        """
        Write the Fasta file with the sequences from an EC number.

        Args:
            data(list): List of sequences and protein identifications from an EC number.
        """

        # Create the directory in case it doesn't exist
        if not os.path.isdir(self.destination_directory):
            os.mkdir(self.destination_directory)

        # Type casting...
        ec_number = data.keys()
        ec_number = str(ec_number[0])

        # The actual file path.
        ec_file = self.destination_directory + '/' + 'EC_' + ec_number + '.fasta'

        self.log.info('Will write the file: ' + str(ec_file))

        # Remove the file it already exists.
        if os.path.exists(ec_file):

            self.log.info(
                'File: ' +
                str(ec_file) +
                ' already exists. Removing it to create a new one.')

            os.remove(ec_file)

        # Actual write the file.
        with open(ec_file, 'a') as f:

            for data in data[ec_number]:

                f.write(data['header'] + "\n")
                f.write(data['sequence'] + "\n")
