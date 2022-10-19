#!/usr/bin/python
"""
Program: creating CAFA benchmark
Author : Huy Nguyen
Start  : 05/31/2017
End    : 05/31/2017
"""

import os
import argparse
from Bio.UniProt import GOA

EXP_EVIDENCE = {'Evidence': set(['EXP', 'IDA', 'IPI', 'IMP', 'IGI', 'IEP', 'HTP', 'HDA', 'HMP', 'HGI', 'HEP'])}


# Process arguments
def process_args(args):
    """
    :param args: Arguments passed via command line -
                gaf from time point 1, gaf from time point 2, output directory name
    :return: text files
    """
    # args = get_arguments()
    t_1 = args.infile1
    t_2 = args.infile2
    outdir = args.outdir
    # t1_name, t1_dic, all_protein_t1 = read_gaf(t_1)
    t1_dic, all_protein_t1 = read_gaf(t_1)
    #    print "t1 \n",t1_dic
    # t2_name, t2_dic, all_protein_t2 = read_gaf(t_2)
    t2_dic, all_protein_t2 = read_gaf(t_2)
    #    print "t2 \n",t2_dic
    nk_dic, lk_dic = analyze(t1_dic, t2_dic, all_protein_t1)
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    # try:
    #    os.mkdir(outdir)
    # except:
    #    print("The directory has already been created")
    num1 = t_1.split('.')[-1]
    num2 = t_2.split('.')[-1]
    name = outdir + '/' + '.'.join(t_1.split('/')[-1].split('.')[:-1]) \
           + '.' + num2 + '-' + num1 + '_benchmark_'
    write_file(nk_dic, 'NK', name)
    write_file(lk_dic, 'LK', name)


# function : given a file handle, parse in using gaf format and return a dictionary
#           that identify those protein with experimental evidence and the ontology
# input    : file text
# output   : dic (key: name of file (number),
#           value is a big dictionary store info about the protein)
def read_gaf(file_name):
    """
    :param file_name: gaf file handle
    :return: handle name, dict
    """
    # name = file_name.split(".")[-1]
    dic = {}
    all_protein_name = set()
    # evidence from experimental
    # evidence = {'Evidence': set(['EXP', 'IDA', 'IPI', 'IMP', 'IGI', 'IEP'])}
    with open(file_name, 'r', encoding='utf8') as file_handle:
        for rec in GOA.gafiterator(file_handle):
            dic_id = rec['DB_Object_Symbol']+"_"+rec['Taxon_ID'][0].split(":")[1]
            all_protein_name.add(dic_id)
            if GOA.record_has(rec, EXP_EVIDENCE) and rec['DB'] == 'UniProtKB':
                if dic_id not in dic:
                    dic[dic_id] = {rec['Aspect']: set([rec['GO_ID']])}
                else:
                    if rec['Aspect'] not in dic[dic_id]:
                        dic[dic_id][rec['Aspect']] = set([rec['GO_ID']])
                    else:
                        dic[dic_id][rec['Aspect']].add(rec['GO_ID'])
    return dic, all_protein_name


# function : given t1 dic, t2 dic, we provide the dic for NK, and LK dic for each ontology
# input    : 2 dics
# output   : NK,LK dictionary
def analyze(t1_dic, t2_dic, all_protein_t1):
    """
    :param t1_dic: dict from time-point 1
    :param t2_dic: dict from time-point 2
    :param all_protein_t1: dict of proteins from time-point 1
    :return: nk and lk dictionaries
    """
    nk_dic = {'P': {}, 'C': {}, 'F': {}}
    lk_dic = {'P': {}, 'C': {}, 'F': {}}
    # dealing with NK and LK

    for protein in t2_dic:
        # check the protein in t2_dic but not appear in t1
        if protein not in t1_dic and protein in all_protein_t1:  # this going to be in NK
            # check which ontology got new annotated
            for ontology in t2_dic[protein]:
                nk_dic[ontology][protein] = t2_dic[protein][ontology]
        # check the protein that in t2_dic and appear in t1
        elif protein in t1_dic:
            # check if in t1, this protein does not have all 3 ontology
            # if yes, then not include since full knowledge
            # else
            if len(t1_dic[protein]) < 3:
                # check if t2_dic include in the ontology that t1 lack of
                for ontology in t2_dic[protein]:
                    if ontology not in t1_dic[protein]:  # for those lack, include in LK
                        lk_dic[ontology][protein] = t2_dic[protein][ontology]
    return nk_dic, lk_dic


# function : given NK,LK dic , write out 6 files
# input    : 2 dics
# output   : NK,LK dictionary
def write_file(dic, knowledge, name):
    final_name = ''
    for ontology in dic:
        if ontology == 'F':
            final_name = name + knowledge + '_mfo'
        elif ontology == 'P':
            final_name = name + knowledge + '_bpo'
        elif ontology == 'C':
            final_name = name + knowledge + '_cco'

        print("Writing {} file".format(final_name))
        file_out = open(final_name, 'w', encoding='utf8')
        for protein in sorted(dic[ontology]):
            for annotation in dic[ontology][protein]:
                file_out.write(protein + '\t' + annotation + '\n')
        file_out.close()
    return None


# Argument parsers
def main():
    parser = argparse.ArgumentParser(
        description='Inputs gaf files and output directory name to generate benchmark for CAFA')
    parser.add_argument("--infile1", "-t1", type=str, help="gaf file from time point 1")
    parser.add_argument("--infile2", "-t2", type=str, help="gaf file from time point 2")
    parser.add_argument("--outdir", "-o", type=str,
                        help="Output directory name to store the 6 generated benchmark files")
    # try:
    #    args = parser.parse_args()
    #    process_args(args)
    # except:
    #    parser.print_help()
    #    sys.exit(0)
    args = parser.parse_args()
    process_args(args)


if __name__ == "__main__":
    main()
