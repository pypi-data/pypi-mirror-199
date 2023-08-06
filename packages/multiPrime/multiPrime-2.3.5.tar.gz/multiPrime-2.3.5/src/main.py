#!/usr/bin/env python3

from .src import *
import time
import sys


def main():
    if len(sys.argv) < 2:
        main_Usage()
    elif sys.argv[1] == "DPrime":
        options, args = DPrime_argsParse()
        NN_APP = NN_degenerate(seq_file=options.input, primer_length=options.plen, coverage=options.fraction,
                               number_of_dege_bases=options.dnum, score_of_dege_bases=options.degeneracy,
                               entropy_threshold=options.entropy, product_len=options.size, position=options.coordinate,
                               variation=options.variation, distance=options.away, GC=options.gc, nproc=options.proc,
                               outfile=options.out)
        NN_APP.run()

    elif sys.argv[1] == "Ppair":
        options, args = Ppair_argsParse()
        primer_pairs = Primers_filter(ref_file=options.ref, primer_file=options.input, adaptor=options.adaptor,
                                      rep_seq_number=options.maxseq, distance=options.dist, outfile=options.out,
                                      size=options.size, position=options.end, fraction=options.fraction,
                                      diff_Tm=options.Tm,
                                      nproc=options.proc)
        primer_pairs.run()

    elif sys.argv[1] == "Perfect":
        (options, args) = Perfect_argsParse()
        results = Product_perfect(primer_file=options.input, output_file=options.out, ref_file=options.ref,
                                  file_format=options.format, coverage=options.stast, nproc=options.process)
        results.run()

    elif sys.argv[1] == "Errors":
        options, args = Errors_argsParse()
        prediction = Errors(primer_file=options.input_file, term_length=options.len, reference_file=options.ref,
                            PCR_product_size=options.size, mismatch_num=options.seedmms, outfile=options.out,
                            term_threshold=options.term, bowtie=options.bowtie, nproc=options.proc)
        prediction.run()
    else:
        print("No subprocess!")
        sys.exit(1)


if __name__ == "__main__":
    e1 = time.time()
    main()
    e2 = time.time()
    print("INFO {} Total times: {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
                                           round(float(e2 - e1), 2)))
