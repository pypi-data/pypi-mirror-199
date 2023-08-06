#!/usr/bin/env python
"""
Split a list of input files into train/test samples

Usage:
   cta-prod-split-list <ascii file with a list of lfns> <percentage of train_en files> <percentage of train_cl files>
   cta-prod-split-list <ascii file with a list of lfns> <percentage of train_cl files>

If 3 arguments are given, it splits the into 3 lists (train_en, train_cl, test)
Example:
  cta-prod-split-list Prod5b_LaPalma_AdvancedBaseline_NSB1x_gamma-diffuse_North_20deg_DL0.list 0.25 0.25
Produces:
Prod5b_LaPalma_AdvancedBaseline_NSB1x_gamma-diffuse_North_20deg_DL0_train_en.list
Prod5b_LaPalma_AdvancedBaseline_NSB1x_gamma-diffuse_North_20deg_DL0_train_cl.list
Prod5b_LaPalma_AdvancedBaseline_NSB1x_gamma-diffuse_North_20deg_DL0_train_test.list

If 2 arguments are given, it splits into 2 lists (train_cl, test)
Example:
  cta-prod-split-list Prod5b_LaPalma_AdvancedBaseline_NSB1x_proton_North_20deg_DL0.list 0.25
Produces:
Prod5b_LaPalma_AdvancedBaseline_NSB1x_proton_North_20deg_DL0_train_cl.list
Prod5b_LaPalma_AdvancedBaseline_NSB1x_proton_North_20deg_DL0_train_test.list
"""

__RCSID__ = "$Id$"

from DIRAC.Core.Base import Script
from DIRAC import gLogger
from CTADIRAC.Core.Utilities.tool_box import read_inputs_from_file


Script.parseCommandLine()
argss = Script.getPositionalArgs()

if len(argss) == 3:
    infile = argss[0]
    meta_key = argss[1]
    meta_value = argss[2]
else:
    Script.showHelp()


def dump_list(infile, lfn_list, split_md):
    split_list_file = infile.split(".list")[0] + "_" + split_md + ".list"
    f = open(split_list_file, "w")
    for lfn in lfn_list:
        f.write(lfn + "\n")
    f.close()
    gLogger.notice(f"{len(lfn_list)} files have been put in {split_list_file}")


@Script()
def main():
    Script.parseCommandLine(ignoreErrors=True)
    argss = Script.getPositionalArgs()
    if len(argss) not in [2, 3]:
        Script.showHelp()

    infile = argss[0]
    if len(argss) == 3:
        split_en = float(argss[1])
        split_cl = float(argss[2])
    elif len(argss) == 2:
        split_cl = float(argss[1])

    lfn_list = read_inputs_from_file(infile)
    gLogger.notice(f"{len(lfn_list)} input files")
    max_run = len(lfn_list)

    if len(argss) == 3:
        train_en_max_run = int(max_run * split_en)
        train_cl_max_run = int(max_run * split_cl)
        train_en_list = lfn_list[0:train_en_max_run]
        train_cl_list = lfn_list[train_en_max_run:train_cl_max_run]
        test_list = lfn_list[train_cl_max_run:]
        dump_list(train_en_list, "train_en")
        dump_list(train_cl_list, "train_cl")
        dump_list(test_list, "test")
    elif len(argss) == 2:
        train_cl_max_run = int(max_run * split_cl)
        train_cl_list = lfn_list[0:train_cl_max_run]
        test_list = lfn_list[train_cl_max_run:]
        dump_list(train_cl_list, "train_cl")
        dump_list(test_list, "test")


if __name__ == "__main__":
    main()
