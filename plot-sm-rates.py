#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import argparse
import json
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from numpy.random import multivariate_normal
import requests

def main(args):
    json_response = json.load(args.infile)

    rates = []
    volumes = []

    for vendor in json_response["results"]:
        if vendor["translatedWordCount"] >= args.word_limit:
            rates.append(vendor["matchedService"]["pricePerUnit"])
            volumes.append(vendor["translatedWordCount"]+1)

    fig, axes = plt.subplots(nrows=2, ncols=2)
    axes[0,0].hist(rates, bins=20, range=(0, args.max_rate))
    axes[0,1].hist(rates, bins=20, weights=volumes, range=(0, args.max_rate), density=True, histtype="stepfilled")
    counts, xedges, yedges, im = axes[1,0].hist2d(rates, np.log10(volumes), range=((0, args.max_rate), (np.log10(volumes).min(), 7)))
    axes[1,1].hist(np.log10(volumes), bins=20, range=(np.log10(volumes).min(), 7), orientation="horizontal")
    # axes[2,2].set_title("Rate vs Volume Distribution")
    # axes[1,1].set_xlabel("Rate [$/word]")
    # axes[1,1].set_ylabel("Volume [log10(words)]")
    axes[1,0].set_xlabel("Rate [$/word]")
    axes[1,0].set_ylabel("Volume [log10(words)]", rotation=90)
    # axes[1,1].yaxis.set_label_position("right")
    axes[0,1].set_title("Rate [$/word] * Volume")
    fig.colorbar(im, ax=axes.ravel().tolist())
    plt.suptitle(args.title)
    plt.savefig(args.outfile)
    plt.clf()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--infile', dest='infile',
        type=argparse.FileType('r', encoding='UTF-8'),
        nargs='?',
        default=sys.stdin,
        help='Input file'
    )
    parser.add_argument(
        '-o', '--outfile', dest='outfile',
        help='Output file'
    )
    parser.add_argument(
        "-w", "--word_limit", dest="word_limit",
        type=int,
        nargs="?",
        default=-1,
        help="Minimum number of words translated by a translator to be included"
    )
    parser.add_argument(
        "-r", "--max_rate", dest="max_rate",
        type=float,
        nargs='?',
        default=0.16,
        help="Max rate"
    )
    parser.add_argument(
        "-t", "--title", dest="title",
        type=str,
        nargs='?',
        default="",
        help="Figure title"
    )
    main(parser.parse_args())
