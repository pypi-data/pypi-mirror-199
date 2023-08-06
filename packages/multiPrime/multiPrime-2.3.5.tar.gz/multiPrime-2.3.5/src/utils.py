#!/usr/bin/env python3

from optparse import OptionParser
import numpy as np
import sys
import math
from operator import mul
from math import log10
from functools import reduce
from bisect import bisect_left


# Melting temperature between 55-80◦C reduces the occurrence of hairpins
# Runs of three or more Cs or Gs at the 3'-ends of primers may promote mispriming at G or C-rich sequences
# (because of stability of annealing), and should be avoided.
def DPrime_argsParse():
    parser = OptionParser('Usage: %prog DPrime -i input -o output -p 10\n \
                Options: { -l [18] -n [4] -d [10] -v [1] -g [0.2,0.7] -f [0.8] -c [4] -p [10] -a [4] }')
    parser.add_option('-i', '--input',
                      dest='input',
                      help='Input file: multi-alignment output (muscle or others).')

    parser.add_option('-l', '--plen',
                      dest='plen',
                      default=18,
                      type="int",
                      help='Length of primer. Default: 18.')

    parser.add_option('-n', '--dnum',
                      dest='dnum',
                      default=4,
                      type="int",
                      help='Number of degenerate. Default: 4.')

    parser.add_option('-d', '--degeneracy',
                      dest='degeneracy',
                      default=10,
                      type="int",
                      help='degeneracy of primer. Default: 10.')

    parser.add_option('-v', '--variation',
                      dest='variation',
                      default=1,
                      type="int",
                      help='Max mismatch number of primer. Default: 1.')

    parser.add_option('-e', '--entropy',
                      dest='entropy',
                      default=3.6,
                      type="float",
                      help='Entropy is actually a measure of disorder. This parameter is used to judge whether the '
                           'window is conservation. Entropy of primer-length window. Default: 3.6.')

    parser.add_option('-g', '--gc',
                      dest='gc',
                      default="0.2,0.7",
                      help="Filter primers by GC content. Default [0.2,0.7].")

    parser.add_option('-s', '--size',
                      dest='size',
                      default="100",
                      type="int",
                      help="Filter primers by mini PRODUCT size. Default 100.")

    parser.add_option('-f', '--fraction',
                      dest='fraction',
                      default="0.8",
                      type="float",
                      help="Filter primers by match fraction. If you set -s lower than 0.8, make sure that "
                           "--entropy greater than 3.6, because disorder region (entropy > 3.6) will not be processed "
                           "in multiPrime. Even these regions can design coverage with error greater than your "
                           "threshold, it wont be processed. Default: 0.8.")

    parser.add_option('-c', '--coordinate',
                      dest='coordinate',
                      default="4",
                      type="int",
                      help="Mismatch index is not allowed to locate in start or stop. "
                           "otherwise, it won't be regard as the mis-coverage. "
                           "With this param, you can control the index of Y-distance (number=variation and position of mismatch) "
                           "when calculate coverage with error."
                           "Default: 4.")

    parser.add_option('-p', '--proc',
                      dest='proc',
                      default="20",
                      type="int",
                      help="Number of process to launch. Default: 20.")

    parser.add_option('-a', '--away',
                      dest='away',
                      default=4,
                      type="int",
                      help='Filter hairpin structure, which means distance of the minimal paired bases. Default: 4. '
                           'Example:(number of X) AGCT[XXXX]AGCT. '
                           'Primers should not have complementary sequences (no consecutive 4 bp complementarities),'
                           'otherwise the primers themselves will fold into hairpin structure.')

    parser.add_option('-o', '--out',
                      dest='out',
                      help='Output file: candidate primers. e.g. [*].candidate.primers.txt.')
    (options, args) = parser.parse_args()
    if len(sys.argv) == 2:
        parser.print_help()
        sys.exit(1)
    elif options.input is None:
        parser.print_help()
        print("Input file must be specified !!!")
        sys.exit(1)
    elif options.out is None:
        parser.print_help()
        print("No output file provided !!!")
        sys.exit(1)
    return parser.parse_args()



def Ppair_argsParse():
    parser = OptionParser('Usage: %prog Ppair -i [input] -r [sequence.fa] -o [output] \n \
                Options: {-f [0.6] -m [500] -n [200] -e [4] -p [9] -s [250,500] -g [0.4,0.6] -d [4] -a ","}.')
    parser.add_option('-i', '--input',
                      dest='input',
                      help='Input file: multiPrime out.')

    parser.add_option('-r', '--ref',
                      dest='ref',
                      help='Reference sequence file: all the sequence in 1 fasta, for example: (Cluster_96_171.tfa).')

    parser.add_option('-g', '--gc',
                      dest='gc',
                      default="0.2,0.7",
                      help="Filter primers by GC content. Default [0.2,0.7].")

    parser.add_option('-f', '--fraction',
                      dest='fraction',
                      default="0.6",
                      type="float",
                      help="Filter primers by match fraction. Default: 0.6. \n"
                           "Sometimes you need a small fraction to get output.")

    parser.add_option('-e', '--end',
                      dest='end',
                      default="4",
                      type="int",
                      help="Filter primers by degenerate base position. e.g. [-e 4] means I dont want degenerate base "
                           "appear at the end four bases when primer pre-filter. Default: 4.")

    parser.add_option('-p', '--proc',
                      dest='proc',
                      default="10",
                      type="int",
                      help="Number of process to launch.  default: 10.")

    parser.add_option('-s', '--size',
                      dest='size',
                      default="250,500",
                      help="Filter primers by PRODUCT size. Default [250,500].")

    parser.add_option('-d', '--dist',
                      dest='dist',
                      default=4,
                      type="int",
                      help='Filter param of hairpin, which means distance of the minimal paired bases. Default: 4. '
                           'Example:(number of X) AGCT[XXXX]AGCT.')

    parser.add_option('-t', '--tm',
                      dest='Tm',
                      default=5,
                      type="int",
                      help='Difference of Tm between primer-F and primer-R. Default: 5. ')

    parser.add_option('-a', '--adaptor',
                      dest='adaptor',
                      default="TCTTTCCCTACACGACGCTCTTCCGATCT,TCTTTCCCTACACGACGCTCTTCCGATCT",
                      type="str",
                      help='Adaptor sequence, which is used for NGS next. Hairpin or dimer detection for [adaptor--primer].'
                           '\n \ For example: TCTTTCCCTACACGACGCTCTTCCGATCT,TCTTTCCCTACACGACGCTCTTCCGATCT (Default). ''If '
                           'you dont want adaptor, use [","] ')

    parser.add_option('-m', '--maxseq',
                      dest='maxseq',
                      default=0,
                      type="int",
                      help='Limit of sequence number. Default: 0. If 0, then all sequence will take into account.\n'
                           'This param should consistent with [max_seq] in multi-alignment [muscle].')

    parser.add_option('-o', '--out',
                      dest='out',
                      help='Output file: candidate primer pairs. e.g. [*].candidate.primers.txt.'
                           'Header of output: Primer_F_seq, Primer_R_seq, Product length:Tm:coverage_percentage, '
                           'coverage_number, Primer_start_end')
    (options, args) = parser.parse_args()
    if len(sys.argv) == 2:
        parser.print_help()
        sys.exit(1)
    elif options.input is None:
        parser.print_help()
        print("Input file must be specified !!!")
        sys.exit(1)
    elif options.ref is None:
        parser.print_help()
        print("Reference file must be specified !!!")
        sys.exit(1)
    elif options.out is None:
        parser.print_help()
        print("No output file provided !!!")
        sys.exit(1)
    return parser.parse_args()


def Perfect_argsParse():
    parser = OptionParser('Usage: %prog Perfect -r [reference] -i [input] -p [10] -f [format] -o [output] '
                          '-s [Coverage.xls]', version="%prog 0.0.2")
    parser.add_option('-r', '--ref',
                      dest='ref',
                      help='reference file: all the input sequences in 1 fasta.')

    parser.add_option('-i', '--input',
                      dest='input',
                      help='Primer file. One of the followed three types:\n '
                           'final_maxprimers_set.xls \n primer.fa \n primer_F,primer_R.')

    parser.add_option('-f', '--format',
                      dest='format',
                      help='Format of primer file: xls or fa or seq; default: xls. \n '
                           'xls: final_primer_set.xls, output of multiPrime. \n'
                           'fa: fasta format. \n'
                           'seq: sequence format, comma seperate. e.g. primer_F,Primer_R.')

    parser.add_option('-o', '--out',
                      dest='out',
                      default="PCR_product",
                      help='Output_dir. default: PCR_product.')

    parser.add_option('-p', '--process',
                      dest='process',
                      default="10",
                      type="int",
                      help='Number of process to launch.  default: 10.')

    parser.add_option('-s', '--stast',
                      dest='stast',
                      default="Coverage.xls",
                      help='Stast information: number of coverage and total. Default: Coverage.xls')
    (options, args) = parser.parse_args()
    if len(sys.argv) == 2:
        parser.print_help()
        sys.exit(1)
    elif options.ref is None:
        parser.print_help()
        print("Input (reference) file must be specified !!!")
        sys.exit(1)
    elif options.input is None:
        parser.print_help()
        print("Primer file or sequence must be specified !!!")
        sys.exit(1)
    elif options.format is None:
        parser.print_help()
        print("Primer file format must be specified !!!")
        sys.exit(1)
    elif options.out is None:
        parser.print_help()
        print("No output file provided !!!")
        sys.exit(1)
    return parser.parse_args()


def Errors_argsParse():
    parser = OptionParser('Usage: %prog Errors -i [input] -r [bowtie index] -l [150,2000] -p [10]-o [output]')

    parser.add_option('-i', '--input',
                      dest='input_file',
                      help='input file: primer.fa.')

    parser.add_option('-r', '--ref',
                      dest='ref',
                      help='reference file: bowtie index.')

    parser.add_option('-l', '--len',
                      dest='len',
                      default=18,
                      type="int",
                      help='Length of primer, which is used for mapping. Default: 18')

    parser.add_option('-t', '--term',
                      dest='term',
                      default=4,
                      type="int",
                      help='Position of mismatch is not allowed in the 3 term of primer. Default: 4')

    parser.add_option('-s', '--s',
                      dest='size',
                      default="150,2000",
                      type="str",
                      help='Length of PCR product, default: 150,2000.')

    parser.add_option('-p', '--proc',
                      dest='proc',
                      default="20",
                      type="int",
                      help='Number of process. Default: 20')

    parser.add_option('-b', '--bowtie',
                      dest='bowtie',
                      default="bowtie2",
                      type="string",
                      help='bowtie or bowtie2 was employed for mapping. Default: bowtie2')

    parser.add_option('-m', '--seedmms',
                      dest='seedmms',
                      default="1",
                      type="int",
                      help='Bowtie: Mismatches in seed (can be 0 - 3, default: -n 1).'
                           'Bowtie2: Gap or mismatches in seed (can be 0 - 1, default: -n 1).')

    parser.add_option('-o', '--out',
                      dest='out',
                      help='PCR product with primers.')

    (options, args) = parser.parse_args()
    if len(sys.argv) == 2:
        parser.print_help()
        sys.exit(1)
    elif options.input_file is None:
        parser.print_help()
        print("Input file must be specified !!!")
        sys.exit(1)
    elif options.ref is None:
        parser.print_help()
        print("reference index (bowtie) must be specified !!!")
        sys.exit(1)
    elif options.out is None:
        parser.print_help()
        print("No output file provided !!!")
        sys.exit(1)
    return parser.parse_args()

def main_Usage():
    print('Usage: \n'
          'multiPrime DPrime:  Degenerate primer design through MD-DPD or MD-EDPD.\n'
          'multiPrime Ppair:   Primer pair selection from the result of multiPrime DPrime.\n'
          'multiPrime Perfect: Extract primer-contained sequences with non-mismatches.\n'
          'multiPrime Errors:  Extract primer-contained sequences with errors.\n')


degenerate_base = {"-": ["-"], "A": ["A"], "G": ["G"], "C": ["C"], "T": ["T"], "R": ["A", "G"], "Y": ["C", "T"],
                   "M": ["A", "C"], "K": ["G", "T"], "S": ["G", "C"], "W": ["A", "T"], "H": ["A", "T", "C"],
                   "B": ["G", "T", "C"], "V": ["G", "A", "C"], "D": ["G", "A", "T"], "N": ["A", "T", "G", "C"]}

score_table = {"-": 100, "#": 0, "A": 1, "G": 1.11, "C": 1.21, "T": 1.4, "R": 2.11, "Y": 2.61, "M": 2.21,
               "K": 2.51, "S": 2.32, "W": 2.4, "H": 3.61, "B": 3.72, "V": 3.32, "D": 3.51, "N": 4.72}

trans_score_table = {v: k for k, v in score_table.items()}

##############################################################################################
############################# Calculate free energy ##########################################
##############################################################################################
freedom_of_H_37_table = [[-0.7, -0.81, -0.65, -0.65],
                         [-0.67, -0.72, -0.8, -0.65],
                         [-0.69, -0.87, -0.72, -0.81],
                         [-0.61, -0.69, -0.67, -0.7]]

penalty_of_H_37_table = [[0.4, 0.575, 0.33, 0.73],
                         [0.23, 0.32, 0.17, 0.33],
                         [0.41, 0.45, 0.32, 0.575],
                         [0.33, 0.41, 0.23, 0.4]]

H_bonds_number = [[2, 2.5, 2.5, 2],
                  [2.5, 3, 3, 2.5],
                  [2.5, 3, 3, 2.5],
                  [2, 2.5, 2.5, 2]]
adjust_initiation = {"A": 0.98, "T": 0.98, "C": 1.03, "G": 1.03}
adjust_terminal_TA = 0.4
# Symmetry correction applies only to self-complementary sequences.
# symmetry_correction = 0.4
symmetry_correction = 0.4

##############################################################################################
base2bit = {"A": 0, "C": 1, "G": 2, "T": 3, "#": 4}
TRANS = str.maketrans("ATCG", "TAGC")


##############################################################################################
# 37°C and 1 M NaCl
Htable2 = [[-7.9, -8.5, -8.2, -7.2, 0],
           [-8.4, -8, -9.8, -8.2, 0],
           [-7.8, -10.6, -8, -8.5, 0],
           [-7.2, -7.8, -8.4, -7.9, 0],
           [0, 0, 0, 0, 0]]
Stable2 = [[-22.2, -22.7, -22.2, -21.3, 0],
           [-22.4, -19.9, -24.4, -22.2, 0],
           [-21, -27.2, -19.9, -22.7, 0],
           [-20.4, -21, -22.4, -22.2, 0],
           [0, 0, 0, 0, 0]]
Gtable2 = [[-1, -1.45, -1.3, -0.58, 0],
           [-1.44, -1.84, -2.24, -1.3, 0],
           [-1.28, -2.17, -1.84, -1.45, 0],
           [-0.88, -1.28, -1.44, -1, 0],
           [0, 0, 0, 0, 0]]
H_adjust_initiation = {"A": 2.3, "T": 2.3, "C": 0.1, "G": 0.1}
S_adjust_initiation = {"A": 4.1, "T": 4.1, "C": -2.8, "G": -2.8}
G_adjust_initiation = {"A": 1.03, "T": 1.03, "C": 0.98, "G": 0.98}
H_symmetry_correction = 0
S_symmetry_correction = -1.4
G_symmetry_correction = 0.4
##############################################################################################
# ng/ul
primer_concentration = 100
Mo_concentration = 50
Di_concentration = 1.5
dNTP_concentration = 0.25
Kelvin = 273.15
# reference (Owczarzy et al.,2008)
crossover_point = 0.22

bases = np.array(["A", "C", "G", "T"])
di_bases = []
for i in bases:
    for j in bases:
        di_bases.append(i + j)


def Penalty_points(length, GC, d1, d2):
    return log10((2 ** length * 2 ** GC) / ((d1 + 0.1) * (d2 + 0.1)))

def nan_removing(pre_list):
    while np.nan in pre_list:
        pre_list.remove(np.nan)
    return pre_list

di_nucleotides = set()
for i in base2bit.keys():
    single = i * 4
    di_nucleotides.add(single)
    for j in base2bit.keys():
        if i != j:
            di = (i + j) * 4
            di_nucleotides.add(di)
        for k in base2bit.keys():
            if i != j != k:
                tri = (i + j + k) * 3
                di_nucleotides.add(tri)

TRANS = str.maketrans("ATGCRYMKSWHBVDN", "TACGYRKMSWDVBHN")


def score_trans(sequence):
    return reduce(mul, [math.floor(score_table[x]) for x in list(sequence)])


def dege_number(sequence):
    return sum(math.floor(score_table[x]) > 1 for x in list(sequence))


def RC(seq):
    return seq.translate(TRANS)[::-1]

def Penalty_points(length, GC, d1, d2):
    return log10((2 ** length * 2 ** GC) / ((2 ** d1 - 0.9) * (2 ** d2 - 0.9)))

##############################################################################################
############## m_distance which is used to calculate (n)-nt variation coverage ###############
# Caution: this function only works when degeneracy of seq2 < 2 (no degenerate in seq2).
##############################################################################################
def Y_distance(seq1, seq2):
    seq_diff = list(np.array([score_table[x] for x in list(seq1)]) - np.array([score_table[x] for x in list(seq2)]))
    m_dist = [idx for idx in range(len(seq_diff)) if seq_diff[idx] not in score_table.values()]
    return m_dist


##############################################################################################
def symmetry(seq):
    if len(seq) % 2 == 1:
        return False
    else:
        F = seq[:int(len(seq) / 2)]
        R = RC(seq[int(len(seq) / 2):][::-1])
        if F == R:
            return True
        else:
            return False


def closest(my_list, my_number1, my_number2):
    index_left = bisect_left(my_list, my_number1)
    # find the first element index in my_list which greater than my_number.
    if my_number2 > my_list[-1]:
        index_right = len(my_list) - 1  # This is index.
    else:
        index_right = bisect_left(my_list, my_number2) - 1
    return index_left, index_right


def Calc_deltaH_deltaS(seq):
    Delta_H = 0
    Delta_S = 0
    for n in range(len(seq) - 1):
        i, j = base2bit[seq[n + 1]], base2bit[seq[n]]
        Delta_H += Htable2[i][j]
        Delta_S += Stable2[i][j]
    seq = seq.replace("#", '')
    Delta_H += H_adjust_initiation[seq[0]] + H_adjust_initiation[seq[-1]]
    Delta_S += S_adjust_initiation[seq[0]] + S_adjust_initiation[seq[-1]]
    if symmetry(seq):
        Delta_S += S_symmetry_correction
    return Delta_H * 1000, Delta_S


# salt_adjust = math.log(Tm_Na_adjust / 1000.0, math.e)
# def S_adjust(seq):
#     n = len(seq) - 1
#     # S_Na_adjust = 0.847 * n * salt_adjust
#     # Oligonucleotide Melting Temperatures under PCR Conditions: Nearest-Neighbor Corrections for
#     # Mg2+ , Deoxynucleotide Triphosphate, and Dimethyl Sulfoxide Concentrations with
#     # Comparison to Alternative Empirical Formulas
#     S_Na_adjust = 0.368 * n * salt_adjust
#     # A unified view of polymer, dumbbell, and oligonucleotide DNA nearest-neighbor thermodynamics
#     return S_Na_adjust
# where n is the total number of phosphates in the duplex divided by 2,
# This is equal to the oligonucleotide length minus 1.

def GC_fraction(seq):
    return round((list(seq).count("G") + list(seq).count("C")) / len(list(seq)), 3)


# different salt corrections for monovalent (Owczarzy et al.,2004) and divalent cations (Owczarzy et al.,2008)
def Calc_Tm_v2(seq):
    delta_H, delta_S = Calc_deltaH_deltaS(seq)
    # Note that the concentrations in the following Eq is mmol/L, In all other equations,concentration are mol/L
    # Monovalent cations are typically present as K+ and Tris+ in PCR buffer,
    # K+ is similar to Na+ in regard to duplex stabilization
    # if Di_concentration > dNTP_concentration:
    #     Tm_Na_adjust = Mo_concentration + 120 * math.sqrt(Di_concentration - dNTP_concentration)
    # else:
    #     Tm_Na_adjust = Mo_concentration
    Tm_Na_adjust = Mo_concentration

    if dNTP_concentration >= Di_concentration:
        free_divalent = 0.00000000001
    else:
        free_divalent = (Di_concentration - dNTP_concentration) / 1000.0
    R_div_monov_ratio = (math.sqrt(free_divalent)) / (Mo_concentration / 1000)

    if R_div_monov_ratio < crossover_point:
        # use only monovalent salt correction, [equation 22] (Owczarzy et al., 2004)
        correction = (((4.29 * GC_fraction(seq)) - 3.95) * pow(10, -5) * math.log(Tm_Na_adjust / 1000.0, math.e)) \
                     + (9.40 * pow(10, -6) * (pow(math.log(Tm_Na_adjust / 1000.0, math.e), 2)))
    else:
        # magnesium effects are dominant, [equation 16] (Owczarzy et al., 2008) is used
        # Table 2
        a = 3.92 * pow(10, -5)
        b = - 9.11 * pow(10, -6)
        c = 6.26 * pow(10, -5)
        d = 1.42 * pow(10, -5)
        e = - 4.82 * pow(10, -4)
        f = 5.25 * pow(10, -4)
        g = 8.31 * pow(10, -5)
        if R_div_monov_ratio < 6.0:
            a = 3.92 * pow(10, -5) * (
                    0.843 - (0.352 * math.sqrt(Tm_Na_adjust / 1000.0) * math.log(Tm_Na_adjust / 1000.0, math.e)))
            d = 1.42 * pow(10, -5) * (
                    1.279 - 4.03 * pow(10, -3) * math.log(Tm_Na_adjust / 1000.0, math.e) - 8.03 * pow(10, -3) * pow(
                math.log(Tm_Na_adjust / 1000.0, math.e), 2))
            g = 8.31 * pow(10, -5) * (
                    0.486 - 0.258 * math.log(Tm_Na_adjust / 1000.0, math.e) + 5.25 * pow(10, -3) * pow(
                math.log(Tm_Na_adjust / 1000.0, math.e), 3))
        # Eq 16
        correction = a + (b * math.log(free_divalent, math.e))
        + GC_fraction(seq) * (c + (d * math.log(free_divalent, math.e)))
        + (1 / (2 * (len(seq) - 1))) * (e + (f * math.log(free_divalent, math.e))
                                        + g * (pow((math.log(free_divalent, math.e)), 2)))

    if symmetry(seq):
        # Equation A
        Tm = round(1 / ((1 / (delta_H / (delta_S + 1.9872 * math.log(primer_concentration / (1 * pow(10, 9)), math.e))))
                        + correction) - Kelvin, 2)
    else:
        # Equation B
        Tm = round(1 / ((1 / (delta_H / (delta_S + 1.9872 * math.log(primer_concentration / (4 * pow(10, 9)), math.e))))
                        + correction) - Kelvin, 2)
    return Tm


##############################################################################################
